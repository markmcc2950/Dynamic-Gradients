import tkinter as tk

def on_resize(event):
    # global screen_w_last, screen_h_last
    # # Keep the window a perfect square
    # if event.width < screen_w_last:
    #     screen_h_last = event.width
    #     screen_w_last = event.width
    #     print('Width decreased!')
    # if event.width > screen_w_last:
    #     screen_h_last = event.width
    #     screen_w_last = event.width
    #     print('Width increased!')
    # if event.height < screen_h_last:
    #     screen_h_last = event.height
    #     screen_w_last = event.height
    #     print('Height decreased!')
    # if event.height > screen_h_last:
    #     screen_h_last = event.height
    #     screen_w_last = event.height
    #     print('Height increased!')

    new_size = min(screen_h_last, screen_w_last)

    # Avoid unnecessary resizing loops
    if root.winfo_width() != new_size or root.winfo_height() != new_size:
        root.geometry(f"{new_size}x{new_size}")  # Adjust window to a perfect square

    # Update global size variables without redrawing
    global screen_width, screen_height, square_width, square_height, border_w, border_h, resize_timeout
    screen_width = screen_height = new_size
    square_width = square_height = new_size * 0.8
    border_w = (screen_width - square_width) / 2
    border_h = (screen_height - square_height) / 2

    if resize_timeout is not None:
        root.after_cancel(resize_timeout)

    # Schedule redraw after a short delay (e.g., 100 ms)
    resize_timeout = root.after(100, redraw_canvas)
    # root.after(resize_timeout, redraw_canvas)

def redraw_canvas():
    global grid_size
    # Draw the canvas again
    canvas.delete("all")
    draw_square_grid(grid_size)
    
    
def rgb_to_hex(r, g, b):
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)
    return f'#{r_int:02x}{g_int:02x}{b_int:02x}'

def add_square(x, y, size=50, color="black", outline=1):
    canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline='')
    # canvas.create_oval(x, y, x + size, y + size, fill=color, outline='')

def draw_square_grid(num_of_squares):
    # Draws a grid of squares that fits within the currently sized window
    global square_width, square_height, border_w, border_h
    
    square_size = square_width / num_of_squares  # Keep squares proportional

    red = 1.0
    blue = 0.0
    green = 0.0
    green_max = False

    # print(['FizzBuzz' if n % 15 == 0 else 'Fizz' if n % 3 == 0 else 'Buzz' if n % 5 == 0 else n for n in range(1, 101)], end = " | ")
    
    for i in range(num_of_squares):
        for j in range(num_of_squares):
            # Define the RGB values first
            if green > 0.9999:
                green_max = True
            red = red - float(1 / grid_size ** 2) if red > 0 else red
            blue = blue + float(1 / grid_size ** 2) if blue < 1.0 else blue
            green = green + float((1 / grid_size ** 2) * 2) if green < 1.0 and not green_max else green - float((1 / grid_size ** 2) * 2) if green_max and green > 0 else green

            # Draw the next square
            add_square(border_w + (square_size * i), border_h + (square_size * j), size=square_size, color=rgb_to_hex(red, green, blue))

def button_click_res_up():
    global grid_size
    grid_size = grid_size + 2 if grid_size < 1000 else grid_size

    button_res_down.config(state=tk.NORMAL if grid_size > 2 else tk.DISABLED)
    button_res_down_l.config(state=tk.NORMAL if grid_size > 20 else tk.DISABLED)
    
    on_resize("<Configure>")

def button_click_res_up_large():
    global grid_size
    grid_size = grid_size + 20 if grid_size < 1000 else grid_size

    button_res_down.config(state=tk.NORMAL if grid_size > 2 else tk.DISABLED)
    button_res_down_l.config(state=tk.NORMAL if grid_size > 20 else tk.DISABLED)

    on_resize("<Configure>")

def button_click_res_down():
    global grid_size
    grid_size = grid_size - 2 if grid_size > 2 else grid_size

    button_res_down.config(state=tk.NORMAL if grid_size > 2 else tk.DISABLED)
    button_res_down_l.config(state=tk.NORMAL if grid_size > 20 else tk.DISABLED)

    on_resize("<Configure>")

def button_click_res_down_large():
    global grid_size
    grid_size = grid_size - 20 if grid_size > 20 else grid_size

    button_res_down.config(state=tk.NORMAL if grid_size > 2 else tk.DISABLED)
    button_res_down_l.config(state=tk.NORMAL if grid_size > 20 else tk.DISABLED)

    on_resize("<Configure>")

grid_size = 6
root = tk.Tk()
root.title("Square Window")

# Set an initial size
initial_size = 800
root.geometry(f"{initial_size}x{initial_size}")

screen_width = screen_height = initial_size
square_width = square_height = screen_width * 0.8
border_w = (screen_width - square_width) / 2
border_h = (screen_height - square_height) / 2

# To store the last set values of a window resize, track what dimensions changed
screen_w_last = screen_width
screen_h_last = screen_height

# Create Canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)

# Draw the initial grid
draw_square_grid(grid_size)
resize_timeout = grid_size

# Create buttons
button_w = 200
button_h = 25

# Increase resolution (small and large)
button_res_up = tk.Button(root, text="Increase Resolution (Small)", command=button_click_res_up)
button_res_up.place(x=border_w, y=(border_h / 2) - (button_h * 1.5), width=button_w, height=button_h)

button_res_up_l = tk.Button(root, text="Increase Resolution (Large)", command=button_click_res_up_large)
button_res_up_l.place(x=border_w, y=(border_h / 2), width=button_w, height=button_h)

# Decrease resolution (small and large)
button_res_down = tk.Button(root, text="Decrease Resolution (Small)", command=button_click_res_down)
button_res_down.place(x=screen_width - border_w - button_w, y=(border_h / 2) - (button_h * 1.5), width=button_w, height=button_h)
button_res_down.config(state=tk.NORMAL if grid_size > 2 else tk.DISABLED)


button_res_down_l = tk.Button(root, text="Decrease Resolution (Large)", command=button_click_res_down_large)
button_res_down_l.place(x=screen_width - border_w - button_w, y=(border_h / 2), width=button_w, height=button_h)
button_res_down_l.config(state=tk.NORMAL if grid_size > 20 else tk.DISABLED)

# Bind resize event (adjust size) and mouse release event (redraw only when done)
# root.bind("<Configure>", on_resize)
root.resizable(False, False)

# button.pack()
root.mainloop()
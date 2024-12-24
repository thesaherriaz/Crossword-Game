import tkinter as tk

def create_gradient(canvas, width, height, start_color, end_color):
    # Convert HEX colors to RGB
    start_rgb = canvas.winfo_rgb(start_color)
    end_rgb = canvas.winfo_rgb(end_color)
    
    # Compute RGB difference per step
    r_diff = (end_rgb[0] - start_rgb[0]) / height
    g_diff = (end_rgb[1] - start_rgb[1]) / height
    b_diff = (end_rgb[2] - start_rgb[2]) / height

    # Draw the gradient
    for i in range(height):
        r = int(start_rgb[0] / 256 + (r_diff * i) / 256)
        g = int(start_rgb[1] / 256 + (g_diff * i) / 256)
        b = int(start_rgb[2] / 256 + (b_diff * i) / 256)
        # Clamp RGB values to 0-255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)

# Initialize Tkinter window
root = tk.Tk()
root.title("Gradient Background - Vertical Gradient")

# Create Canvas widget
width, height = 400, 300
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

# Apply the gradient
create_gradient(canvas, width, height, "#191970", "#9400D3")  # Midnight Blue to Dark Violet

root.mainloop()

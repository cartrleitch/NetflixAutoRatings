import tkinter as tk

current_toast_window = None

def round_rectangle(canvas, x1, y1, x2, y2, radius=15, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def show_rating_toast(text, rating, duration):
    global current_toast_window
    
    # Close existing toast if any
    close_rating_toast()
    
    root = tk.Tk()
    current_toast_window = root
    
    root.overrideredirect(True)  # no window borders
    root.attributes("-topmost", True)
    root.attributes("-alpha", 1)  # transparency

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Position: bottom-right-ish (Netflix safe area)
    width = screen_w // 4
    height = screen_h // 12
    x = screen_w - width - 40
    y = int(screen_h*0.05)

    root.geometry(f"{width}x{height}+{x}+{y}")

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    root.wm_attributes("-transparentcolor", "black")  # Make black areas transparent

    display_text = f"{text} Rating: {rating}/10"

    background_color = "#141414"  # Default dark background
    text_color = "#FFFFFF"        # Default white text
    font_size = 18

    if rating >= 9.7:
        background_color = "#1da1f2"  # Blue for highest ratings
    elif rating >= 9:
        background_color = "#186a3b"  # Dark Green for higher ratings
    elif rating >= 8:
        background_color = "#28b463"  # Green for high ratings
        text_color = "#111111"      
    elif rating >= 7.1:
        background_color = "#f4d03f"  # Yellow for good ratings
        text_color = "#111111"
    elif rating >= 6:
        background_color = "#f39c12"  # Orange for regular ratings 
        text_color = "#111111"  
    elif rating >= 5:
        background_color = "#e74c3c"  # Red for bad ratings
    elif rating == -1:
        background_color = "#0E0B0B"  # Black for error ratings
        display_text = f"Could not display rating (only works on fullscreen)!"
        font_size = 12
    elif rating == -2:
        background_color = "#7f8c8d"  # Gray for multiple series found
        display_text = f"{text}"
        font_size = 10
    else:
        background_color = "#633974"  # Purple for garbage ratings

    # Draw rounded rectangle
    round_rectangle(canvas, 10, 10, width-10, height-10, radius=10, fill=background_color, outline="")
    
    # Add text on top
    canvas.create_text(
        width//2, 
        height//2, 
        text=display_text, 
        fill=text_color, 
        font=("Segoe UI", font_size, "bold"),
        justify="center"
    )

    if duration > 0:
        root.after(duration, root.destroy)

def close_rating_toast():
    global current_toast_window
    if current_toast_window is not None:
        try:
            current_toast_window.destroy()
        except:
            pass
        current_toast_window = None

def update_toast():
    global current_toast_window
    if current_toast_window is not None:
        try:
            current_toast_window.update()
        except:
            current_toast_window = None

if __name__ == "__main__":
    pass
    # show_rating_toast("Episode 601", 5, duration=4000)
    # show_rating_toast("Episode 601", 9.8, duration=4000)
    # show_rating_toast("Episode 601", 7.5, duration=4000)
    # show_rating_toast("Episode 601", 3.2, duration=4000)
    # show_rating_toast("Episode 601", 8.6, duration=4000)
    # show_rating_toast("Episode 601", 6.4, duration=4000)
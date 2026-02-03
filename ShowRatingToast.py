import tkinter as tk
from MyLogger import logger

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

def show_selection_dialog(title, message, options):
    """
    Show a GUI selection dialog with clickable options.
    
    Args:
        title: Dialog title
        message: Message to display above options
        options: List of tuples (display_text, value) for each option
    
    Returns:
        Selected value or None if cancelled
    """
    selected_value = [None]  # Use list to allow modification in nested function
    
    root = tk.Tk()
    root.title(title)
    root.attributes("-topmost", True)
    root.configure(bg="#141414")
    
    # Calculate size based on content
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    width = min(600, screen_w // 2)
    height = min(400, screen_h // 2)
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)
    
    # Message label
    message_label = tk.Label(
        root, 
        text=message, 
        font=("Segoe UI", 12, "bold"),
        fg="#FFFFFF",
        bg="#141414",
        wraplength=width-40,
        justify="center"
    )
    message_label.pack(pady=20)
    
    # Frame for buttons with scrollbar if needed
    button_frame = tk.Frame(root, bg="#141414")
    button_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Canvas and scrollbar for many options
    canvas = tk.Canvas(button_frame, bg="#141414", highlightthickness=0)
    scrollbar = tk.Scrollbar(button_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#141414")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def on_select(value):
        selected_value[0] = value
        canvas.unbind_all("<MouseWheel>")
        root.destroy()
    
    # Create button for each option
    for i, (display_text, value) in enumerate(options):
        btn = tk.Button(
            scrollable_frame,
            text=display_text,
            font=("Segoe UI", 11),
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#555555",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=lambda v=value: on_select(v)
        )
        btn.pack(fill="x", pady=5, padx=10)
        
        # Hover effects
        def on_enter(e):
            e.widget['bg'] = '#555555'
        def on_leave(e):
            e.widget['bg'] = '#333333'
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    if len(options) > 6:  # Show scrollbar only if many options
        scrollbar.pack(side="right", fill="y")
    
    # Cancel button
    cancel_btn = tk.Button(
        root,
        text="Cancel",
        font=("Segoe UI", 10),
        bg="#e74c3c",
        fg="#FFFFFF",
        activebackground="#c0392b",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        command=lambda: [canvas.unbind_all("<MouseWheel>"), root.destroy()]
    )
    cancel_btn.pack(pady=5)
    
    # Make dialog modal
    root.grab_set()
    root.focus_force()
    
    # Wait for dialog to close
    root.mainloop()
    
    return selected_value[0]

if __name__ == "__main__":
    pass
    # show_rating_toast("Episode 601", 5, duration=4000)
    # show_rating_toast("Episode 601", 9.8, duration=4000)
    # show_rating_toast("Episode 601", 7.5, duration=4000)
    # show_rating_toast("Episode 601", 3.2, duration=4000)
    # show_rating_toast("Episode 601", 8.6, duration=4000)
    # show_rating_toast("Episode 601", 6.4, duration=4000)
    
        # Test selection dialog
    # options = [
    #     ("ONE PIECE (1999): Rating 9.0", "tt0388629"),
    #     ("ONE PIECE (2023): Rating 8.3", "tt11737520"),
    # ]
    # result = show_selection_dialog("Select Series", "Multiple series found. Select the correct one:", options)
    # print(f"Selected: {result}")
import tkinter as tk

def show_rating_toast(text, rating, duration=4000):
    root = tk.Tk()
    root.overrideredirect(True)  # no window borders
    root.attributes("-topmost", True)
    root.attributes("-alpha", 1)  # transparency

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Position: bottom-right-ish (Netflix safe area)
    width = 450
    height = 80
    x = screen_w - width - 40
    y = int(screen_h*0.05)

    root.geometry(f"{width}x{height}+{x}+{y}")

    frame = tk.Frame(root, bg="black")
    frame.pack(fill="both", expand=True)
    root.wm_attributes("-transparentcolor", "black")  # Make black areas transparent

    display_text = f"{text} Rating: {rating}/10"

    background_color = "#141414"  # Default dark background
    if rating >= 9.7:
        background_color = "#1da1f2"  # Blue for highest ratings
    elif rating >= 9:
        background_color = "#186a3b"  # Dark Green for higher ratings
    elif rating >= 8:
        background_color = "#28b463"  # Green for high ratings
    elif rating >= 7.1:
        background_color = "#f4d03f"  # Yellow for good ratings
    elif rating >= 6:
        background_color = "#f39c12"  # Orange for regular ratings   
    elif rating >= 5:
        background_color = "#e74c3c"  # Red for bad ratings
    else:
        background_color = "#633974"  # Purple for garbage ratings

    label = tk.Label(
        frame,
        text=display_text,
        fg="white",
        bg=background_color,
        font=("Segoe UI", 18, "bold"),
        wraplength=450,
        justify="left"
    )
    label.pack(padx=20, pady=20)

    root.after(duration, root.destroy)
    root.mainloop()

# Example usage:
show_rating_toast("Episode 601", 4, duration=4000)
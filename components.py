import tkinter as tk

# the colors for the dark theme
theme = {
    "bg": "#0f1117",
    "sidebar": "#1a1d27",
    "card": "#22263a",
    "border": "#2e3352",
    "accent1": "#6c63ff", # purple for original function
    "accent2": "#00d4aa", # teal for derivative
    "accent3": "#ff6584", # pink for integral
    "accent4": "#ffd166", # amber for area between
    "text": "#e2e8f0",
    "subtext": "#8892b0",
    "input_bg": "#12151f"
}

# makes a small title for sections
def create_label(parent, text, is_header=False):
    font = ("Segoe UI", 14, "bold") if is_header else ("Segoe UI", 8)
    color = theme["accent1"] if is_header else theme["subtext"]
    return tk.Label(parent, text=text, bg=theme["sidebar"], fg=color, font=font)

# a basic text input box
def create_entry(parent, var):
    return tk.Entry(parent, textvariable=var, bg=theme["input_bg"], fg=theme["text"], 
                    insertbackground="white", borderwidth=0, font=("Consolas", 11))

# a tiny input box for things like ranges
def create_small_entry(parent, var):
    return tk.Entry(parent, textvariable=var, bg=theme["input_bg"], fg=theme["text"], 
                    insertbackground="white", borderwidth=0, font=("Consolas", 10), width=7)

# a button that matches our theme
def create_btn(parent, text, cmd, primary=True):
    bg_color = theme["accent1"] if primary else theme["card"]
    return tk.Button(parent, text=text, command=cmd, bg=bg_color, fg="white", 
                     font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", pady=6)
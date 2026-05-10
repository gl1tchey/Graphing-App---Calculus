import tkinter as tk

THEME = {
    "bg_main": "#0b0e14", "bg_sidebar": "#151921", "bg_card": "#1c222d",
    "accent": "#7c4dff", "secondary": "#00e5ff", "text": "#ffffff",
    "danger": "#ff5252", "success": "#00c853", "grid": "#232933"
}

def create_sidebar_button(parent, text, command, type="default"):
    bg = THEME["success"] if type == "success" else THEME["bg_card"]
    return tk.Button(parent, text=text, command=command, bg=bg, fg="white", 
                     font=("Segoe UI", 9, "bold"), relief="flat", padx=20, pady=10, cursor="hand2")

def create_function_row(parent, on_delete, on_change):
    frame = tk.Frame(parent, bg=THEME["bg_card"], pady=8, padx=12)
    var = tk.StringVar()
    var.trace_add("write", lambda *args: on_change())

    tk.Label(frame, text="f(x)=", bg=THEME["bg_card"], fg=THEME["secondary"], font=("Consolas", 11, "bold")).pack(side="left")
    entry = tk.Entry(frame, textvariable=var, bg="#252b37", fg="white", borderwidth=0, 
                     insertbackground="white", highlightthickness=1, highlightbackground="#3a4253")
    entry.pack(side="left", fill="x", expand=True, padx=8)

    tk.Button(frame, text="✕", command=lambda: on_delete(frame), 
              bg=THEME["bg_card"], fg=THEME["danger"], borderwidth=0).pack(side="right")
    return frame, entry, var
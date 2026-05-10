import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg") # [cite: 176]
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import engine

# Color Palette from Redoblado et al. [cite: 187-221]
CLR = {"bg": "#0f1117", "panel": "#1a1d27", "card": "#22263a", "accent": "#6c63ff", "text": "#e2e8f0"}

class CalculusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculus Visualizer | Final Project")
        self.geometry("1300x850")
        self.configure(bg=CLR["bg"])
        
        # State Variables [cite: 300-367]
        self.f_var = tk.StringVar(value="x**3 - 3*x**2 + 2")
        self.g_var = tk.StringVar(value="")
        self.xmin_var = tk.StringVar(value="-5")
        self.xmax_var = tk.StringVar(value="5")
        self.a_var = tk.StringVar(value="0")
        self.b_var = tk.StringVar(value="2")
        self.order_var = tk.IntVar(value=1)
        
        self._build_ui()

    def _build_ui(self):
        # Sidebar (Left) [cite: 282]
        sb = tk.Frame(self, bg=CLR["panel"], width=320)
        sb.pack(side="left", fill="y", padx=10, pady=10)
        sb.pack_propagate(False)

        tk.Label(sb, text="Calculus Visualizer", bg=CLR["panel"], fg=CLR["accent"], font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        # Inputs Section [cite: 299-356]
        self._create_input(sb, "Function f(x)", self.f_var)
        self._create_input(sb, "Second Function g(x) (Optional)", self.g_var)
        
        # Range & Bounds [cite: 306, 325]
        range_fr = tk.Frame(sb, bg=CLR["panel"])
        range_fr.pack(fill="x", padx=15, pady=5)
        self._create_small_input(range_fr, "X Start", self.xmin_var, 0)
        self._create_small_input(range_fr, "X End", self.xmax_var, 1)
        
        bounds_fr = tk.Frame(sb, bg=CLR["panel"])
        bounds_fr.pack(fill="x", padx=15, pady=5)
        self._create_small_input(bounds_fr, "Bound a", self.a_var, 0)
        self._create_small_input(bounds_fr, "Bound b", self.b_var, 1)

        # Buttons [cite: 393-397]
        tk.Button(sb, text="Plot Graphs", command=self._on_plot, bg=CLR["accent"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat").pack(fill="x", padx=20, pady=10)
        tk.Button(sb, text="Save Graph", command=self._on_save, bg=CLR["card"], fg="white", font=("Segoe UI", 10)).pack(fill="x", padx=20, pady=5) # 

        # Results Panel (Right) [cite: 417, 629]
        self.results_txt = tk.Text(sb, height=15, bg="#12151f", fg=CLR["text"], font=("Consolas", 9), relief="flat")
        self.results_txt.pack(fill="x", padx=15, pady=10)

        # Plot Area (Center) [cite: 404]
        self.fig = Figure(facecolor=CLR["bg"], tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def _create_input(self, parent, label, var):
        tk.Label(parent, text=label, bg=CLR["panel"], fg="#8892b0", font=("Segoe UI", 8)).pack(anchor="w", padx=20)
        tk.Entry(parent, textvariable=var, bg="#12151f", fg="white", insertbackground="white", borderwidth=0).pack(fill="x", padx=20, pady=(2, 10), ipady=5)

    def _create_small_input(self, parent, label, var, col):
        tk.Label(parent, text=label, bg=CLR["panel"], fg="#8892b0", font=("Segoe UI", 8)).grid(row=0, column=col*2, padx=5)
        tk.Entry(parent, textvariable=var, width=8, bg="#12151f", fg="white", borderwidth=0).grid(row=0, column=col*2+1, padx=5, ipady=3)

    def _on_plot(self):
        data = engine.compute_calculus(
            self.f_var.get(), 
            (float(self.xmin_var.get()), float(self.xmax_var.get())),
            float(self.a_var.get()), float(self.b_var.get()),
            self.order_var.get(),
            self.g_var.get() if self.g_var.get() else None
        )

        if data:
            self.fig.clear()
            # Multi-subplot layout inspired by Redoblado et al. [cite: 546-562]
            axes = self.fig.subplots(2, 2)
            titles = ["Original Function", "Derivative", "Cumulative Integral", "Calculus Analysis"]
            colors = ["#6c63ff", "#00d4aa", "#ff6584", "#ffd166"]
            
            # 1. Original Plot with Area Shading [cite: 580-585]
            ax1 = axes[0,0]
            ax1.plot(data["x"], data["y"], color=colors[0], lw=2)
            mask = (data["x"] >= data["a"]) & (data["x"] <= data["b"])
            ax1.fill_between(data["x"][mask], data["y"][mask], alpha=0.3, color=colors[0], label="Area Under")
            if data["g_y"] is not None:
                ax1.plot(data["x"], data["g_y"], '--', color=colors[2], label="g(x)")
                ax1.fill_between(data["x"][mask], data["y"][mask], data["g_y"][mask], color=colors[2], alpha=0.2, label="Area Between")
            
            # 2. Derivative [cite: 608]
            axes[0,1].plot(data["x"], data["dy"], color=colors[1], lw=2)
            
            # 3. Integral Curve [cite: 620-624]
            axes[1,0].plot(data["x"], data["int_curve"], color=colors[2], lw=2)
            axes[1,0].fill_between(data["x"], data["int_curve"], alpha=0.1, color=colors[2])
            
            for ax, title in zip(axes.flatten(), titles):
                ax.set_title(title, color="white", fontsize=9)
                ax.set_facecolor(CLR["card"])
                ax.grid(True, color="#2e3352", alpha=0.4)
                ax.tick_params(colors="#8892b0", labelsize=7)

            # Update Results Panel [cite: 629, 652-656]
            self.results_txt.delete("1.0", tk.END)
            res_str = (
                f"[ FUNCTIONS ]\n"
                f"f(x) = {data['expr']}\n"
                f"f'(x) = {data['d_expr']}\n\n"
                f"[ INTEGRATION ]\n"
                f"Bounds: [{data['a']}, {data['b']}]\n"
                f"Area Under: {data['area']:.6f}\n"
                f"Error: {data['error']:.2e}\n"
            )
            if data['between']:
                res_str += f"Area Between: {data['between']:.6f}"
            self.results_txt.insert(tk.END, res_str)
            self.canvas.draw() # [cite: 628]

    def _on_save(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")]) # [cite: 513-516]
        if path:
            self.fig.savefig(path, dpi=150, facecolor=CLR["bg"]) # [cite: 520]
            messagebox.showinfo("Success", f"Graph saved to {path}")

if __name__ == "__main__":
    CalculusApp().mainloop()
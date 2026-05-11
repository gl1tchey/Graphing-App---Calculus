import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg") 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import engine
import components as ui

class CalculusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculus Visualizer")
        self.geometry("1350x850")
        self.configure(bg=ui.theme["bg"])
        
        # variables to store what you type in the app
        self.f_var = tk.StringVar(value="x**2")
        self.g_var = tk.StringVar(value="x")
        self.xmin_var = tk.StringVar(value="-5")
        self.xmax_var = tk.StringVar(value="5")
        self.a_var = tk.StringVar(value="0")
        self.b_var = tk.StringVar(value="2")
        self.order_var = tk.IntVar(value=1)
        
        self._build_ui()

    def _build_ui(self):
        # sidebar for inputs and buttons
        sb = tk.Frame(self, bg=ui.theme["sidebar"], width=320)
        sb.pack(side="left", fill="y", padx=10, pady=10)
        sb.pack_propagate(False)

        ui.create_label(sb, "Calculus Visualizer", True).pack(pady=15, padx=16, anchor="w")
        
        # text boxes for f(x) and g(x)
        ui.create_label(sb, "Function f(x)").pack(anchor="w", padx=20, pady=(10, 0))
        ui.create_entry(sb, self.f_var).pack(fill="x", padx=20, pady=(2, 10), ipady=5)
        
        ui.create_label(sb, "Second Function g(x)").pack(anchor="w", padx=20, pady=(10, 0))
        ui.create_entry(sb, self.g_var).pack(fill="x", padx=20, pady=(2, 10), ipady=5)
        
        # small boxes for x limits and area bounds
        range_fr = tk.Frame(sb, bg=ui.theme["sidebar"])
        range_fr.pack(fill="x", padx=20, pady=5)
        ui.create_label(range_fr, "Limits (start, end, a, b)").grid(row=0, column=0, columnspan=2, sticky="w")
        ui.create_small_entry(range_fr, self.xmin_var).grid(row=1, column=0, padx=2, pady=5)
        ui.create_small_entry(range_fr, self.xmax_var).grid(row=1, column=1, padx=2, pady=5)
        ui.create_small_entry(range_fr, self.a_var).grid(row=2, column=0, padx=2, pady=5)
        ui.create_small_entry(range_fr, self.b_var).grid(row=2, column=1, padx=2, pady=5)

        # plot and save buttons
        ui.create_btn(sb, "Plot Analysis", self._on_plot).pack(fill="x", padx=20, pady=10)
        ui.create_btn(sb, "Save Graph Image ", self._on_save, False).pack(fill="x", padx=20, pady=5)

        # the text area where math results are shown
        self.results_txt = tk.Text(sb, height=12, bg=ui.theme["input_bg"], 
                                   fg=ui.theme["text"], relief="flat", font=("Consolas", 9))
        self.results_txt.pack(fill="x", padx=15, pady=10)

        # the white area where the graphs go
        self.fig = Figure(facecolor=ui.theme["bg"], tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def _on_plot(self):
        # runs when you click plot. it asks the engine for math then draws it
        try:
            data = engine.compute_calculus(
                self.f_var.get(), 
                (float(self.xmin_var.get()), float(self.xmax_var.get())),
                float(self.a_var.get()), float(self.b_var.get()),
                self.order_var.get(), self.g_var.get()
            )

            if data:
                self.fig.clear()
                # creates 4 windows for different calculus views
                axes = self.fig.subplots(2, 2)
                
                # window 1: just f(x) and the area color
                axes[0,0].plot(data["x"], data["y"], color=ui.theme["accent1"], lw=2)
                mask = (data["x"] >= data["a"]) & (data["x"] <= data["b"])
                axes[0,0].fill_between(data["x"][mask], data["y"][mask], alpha=0.3, color=ui.theme["accent1"])
                axes[0,0].set_title("Original Function", color="white", fontsize=9)

                # window 2: the derivative graph
                axes[0,1].plot(data["x"], data["dy"], color=ui.theme["accent2"], lw=2)
                axes[0,1].set_title("First Derivative", color="white", fontsize=9)

                # window 3: the integral line
                axes[1,0].plot(data["x"], data["int_curve"], color=ui.theme["accent3"], lw=2)
                axes[1,0].fill_between(data["x"], data["int_curve"], alpha=0.1, color=ui.theme["accent3"])
                axes[1,0].set_title("Cumulative Integral", color="white", fontsize=9)

                # window 4: shows area between two functions
                ax_an = axes[1,1]
                ax_an.set_title("Area Between Curves", color="white", fontsize=9)
                if data["g_y"] is not None:
                    ax_an.plot(data["x"], data["y"], color=ui.theme["accent1"], lw=1.5)
                    ax_an.plot(data["x"], data["g_y"], '--', color=ui.theme["accent4"], lw=1.5)
                    ax_an.fill_between(data["x"][mask], data["y"][mask], data["g_y"][mask], 
                                     color=ui.theme["accent4"], alpha=0.25)

                # makes all graphs look clean with the dark theme
                for ax in axes.flatten():
                    ax.set_facecolor(ui.theme["card"])
                    ax.grid(True, color=ui.theme["border"], alpha=0.4)
                    ax.tick_params(colors=ui.theme["subtext"], labelsize=7)

                # updates the text results on the left
                self._update_results(data)
                self.canvas.draw() 
        except Exception as e:
            messagebox.showerror("error", f"could not plot: {e}")

    def _update_results(self, data):
        # clears the old text and puts in new math results
        self.results_txt.delete("1.0", tk.END)
        res = (f"[ functions ]\nf(x) = {data['expr']}\nf'(x) = {data['d_expr']}\n\n"
               f"[ integration ]\narea under: {data['area']:.6f}\nerror: {data['error']:.2e}\n")
        if data['between'] is not None:
            res += f"\n[ area between ]\narea: {data['between']:.6f}"
        self.results_txt.insert(tk.END, res)

    def _on_save(self):
        # lets you save the current graph to your computer
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if path:
            self.fig.savefig(path, dpi=150, facecolor=ui.theme["bg"])
            messagebox.showinfo("success", "graph saved")

if __name__ == "__main__":
    app = CalculusApp()
    app.mainloop()
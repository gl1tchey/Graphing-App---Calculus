import numpy as np
import sympy as sp
from scipy.integrate import quad
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Transformations allow inputs like '2x' instead of '2*x' [cite: 222, 223]
TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)

def compute_calculus(func_str, x_range, a, b, deriv_order=1, g_str=None):
    x_sym = sp.symbols('x')
    try:
        # Standardize and parse the expression [cite: 228, 689]
        expr = parse_expr(func_str.strip(), transformations=TRANSFORMATIONS)
        f_num = sp.lambdify(x_sym, expr, 'numpy')
        
        # 1. Global Plotting Data [cite: 696]
        x_plot = np.linspace(x_range[0], x_range[1], 1000)
        y_plot = f_num(x_plot)
        if np.isscalar(y_plot): y_plot = np.full_like(x_plot, y_plot)

        # 2. Derivative (Symbolic for results, Numerical for plot) [cite: 680, 692]
        d_expr = sp.diff(expr, x_sym, deriv_order)
        d_num = sp.lambdify(x_sym, d_expr, 'numpy')
        dy_plot = d_num(x_plot)
        if np.isscalar(dy_plot): dy_plot = np.full_like(x_plot, dy_plot)

        # 3. Numerical Integration (Area Value) 
        area_val, error = quad(f_num, a, b)
        
        # Integral Curve (Cumulative) [cite: 682, 246]
        dx = x_plot[1] - x_plot[0]
        integral_curve = np.cumsum(y_plot) * dx
        
        # 4. Area Between Curves (Optional) [cite: 683, 498]
        between_val = None
        g_plot = None
        if g_str:
            g_expr = parse_expr(g_str.strip(), transformations=TRANSFORMATIONS)
            g_num = sp.lambdify(x_sym, g_expr, 'numpy')
            g_plot = g_num(x_plot)
            if np.isscalar(g_plot): g_plot = np.full_like(x_plot, g_plot)
            # Area = integral of |f(x) - g(x)|
            diff_f = lambda x_v: abs(float(f_num(x_v)) - float(g_num(x_v)))
            between_val, _ = quad(diff_f, a, b)

        return {
            "x": x_plot, "y": y_plot, "dy": dy_plot, "int_curve": integral_curve,
            "a": a, "b": b, "area": area_val, "error": error,
            "expr": expr, "d_expr": d_expr, "between": between_val, "g_y": g_plot
        }
    except Exception as e:
        print(f"Engine Error: {e}")
        return None
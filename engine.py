import numpy as np
import sympy as sp
from scipy.integrate import quad
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# helps the app understand 2x as 2 times x
transformations = standard_transformations + (implicit_multiplication_application,)

def compute_calculus(func_str, x_range, a, b, deriv_order=1, g_str=None):
    # makes sure x is recognized as a variable
    x_sym = sp.symbols('x')
    
    # helper to clean up human typing like ^ or sin
    def clean_math(text):
        if not text: return ""
        return text.lower().replace('^', '**')

    try:
        # turns the text into a real math expression
        f_clean = clean_math(func_str)
        if not f_clean: return None
        
        expr = parse_expr(f_clean, transformations=transformations)
        f_num = sp.lambdify(x_sym, expr, 'numpy')
        
        # creates the points for the graph
        x_plot = np.linspace(x_range[0], x_range[1], 1000)
        y_plot = f_num(x_plot)
        if np.isscalar(y_plot): y_plot = np.full_like(x_plot, y_plot)

        # does the derivative
        d_expr = sp.diff(expr, x_sym, deriv_order)
        d_num = sp.lambdify(x_sym, d_expr, 'numpy')
        dy_plot = d_num(x_plot)
        if np.isscalar(dy_plot): dy_plot = np.full_like(x_plot, dy_plot)

        # calculates the area under the curve
        area_val, error = quad(f_num, a, b)
        
        # makes the line for the integral graph
        integral_curve = np.cumsum(y_plot) * (x_plot[1] - x_plot[0]) 
        
        # handles the second function if you want to find area between two curves
        between_val, g_plot = None, None
        if g_str and g_str.strip():
            g_clean = clean_math(g_str)
            g_expr = parse_expr(g_clean, transformations=transformations)
            g_num = sp.lambdify(x_sym, g_expr, 'numpy')
            g_plot = g_num(x_plot)
            if np.isscalar(g_plot): g_plot = np.full_like(x_plot, g_plot)
            
            # finds the difference between the two functions for the area
            diff_f = lambda v: abs(float(f_num(v)) - float(g_num(v)))
            between_val, _ = quad(diff_f, a, b)

        # sends all the math back to the main app
        return {
            "x": x_plot, "y": y_plot, "dy": dy_plot, "int_curve": integral_curve,
            "a": a, "b": b, "area": area_val, "error": error,
            "expr": expr, "d_expr": d_expr, "between": between_val, "g_y": g_plot
        }
    except Exception as e:
        print(f"math error: {e}")
        return None
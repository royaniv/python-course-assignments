import tkinter as tk
from funct import expgrowth


def calculate():
    try:
        N0 = float(entry_N0.get())
        r = float(entry_r.get())
        t = float(entry_t.get())
        k = float(entry_k.get())

        final_amount = expgrowth(N0, r, t, k)
        result_label.config(text=f"Final amount (N(t)): {final_amount:.4f}")

    except ValueError:
        result_label.config(text="Error: please enter valid numbers")


# Window
root = tk.Tk()
root.title("Exponential Growth Calculator")
root.geometry("320x300")

# Equation (shown at top)
equation_label = tk.Label(
    root,
    text="N(t) = N₀ · e^((r − k)t)",
    font=("Arial", 12, "bold")
)
equation_label.pack(pady=10)

# Inputs
tk.Label(root, text="Initial amount (N0)").pack()
entry_N0 = tk.Entry(root)
entry_N0.pack()

tk.Label(root, text="Growth rate (r)").pack()
entry_r = tk.Entry(root)
entry_r.pack()

tk.Label(root, text="Time (t)").pack()
entry_t = tk.Entry(root)
entry_t.pack()

tk.Label(root, text="Decay rate (k)").pack()
entry_k = tk.Entry(root)
entry_k.pack()

# Button
tk.Button(root, text="Calculate", command=calculate).pack(pady=10)

# Output
result_label = tk.Label(root, text="")
result_label.pack()

# Run
root.mainloop()
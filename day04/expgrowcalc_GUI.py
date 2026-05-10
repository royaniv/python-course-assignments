import tkinter as tk
import matplotlib.pyplot as plt
from funct import expgrowth

history = []

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

    history.append(f"{final_amount:.4f}")

    history_label.config(text=str(history))

def plot_graph():

    try:
        N0 = float(entry_N0.get())
        r = float(entry_r.get())
        t = float(entry_t.get())
        k = float(entry_k.get())

        times = []
        values = []

        current_time = 0

        while current_time <= t:

            value = expgrowth(N0, r, current_time, k)

            times.append(current_time)
            values.append(value)

            current_time += 1

        plt.plot(times, values)
        plt.xlabel("Time")
        plt.ylabel("N(t)")
        plt.title("Exponential Growth")
        plt.show()

    except ValueError:
        result_label.config(text="Error: please enter valid numbers")

def save_history():

    file = open("expgrowcalc_GUI_history.txt", "w")
    file.write(str(history))
    file.close()

def clear_fields():

    entry_N0.delete(0, tk.END)
    entry_r.delete(0, tk.END)
    entry_t.delete(0, tk.END)
    entry_k.delete(0, tk.END)

    result_label.config(text="")
# Window
root = tk.Tk()
root.title("Exponential Growth Calculator")
root.geometry("400x500")

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
tk.Button(root, text="Plot Growth Curve", command=plot_graph).pack(pady=5)
tk.Button(root, text="Clear", command=clear_fields).pack(pady=5)
tk.Button(root, text="Save History", command=save_history).pack(pady=5)

# Output
result_label = tk.Label(root, text="")
result_label.pack()

history_label = tk.Label(root, text="")
history_label.pack()

# Run
root.mainloop()
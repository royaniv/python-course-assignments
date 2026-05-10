09.05.26 I copied over all my work from day03 to extend the file. I want to show population growth over time instead of only one final value on a curve using the "expgrowcalc_GUI.py" file.

I installed pip install "matplotlib" using "pip install matplotlib". 
Now to add a Plot Growth Curve graph and a button so when clicked it will calculate values from time 0 → t and display graph window:
1. Added a "def plot_graph():" 
2. Added a button to create the growth curve "- tk.Button(root, text="Plot Growth Curve", command=plot_graph).pack(pady=5)".

I also added save history button under" def history():" and clear button "def clear_fields():" and a show history with "history = []", "history.append(f"{final_amount:.4f}")", "history_label.config(text=str(history))".

I also added a "requirements.txt" files with "matplotlib" and generated a ".gitignore" file so pycache is no on github.

this is the end of day04 explanation the rest of the readme is old explanation but includes the calculation explanation for the program so I am leaving it in.

-------------------------------------------------------
copied over from day02:
Exponential Growth Calculation  
This program calculates the final amount (N) after a certain time (t) given an initial amount (N0) and a growth rate (r) using the formula:N = N0 * e^((r-k) * t)
N0 = initial number of items  
r = growth rate (per unit time) e.g., 0.05 for 5% growth per unit time  
t = time (in the same units as the growth rate)  
k = decay rate (per unit time) e.g., 0.02 for 2% decay per unit time
example inputs should be small to avoid overflow issues with the exponential function.   
e.g., N0 = 100, r = 0.05, t = 10   

Using ChatGPT I asked: "what should I write in expontential growth to give 'e' in python?  
The answer was math.exp
Also the explanations for each term include suggestions that I was given when writing the code in the file.
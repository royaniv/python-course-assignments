Exponential Growth Calculation  
This program calculates the final amount (N) after a certain time (t) given an initial amount (N0) and a growth rate (r) using the formula:N = N0 * e^(r * t)  
N0 = initial number of items  
r = growth rate (per unit time) e.g., 0.05 for 5% growth per unit time  
t = time (in the same units as the growth rate)  
k = decay rate (per unit time) e.g., 0.02 for 2% decay per unit time
example inputs should be small to avoid overflow issues with the exponential function.   
e.g., N0 = 100, r = 0.05, t = 10   

Using ChatGPT I asked: "what should I write in expontential growth to give 'e' in python?  
The answer was math.exp
Also the explanations for each term include suggestions that I was given when writing the code in the file.
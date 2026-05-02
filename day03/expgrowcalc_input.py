# exponential growth calculation using a function and input

from expgrowfunct import expgrowth

if __name__ == "__main__":
    N0 = float(input("initial amount (N0): "))
    r = float(input("growth rate (r): "))
    t = float(input("time (t): "))
    k = float(input("decay rate (k): "))

    final_amount = expgrowth(N0, r, t, k)
    print(f"Final amount (N(t)): {final_amount}")

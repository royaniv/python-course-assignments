import sys

from expgrowfunct import expgrowth

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python exprgrowcalc_sysargv.py N0 r t k")
        print("Example: python exprgrowcalc_sysargv.py 100 0.05 10 0.02")
        sys.exit(1)

    try:
        N0 = float(sys.argv[1])
        r = float(sys.argv[2])
        t = float(sys.argv[3])
        k = float(sys.argv[4])
    except ValueError:
        print("All arguments must be numbers.")
        sys.exit(1)

    final_amount = expgrowth(N0, r, t, k)
    print(f"Final amount (N) after time t: {final_amount}")

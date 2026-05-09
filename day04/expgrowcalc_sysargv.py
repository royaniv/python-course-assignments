import sys

from funct import expgrowth


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python expgrowcalc_sysargv.py N0 r t k")
        print("Example: python expgrowcalc_sysargv.py 100 0.05 10 0.02")
        sys.exit(1)

    N0 = float(sys.argv[1])
    r = float(sys.argv[2])
    t = float(sys.argv[3])
    k = float(sys.argv[4])

    final_amount = expgrowth(N0, r, t, k)
    print(f"Final amount (N) after time t: {final_amount}")

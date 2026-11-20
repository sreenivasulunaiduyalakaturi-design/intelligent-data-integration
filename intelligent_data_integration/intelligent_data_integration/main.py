"""Run the Intelligent Data Integration pipeline."""
import argparse
from idi import integrate


def main():
    p = argparse.ArgumentParser(description="Intelligent Data Integration")
    p.add_argument("--input", default="data", help="folder with CSV/JSON sources")
    p.add_argument("--output", default="integrated_output.csv")
    p.add_argument("--threshold", type=float, default=0.85)
    args = p.parse_args()

    result = integrate(args.input, args.threshold)
    result.to_csv(args.output, index=False)
    print(f"\nSaved to {args.output}\n")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()

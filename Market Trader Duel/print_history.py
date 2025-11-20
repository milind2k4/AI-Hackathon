import csv
import os

def print_history(filename="simulation_history.csv"):
    if not os.path.exists(filename):
        print(f"No history file found at {filename}")
        return

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    if not data:
        print("History file is empty.")
        return

    # Calculate column widths
    headers = data[0]
    col_widths = [len(h) for h in headers]
    
    for row in data[1:]:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    # Format string
    fmt = " | ".join([f"{{:<{w}}}" for w in col_widths])
    separator = "-+-".join(["-" * w for w in col_widths])

    # Print Table
    print(separator)
    print(fmt.format(*headers))
    print(separator)
    
    for row in data[1:]:
        print(fmt.format(*row))
    print(separator)

if __name__ == "__main__":
    print_history()

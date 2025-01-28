import heapq
import math
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Canvas

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(chars, freq):
    priority_queue = [Node(char, f) for char, f in zip(chars, freq)]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)

    return huffman_codes

def calculate_frequencies(input_string):
    char_counts = {}
    for char in input_string:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1

    total_chars = len(input_string)
    chars = list(char_counts.keys())
    freq = [count / total_chars for count in char_counts.values()]
    return chars, freq, char_counts

def calculate_huffman(input_string):
    chars, freq, char_counts = calculate_frequencies(input_string)
    root = build_huffman_tree(chars, freq)
    huffman_codes = generate_huffman_codes(root)

    sorted_huffman_codes = sorted(huffman_codes.items(), key=lambda item: (len(item[1]), chars.index(item[0])))

    average_code_length = sum(frequency * len(huffman_codes[char]) for char, frequency in zip(chars, freq))
    entropy = sum(frequency * math.log2(1 / frequency) for frequency in freq)
    efficiency = entropy / average_code_length

    return root, sorted_huffman_codes, char_counts, average_code_length, entropy, efficiency

def draw_huffman_tree(canvas, node, x, y, x_offset):
    if node.left is not None:
        canvas.create_line(x, y, x - x_offset, y + 50)
        draw_huffman_tree(canvas, node.left, x - x_offset, y + 50, x_offset // 2)
    if node.right is not None:
        canvas.create_line(x, y, x + x_offset, y + 50)
        draw_huffman_tree(canvas, node.right, x + x_offset, y + 50, x_offset // 2)

    if node.symbol is not None:
        canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue")
        canvas.create_text(x, y, text=node.symbol)
    else:
        canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightgray")
        canvas.create_text(x, y, text=f"{node.frequency:.2f}")

def on_calculate():
    input_text = text_input.get().strip()
    if not input_text:
        messagebox.showerror("Error", "Please enter a valid text fragment.")
        return

    root_node, sorted_codes, char_counts, avg_length, entropy, efficiency = calculate_huffman(input_text)

    for row in table.get_children():
        table.delete(row)

    for char, code in sorted_codes:
        frequency = f"{char_counts[char]}/{len(input_text)}"
        table.insert("", "end", values=(char.upper(), frequency, code, len(code)))

    avg_code_length_var.set(f"{avg_length:.4f} bits")
    entropy_var.set(f"{entropy:.4f} bits/symbol")
    efficiency_var.set(f"{efficiency * 100:.2f}%")

    canvas.delete("all")
    canvas.config(scrollregion=(0, 0, 800, 800))
    draw_huffman_tree(canvas, root_node, 400, 20, 200)

root = tk.Tk()
root.title("Huffman Coding Application")

input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky="EW")
ttk.Label(input_frame, text="Enter a text fragment:").grid(row=0, column=0, sticky="W")
text_input = ttk.Entry(input_frame, width=40)
text_input.grid(row=0, column=1, padx=5)
ttk.Button(input_frame, text="Find", command=on_calculate).grid(row=0, column=2, padx=5)

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=1, column=0, sticky="NSEW")

canvas_frame = ttk.Frame(main_frame)
canvas_frame.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)
canvas = Canvas(canvas_frame, width=800, height=250, bg="white")
canvas.grid(row=0, column=0, sticky="NSEW")
canvas_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas_scroll.grid(row=0, column=1, sticky="NS")
canvas.configure(yscrollcommand=canvas_scroll.set)

columns = ("Symbol", "Frequency", "Code", "Length")
table_frame = ttk.Frame(main_frame)
table_frame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=100)
table.grid(row=0, column=0, sticky="NSEW")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.grid(row=0, column=1, sticky="NS")
table.configure(yscrollcommand=scrollbar.set)

results_frame = ttk.Frame(root, padding="10")
results_frame.grid(row=2, column=0, sticky="EW")

avg_code_length_var = tk.StringVar()
entropy_var = tk.StringVar()
efficiency_var = tk.StringVar()

metrics = ["Average Code Length", "Entropy", "Efficiency"]
vars = [avg_code_length_var, entropy_var, efficiency_var]
for i, metric in enumerate(metrics):
    ttk.Label(results_frame, text=f"{metric}:").grid(row=i, column=0, sticky="W")
    ttk.Label(results_frame, textvariable=vars[i]).grid(row=i, column=1, sticky="W")

formula_frame = ttk.Frame(root, padding="10")
formula_frame.grid(row=3, column=0, sticky="EW")
ttk.Label(formula_frame, text="Formulas:").grid(row=0, column=0, sticky="W")
ttk.Label(formula_frame, text="1. Average Code Length (L) = Σ (frequency * code length)").grid(row=1, column=0, sticky="W")
ttk.Label(formula_frame, text="2. Entropy (H) = Σ (frequency * log2(1 / frequency))").grid(row=2, column=0, sticky="W")
ttk.Label(formula_frame, text="3. Efficiency (η) = H / L").grid(row=3, column=0, sticky="W")

root.columnconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
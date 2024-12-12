import heapq, math

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

input_string = input("Enter a text fragment: ").strip()
chars, freq, char_counts = calculate_frequencies(input_string)
root = build_huffman_tree(chars, freq)
huffman_codes = generate_huffman_codes(root)
sorted_huffman_codes = sorted(huffman_codes.items(), key=lambda item: (len(item[1]), -char_counts[item[0]]))

average_code_length = sum(frequency * len(huffman_codes[char]) for char, frequency in zip(chars, freq))
entropy = sum(frequency * math.log2(1 / frequency) for frequency in freq)
efficiency = entropy / average_code_length

print("\n" + "-" * 50)
print(f"{'Symbols (Frequency)':<25}{'Code':<10}{'Length':<10}")
print("-" * 50)
for char, code in sorted_huffman_codes:
    frequency = f"{char_counts[char]}/{len(input_string)}"
    length = len(code)
    print(f"    {char.upper()} ({frequency})\t\t  {code:<10} {length:<10}")
print("-" * 50)
print("Encode Table".center(50,' '))

print("\nAverage Code Length:")
print("= Σ (frequency * code length)")
print(f"= {average_code_length:.4f} bits")
print("\nEntropy:")
print("= Σ (frequency * log2(1 / frequency))")
print(f"= {entropy:.4f} bits/symbol")
print("\nEfficiency:")
print("= Entropy / Average Code Length")
print(f"= {efficiency * 100:.2f}%\n")
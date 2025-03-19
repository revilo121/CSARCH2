import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random

# ----------------------------
# Cache Simulator Class
# ----------------------------
class CacheSimulator:
    def __init__(self, total_memory_blocks):
        self.total_memory_blocks = total_memory_blocks
        self.cache_blocks = 32          # Fixed number of cache blocks
        self.associativity = 8          # 8-way set associative (Group 7)
        self.num_sets = self.cache_blocks // self.associativity  # 32/8 = 4 sets
        # Initialize cache: a list with one list per set; each set stores entries as dicts: { 'block': int, 'timestamp': int }
        self.cache = [ [] for _ in range(self.num_sets) ]
        self.time_counter = 0           # Global counter to record order of accesses
        self.hits = 0
        self.misses = 0
        self.log = []                   # List to hold the trace log

    def access(self, block_address):
        self.time_counter += 1
        # Validate block address against total memory blocks.
        if block_address >= self.total_memory_blocks:
            self.log.append(f"Invalid block address: {block_address} (exceeds total memory blocks)")
            return

        # Determine the set using modulo operation.
        set_index = block_address % self.num_sets

        # Check for a hit: search the set for the block.
        found = False
        for entry in self.cache[set_index]:
            if entry['block'] == block_address:
                found = True
                entry['timestamp'] = self.time_counter  # Update timestamp for MRU
                self.hits += 1
                self.log.append(f"Access block {block_address}: HIT in set {set_index}")
                break

        if not found:
            self.misses += 1
            self.log.append(f"Access block {block_address}: MISS in set {set_index}")
            # If there is room in the set, simply load the block.
            if len(self.cache[set_index]) < self.associativity:
                self.cache[set_index].append({'block': block_address, 'timestamp': self.time_counter})
                self.log.append(f"Loaded block {block_address} into set {set_index}")
            else:
                # MRU Replacement: Identify the block with the highest timestamp.
                mru_index = None
                mru_time = -1
                for i, entry in enumerate(self.cache[set_index]):
                    if entry['timestamp'] > mru_time:
                        mru_time = entry['timestamp']
                        mru_index = i
                replaced_block = self.cache[set_index][mru_index]['block']
                self.cache[set_index][mru_index] = {'block': block_address, 'timestamp': self.time_counter}
                self.log.append(f"Replaced block {replaced_block} with block {block_address} in set {set_index} (MRU replaced)")

    def run_sequence(self, sequence):
        for block in sequence:
            self.access(block)

    def get_statistics(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        miss_rate = self.misses / total if total > 0 else 0
        # For simulation purposes, assume:
        #   Cache hit time = 1 unit
        #   Main memory access (on a miss) = 101 units (1 for cache access + 100 for memory access)
        total_time = self.hits * 1 + self.misses * 101
        avg_time = total_time / total if total > 0 else 0
        return {
            'Total Accesses': total,
            'Hits': self.hits,
            'Misses': self.misses,
            'Hit Rate': hit_rate,
            'Miss Rate': miss_rate,
            'Total Memory Access Time': total_time,
            'Average Memory Access Time': avg_time
        }

    def get_cache_snapshot(self):
        snapshot = ""
        for set_index, cache_set in enumerate(self.cache):
            snapshot += f"Set {set_index}:\n"
            for entry in cache_set:
                snapshot += f"  Block: {entry['block']}, Last Access: {entry['timestamp']}\n"
        return snapshot

# ----------------------------
# Test Sequence Generators
# ----------------------------
def generate_sequential_sequence(n):
    """
    Sequential test: Addresses 0 to 2*n - 1 repeated 4 times.
    For our fixed cache (n=32), that is addresses 0 to 63.
    """
    seq = list(range(0, 2*n))
    return seq * 4

def generate_random_sequence(n, total_memory_blocks):
    """
    Random test: Generate 4*n random addresses in the range [0, total_memory_blocks-1].
    """
    seq = [random.randint(0, total_memory_blocks-1) for _ in range(4*n)]
    return seq

def generate_midrepeat_sequence(n):
    """
    Mid-Repeat test:
      - First part: 0 to n-1
      - Then, mid-repeat: 1 to n-1
      - Then, last part: n to 2*n-1
    Repeat the combined sequence 4 times.
    """
    first_part = list(range(0, n))
    mid_repeat = list(range(1, n))
    last_part = list(range(n, 2*n))
    seq = first_part + mid_repeat + last_part
    return seq * 4

# ----------------------------
# GUI Application
# ----------------------------
class CacheSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cache Simulator - Group 7 (8-way BSA + MRU)")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="NSEW")

        # Total Memory Blocks input
        ttk.Label(frame, text="Total Memory Blocks (min 1024):").grid(row=0, column=0, sticky="W")
        self.memory_blocks_var = tk.IntVar(value=1024)
        self.memory_blocks_entry = ttk.Entry(frame, textvariable=self.memory_blocks_var, width=10)
        self.memory_blocks_entry.grid(row=0, column=1, sticky="W")

        # Test Case Selection
        ttk.Label(frame, text="Select Test Case:").grid(row=1, column=0, sticky="W")
        self.test_case_var = tk.StringVar()
        self.test_case_combo = ttk.Combobox(frame, textvariable=self.test_case_var, state="readonly", 
                                            values=["Sequential", "Random", "Mid-Repeat"])
        self.test_case_combo.current(0)
        self.test_case_combo.grid(row=1, column=1, sticky="W")

        # Run Simulation Button
        self.run_button = ttk.Button(frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Simulation Log Display
        ttk.Label(frame, text="Simulation Log:").grid(row=3, column=0, sticky="W", pady=(10,0))
        self.log_text = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.log_text.grid(row=4, column=0, columnspan=2, pady=5)

        # Cache Snapshot Display
        ttk.Label(frame, text="Cache Snapshot:").grid(row=5, column=0, sticky="W", pady=(10,0))
        self.snapshot_text = scrolledtext.ScrolledText(frame, width=80, height=10)
        self.snapshot_text.grid(row=6, column=0, columnspan=2, pady=5)

        # Statistics Display
        ttk.Label(frame, text="Statistics:").grid(row=7, column=0, sticky="W", pady=(10,0))
        self.stats_text = scrolledtext.ScrolledText(frame, width=80, height=5)
        self.stats_text.grid(row=8, column=0, columnspan=2, pady=5)

    def run_simulation(self):
        # Clear previous outputs
        self.log_text.delete(1.0, tk.END)
        self.snapshot_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)

        # Validate Total Memory Blocks
        try:
            total_memory_blocks = int(self.memory_blocks_var.get())
            if total_memory_blocks < 1024:
                messagebox.showerror("Input Error", "Total Memory Blocks must be at least 1024.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for Total Memory Blocks.")
            return

        # Fixed n = 32 cache blocks (per specification)
        n = 32
        test_case = self.test_case_var.get()
        if test_case == "Sequential":
            sequence = generate_sequential_sequence(n)
        elif test_case == "Random":
            sequence = generate_random_sequence(n, total_memory_blocks)
        elif test_case == "Mid-Repeat":
            sequence = generate_midrepeat_sequence(n)
        else:
            messagebox.showerror("Test Case Error", "Unknown test case selected.")
            return

        # Create the cache simulator and run the simulation
        simulator = CacheSimulator(total_memory_blocks)
        simulator.run_sequence(sequence)

        # Display simulation log
        for line in simulator.log:
            self.log_text.insert(tk.END, line + "\n")

        # Display cache snapshot
        snapshot = simulator.get_cache_snapshot()
        self.snapshot_text.insert(tk.END, snapshot)

        # Display performance statistics
        stats = simulator.get_statistics()
        stats_str = "\n".join(f"{key}: {value}" for key, value in stats.items())
        self.stats_text.insert(tk.END, stats_str)

        messagebox.showinfo("Simulation Completed", "Cache simulation has completed.")

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorApp(root)
    root.mainloop()

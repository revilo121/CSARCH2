# CSARCH2
Designed a cache simulation system and analyze the various test set scenarios of the assigned cache mapping and replacement policy.

## Overview
This project is an **8-way set-associative cache simulator** with **Most Recently Used (MRU) replacement policy**. The simulator is implemented using Python and **Tkinter** for the graphical interface. The cache has a fixed size of **32 blocks**, divided into **4 sets** (since each set has 8 blocks). The simulator allows users to test cache performance using different access patterns.

## Features
- **Configurable Total Memory Blocks** (minimum 1024)
- **8-way set-associative caching**
- **MRU Replacement Policy**
- **Three Test Cases**:
  - *Sequential*: Accesses memory blocks in a linear increasing order.
  - *Random*: Generates random memory block accesses.
  - *Mid-Repeat*: Introduces repeated accesses to test locality.
- **Performance Metrics**: Displays hit rate, miss rate, and memory access time.
- **Cache Visualization**: Shows the content of each set after simulation.

## How It Works
1. **Address Mapping**: The block address is mapped to a set using `block_address % num_sets`.
2. **Cache Access**:
   - If the block exists in the set (hit), update its timestamp.
   - If it’s a miss, load the block into the set.
   - If the set is full, replace the *Most Recently Used (MRU)* block.
3. **Test Sequences**: The user selects a test case to evaluate cache efficiency.
4. **Results & Statistics**: The simulator logs each access, updates cache state, and calculates hit/miss rates.

## Analysis
- **Sequential Access**: Leads to high misses initially but improves with repeated iterations.
- **Random Access**: Has a low hit rate due to scattered accesses.
- **Mid-Repeat**: Balances locality and variation, often achieving moderate hit rates.
- **MRU Policy Impact**: Unlike LRU, MRU evicts the most recently used block, making it suitable for workloads with frequent access pattern shifts.

## Usage
1. **Run the script**: `python cache_simulator.py`
2. **Enter total memory blocks** (min. 1024).
3. **Select a test case**.
4. **Click "Run Simulation"** to execute the test.
5. **Review logs, cache state, and statistics**.

## Future Improvements
- Allow dynamic cache sizes.
- Implement additional replacement policies (e.g., LRU, FIFO).
- Support more test patterns to simulate real-world workloads.

## Video Demo Link
https://drive.google.com/file/d/1iUsR9FO7nTqhrW2qUCjv81EIETWt4t5f/view?usp=drive_link

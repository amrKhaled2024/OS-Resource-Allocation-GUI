# Deadlock Detection & Avoidance Simulator

## Overview
This project is a graphical simulator for understanding deadlock conditions in operating systems and how to avoid them using algorithms such as the Banker's Algorithm. It visually represents processes and resources, simulates request and allocation edges, detects deadlocks, and demonstrates safe and unsafe states.

The simulator is implemented in Python using the `tkinter` library for the GUI and `networkx` for graph management.

---

## Features
- Add processes with arrival time and burst time.
- Add resources with multiple instances.
- Create **Request Edges** (Process → Resource).
- Create **Assignment Edges** (Resource → Process).
- Visual detection of cycles in the resource allocation graph to identify deadlocks.
- Banker's Algorithm implementation to check system safety and avoid deadlocks.
- View underlying data structures for debugging and learning.
- Reset the simulation at any time.

---

## Installation

1. Ensure you have Python 3.x installed.
2. Install required dependencies using pip:

```bash
pip install networkx
```
## Run the simulator
``` bash
python deadlock_simulator.py
```

## Usage

- **Add Process:** Click the button and input a unique process name starting with `P`, along with arrival and burst times.

- **Add Resource:** Click the button and input a unique resource name starting with `R`, and the number of instances.

- **Add Request Edge:** Select a process and a resource to create a request edge.

- **Add Assignment Edge:** Select a resource and a process to create an assignment edge.

- **Check Deadlock:** Detect cycles in the graph to identify deadlocks.

- **Banker's Algorithm:** Check if the current allocation and request state is safe.

- **View Data Structures:** Display current allocations, requests, and available resources.

- **Reset Simulator:** Clear all data and start fresh.

---

## How It Works

- **Resource Allocation Graph:** Processes and resources are nodes; edges represent requests and allocations.

- **Deadlock Detection:** Uses cycle detection in the directed graph.

- **Banker's Algorithm:** Evaluates if the system is in a safe state by simulating process executions and resource releases.

---

## Code Structure

- `deadlock_simulator.py` - Main program containing the GUI and logic.

- Uses `tkinter` for UI, `networkx` for graph management.

---

## Future Improvements

- Support for multiple requests and releases dynamically.

- Enhanced visualization with animations.

- Save/load simulation states.

- More detailed reports on deadlock cycles.

## Author
Created by `Amr Khaled`

import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
from networkx.exception import NetworkXNoCycle

class DeadlockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection & Avoidance Simulator")
        self.root.geometry("1000x700")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 11), padding=6)
        style.configure('TLabel', font=('Helvetica', 11))
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))

        header = ttk.Frame(root, padding=10)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Deadlock Detection & Avoidance Simulator", style='Title.TLabel').pack()

        self.canvas = tk.Canvas(root, bg="#f5f5f5", width=800, height=600, highlightthickness=2, highlightbackground="#999")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.panel = ttk.Frame(root, padding=10)
        self.panel.pack(side=tk.LEFT, fill=tk.Y)

        buttons = [
            ("Add Process", self.add_process_prompt),
            ("Add Resource", self.add_resource_prompt),
            ("Add Request Edge", self.add_request_edge),
            ("Add Assignment Edge", self.add_assignment_edge),
            ("Check Deadlock", self.check_deadlock),
            ("Banker's Algorithm", self.Avoidance_bankerAlgorithm),
            ("View Data Structures", self.display_datastructure),
            ("Reset Simulator", self.reset_simulator)
        ]

        for text, command in buttons:
            ttk.Button(self.panel, text=text, command=command).pack(pady=6, fill=tk.X)

        self.graph = nx.DiGraph()
        self.nodes = {}
        self.process_data = {}
        self.resource_data = {}
        self.process_count = 0
        self.resource_count = 0

    def validate_number(self, value):
        try:
            return int(value) >= 0
        except:
            return False

    def add_process_prompt(self):
        top = tk.Toplevel(self.root)
        top.title("Add Process")
        labels = ["Process Name (P#)", "Arrival Time", "Burst Time"]
        entries = []
        for label in labels:
            ttk.Label(top, text=label).pack()
            e = ttk.Entry(top)
            e.pack()
            entries.append(e)

        def submit():
            name, arrival, burst = [e.get().strip() for e in entries]
            if not name.startswith("P") or name in self.nodes:
                return messagebox.showerror("Error", "Invalid or duplicate process name.")
            if not self.validate_number(arrival) or not self.validate_number(burst):
                return messagebox.showerror("Error", "Times must be non-negative integers.")
            x, y = 100 + self.process_count * 100, 100
            self.draw_circle(name, x, y, 'skyblue')
            self.process_count += 1
            self.process_data[name] = {"arrival": int(arrival), "burst": int(burst)}
            top.destroy()

        ttk.Button(top, text="Add", command=submit).pack(pady=5)

    def add_resource_prompt(self):
        top = tk.Toplevel(self.root)
        top.title("Add Resource")
        ttk.Label(top, text="Resource Name (R#)").pack()
        entry_name = ttk.Entry(top)
        entry_name.pack()
        ttk.Label(top, text="Instance Count").pack()
        entry_instances = ttk.Entry(top)
        entry_instances.pack()

        def submit():
            name = entry_name.get().strip()
            instances = entry_instances.get().strip()
            if not name.startswith("R") or name in self.nodes:
                return messagebox.showerror("Error", "Invalid or duplicate resource name.")
            if not self.validate_number(instances):
                return messagebox.showerror("Error", "Instance count must be a non-negative integer.")
            x, y = 100 + self.resource_count * 100, 300
            self.resource_data[name] = {"instances": int(instances)}
            self.draw_rect(name, x, y, 'gold')
            self.resource_count += 1
            top.destroy()

        ttk.Button(top, text="Add", command=submit).pack(pady=5)

    def draw_circle(self, name, x, y, color):
        self.canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, outline="black", width=2)
        self.canvas.create_text(x, y, text=name, font=('Arial', 10, 'bold'))
        self.nodes[name] = (x, y)
        self.graph.add_node(name)

    def draw_rect(self, name, x, y, color):
        self.canvas.create_rectangle(x-30, y-30, x+30, y+30, fill=color, outline="black", width=2, tags=name)
        self.canvas.create_text(x, y, text=name, font=('Arial', 10, 'bold'))
        self.canvas.create_text(x, y - 40, text=f"Instances: {self.resource_data[name]['instances']}", 
                                fill="black", font=('Arial', 8), tags=f"{name}_inst")
        self.nodes[name] = (x, y)
        self.graph.add_node(name)
        self.canvas.tag_bind(name, "<Button-1>", lambda e, n=name: self.edit_resource_instances(n))

    def add_edge(self, from_node, to_node, dashed=False):
        if from_node not in self.nodes or to_node not in self.nodes:
            return messagebox.showerror("Error", "Invalid node names.")
        if dashed and not (from_node.startswith("P") and to_node.startswith("R")):
            return messagebox.showerror("Error", "Request edges must go from Process to Resource.")
        if not dashed and not (from_node.startswith("R") and to_node.startswith("P")):
            return messagebox.showerror("Error", "Assignment edges must go from Resource to Process.")
        x1, y1 = self.nodes[from_node]
        x2, y2 = self.nodes[to_node]
        style = (5, 2) if dashed else None
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, dash=style, fill="darkred", width=2)
        self.graph.add_edge(from_node, to_node)

    def add_request_edge(self):
        self.prompt_edge("Add Request Edge", dashed=True)

    def add_assignment_edge(self):
        self.prompt_edge("Add Assignment Edge", dashed=False)

    def prompt_edge(self, title, dashed):
        top = tk.Toplevel(self.root)
        top.title(title)
        ttk.Label(top, text="From:").pack()
        entry_from = ttk.Entry(top)
        entry_from.pack()
        ttk.Label(top, text="To:").pack()
        entry_to = ttk.Entry(top)
        entry_to.pack()

        def submit():
            self.add_edge(entry_from.get().strip(), entry_to.get().strip(), dashed)
            top.destroy()

        ttk.Button(top, text="Add", command=submit).pack(pady=5)

    def check_deadlock(self):
        try:
            cycle = nx.find_cycle(self.graph, orientation='original')
            cycle_str = " → ".join(u for u, v, d in cycle) + f" → {cycle[0][0]}"
            messagebox.showinfo("Deadlock Detected", f"Cycle: {cycle_str}")
        except NetworkXNoCycle:
            messagebox.showinfo("No Deadlock", "No cycles detected.")

    def Avoidance_bankerAlgorithm(self):
        processes = sorted(self.process_data)
        resources = sorted(self.resource_data)
        p_len, r_len = len(processes), len(resources)
        allocation = [[0]*r_len for _ in range(p_len)]
        max_matrix = [[1]*r_len for _ in range(p_len)]
        available = [self.resource_data[r]['instances'] for r in resources]
        for u, v in self.graph.edges():
            if u.startswith("P") and v.startswith("R"):
                i, j = processes.index(u), resources.index(v)
                max_matrix[i][j] = 1
            elif u.startswith("R") and v.startswith("P"):
                i, j = processes.index(v), resources.index(u)
                allocation[i][j] = 1
                available[j] -= 1
        need = [[max_matrix[i][j] - allocation[i][j] for j in range(r_len)] for i in range(p_len)]
        finish = [False]*p_len
        safe_sequence = []
        while len(safe_sequence) < p_len:
            found = False
            for i in range(p_len):
                if not finish[i] and all(need[i][j] <= available[j] for j in range(r_len)):
                    for j in range(r_len):
                        available[j] += allocation[i][j]
                    safe_sequence.append(processes[i])
                    finish[i] = True
                    found = True
                    break
            if not found:
                break
        if len(safe_sequence) == p_len:
            messagebox.showinfo("Safe State", f"System is in safe state.\nSequence: {' → '.join(safe_sequence)}")
        else:
            messagebox.showwarning("Unsafe State", "System is in unsafe state!\nRequest may lead to deadlock.")

    def display_datastructure(self):
        top = tk.Toplevel(self.root)
        top.title("System Datastructures")
        processes = sorted(self.process_data)
        resources = sorted(self.resource_data)
        p_len, r_len = len(processes), len(resources)
        allocation_matrix = [[0]*r_len for _ in range(p_len)]
        request_matrix = [[0]*r_len for _ in range(p_len)]
        available_vector = [self.resource_data[r]["instances"] for r in resources]

        for u, v in self.graph.edges():
            if u.startswith("P") and v.startswith("R"):
                i, j = processes.index(u), resources.index(v)
                request_matrix[i][j] = 1
            elif u.startswith("R") and v.startswith("P"):
                i, j = processes.index(v), resources.index(u)
                allocation_matrix[i][j] = 1
                available_vector[j] -= 1

        need_matrix = [[request_matrix[i][j] - allocation_matrix[i][j] for j in range(r_len)] for i in range(p_len)]

        def create_matrix_label(frame, matrix, title, row_labels, col_labels):
            tk.Label(frame, text=title, font=('Arial', 10, 'bold')).pack()
            mat_frame = tk.Frame(frame)
            mat_frame.pack(pady=2)
            tk.Label(mat_frame, text='').grid(row=0, column=0)
            for j, label in enumerate(col_labels):
                tk.Label(mat_frame, text=label, fg='red', padx=5).grid(row=0, column=j+1)
            for i, row in enumerate(matrix):
                tk.Label(mat_frame, text=row_labels[i]).grid(row=i+1, column=0)
                for j, val in enumerate(row):
                    tk.Label(mat_frame, text=str(val)).grid(row=i+1, column=j+1)

        wrapper = tk.Frame(top)
        wrapper.pack(padx=10, pady=10)
        create_matrix_label(wrapper, allocation_matrix, "Allocation Matrix", processes, resources)
        create_matrix_label(wrapper, request_matrix, "Request Matrix", processes, resources)
        create_matrix_label(wrapper, need_matrix, "Need Matrix", processes, resources)

        tk.Label(wrapper, text="Available Vector", font=('Arial', 10, 'bold')).pack()
        vec_frame = tk.Frame(wrapper)
        vec_frame.pack(pady=2)
        for i, label in enumerate(resources):
            tk.Label(vec_frame, text=label, fg='red', padx=5).grid(row=0, column=i)
        for i, val in enumerate(available_vector):
            tk.Label(vec_frame, text=str(val)).grid(row=1, column=i)


    def edit_resource_instances(self, resource_name):
        top = tk.Toplevel(self.root)
        top.title(f"Edit {resource_name}")
        ttk.Label(top, text=f"Current Instances: {self.resource_data[resource_name]['instances']}").pack()
        ttk.Label(top, text="New Instance Count:").pack()
        entry_new = ttk.Entry(top)
        entry_new.pack()

        def update():
            new_val = entry_new.get().strip()
            if not self.validate_number(new_val):
                return messagebox.showerror("Error", "Instance count must be a non-negative integer")
            self.resource_data[resource_name]['instances'] = int(new_val)
            x, y = self.nodes[resource_name]
            self.canvas.delete(f"{resource_name}_inst")
            self.canvas.create_text(x, y - 40, text=f"Instances: {new_val}", fill="black", font=('Arial', 8), tags=f"{resource_name}_inst")
            top.destroy()
            self.check_deadlock()

        ttk.Button(top, text="Update", command=update).pack(pady=5)

    def reset_simulator(self):
        self.canvas.delete("all")
        self.graph.clear()
        self.nodes.clear()
        self.process_data.clear()
        self.resource_data.clear()
        self.process_count = 0
        self.resource_count = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockSimulator(root)
    root.mainloop()
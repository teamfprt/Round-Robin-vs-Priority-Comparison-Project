import tkinter as tk
from tkinter import messagebox
import customtkinter as tkk
from copy import deepcopy

from models.process import Process
from algorithms.round_robin import round_robin
from algorithms.priority import priority_scheduling, calculate_metrics


class APP:
    def __init__(self, root):
        self.starvation_risk = ""
        self.better_algo = ""
        root.title("Scheduling Comparison")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.main_frame = tkk.CTkFrame(root)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.input_frame = tkk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=0, column=0, sticky="nsew")
        self.input_frame.grid_rowconfigure(0, weight=0)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.result_frame = tkk.CTkScrollableFrame(self.main_frame, height=800)
        self.result_frame.grid_rowconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=0)
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(1, weight=1)

        pad_buttons = {"padx": 5, "pady": 5}
        pad = {"padx": 5, "pady": 5}
        self.entries_padding = {"padx": 10, "pady": 10}
        self.buttons_padding = {"padx": 10, "pady": 10}
        self.frame_of_buttons_padding = {"padx": 10, "pady": 10}
        self.my_font_menu_buttons = tkk.CTkFont(family="Arial", size=16, weight="normal")
        self.my_font = tkk.CTkFont(family="Arial", size=18, weight="normal")
        self.my_font_label = tkk.CTkFont(family="Arial", size=20, weight="normal")
        self.my_font_label_main = tkk.CTkFont(family="Arial", size=22, weight="normal")
        self.count_process_round_robin = ""
        self.count_process_priority = ""
        self.arr_p_round_robin = []
        self.arr_p_priority = []

        self.entries = []

        # -----------Menu Bar--------------
        self.menu_bar = tkk.CTkFrame(self.input_frame, width=100)
        self.menu_bar.grid(row=0, column=0, columnspan=2, sticky="we")

        self.load_button_case1 = tkk.CTkButton(self.menu_bar, text="Load Case A", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_a)
        self.load_button_case1.grid(row=0, column=0, **pad_buttons)

        self.load_button_case2 = tkk.CTkButton(self.menu_bar, text="Load Case B", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_b)
        self.load_button_case2.grid(row=0, column=1, **pad_buttons)

        self.load_button_case3 = tkk.CTkButton(self.menu_bar, text="Load Case C", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_c)
        self.load_button_case3.grid(row=0, column=2, **pad_buttons)

        self.load_button_case4 = tkk.CTkButton(self.menu_bar, text="Load Case D", fg_color="black", font=self.my_font_menu_buttons, command=self.load_case_d)
        self.load_button_case4.grid(row=0, column=3, **pad_buttons)

        self.load_button_case5 = tkk.CTkButton(self.menu_bar, text="Load Case E", fg_color="black", font=self.my_font_menu_buttons)
        self.load_button_case5.grid(row=0, column=4, **pad_buttons)

        # -----------Left Frame-----------
        self.left_frame = tkk.CTkFrame(self.input_frame)
        self.left_frame.grid(row=1, column=0, sticky="nsew")

        self.left_frame_label = tkk.CTkLabel(self.left_frame, text="Priority Scheduling", font=self.my_font_label_main)
        self.left_frame_label.grid(row=0, columnspan=2)

        self.left_frame_label_entry1 = tkk.CTkLabel(self.left_frame, text="Process ID", font=self.my_font_label)
        self.left_frame_label_entry1.grid(row=1, column=0)
        self.left_frame_entry1 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry1.grid(row=1, column=1, sticky="nsew", **self.entries_padding)

        self.left_frame_label_entry2 = tkk.CTkLabel(self.left_frame, text="Process arrival", font=self.my_font_label)
        self.left_frame_label_entry2.grid(row=2, column=0)
        self.left_frame_entry2 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry2.grid(row=2, column=1, sticky="nsew", **self.entries_padding)

        self.left_frame_label_entry3 = tkk.CTkLabel(self.left_frame, text="Process burst", font=self.my_font_label)
        self.left_frame_label_entry3.grid(row=3, column=0)
        self.left_frame_entry3 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry3.grid(row=3, column=1, sticky="nsew", **self.entries_padding)

        self.left_frame_label_entry4 = tkk.CTkLabel(self.left_frame, text="Process Priority", font=self.my_font_label)
        self.left_frame_label_entry4.grid(row=4, column=0)
        self.left_frame_entry4 = tkk.CTkEntry(self.left_frame, font=self.my_font)
        self.left_frame_entry4.grid(row=4, column=1, sticky="nsew", **self.entries_padding)

        # -------------left frame of Buttons-------------
        self.left_frame_frame_buttons = tkk.CTkFrame(self.left_frame)
        self.left_frame_frame_buttons.grid(row=5, column=1, sticky="nsew", **self.frame_of_buttons_padding)
        self.left_frame_frame_buttons.grid_columnconfigure((0, 1, 2), weight=1)
        self.left_frame_frame_buttons.grid_rowconfigure(0, weight=1)

        self.left_frame_add_process = tkk.CTkButton(self.left_frame_frame_buttons, text="Add Process", font=self.my_font, command=self.add_process_priority)
        self.left_frame_add_process.grid(row=0, column=0, sticky="nsew", **self.buttons_padding)

        self.left_frame_reset_process = tkk.CTkButton(self.left_frame_frame_buttons, text="Reset Processes", font=self.my_font, fg_color="red", command=self.reset_process_priority)
        self.left_frame_reset_process.grid(row=0, column=1, sticky="nsew", **self.buttons_padding)

        self.left_frame_load_process = tkk.CTkButton(self.left_frame_frame_buttons, text="Load Process", font=self.my_font, fg_color="black", command=self.load_process_priority)
        self.left_frame_load_process.grid(row=0, column=2, sticky="nsew", **self.buttons_padding)

        self.left_frame_count_process = tkk.CTkLabel(self.left_frame, text="Process Number: 0", font=self.my_font_label)
        self.left_frame_count_process.grid(row=5, column=0, **pad)

        # ---------Right Frame--------
        self.right_frame = tkk.CTkFrame(self.input_frame)
        self.right_frame.grid(row=1, column=1, sticky="nsew")
        self.right_frame_label = tkk.CTkLabel(self.right_frame, text="Round Robin", font=self.my_font_label_main)
        self.right_frame_label.grid(row=0, columnspan=2)

        self.right_frame_label_entry1 = tkk.CTkLabel(self.right_frame, text="Process ID", font=self.my_font_label)
        self.right_frame_label_entry1.grid(row=1, column=0)
        self.right_frame_entry1 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry1.grid(row=1, column=1, sticky="nsew", **self.entries_padding)

        self.right_frame_label_entry2 = tkk.CTkLabel(self.right_frame, text="Process arrival", font=self.my_font_label)
        self.right_frame_label_entry2.grid(row=2, column=0)
        self.right_frame_entry2 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry2.grid(row=2, column=1, sticky="nsew", **self.entries_padding)

        self.right_frame_label_entry3 = tkk.CTkLabel(self.right_frame, text="Process burst", font=self.my_font_label)
        self.right_frame_label_entry3.grid(row=3, column=0)
        self.right_frame_entry3 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry3.grid(row=3, column=1, sticky="nsew", **self.entries_padding)

        self.right_frame_label_entry4 = tkk.CTkLabel(self.right_frame, text="Quantum Time", font=self.my_font_label)
        self.right_frame_label_entry4.grid(row=4, column=0)
        self.right_frame_entry4 = tkk.CTkEntry(self.right_frame, font=self.my_font)
        self.right_frame_entry4.grid(row=4, column=1, sticky="nsew", **self.entries_padding)

        # -------Frame of Buttons-------
        self.right_frame_frame_buttons = tkk.CTkFrame(self.right_frame)
        self.right_frame_frame_buttons.grid(row=5, column=1, sticky="nsew", **self.frame_of_buttons_padding)
        self.right_frame_frame_buttons.grid_columnconfigure((0, 1, 2), weight=1)
        self.right_frame_frame_buttons.grid_rowconfigure(0, weight=1)

        self.right_frame_add_process = tkk.CTkButton(self.right_frame_frame_buttons, text="Add Process", font=self.my_font, command=self.add_process_round_robin)
        self.right_frame_add_process.grid(row=0, column=0, sticky="nsew", **self.buttons_padding)

        self.right_frame_reset_process = tkk.CTkButton(self.right_frame_frame_buttons, text="Reset Processes", font=self.my_font, fg_color="red", command=self.reset_process_round_robin)
        self.right_frame_reset_process.grid(row=0, column=1, sticky="nsew", **self.buttons_padding)

        self.right_frame_load_process = tkk.CTkButton(self.right_frame_frame_buttons, text="Load Process", font=self.my_font, fg_color="black", command=self.load_process_round_robin)
        self.right_frame_load_process.grid(row=0, column=2, sticky="nsew", **self.buttons_padding)

        self.right_frame_count_process = tkk.CTkLabel(self.right_frame, text="Process Number: 0", font=self.my_font_label)
        self.right_frame_count_process.grid(row=5, column=0)

        # ----------Start Simulation button------------
        self.run_simulation = tkk.CTkButton(self.input_frame, text="Start Simulation", height=80, font=self.my_font_label, command=self.start_simulation)
        self.run_simulation.grid(row=2, column=0, columnspan=2, sticky="nsew", **pad)

        for i in range(6):  # rows
            self.left_frame.grid_rowconfigure(i, weight=1)
            self.right_frame.grid_rowconfigure(i, weight=1)

        self.left_frame.grid_columnconfigure(0, weight=2)
        self.left_frame.grid_columnconfigure(1, weight=3)

        self.right_frame.grid_columnconfigure(0, weight=2)
        self.right_frame.grid_columnconfigure(1, weight=3)

    def add_process_round_robin(self):
        try:
            pid = int(self.right_frame_entry1.get())
            arrival = int(self.right_frame_entry2.get())
            burst = int(self.right_frame_entry3.get())
            self.quantum = int(self.right_frame_entry4.get())

            if pid < 0 or arrival < 0 or burst < 0 or self.quantum < 0:
                messagebox.showerror("Error", "Invalid Input: Values cannot be negative")
                return

            for pi, a in enumerate(self.arr_p_round_robin):
                if pid == a.id:
                    messagebox.showerror("Error", "Process IP already exist.")
                    self.right_frame_entry1.delete(0, tk.END)
                    self.right_frame_entry2.delete(0, tk.END)
                    self.right_frame_entry3.delete(0, tk.END)
                    self.right_frame_entry4.delete(0, tk.END)
                    self.quantum = None
                    return

            p = Process(pid, arrival, burst, quantum=self.quantum)
            self.arr_p_round_robin.append(p)

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")

            self.right_frame_entry1.delete(0, tk.END)
            self.right_frame_entry2.delete(0, tk.END)
            self.right_frame_entry3.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please fill all fields with numbers.")

    def add_process_priority(self):
        try:
            pid = int(self.left_frame_entry1.get())
            arrival = int(self.left_frame_entry2.get())
            burst = int(self.left_frame_entry3.get())
            priority = int(self.left_frame_entry4.get())

            if pid < 0 or arrival < 0 or burst < 0 or priority < 0:
                messagebox.showerror("Error", "Invalid Input: Values cannot be negative")
                return

            for pi, a in enumerate(self.arr_p_priority):
                if pid == a.id:
                    messagebox.showerror("Error", "Process IP already exist.")
                    self.left_frame_entry1.delete(0, tk.END)
                    self.left_frame_entry2.delete(0, tk.END)
                    self.left_frame_entry3.delete(0, tk.END)
                    self.left_frame_entry4.delete(0, tk.END)
                    return

            p = Process(pid, arrival, burst, priority)
            self.arr_p_priority.append(p)

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")

            self.left_frame_entry1.delete(0, tk.END)
            self.left_frame_entry2.delete(0, tk.END)
            self.left_frame_entry3.delete(0, tk.END)
            self.left_frame_entry4.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please fill all fields with numbers.")

    def reset_process_priority(self):
        try:
            self.arr_p_priority.clear()
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")
            self.left_frame_entry1.delete(0, tk.END)
            self.left_frame_entry2.delete(0, tk.END)
            self.left_frame_entry3.delete(0, tk.END)
            self.left_frame_entry4.delete(0, tk.END)
            messagebox.showinfo("Success", "Processes has been resetted")
        except ValueError:
            messagebox.showerror("Error", "Couldn't Delete Processes")

    def reset_process_round_robin(self):
        try:
            self.arr_p_round_robin.clear()
            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")
            self.right_frame_entry1.delete(0, tk.END)
            self.right_frame_entry2.delete(0, tk.END)
            self.right_frame_entry3.delete(0, tk.END)
            self.right_frame_entry4.delete(0, tk.END)
            messagebox.showinfo("Success", "Processes has been resetted")
        except ValueError:
            messagebox.showerror("Error", "Couldn't Delete Processes")













# -----------Load Cases for Both Algorithms-----------
    def load_case_a(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            pid = [1, 2, 3]
            p_arrival = [0, 1, 2]
            p_burst = [5, 3, 4]
            p_priority = [2, 1, 3]
            self.quantum = 3

            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")
            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")
        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_case_b(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            pid = [1, 2, 3]
            p_arrival = [0, 1, 2]
            p_burst = [8, 8, 2]
            p_priority = [3, 3, 1]
            self.quantum = 3

            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")
            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")
        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_case_c(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            self.quantum = 2
            pid = [1, 2, 3]
            p_arrival = [0, 0, 0]
            p_burst = [10, 10, 10]
            p_priority = [1, 2, 3]

            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")
            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")
        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_case_d(self):
        try:
            self.arr_p_round_robin.clear()
            self.arr_p_priority.clear()
            self.quantum = 3
            pid = [1, 2, 3, 4]
            p_arrival = [0, 1, 3, 5]
            p_burst = [10, 3, 3, 3]
            p_priority = [4, 1, 1, 1]

            for i in range(len(pid)):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_round_robin.append(p_rr)
                self.arr_p_priority.append(p_pp)

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")
            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")
            messagebox.showinfo("Success", "Loaded Processes of The Two Algorithms")
        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_process_round_robin(self):
        try:
            self.arr_p_round_robin.clear()
            pid = [1, 2, 3, 4]
            p_arrival = [0, 1, 2, 4]
            p_burst = [5, 3, 8, 6]
            self.quantum = 3

            for i in range(4):
                p_rr = Process(pid[i], p_arrival[i], p_burst[i], quantum=self.quantum)
                self.arr_p_round_robin.append(p_rr)

            self.right_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_round_robin)}")
            messagebox.showinfo("Success", "Loaded Process for Round Robin")
        except ValueError:
            messagebox.showerror("Error", "Failed to load data")

    def load_process_priority(self):
        try:
            self.arr_p_priority.clear()
            pid = [1, 2, 3, 4]
            p_arrival = [0, 1, 2, 4]
            p_burst = [5, 3, 8, 6]
            p_priority = [2, 1, 4, 3]

            for i in range(4):
                p_pp = Process(pid[i], p_arrival[i], p_burst[i], p_priority[i])
                self.arr_p_priority.append(p_pp)

            self.left_frame_count_process.configure(text=f"Process Number: {len(self.arr_p_priority)}")
            messagebox.showinfo("Success", "Loaded Process for Priority Scheduling")
        except ValueError:
            messagebox.showerror("Error", "Failed to load data")






















# -----------Gantt Chart Creation-----------
    def create_gantt_chart(self, frame, timeline, row_start, num_process, merge_consecutive_segments=False):
        if not timeline:
            return

        if merge_consecutive_segments:
            merged = []
            for pid, start, end in timeline:
                if merged and merged[-1][0] == pid and merged[-1][2] == start:
                    merged[-1] = (merged[-1][0], merged[-1][1], end)
                else:
                    merged.append((pid, start, end))
            timeline = merged

        frame.update_idletasks()

        frame_width = frame.winfo_width()
        visible_width = frame_width - 30 if frame_width > 100 else 370

        total_time = timeline[-1][2]
        pixels_per_unit = 25
        calculated_width = total_time * pixels_per_unit

        canvas_draw_width = max(visible_width, calculated_width)

        container = tk.Frame(frame, bg="#2b2b2b")
        container.grid(row=row_start, column=0, columnspan=4, sticky="ew", pady=15, padx=15)
        container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(
            container,
            width=visible_width,
            height=90,
            bg="#2b2b2b",
            highlightthickness=0
        )

        if calculated_width > visible_width:
            scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=scrollbar.set)

            canvas.grid(row=0, column=0, sticky="ew")
            scrollbar.grid(row=1, column=0, sticky="ew", pady=(5, 0))

            canvas.bind("<MouseWheel>", lambda event: canvas.xview_scroll(int(-1 * (event.delta / 120)), "units"))
            canvas.bind("<Button-4>", lambda event: canvas.xview_scroll(-1, "units"))
            canvas.bind("<Button-5>", lambda event: canvas.xview_scroll(1, "units"))
        else:
            canvas.grid(row=0, column=0, sticky="ew")

        canvas.config(scrollregion=(0, 0, canvas_draw_width, 90))

        margin = 15
        usable_width = canvas_draw_width - (2 * margin)
        scale = usable_width / total_time if total_time > 0 else 1

        x = margin
        for pid, start, end in timeline:
            width = (end - start) * scale
            color = "#1f6aa5" if pid != "Idle" else "#555555"

            canvas.create_rectangle(x, 15, x + width, 50, fill=color, outline="white", width=1)

            label_text = f"P{pid}" if pid != "Idle" else "Idle"
            if width > 35:
                canvas.create_text(x + width / 2, 32, text=label_text, fill="white", font=("Arial", 10, "bold"))
            elif width > 18:
                short_text = str(pid) if pid != "Idle" else "I"
                canvas.create_text(x + width / 2, 32, text=short_text, fill="white", font=("Arial", 8, "bold"))

            canvas.create_text(x, 60, text=str(start), fill="#cccccc", font=("Arial", 9), anchor="n")

            x += width

        canvas.create_text(x, 60, text=str(timeline[-1][2]), fill="#cccccc", font=("Arial", 9), anchor="n")

    def back_to_input(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_frame.grid_forget()
        self.input_frame.grid(row=0, column=0, sticky="nsew")

    def generate_analysis(self, prio_avg, rr_avg, processes):
        prio_tat, prio_wt, prio_rt = prio_avg
        rr_tat, rr_wt, rr_rt = rr_avg

        analysis = []

        # Basic Comparison
        if prio_wt < rr_wt:
            analysis.append("Priority Scheduling (Preemptive) minimized average waiting time.")
        elif rr_wt < prio_wt:
            analysis.append("Round Robin provided a lower average waiting time.")

        if prio_rt < rr_rt:
            analysis.append("Priority Scheduling offered faster initial response for high-priority tasks.")
        else:
            analysis.append("Round Robin provided better overall responsiveness for all tasks.")

        # --- Enhanced Starvation Detection Logic ---
        # We check if Priority WT is significantly higher than RR WT, 
        # or if any individual process has an abnormally high WT.
        max_wait = max((p.completion - p.arrival - p.burst) for p in processes)
        
        analysis.append("--- Starvation Risk Assessment ---")
        
        if prio_wt > rr_wt * 1.4 or max_wait > (prio_wt * 2):
            analysis.append("**CRITICAL:** High risk of starvation detected. Low-priority processes are being indefinitely postponed by higher-priority arrivals.")
            analysis.append("Recommendation: Implement 'Aging' to gradually increase the priority of waiting processes.")
            self.starvation_risk = "High"
            self.better_algo = "Round Robin"
        else:
            analysis.append("Starvation risk is low; priorities are balanced or process flow is consistent.")
            self.starvation_risk = "Low"
            self.better_algo = "Priority Scheduling"

        analysis.append("Preemptive Priority is ideal for real-time systems where urgent tasks cannot wait.")
        analysis.append("Round Robin is recommended if fairness and prevention of starvation are the primary goals.")

        return analysis

    def start_simulation(self):
        if not hasattr(self, "quantum"):
            messagebox.showerror("Error", "Please set Quantum Time for Round Robin")
            return
        if self.quantum is None:
            self.quantum = self.arr_p_round_robin[0].quantum

        if not self.arr_p_priority or not self.arr_p_round_robin:
            messagebox.showerror("Error", "Please add processes first.")
            return

        prio_processes = deepcopy(self.arr_p_priority)
        rr_processes = deepcopy(self.arr_p_round_robin)

        prio_done, prio_time_line = priority_scheduling(prio_processes)
        rr_done, rr_time_line = round_robin(rr_processes, self.quantum)

        prio_results, prio_avg = calculate_metrics(prio_done)
        rr_results, rr_avg = calculate_metrics(rr_done)

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.input_frame.grid_forget()
        self.result_frame.grid(row=0, column=0, sticky="nsew")

        back_btn = tkk.CTkButton(
            self.result_frame,
            text="Back",
            command=self.back_to_input
        )
        back_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        def create_table(frame, title, results, avg, time_line, merge_gantt_segments=False):
            frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            count = 0

            tkk.CTkLabel(frame, text=title, font=self.my_font_label_main) \
                .grid(row=0, column=0, columnspan=4, pady=10)

            headers = ["PID", "WT", "TAT", "RT"]
            for col, h in enumerate(headers):
                tkk.CTkLabel(frame, text=h, font=self.my_font_label) \
                    .grid(row=1, column=col, padx=5, pady=5)

            for i, (pid, tat, wt, rt) in enumerate(results, start=2):
                count += 1
                tkk.CTkLabel(frame, text=str(pid), font=self.my_font).grid(row=i, column=0)
                tkk.CTkLabel(frame, text=str(wt), font=self.my_font).grid(row=i, column=1)
                tkk.CTkLabel(frame, text=str(tat), font=self.my_font).grid(row=i, column=2)
                tkk.CTkLabel(frame, text=str(rt), font=self.my_font).grid(row=i, column=3)

            avg_tat, avg_wt, avg_rt = avg
            last_row = len(results) + 2

            tkk.CTkLabel(frame, text="AVG", font=self.my_font_label).grid(row=last_row, column=0)
            tkk.CTkLabel(frame, text=f"{avg_wt:.2f}", font=self.my_font).grid(row=last_row, column=1)
            tkk.CTkLabel(frame, text=f"{avg_tat:.2f}", font=self.my_font).grid(row=last_row, column=2)
            tkk.CTkLabel(frame, text=f"{avg_rt:.2f}", font=self.my_font).grid(row=last_row, column=3)

            for r in range(last_row + 2):
                frame.grid_rowconfigure(r, weight=1)
            self.create_gantt_chart(frame, time_line, last_row + 1, count, merge_gantt_segments)

        self.left_frame_result = tkk.CTkFrame(self.result_frame)
        self.left_frame_result.grid(row=0, column=0, sticky="nsew")

        self.right_frame_result = tkk.CTkFrame(self.result_frame)
        self.right_frame_result.grid(row=0, column=1, sticky="nsew")

        self.bottom_frame_result = tkk.CTkFrame(self.result_frame)
        self.bottom_frame_result.grid(row=1, column=0, columnspan=2, sticky="nsew")

        create_table(self.left_frame_result, "Priority Scheduling Results", prio_results, prio_avg, prio_time_line, merge_gantt_segments=True)
        create_table(self.right_frame_result, "Round Robin Results", rr_results, rr_avg, rr_time_line)

        self.comparison_frame = tkk.CTkFrame(self.bottom_frame_result)
        self.comparison_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.comparison_frame.grid_columnconfigure(0, weight=3)
        self.comparison_frame.grid_columnconfigure(1, weight=2)

        analysis_container = tkk.CTkFrame(self.comparison_frame, fg_color="transparent")
        analysis_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        tkk.CTkLabel(analysis_container, text="Summary & Analysis", font=self.my_font_label_main).pack(pady=(0, 10), anchor="w")

        analysis = self.generate_analysis(prio_avg, rr_avg, prio_done)
        for line in analysis:
            tkk.CTkLabel(analysis_container, text="• " + line, font=self.my_font, anchor='w', justify='left').pack(anchor="w", pady=4)

        conclusion_container = tkk.CTkFrame(self.comparison_frame, fg_color="transparent")
        conclusion_container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        tkk.CTkLabel(conclusion_container, text="Conclusion", font=self.my_font_label_main).pack(pady=(0, 10), anchor="w")

        # better_algo = "Round Robin" if rr_avg[1] < prio_avg[1] else "Priority Scheduling"
        # starvation_risk = "Yes" if prio_avg[1] > rr_avg[1] else "Low"

        conclusions = [
            f"Better Algorithm: {self.better_algo}",
            "Priority improves urgent-task execution.",
            "Round Robin improves fairness.",
            f"Starvation risk: {self.starvation_risk}"
        ]

        for line in conclusions:
            tkk.CTkLabel(conclusion_container, text="• " + line, font=self.my_font, anchor='w', justify='left').pack(anchor="w", pady=4)


# -------RUN-------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    root.configure(background='black')
    app = APP(root)
    root.mainloop()
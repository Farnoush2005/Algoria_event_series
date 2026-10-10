"""
Algoria_event_series

Presented by Farnoush Pourshaban
University of Isfahan
Mathematics and Computer Science Scientific Association (Rika)
Event year: Fall 2026
Session 1: (Logic and Set Theory)
"""

import customtkinter as ctk

# Configure modern dark theme settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# =========================================================
# 1. SAT Solver Engine (DPLL Algorithm)
# =========================================================

def is_clause_satisfied(clause, assignment):
    """
    Checks if a single CNF clause is satisfied under the current variable assignment.
    
    :param clause: List of non-zero integers representing literals (e.g., [-1, 2]).
    :param assignment: Dictionary mapping variable indices to Boolean values {var_id: bool}.
    :return: True if at least one literal evaluates to True, False otherwise.
    """
    for literal in clause:
        var = abs(literal)
        if var in assignment:
            # Literal > 0 implies standard positive variable (P)
            # Literal < 0 implies negated variable (NOT P)
            if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                return True
    return False

def solve_sat_dpll(clauses, assignment=None):
    """
    Solves a Satisfiability Problem (SAT) in Conjunctive Normal Form (CNF) using the DPLL algorithm.
    Includes Unit Propagation and Backtracking search.
    
    :param clauses: List of lists, where each sublist represents a CNF clause.
    :param assignment: Current truth assignments during recursive search.
    :return: Dictionary of truth assignments if SAT, None if UNSAT (Contradiction).
    """
    if assignment is None:
        assignment = {}
    else:
        assignment = assignment.copy()

    # Step 1: Unit Propagation Loop
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            # Find all variables in the clause that haven't been assigned a value yet
            unassigned = [lit for lit in clause if abs(lit) not in assignment]
            
            # Conflict detected: Clause is completely unassigned and unsatisfied (UNSAT branch)
            if len(unassigned) == 0 and not is_clause_satisfied(clause, assignment):
                return None
            
            # Unit Clause Rule: Exactly one unassigned literal remains and clause is not yet satisfied
            if len(unassigned) == 1 and not is_clause_satisfied(clause, assignment):
                unit_lit = unassigned[0]
                var = abs(unit_lit)
                # Force assign truth value to satisfy the unit clause
                assignment[var] = True if unit_lit > 0 else False
                changed = True

    # Step 2: Base Case Verification - Check if all clauses are satisfied under current assignment
    if all(is_clause_satisfied(c, assignment) for c in clauses):
        return assignment

    # Step 3: Branching / Decision Variable Selection
    unassigned_vars = {abs(lit) for clause in clauses for lit in clause if abs(lit) not in assignment}
    if not unassigned_vars:
        return None

    # Pick the first unassigned variable for recursive splitting
    chosen_var = list(unassigned_vars)[0]
    
    # Recursive Branch 1: Assume chosen variable is TRUE
    assignment[chosen_var] = True
    res = solve_sat_dpll(clauses, assignment)
    if res is not None:
        return res

    # Recursive Branch 2: Assume chosen variable is FALSE (Backtracking)
    assignment[chosen_var] = False
    return solve_sat_dpll(clauses, assignment)


# =========================================================
# 2. Modern Dark Dashboard GUI
# =========================================================

class KnightsSATApp(ctk.CTk):
    """
    GUI Application for configuring, parsing, and solving Knights & Knaves logic puzzles via CNF & DPLL.
    """
    def __init__(self):
        super().__init__()

        # Window Title & Display Geometry Setup
        self.title("Knights & Knaves SAT Solver Framework")
        self.geometry("1150x780")
        self.configure(fg_color="#18181b")

        # Master pool of available participant names (Up to 8 max)
        self.all_names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace", "Henry"]
        self.active_names = []
        self.var_map = {}

        # Configure Grid Layout Geometry (2 Main Columns)
        self.grid_columnconfigure(0, weight=0, minsize=400) # Left control sidebar
        self.grid_columnconfigure(1, weight=1)              # Right output console terminal
        self.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # Left Panel: Configuration & Statement Inputs
        # ----------------------------------------------------
        self.left_panel = ctk.CTkFrame(self, fg_color="#27272a", corner_radius=12)
        self.left_panel.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")

        # Left Panel Title Label
        ctk.CTkLabel(
            self.left_panel, 
            text="Configuration & Statements", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f4f4f5"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        # Participant Count Selection Toolbar
        count_frame = ctk.CTkFrame(self.left_panel, fg_color="#18181b", corner_radius=8)
        count_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            count_frame, 
            text="Number of People (1-8):", 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#d4d4d8"
        ).pack(side="left", padx=10, pady=8)

        # Set default initial count to 2 participants
        self.count_var = ctk.StringVar(value="2")
        self.count_dropdown = ctk.CTkOptionMenu(
            count_frame, 
            values=[str(i) for i in range(1, 9)],
            variable=self.count_var,
            width=70,
            fg_color="#27272a", button_color="#3f3f46"
        )
        self.count_dropdown.pack(side="left", padx=5, pady=8)

        self.btn_update = ctk.CTkButton(
            count_frame, 
            text="Set", 
            width=60,
            fg_color="#0284c7", hover_color="#0369a1",
            command=self.update_person_count
        )
        self.btn_update.pack(side="right", padx=10, pady=8)

        # Container Frame for Dynamic Person Inputs (Scrollable)
        self.inputs_frame = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.inputs_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.person_rows = []

        # Action Buttons Section
        self.btn_run = ctk.CTkButton(
            self.left_panel, text="1. Run SAT Solver", fg_color="#0284c7", hover_color="#0369a1", 
            height=38, font=ctk.CTkFont(size=13, weight="bold"), command=self.run_sat_solver
        )
        self.btn_run.pack(fill="x", padx=15, pady=4)

        self.btn_cnf = ctk.CTkButton(
            self.left_panel, text="2. Generate CNF Clauses", fg_color="#0284c7", hover_color="#0369a1", 
            height=38, font=ctk.CTkFont(size=13, weight="bold"), command=self.show_cnf
        )
        self.btn_cnf.pack(fill="x", padx=15, pady=4)

        self.btn_clear = ctk.CTkButton(
            self.left_panel, text="3. Clear Output", fg_color="#dc2626", hover_color="#b91c1c", 
            height=38, font=ctk.CTkFont(size=13, weight="bold"), command=self.clear_logs
        )
        self.btn_clear.pack(fill="x", padx=15, pady=4)

        self.btn_exit = ctk.CTkButton(
            self.left_panel, text="4. Exit App", fg_color="#3f3f46", hover_color="#27272a", 
            height=38, font=ctk.CTkFont(size=13, weight="bold"), command=self.quit
        )
        self.btn_exit.pack(fill="x", padx=15, pady=(4, 15))

        # ----------------------------------------------------
        # Right Panel: Terminal Output & Console Log
        # ----------------------------------------------------
        self.right_panel = ctk.CTkFrame(self, fg_color="#09090b", corner_radius=12, border_width=1, border_color="#27272a")
        self.right_panel.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="nsew")

        # Top Header Bar for Output Terminal Console
        log_header = ctk.CTkFrame(self.right_panel, fg_color="#18181b", height=40, corner_radius=0)
        log_header.pack(fill="x", side="top")
        
        ctk.CTkLabel(
            log_header, 
            text="  ● ● ●   System Terminal & SAT Engine Logs", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            text_color="#71717a"
        ).pack(side="left", padx=10, pady=8)

        # Monospaced Scrollable Text Box for Logs
        self.log_box = ctk.CTkTextbox(
            self.right_panel, 
            fg_color="#09090b", 
            text_color="#22c55e", 
            font=ctk.CTkFont(family="Courier", size=13),
            activate_scrollbars=True
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

        # Output Initial Initialization Log
        self.write_log("--- Knights & Knaves DPLL Framework Initialized ---")
        
        # Build initial UI with default 2 variables
        self.update_person_count()

    def update_person_count(self):
        """
        Dynamically rebuilds statement input dropdown rows based on selected participant count (1 to 8).
        """
        count = int(self.count_var.get())
        
        # Enforce range limits between 1 and 8
        if count < 1:
            count = 1
        elif count > 8:
            count = 8
            self.count_var.set("8")

        # Update active participant subset and mapping (e.g., Alice -> 1, Bob -> 2)
        self.active_names = self.all_names[:count]
        self.var_map = {name: i + 1 for i, name in enumerate(self.active_names)}

        # Clear existing dynamic widgets from scrollable container
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        self.person_rows.clear()

        # Re-populate dynamic UI rows for active participants
        for name in self.active_names:
            row_frame = ctk.CTkFrame(self.inputs_frame, fg_color="#18181b", corner_radius=8)
            row_frame.pack(fill="x", pady=4, padx=2)

            ctk.CTkLabel(
                row_frame, 
                text=f"{name}:", 
                font=ctk.CTkFont(size=12, weight="bold"), 
                text_color="#f4f4f5"
            ).pack(anchor="w", padx=10, pady=(6, 2))

            # Dropdown menu for claim statement type
            claim_combo = ctk.CTkOptionMenu(
                row_frame, 
                values=[
                    "No Claim / Unknown",
                    "At least one of us is a Knave",
                    "All of us are Knights",
                    "Claims target is a Knave",
                    "Claims target is a Knight"
                ],
                fg_color="#27272a", button_color="#3f3f46", text_color="#ffffff", dropdown_fg_color="#27272a", height=30
            )
            claim_combo.pack(fill="x", padx=10, pady=(0, 4))

            # Dropdown menu for target participant
            target_list = [n for n in self.active_names if n != name] + [name]
            target_combo = ctk.CTkOptionMenu(
                row_frame,
                values=target_list,
                fg_color="#27272a", button_color="#3f3f46", text_color="#ffffff", dropdown_fg_color="#27272a", height=30
            )
            target_combo.pack(fill="x", padx=10, pady=(0, 6))

            # Keep references for reading GUI inputs
            self.person_rows.append({
                "name": name,
                "claim": claim_combo,
                "target": target_combo
            })

        self.write_log(f"\n[CONFIG UPDATED]: Set active participants count to {count}.")
        self.write_log(f"Active Variables: {self.var_map}")

    def write_log(self, text):
        """Appends formatted text string to terminal log display."""
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def clear_logs(self):
        """Clears all console terminal text."""
        self.log_box.delete("1.0", "end")

    def get_generated_cnf(self):
        """
        Translates GUI dropdown statement selections into CNF logic clauses (Bi-conditional Equivalence).
        
        :return: Tuple containing (list of CNF clauses, list of statement descriptions).
        """
        cnf_clauses = []
        descriptions = []

        for row in self.person_rows:
            speaker = row["name"]
            var_id = self.var_map[speaker]
            claim_type = row["claim"].get()
            target = row["target"].get()
            target_id = self.var_map[target]

            # Case 1: Speaker claims "At least one of us is a Knave"
            # Formula: P_speaker <=> (NOT P_1 OR NOT P_2 OR ... OR NOT P_N)
            if claim_type == "At least one of us is a Knave":
                cnf_clauses.append([-var_id] + [-v for v in self.var_map.values()])
                cnf_clauses.append([var_id])
                descriptions.append(f"{speaker}: At least one is a Knave")

            # Case 2: Speaker claims "All of us are Knights"
            # Formula: P_speaker <=> (P_1 AND P_2 AND ... AND P_N)
            elif claim_type == "All of us are Knights":
                for v in self.var_map.values():
                    cnf_clauses.append([-var_id, v])
                cnf_clauses.append([var_id] + [-v for v in self.var_map.values()])
                descriptions.append(f"{speaker}: All are Knights")

            # Case 3: Speaker claims target is a Knave
            # Formula: P_speaker <=> NOT P_target
            elif claim_type == "Claims target is a Knave":
                cnf_clauses.append([-var_id, -target_id])
                cnf_clauses.append([var_id, target_id])
                descriptions.append(f"{speaker}: {target} is a Knave")

            # Case 4: Speaker claims target is a Knight
            # Formula: P_speaker <=> P_target
            elif claim_type == "Claims target is a Knight":
                cnf_clauses.append([-var_id, target_id])
                cnf_clauses.append([var_id, -target_id])
                descriptions.append(f"{speaker}: {target} is a Knight")

        return cnf_clauses, descriptions

    def run_sat_solver(self):
        """
        Executes the DPLL solver on current CNF clauses and prints truth assignments or contradiction status.
        """
        self.write_log("══════════════════════════════════════════════════")
        self.write_log(f"▶ Executing DPLL SAT Solver for {len(self.active_names)} Participants...")
        
        cnf_clauses, descriptions = self.get_generated_cnf()

        # Execute DPLL Algorithm
        solution = solve_sat_dpll(cnf_clauses)

        # Render output based on satisfiability result
        if solution:
            self.write_log("[STATUS]: SUCCESS (SAT Satisfiability Model Found)\n")
            self.write_log("Truth Value Assignments:")
            for name, v_id in self.var_map.items():
                is_knight = solution.get(v_id, False)
                status = "Knight 🛡 [True]" if is_knight else "Knave  🗡️ [False]"
                self.write_log(f"   • {name:<10} ───►  {status}")
        else:
            self.write_log("[STATUS]: CONTRADICTION DETECTED (UNSAT)")
            self.write_log("   ✖ No valid truth assignment exists for these statements.")
        
        self.write_log("══════════════════════════════════════════════════\n")

    def show_cnf(self):
        """
        Displays raw CNF clauses and variable indexing in the terminal box for verification.
        """
        self.write_log("--- Generated CNF Formula & Clauses ---")
        self.write_log(f"Variable Indexing: {self.var_map}")
        cnf_clauses, descriptions = self.get_generated_cnf()

        self.write_log("\nActive Rules:")
        for desc in descriptions:
            self.write_log(f" - {desc}")

        self.write_log(f"\nCNF Representation ({len(cnf_clauses)} clauses):")
        self.write_log(str(cnf_clauses))
        self.write_log("------------------------------------------\n")

# Main Application Entry Point
if __name__ == "__main__":
    app = KnightsSATApp()
    app.mainloop()
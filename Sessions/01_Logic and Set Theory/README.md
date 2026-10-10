# 📌 Session 01: Logic & Set Theory

Welcome to the official repository for **Session 01** of the **Algoria Event Series**[cite: 1]. This session covers the foundational concepts of mathematical logic, set theory, and their direct applications in computing, hardware design, and automated reasoning.

---

## 🎯 Topics & Core Concepts
- **Historical Evolution:** From Aristotelian deductive logic and George Boole’s algebraic logic to Russell's Paradox and Gödel's Incompleteness Theorems.
- **Computer Science Applications:** 
  - Designing digital logic circuits (Combinational & Sequential logic).
  - Automated theorem proving and boolean satisfiability.
- **Key Frameworks:** Propositional logic, Boolean algebra, CNF (Conjunctive Normal Form), and the DPLL algorithm.

---

## 📂 Session Materials & Contents

This directory contains two interactive and hands-on projects developed for this session:

### 1. 🌐 Logic Gates Simulator (`Logic Gates Simulator.html`)
* **Description:** An interactive, browser-based visual canvas simulator for building and testing digital logic circuits.
* **Supported Gates:** `AND`, `OR`, `NOT`, `XOR`, `NAND`, `NOR`, alongside interactive Input toggles (`0`/`1`).
* **How to Run:** 
  Simply double-click or open `Logic Gates Simulator.html` in any modern web browser.

### 2. 🐍 SAT Solver Engine (`SAT Solver Engine.py`)
* **Description:** A complete, modern desktop GUI application built with `CustomTkinter` and powered by a custom **DPLL Algorithm** implementation. It parses and solves classic "Knights & Knaves" logic puzzles by translating statements into Conjunctive Normal Form (CNF) clauses.
* **Prerequisites:** Python 3.10+ and `customtkinter`.

---

## 🛠️ How to Run the Python SAT Solver

1. Navigate to the session directory in your terminal.
2. Install the required dependencies:
   ```bash
   pip install customtkinter
   ```
3. Run the script:
   ```bash
   python "SAT Solver Engine.py"
   ```

---

## 📄 Presentation Slides
* [Download Session 01 Presentation Slides (PDF)](slides/session-01-slides.pdf) *(Place your PDF file inside the `slides/` folder)*
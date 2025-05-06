
# Nand2Tetris Project 6: Hack Assembler

**An implementation of the Hack Assembler for Nand2Tetris Project 6.**

This project implements a two-pass assembler that translates Hack assembly language into Hack binary machine code. The assembler processes `.asm` files and outputs corresponding `.hack` files with 16-bit machine instructions.

## Features

- **Two-Pass Assembler:**
  - **Pass 1:** Builds the symbol table, resolving label declarations.
  - **Pass 2:** Translates each assembly command to binary, handling variables and predefined symbols.

- **Predefined Symbols:**  
  Includes built-in symbols like `R0`–`R15`, `SCREEN`, `KBD`, `SP`, `LCL`, etc.

- **Error Handling:**  
  Detects and reports syntax errors and undefined symbols.

- **Simple CLI Usage:**  
  Specify the input `.asm` file, and the assembler will generate the `.hack` binary file.

---

## Usage

1️⃣ **Clone the repository:**

```bash
git clone the project
cd nand2tetris-project6
```

2️⃣ **Run the assembler:**

```bash
python assembler.py <path_to_file.asm>
```

Example:

```bash
python assembler.py Add.asm
```

This will create `Add.hack` in the same directory.

---

## Repository Structure

```
├── assembler.py               # Main assembler implementation
├── parser.py                  # Parses assembly commands
├── code.py                    # Translates mnemonics to binary codes
├── symbol_table.py            # Manages symbols and addresses
└── README.md
```

---

## How It Works

- **First Pass:**
  - Scans the `.asm` file to identify `(LABEL)` declarations.
  - Records each label’s corresponding instruction address in the symbol table.

- **Second Pass:**
  - Parses each instruction:
    - **A-instruction (`@value`)**: Converts to binary (either numeric or variable-based).
    - **C-instruction (`dest=comp;jump`)**: Converts using binary templates.

- **Symbols:**
  - Predefined symbols (like `R0`–`R15`, `SCREEN`) are initialized.
  - New variables are dynamically allocated starting at address 16.

---

## Example

**Assembly (`Add.asm`):**

```asm
@2
D=A
@3
D=D+A
@0
M=D
```

**Output (`Add.hack`):**

```
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
```

---

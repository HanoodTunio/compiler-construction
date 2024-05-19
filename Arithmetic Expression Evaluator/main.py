import tkinter as tk
from tkinter import messagebox, scrolledtext
import re
import atexit

# Token types
NUMBER = 'NUMBER'
PLUS = 'PLUS'
MINUS = 'MINUS'
TIMES = 'TIMES'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'

# Token specification
token_specification = [
    (NUMBER,  r'\d+(\.\d*)?'),
    (PLUS,    r'\+'),
    (MINUS,   r'-'),
    (TIMES,   r'\*'),
    (DIVIDE,  r'/'),
    (LPAREN,  r'\('),
    (RPAREN,  r'\)'),
    ('SKIP',  r'[ \t]+'),
    ('MISMATCH', r'.'),
]

HISTORY_FILE = "history.txt"

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for tok in token_specification:
            pattern = re.compile(tok[1])
            match = pattern.match(code, pos)
            if match:
                text = match.group(0)
                if tok[0] != 'SKIP':
                    tokens.append((tok[0], text))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[pos]}")
    return tokens

class Number:
    def __init__(self, value):
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.expr()

    def eat(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == token_type:
            self.pos += 1
        else:
            raise Exception(f"Expected token {token_type}, got {self.tokens[self.pos][0]}")

    def factor(self):
        token = self.tokens[self.pos]
        if token[0] == NUMBER:
            self.eat(NUMBER)
            return Number(float(token[1]))
        elif token[0] == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in (TIMES, DIVIDE):
            token = self.tokens[self.pos]
            if token[0] == TIMES:
                self.eat(TIMES)
            elif token[0] == DIVIDE:
                self.eat(DIVIDE)
            node = BinOp(left=node, op=token[0], right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in (PLUS, MINUS):
            token = self.tokens[self.pos]
            if token[0] == PLUS:
                self.eat(PLUS)
            elif token[0] == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token[0], right=self.term())
        return node

class Evaluator:
    def visit(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, BinOp):
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            if node.op == PLUS:
                return left_val + right_val
            elif node.op == MINUS:
                return left_val - right_val
            elif node.op == TIMES:
                return left_val * right_val
            elif node.op == DIVIDE:
                return left_val / right_val

def evaluate(expression):
    try:
        tokens = tokenize(expression)
        parser = Parser(tokens)
        ast = parser.parse()
        evaluator = Evaluator()
        return evaluator.visit(ast)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def evaluate_expression():
    expression = entry.get()
    if expression.strip():
        result = evaluate(expression)
        if result is not None:
            result_label.config(text=f"Result: {result}", font=("Arial", 12, "bold"))
            history_text.insert(tk.END, f"{expression} = {result}\n")
            history_text.see(tk.END)
            save_history(expression, result)
    else:
        messagebox.showwarning("Warning", "Please enter an expression to evaluate.")

def save_history(expression, result):
    with open(HISTORY_FILE, "a") as file:
        file.write(f"{expression} = {result}\n")

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history_text.insert(tk.END, file.read())
            history_text.see(tk.END)
    except FileNotFoundError:
        pass

def clear_history():
    with open(HISTORY_FILE, "w"):
        pass
    history_text.delete("1.0", tk.END)




def on_exit():
    save_history_on_exit()
    root.quit()

def save_history_on_exit():
    history_content = history_text.get("1.0", tk.END)
    with open(HISTORY_FILE, "w") as file:
        file.write(history_content)



def save_history_on_exit():
    history_content = history_text.get("1.0", tk.END)
    with open(HISTORY_FILE, "w") as file:
        file.write(history_content)



# Create GUI
root = tk.Tk()
root.title("Math Expression Evaluator")
root.geometry("400x400")

# Define styles
entry_style = {"width": 30, "font": ("Arial", 12)}
button_style = {"font": ("Arial", 12), "padx": 10, "pady": 5}
label_style = {"font": ("Arial", 12)}
scrolledtext_style = {"width": 40, "height": 10, "font": ("Arial", 12)}

# Entry field for expression
entry = tk.Entry(root, **entry_style)
entry.pack(pady=10)

# Button to evaluate expression
evaluate_button = tk.Button(root, text="Evaluate", command=evaluate_expression, **button_style)
evaluate_button.pack()

# Label to display result
result_label = tk.Label(root, text="", **label_style)
result_label.pack(pady=10)

# History of evaluated expressions
history_label = tk.Label(root, text="History:", **label_style)
history_label.pack()

history_text = scrolledtext.ScrolledText(root, **scrolledtext_style)
history_text.pack()

# Load history on program start
load_history()

# Button to clear history
clear_button = tk.Button(root, text="Clear History", command=clear_history, **button_style)
clear_button.pack()

# Register exit handler
root.protocol("WM_DELETE_WINDOW", on_exit)

root.mainloop()

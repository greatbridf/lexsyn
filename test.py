import sys
from lexer import * 
from parser import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]

    with open(source_file, 'r') as f:
        text = f.read()

    tokens = run_lexer(text) 
    RustGrammar.compute_first_set()
    parser = LR1Parser()
    ast = LR1Parser().parse(tokens) 
    # ast.to_png()

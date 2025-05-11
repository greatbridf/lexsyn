import sys
from lexer import * 
from parser import *
from astprint import *

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
    image_path = ast_to_png(ast)
    print(f'AST visualization saved to: {image_path}')

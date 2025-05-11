import sys
from lexer import * 
from parser import *
from astprint import *

def export_tokens(tokens: list[Token], filename: str) -> None:
    with open(filename, 'w') as f:
        for token in tokens:
            f.write(f'{token}\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]

    with open(source_file, 'r') as f:
        text = f.read()

    tokens = run_lexer(text) 

    output_dir = os.path.join(os.path.curdir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tokens_path = os.path.join(output_dir, 'tokens.txt')
    export_tokens(tokens, tokens_path)

    print(f'Tokens exported to: {tokens_path}')

    RustGrammar.compute_first_set()
    parser = LR1Parser()
    ast = LR1Parser().parse(tokens) 
    image_path = ast_to_png(ast)
    print(f'AST visualization saved to: {image_path}')

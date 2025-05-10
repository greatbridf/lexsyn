from typing import Callable

from ttoken import Token
import ttoken as tt

KEYWORDS = {
    "i32": tt.TT_I32,
    "let": tt.TT_LET,
    "if": tt.TT_IF,
    "else": tt.TT_ELSE,
    "while": tt.TT_WHILE,
    "return": tt.TT_RETURN,
    "mut": tt.TT_MUT,
    "fn": tt.TT_FN,
    "for": tt.TT_FOR,
    "in": tt.TT_IN,
    "loop": tt.TT_LOOP,
    "break": tt.TT_BREAK,
    "continue": tt.TT_CONTINUE,
}

class Lexer:
    def __init__(self, text: str):
        self.tokens: list[Token] = []
        self.text = text
        self.pos = 0
        self.current_char = self.getchar()
    
    def getchar_at(self, pos: int) -> str | None:
        return self.text[pos] if pos < len(self.text) else None
    
    def getchar(self) -> str | None:
        return self.getchar_at(self.pos)

    def advance(self, count=1) -> None:
        self.pos += count
        self.current_char = self.getchar()

    def peek(self) -> str | None:
        return self.getchar_at(self.pos + 1)
    
    def skip_while(self, pred: Callable[[str], bool]) -> None:
        while self.current_char is not None and pred(self.current_char):
            self.advance()

    def skip_comment(self) -> bool:
        if self.current_char != '/':
            return False
        
        next_char = self.peek()

        if next_char == '/':  # Single-line comment
            self.skip_while(lambda ch: ch != '\n')
            # The newline character itself will be handled by skip_whitespace or consumed if it's the last char

            return True

        if next_char == '*':  # Multi-line comment
            # Consume '/*' to avoid '/*/'
            self.advance(2)
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance(2)  # Consume '*/'
                    break
                self.advance()
            else:
                raise ValueError(f'Unterminated multi-line comment at position {self.pos}')

            return True
        
        return False

    def make_number(self) -> Token:
        num_str = ""

        if self.current_char is None:
            raise RuntimeError("Unexpected EOF while reading number at position {self.pos}.")

        while self.current_char is not None:
            if self.current_char.isalpha():
                raise ValueError(f"Unexpected `{self.current_char}` in number at position {self.pos}.")

            if not self.current_char.isdigit():
                break

            num_str += self.current_char
            self.advance()

        return Token(tt.TT_NUMBER, num_str)

    def make_identifier_or_keyword(self) -> Token:
        ident_str = ''

        if self.current_char is None:
            raise RuntimeError("Unexpected EOF while reading identifier or keyword at position {self.pos}.")
        
        if not (self.current_char.isalpha() or self.current_char == '_'):
            raise RuntimeError(f"Unexpected `{self.current_char}` at position {self.pos}.")

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            ident_str += self.current_char
            self.advance()
        
        token_type = KEYWORDS.get(ident_str, tt.TT_IDENTIFIER)
        return Token(token_type, ident_str)

    def tokenize(self) -> list[Token]:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_while(lambda ch: ch.isspace())
                continue

            if self.skip_comment():
                continue

            if self.current_char.isdigit():
                self.tokens.append(self.make_number())
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.make_identifier_or_keyword())
                continue

            # Two-character tokens
            if self.current_char == '=' and self.peek() == '=':
                self.tokens.append(Token(tt.TT_EQ, '=='))
                self.advance(2)
                continue
            elif self.current_char == '>' and self.peek() == '=':
                self.tokens.append(Token(tt.TT_GTE, '>='))
                self.advance(2)
                continue
            elif self.current_char == '<' and self.peek() == '=':
                self.tokens.append(Token(tt.TT_LTE, '<='))
                self.advance(2)
                continue
            elif self.current_char == '!' and self.peek() == '=':
                self.tokens.append(Token(tt.TT_NE, '!='))
                self.advance(2)
                continue
            elif self.current_char == '-' and self.peek() == '>':
                self.tokens.append(Token(tt.TT_ARROW, '->'))
                self.advance(2)
                continue
            elif self.current_char == '.' and self.peek() == '.':
                self.tokens.append(Token(tt.TT_DOTDOT, '..'))
                self.advance(2)
                continue
            
            # Single-character tokens
            single_char_map = {
                '=': tt.TT_EQUAL, '+': tt.TT_PLUS, '-': tt.TT_MINUS, '*': tt.TT_MUL, '/': tt.TT_DIV,
                '>': tt.TT_GT, '<': tt.TT_LT, 
                '(': tt.TT_LP, ')': tt.TT_RP, 
                '{': tt.TT_LBRACE, '}': tt.TT_RBRACE,
                '[': tt.TT_LBRACKET, ']': tt.TT_RBRACKET,
                ';': tt.TT_SEMICOLON, ':': tt.TT_COLON, ',': tt.TT_COMMA, '.': tt.TT_DOT
            }

            if self.current_char in single_char_map:
                token_type = single_char_map[self.current_char]
                self.tokens.append(Token(token_type, self.current_char))
                self.advance()
                continue
            
            raise ValueError(f"Unknown `{self.current_char}` at position {self.pos}")

        return self.tokens


def run_lexer(text: str) -> list[Token]:
    lexer = Lexer(text)
    return lexer.tokenize()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python lexer.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]

    with open(source_file, 'r') as f:
        text = f.read()

    tokens = run_lexer(text)

    for token in tokens:
        print(token)

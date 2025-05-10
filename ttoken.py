class TokenType:
    _next_id = 0

    def __init__(self, id: int, name: str):
        """
            DO NOT CALL THIS EXPLICITLY, USE THE TT_* GLOBAL CONTANTS
        """
        self.id = TokenType._next_id
        TokenType._next_id += 1

        self.name = name

def _make_token_type(name: str) -> TokenType:
    id = TokenType._next_id
    TokenType._next_id += 1
    return TokenType(id, name)

class Token:
    def __init__(self, type: TokenType, value: str):
        self._type = type
        self._value = value
    
    def type(self) -> TokenType:
        return self._type
    
    def value(self) -> str:
        return self._value

TT_I32 = _make_token_type('i32')
TT_LET = _make_token_type('let')
TT_IF = _make_token_type('if')
TT_ELSE = _make_token_type('else')
TT_WHILE = _make_token_type('while')
TT_RETURN = _make_token_type('return')
TT_MUT = _make_token_type('mut')
TT_FN = _make_token_type('fn')
TT_FOR = _make_token_type('for')
TT_IN = _make_token_type('in')
TT_LOOP = _make_token_type('loop')
TT_BREAK = _make_token_type('break')
TT_CONTINUE = _make_token_type('continue')

TT_NUMBER = _make_token_type('number')
TT_IDENTIFIER = _make_token_type('identifier')

TT_EQUAL = _make_token_type('=')

TT_PLUS = _make_token_type('+')
TT_MINUS = _make_token_type('-')
TT_MUL = _make_token_type('*')
TT_DIV = _make_token_type('/')
TT_EQ = _make_token_type('==')
TT_GT = _make_token_type('>')
TT_GTE = _make_token_type('>=')
TT_LT = _make_token_type('<')
TT_LTE = _make_token_type('<=')
TT_NE = _make_token_type('!=')

TT_LP = _make_token_type('(')
TT_RP = _make_token_type(')')
TT_LBRACE = _make_token_type('{')
TT_RBRACE = _make_token_type('}')
TT_LBRACKET = _make_token_type('[')
TT_RBRACKET = _make_token_type(']')

TT_SEMICOLON = _make_token_type(';')
TT_COLON = _make_token_type(':')
TT_COMMA = _make_token_type(',')

TT_ARROW = _make_token_type('->')
TT_DOT = _make_token_type('.')
TT_DOTDOT = _make_token_type('..')

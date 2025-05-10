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

TT_INTEGER = _make_token_type('integer')

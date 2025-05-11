from collections import defaultdict

# Must have "Empty"
NonTerminalTable = [
    "Program",                      #Program
    "Empty",                        #空 
    "DeclareList",                  #声明串
    "Declare",                      #声明
    "FunctionDeclare",              #函数声明
    "FunctionHeaderDeclare",        #函数头声明
    "SentenceBlock",                #语句块
    "ParameterList",                #形参列表
    "Parameter",                    #形参 
    "Type",                         #类型
    "SentenceList",                 #语句串
    "Sentence",                     #语句
    "VarDeclareInner",              #变量声明内部
    "ReturnSentence",               #返回语句
    "VarDeclareSentence",           #变量声明语句
    "AssignSentence",               #赋值语句
    "Expression",                   #表达式
    "VarDeclareAndAssignSentence",  #变量声明赋值语句
    "AddExpression",                #加法表达式
    "Item",                         #项
    "Factor",                       #因子
    "Element",                      #元素
    "CompareOperator",              #比较运算符
    "AddSubOperator",               #加减运算符
    "MulDivOperator",               #乘除运算符
    "ArgumentList",                 #实参列表
    "IfSentence",                   #if语句
    "ElsePart",                     #else部分
    "AssignableItem",               #可赋值元素
    "LoopSentence",                 #循环语句
    "WhileSentence",                #while语句

    # "Program","S","C","Empty"
]

TerminalTable = [
    "i32",
    "let",
    "if",
    "else",
    "while",
    "return",
    "mut",
    "fn",
    "for",
    "in",
    "loop",
    "break",
    "continue",
    "ID",
    "NUM",
    '=',
    '+','-','*','/','==','>','>=','<','<=','!=',
    ';',':',',',
    '(',')','{','}','[',']',
    '->','.','..',
    '$',
    # "c","d","$"
]


def SymbolfromStr(symbol: str):
    if symbol in NonTerminalTable:
        return NonTerminalSymbol(NonTerminalTable.index(symbol))
    elif symbol in TerminalTable:
        return TerminalSymbol(TerminalTable.index(symbol))
    else:
        raise ValueError(f"Unknown symbol: {symbol}")

class TerminalSymbol:
    def __init__(self, symbol_id: int):
        self.symbol_id = symbol_id

    def __repr__(self):
        return f'{TerminalTable[self.symbol_id]}' 
    
    def __eq__(self, other):
        if not isinstance(other, TerminalSymbol):
            return NotImplemented
        return self.symbol_id == other.symbol_id 
    
    def __hash__(self):
        return hash(self.symbol_id)

class NonTerminalSymbol:
    def __init__(self, symbol_id: int):
        self.symbol_id = symbol_id

    def __repr__(self):
        return f'{NonTerminalTable[self.symbol_id]}'
    
    def __str__(self):
        return NonTerminalTable[self.symbol_id]
    
    def __eq__(self, other):
        if not isinstance(other, NonTerminalSymbol):
            return NotImplemented
        return self.symbol_id == other.symbol_id
    
    def __hash__(self):
        return hash(self.symbol_id)

class Production:
    def __init__(self, left: str, right: list[str]):
        self.left = SymbolfromStr(left)
        self.right = [SymbolfromStr(s) for s in right]
    
    def __len__(self):
        return len(self.right)
    
    def __repr__(self):
        right_str = ' '.join([str(sym) for sym in self.right])
        return f"[{self.left} -> {right_str}]"

class Grammar:
    def __init__(self, productions: list[list[str]], start_symbol: str = "Program"):
        self.productions = [Production(p[0], p[1:]) for p in productions] 
        self.start_symbol = SymbolfromStr(start_symbol) 
        self.terminal_symbols = TerminalTable
        self.non_terminal_symbols = NonTerminalTable
        self.emptyable_set = set() # {NonTerminalSymbol}
        self.first_set = {} # {Symbol: set[TernimalSymbol]}
    
    def compute_first_set(self):
        self.emptyable_set.add(SymbolfromStr("Empty"))

        for t in self.terminal_symbols:
            t = SymbolfromStr(t)
            self.first_set[t] = {t}
        for nt in self.non_terminal_symbols:
            nt = SymbolfromStr(nt)
            self.first_set[nt] = set()
        
        changed = True
        while changed:
            changed = False
            for p in self.productions:
                A = p.left # NonTerminalSymbol

                # Rule: For a production A -> Y1 Y2 ... Yk
                # Add First(Y1) to First(A).
                # If Y1 is nullable, add First(Y2) to First(A).
                # Continue this for Y3, ..., Yk if Y1, ..., Yi-1 are all emptyable.
                for idx, Y in enumerate(p.right):
                    if isinstance(Y, TerminalSymbol):
                        if Y not in self.first_set[A]:
                            self.first_set[A].add(Y)
                            changed = True
                        break # No need to check further symbols in this production
                    else: # Y is a NonTerminalSymbol
                        if Y == SymbolfromStr("Empty"):
                            if len(p.right) == idx + 1 and A not in self.emptyable_set:
                                self.emptyable_set.add(A) 
                                changed = True
                        else:
                            for terminal_in_first_Y in self.first_set[Y]:
                                if terminal_in_first_Y not in self.first_set[A]:
                                    self.first_set[A].add(terminal_in_first_Y)
                                    changed = True
                        
                            # If Y is not nullable, then subsequent symbols don't contribute to First(A)
                            if not Y in self.emptyable_set:
                                break # No need to check further symbols in this production

# Make sure start symbol(Program) is in 0 and only one
RustGrammar = Grammar([
    # 1.1
    ["Program","DeclareList"],
    ["DeclareList","Empty"],
    ["DeclareList","Declare","DeclareList"],
    ["Declare","FunctionDeclare"],
    ["FunctionDeclare","FunctionHeaderDeclare","SentenceBlock"],
    ["FunctionHeaderDeclare",'fn','ID','(',"ParameterList",')'],
    ["ParameterList","Empty"],
    ["SentenceBlock",'{',"SentenceList",'}'],
    ["SentenceList","Empty"],
    # 1.2
    ["SentenceList","Sentence","SentenceList"],
    ["Sentence",';'],
    # 1.3
    ["Sentence","ReturnSentence"],
    ["ReturnSentence",'return',';'],
    # 1.4
    ["ParameterList","Parameter"],
    ["ParameterList","Parameter",',',"ParameterList"],
    ["Parameter","VarDeclareInner",':',"Type"],
    # 1.5
    ["FunctionHeaderDeclare",'fn','ID','(',"ParameterList",')','->',"Type"],
    ["ReturnSentence",'return',"Expression",';'],

    # 2.1
    ["Sentence","VarDeclareSentence"],
    ["VarDeclareSentence",'let',"VarDeclareInner",':',"Type",';'],
    ["VarDeclareSentence",'let',"VarDeclareInner",';'],
    # 2.2
    ["Sentence","AssignSentence"],
    ["AssignSentence","AssignableItem",'=',"Expression",';'],
    # 2.3
    ["Sentence","VarDeclareAndAssignSentence"],
    ["VarDeclareAndAssignSentence",'let',"VarDeclareInner",':',"Type",'=',"Expression",';'],
    ["VarDeclareAndAssignSentence",'let',"VarDeclareInner",'=',"Expression",';'],

    # 3.1
    ["Sentence","Expression",';'],
    ["Expression","AddExpression"],
    ["AddExpression","Item"],
    ["Item","Factor"],
    ["Factor","Factor"],
    ["Element",'NUM'],
    ["Element","AssignableItem"],
    ["Element",'(',"Expression",')'],
    # 3.2
    ["Expression","Expression","CompareOperator","AddExpression"],
    ["AddExpression","AddExpression","AddSubOperator","Item"],
    ["Item","Item","MulDivOperator","Factor"],
    ["CompareOperator",'<'],
    ["CompareOperator",'>'],
    ["CompareOperator",'>='],
    ["CompareOperator",'<='],
    ["CompareOperator",'=='],
    ["CompareOperator",'!='],
    ["AddSubOperator",'+'],
    ["AddSubOperator",'-'],
    ["MulDivOperator",'*'],
    ["MulDivOperator",'/'],
    # 3.3
    ["Element",'ID','(',"ArgumentList",')'], 
    ["ArgumentList","Empty"],
    ["ArgumentList","Expression"],
    ["ArgumentList","Expression",',',"ArgumentList"],
    
    # 4.1
    ["Sentence","IfSentence"],
    ["IfSentence",'if',"Expression","SentenceBlock","ElsePart"],
    ["ElsePart","Empty"],
    ["ElsePart",'else',"SentenceBlock"],

    # 5.1
    ["Sentence","LoopSentence"],
    ["LoopSentence","WhileSentence"],
    ["WhileSentence",'while',"Expression","SentenceBlock"],

    # 0.1
    ["VarDeclareInner",'mut','ID'],

    # 0.2
    ["Type",'i32'],

    # 0.3
    ["AssignableItem",'ID'],

    # ["Program","S"],
    # ["S","C","C"],
    # ["C",'c',"C"],
    # ["C",'d']
])

class LR1Item:
    def __init__(self, production_idx: int, dot_pos: int, lookahead_symbols: set[TerminalSymbol]):
        self.production_idx = production_idx
        self.dot_pos = dot_pos
        self.lookahead_symbols = lookahead_symbols
    
    def __hash__(self):
        return hash((self.production_idx, self.dot_pos))

    def __eq__(self, other):
        if not isinstance(other, LR1Item):
            return NotImplemented
        return (self.production_idx == other.production_idx and
                self.dot_pos == other.dot_pos and
                frozenset(self.lookahead_symbols) == frozenset(other.lookahead_symbols))
    
    def __repr__(self):
        """
        [Left -> Alpha . Beta, {lookahead1, lookahead2, ...}]
        """
        prod = RustGrammar.productions[self.production_idx]
        if prod is None:
            prod_str = f"Production(idx={self.production_idx} not found, dot_pos={self.dot_pos})"
        else:
            left_symbol_name = str(prod.left)
            before_dot = [str(s) for s in prod.right[:self.dot_pos]]
            after_dot = [str(s) for s in prod.right[self.dot_pos:]]
            
            rhs_str = ' '.join(before_dot) + " . " + ' '.join(after_dot)
            prod_str = f"{left_symbol_name} -> {rhs_str}"

        lookaheads_str = ', '.join(sorted(str(s) for s in self.lookahead_symbols))

        return f"[{prod_str}, {{{lookaheads_str}}}]"

    def is_reducible(self):
        return self.dot_pos == len(RustGrammar.productions[self.production_idx])

class LR1Action:
    def __init__(self, action_type: int, value: int):
        self.action_type = action_type  # 0 for shift, 1 for reduce
        self.value = value  # lr1 state number or production index
    
    def __repr__(self):
        if self.action_type == 0:
            return f"S{self.value}"
        elif self.action_type == 1:
            return f"R{self.value}"
        else:
            return f"UnknownAction(type={self.action_type}, value={self.value})"

    def is_shift(self):
        return self.action_type == 0

    def is_reduce(self):
        return self.action_type == 1

class LR1Table:
    def __init__(self, action_table: dict, goto_table: dict):
        self.action_table = action_table  # {state: {token_id: action}}
        self.goto_table = goto_table    # {state: {nonterminal_id: next_state_id}} 
    
    def __repr__(self):
        return f"LR1Table(\n    {self.action_table}\n   {self.goto_table}\n)"
        

class LR1State:
    def __init__(self, items: set[LR1Item]):
        self.items = items

    def __hash__(self):
        return hash(frozenset(self.items))

    def __eq__(self, other):
        return isinstance(other, LR1State) and self.items == other.items
    
    def __repr__(self):
        sorted_items = sorted(list(self.items), key=lambda item: (item.production_idx, item.dot_pos, sorted(s.symbol_id for s in item.lookahead_symbols)))
        item_reprs = ",\n    ".join(repr(item) for item in sorted_items)
        return f"LR1State(\n    {item_reprs}\n)" 
    
    def get_reducible(self):
        items = set()
        for item in self.items:
            if item.is_reducible():
                items.add((item.production_idx, frozenset(item.lookahead_symbols))) 
        return items

def state_transform(state: LR1State, symbol):
    new_items = set()
    for item in state.items:
        production_idx, dot_pos, lookahead_symbols = item.production_idx, item.dot_pos, item.lookahead_symbols
        if dot_pos < len(RustGrammar.productions[production_idx]):
            if RustGrammar.productions[production_idx].right[dot_pos] == symbol:
                new_item = LR1Item(production_idx, dot_pos + 1, lookahead_symbols)
                new_items.add(new_item)
    return LR1State(closure(new_items)) if new_items else None

def get_first(symstr: list, lookhead: set[TerminalSymbol]):
    can_be_empty = True
    first_set = set() 
    for sym in symstr:
        if isinstance(sym, TerminalSymbol):
            first_set.add(sym)
            can_be_empty = False
            break
        elif isinstance(sym, NonTerminalSymbol):
            for terminal in RustGrammar.first_set[sym]:
                first_set.add(terminal) 
            if not sym in RustGrammar.emptyable_set:
                can_be_empty = False
                break
        else:
            raise Exception("get_first error")
    
    if can_be_empty:
        first_set.update(lookhead)
    
    return first_set
    

def closure(items: set[LR1Item]):
    closure_set = set(items)
    changed = True
    while changed:
        changed = False
        new_items = set()
        for item in closure_set:
            prod_idx, dot_pos, lookahead = item.production_idx, item.dot_pos, item.lookahead_symbols
            
            if dot_pos < len(RustGrammar.productions[prod_idx]):
                current_symbol = RustGrammar.productions[prod_idx].right[dot_pos]

                # for [A -> alpha . B beta, a]
                # Add [B -> . gamma, b]
                if isinstance(current_symbol, NonTerminalSymbol):
                    for idx, production in enumerate(RustGrammar.productions):
                        if production.left == current_symbol:
                            new_item = LR1Item(idx, 0, get_first(RustGrammar.productions[prod_idx].right[dot_pos + 1:], lookahead))
                            if new_item not in closure_set:
                                new_items.add(new_item)
                                changed = True

        closure_set.update(new_items)
    return closure_set

class LR1TableBuilder:
    def build(self):
        action_table = defaultdict(dict) 
        goto_table = defaultdict(dict)

        initial_item = LR1Item(0, 0, {SymbolfromStr('$')})
        initial_state = LR1State(closure([initial_item]))
        states_stack = [initial_state]
        states_set = {initial_state: 0}

        while len(states_stack):
            current_state = states_stack.pop() 
            current_state_id = states_set[current_state] 
            # print("current")
            # print(current_state_id)
            # print(current_state)
            # print("")

            items = current_state.get_reducible()
            for production_idx, lookahead_symbols in items:
                # print(current_state_id)
                # print(production_idx)
                # print(lookahead_symbols)
                for symbol in lookahead_symbols:
                    action_table[current_state_id][symbol] = LR1Action(1, production_idx)

            for symbol in RustGrammar.terminal_symbols:
                symbol = SymbolfromStr(symbol)
                next_state = state_transform(current_state, symbol)
                if next_state:
                    # print("next")
                    # print(symbol)
                    # print(next_state)
                    if next_state not in states_set:
                        states_set[next_state] = len(states_set)
                        states_stack.append(next_state)

                    if current_state_id in action_table and symbol in action_table[current_state_id]:
                        raise Exception("Build error") 
                    else:
                        action_table[current_state_id][symbol] = LR1Action(0, states_set[next_state])

            
            for symbol in RustGrammar.non_terminal_symbols:
                symbol = SymbolfromStr(symbol)
                next_state = state_transform(current_state, symbol)
                if next_state:
                    # print("next")
                    # print(symbol)
                    # print(next_state)
                    if next_state not in states_set:
                        states_set[next_state] = len(states_set)
                        states_stack.append(next_state)
                    if current_state_id in goto_table and symbol in goto_table[current_state_id]:
                        raise Exception("Build error") 
                    else:
                        goto_table[current_state_id][symbol] = states_set[next_state]

        return LR1Table(action_table, goto_table)

class ASTNode:
    def __init__(self, symbol, children, val = None):
        self.children = children
        self.symbol = symbol
        self.val = val
    
    def __repr__(self):
        return f"ASTNode {self.symbol} {self.children} {self.val}" 

class AST:
    def __init__(self, root: ASTNode):
       self.root = root

class Token:
    def __init__(self, type: str, value: str):
        self._type = type
        self._value = value
    
    def __repr__(self) -> str:
        return f'Token({repr(self._type)}, `{self._value}`)'
    
    def __str__(self) -> str:
        return f'Token({self._type}, `{self._value}`)'
    
    def value(self) -> str:
        return self._value
    
    def type(self) -> str:
        return self._type


def SymbolfromToken(token: Token):
    return SymbolfromStr(token.type()) 

class LR1Parser:
    def __init__(self):
        self.lr1_table = LR1TableBuilder().build()

    def parse(self, tokens: list[Token]):
        symbol_stack = [] # (ASTNode)
        state_stack = []

        symbol_stack.append(ASTNode(SymbolfromStr('Program'), None))
        state_stack.append(0)
        idx = 0

        while True:
            state = state_stack[-1]
            token = tokens[idx]

            print(symbol_stack)
            print(idx)
            print(token)

            action = self.lr1_table.action_table[state][SymbolfromToken(token)]

            if action.is_shift():
                next_state = action.value
                symbol_stack.append(ASTNode(SymbolfromToken(token), None, token))
                state_stack.append(next_state)
                idx += 1
            elif action.is_reduce():
                production_idx = action.value
                production = RustGrammar.productions[production_idx]

                childs = symbol_stack[-len(production.right):] 

                symbol_stack = symbol_stack[:len(symbol_stack) - len(production.right)] 
                state_stack = state_stack[:len(state_stack) - len(production.right)]
                
                state = state_stack[-1]
                if production.left == SymbolfromStr("Program"):  # parse End
                    return AST(ASTNode(production.left, childs))
                
                next_state = self.lr1_table.goto_table[state][production.left]
                symbol_stack.append(ASTNode(production.left, childs))
                state_stack.append(next_state)
            else:
                raise Exception("Parse error")

if __name__ == "__main__":
    RustGrammar.compute_first_set()
    
    print("compute first finish")
    table = LR1TableBuilder().build() 
    # print(table)

    LR1Parser().parse([Token('c', "c"), Token('d', "d"), Token('d', "d"), Token('$', "$")]) 

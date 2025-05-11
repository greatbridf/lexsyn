from parser import AST, ASTNode, TerminalSymbol, TerminalTable, NonTerminalSymbol, NonTerminalTable
from ttoken import Token, TokenType, TT_NUMBER, TT_IDENTIFIER, TT_PLUS
from graphviz import Digraph
import os

def ast_to_png(ast: AST) -> str:
    """
    Convert the AST to a PNG image using Graphviz.
    The image will be saved in the current working directory with the name 'ast.png'.
    """
    def add_nodes_edges(graph: Digraph, node: ASTNode | None):
        node_id = str(id(node))

        if node.children is None:
            return

        for child in node.children:
            child_id = str(id(child))
            if isinstance(child.symbol, TerminalSymbol):
                child_name = TerminalTable[child.symbol.symbol_id]
            elif isinstance(child.symbol, NonTerminalSymbol):
                child_name = NonTerminalTable[child.symbol.symbol_id]
            else:
                raise RuntimeError(f'Unknown symbol type: {child.symbol}')

            graph.node(child_id, child_name)
            graph.edge(child_id, node_id, child_name)
            add_nodes_edges(graph, child)

    dot = Digraph(comment='二叉树可视化')
    add_nodes_edges(dot, ast.root)

    output_dir = os.path.join(os.path.curdir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, 'ast.png')

    return dot.render(outfile=output_file, format='png', cleanup=True)

if __name__ == "__main__":
    """
    Test:
        Create a simple AST and visualize it.
    """
    # Create a simple AST:  +
    #                       / \
    #                      1   *
    #                         / \
    #                        2   3
    node3 = ASTNode(TerminalSymbol(TerminalTable.index('NUM')), None, Token(TT_NUMBER, '3'))
    node2 = ASTNode(TerminalSymbol(TerminalTable.index('NUM')), None, Token(TT_NUMBER, '2'))
    node_mul = ASTNode(NonTerminalSymbol(NonTerminalTable.index('Factor')), [node2, node3], None)
    node1 = ASTNode(TerminalSymbol(TerminalTable.index('NUM')), [], Token(TT_NUMBER, '1'))
    root_node = ASTNode(NonTerminalSymbol(NonTerminalTable.index('Element')), [node1, node_mul], None)

    ast_instance = AST(root_node)
    image_path = ast_to_png(ast_instance)
    print(f'AST visualization saved to: {image_path}')


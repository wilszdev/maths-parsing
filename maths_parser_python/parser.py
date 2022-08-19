# adaptation of the pseudocode in this video on recursive descent pasrsing:
# https://www.youtube.com/watch?v=SToUyjAsaFk

from lexer import *
from nodetypes import *


def parse(string_to_parse: str) -> TreeNode:
    lex = Lexer(string_to_parse)

    def parse_expr() -> tuple[TreeNode, Token]:
        a, token = parse_term()
        if a is None:
            return

        while 1:
            if token.type == TokenType.PLUS:
                b, token = parse_term()
                if b is None:
                    return
                a = Add(a, b)

            elif token.type == TokenType.MINUS:
                b, token = parse_term()
                if b is None:
                    return
                a = Subtract(a, b)

            else:
                return (a, token)

    def parse_term() -> tuple[TreeNode, Token]:
        a, token = parse_factor()
        if a is None:
            return

        while 1:
            if token.type == TokenType.ASTERISK:
                b, token = parse_factor()
                if b is None:
                    return
                a = Mult(a, b)

            elif token.type == TokenType.SLASH:
                b, token = parse_factor()
                if b is None:
                    return
                a = Div(a, b)

            else:
                return (a, token)

    def parse_factor() -> tuple[TreeNode, Token]:
        token = lex.next()

        if token.type == TokenType.IDENTIFIER:
            return (Identifier(token.lexeme), lex.next())

        if token.type == TokenType.NUMBER:
            return (Number(token.lexeme), lex.next())

        if token.type == TokenType.LPAREN:
            a, token = parse_expr()
            if a is None:
                return

            if token.type == TokenType.RPAREN:
                return (a, lex.next())
            else:
                return

        if token.type == TokenType.MINUS:
            a, token = parse_factor()
            if a is None:
                return

            return (Negate(a), token)

    tree, token = parse_expr()
    assert token.type == TokenType.END
    return tree


if __name__ == '__main__':
    tree = parse("identifier + 69 * 8")
    assert str(tree) == "(identifier + (69 * 8))"

    tree = parse("(7 + (5 * 2))")
    assert str(tree) == "(7 + (5 * 2))"
    assert tree.eval() == 17

    tree = parse("6 + (-4 + (3*x+7) * y * 9 / (4 + 3))")
    assert str(tree) == "(6 + ((-4) + (((((3 * x) + 7) * y) * 9) / (4 + 3))))"
    assert tree.eval({'x': 7, 'y': 2}) == 74.0

    tree = parse("x + 5 * 2")
    assert str(tree) == "(x + (5 * 2))"
    assert tree.eval({'x': 12}) == 22

    simplified_tree = tree.simplify()
    assert str(simplified_tree) == "(x + 10)"
    assert simplified_tree.eval({'x': 12}) == 22

    tree = parse("x / 7 + 42 * 8 / (8 - 6)")
    assert str(tree) == "((x / 7) + ((42 * 8) / (8 - 6)))"
    assert tree.eval({'x': 28}) == 172

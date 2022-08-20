# adaptation of the pseudocode in this video on recursive descent pasrsing:
# https://www.youtube.com/watch?v=SToUyjAsaFk

from lexer import *
from nodetypes import *


class ParseError(Exception):
    pass


def parse(string_to_parse: str) -> TreeNode:
    lex = Lexer(string_to_parse)

    def parse_expr() -> tuple[TreeNode, Token]:
        a, token = parse_term()

        while 1:
            if token.type == TokenType.PLUS:
                b, token = parse_term()
                a = Add(a, b)

            elif token.type == TokenType.MINUS:
                b, token = parse_term()
                a = Subtract(a, b)

            else:
                return (a, token)

    def parse_term() -> tuple[TreeNode, Token]:
        a, token = parse_factor()

        while 1:
            if token.type == TokenType.ASTERISK:
                b, token = parse_factor()
                a = Mult(a, b)

            elif token.type == TokenType.SLASH:
                b, token = parse_factor()
                a = Div(a, b)

            else:
                return (a, token)

    def parse_factor() -> tuple[TreeNode, Token]:
        token = lex.next()

        if token.type == TokenType.IDENTIFIER:
            return (Identifier(token.lexeme), lex.next())

        if token.type == TokenType.NUMBER:
            lexemes = token.lexeme
            token = lex.next()

            if token.type == TokenType.DOT:
                lexemes += token.lexeme
                token = lex.next()
                if token.type == TokenType.NUMBER:
                    # make sure the next token is not another dot
                    lexemes += token.lexeme
                    token = lex.next()
                    if token.type == TokenType.DOT:
                        raise ParseError
                    else:
                        return (Float(lexemes), token)
            else:
                return (Integer(lexemes), token)

        if token.type == TokenType.LPAREN:
            a, token = parse_expr()

            if token.type == TokenType.RPAREN:
                return (a, lex.next())
            else:
                raise ParseError

        if token.type == TokenType.MINUS:
            a, token = parse_factor()

            return (Negate(a), token)

    tree, token = parse_expr()
    if token.type != TokenType.END:
        raise ParseError
    return tree


if __name__ == '__main__':
    tree = parse("identifier + 69 * 8")
    assert str(tree) == "(identifier + (69 * 8))"

    tree = parse("(7 + (5 * 2))")
    assert str(tree) == "(7 + (5 * 2))"
    assert tree.eval() == 17

    simplified_tree = tree.simplify()
    assert str(simplified_tree) == "17"
    assert simplified_tree.eval() == 17

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

    tree = parse("3.14159")
    assert abs(tree.eval() - 3.14159) < 1e-100

    tree = parse("6/3 + (-4 + (3*123.057922+7) * 879 / (4 + 3))")
    simplified_tree = tree.simplify()
    assert abs(simplified_tree.eval() - 47234.67718771428) < 1e-100

    try:
        tree = parse("3.14159.01928347")
    except ParseError:
        pass
    else:
        assert False, "Expected a ParseError :("

    try:
        tree = parse("897asdfasdf987")
    except ParseError:
        pass
    else:
        assert False, "Expected a ParseError :("

# based on this C++ lexer:
# https://gist.github.com/arrieta/1a309138689e09375b90b3b1aa768e20

from enum import Enum


class TokenType(Enum):
    UNEXPECTED = 0
    END = 1
    IDENTIFIER = 2
    NUMBER = 3
    LPAREN = 4
    RPAREN = 5
    PLUS = 6
    MINUS = 7
    ASTERISK = 8
    SLASH = 9
    DOT = 10


class Token:
    def __init__(self, type: TokenType, lexeme: str):
        self.type = type
        self.lexeme = lexeme


class Lexer:
    def __init__(self, string_to_lex: str):
        self._str = string_to_lex
        self._index = 0

    def peek(self) -> str:
        if self._index >= len(self._str):
            return "\0"
        return self._str[self._index]

    def get(self) -> str:
        self._index += 1
        return self._str[self._index - 1]

    @staticmethod
    def is_space(char: str) -> bool:
        assert len(char) == 1
        return char in " \t\r\n"

    @staticmethod
    def is_digit(char: str) -> bool:
        assert len(char) == 1
        return char >= "0" and char <= "9"

    @staticmethod
    def is_letter(char: str) -> bool:
        assert len(char) == 1
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z")

    def is_identifier_char(self, char: str) -> bool:
        assert len(char) == 1
        return self.is_letter(char) or self.is_digit(char) or char == "_"

    # for single-character tokens
    def atom(self, type: TokenType):
        return Token(type, self.get())

    def next(self) -> Token:
        # skip whitespace
        while self.is_space(self.peek()):
            self.get()

        char = self.peek()

        if self.is_letter(char):
            return self.identifier()
        elif self.is_digit(char):
            return self.number()
        elif char == "(":
            return self.atom(TokenType.LPAREN)
        elif char == ")":
            return self.atom(TokenType.RPAREN)
        elif char == "*":
            return self.atom(TokenType.ASTERISK)
        elif char == "/":
            return self.atom(TokenType.SLASH)
        elif char == "+":
            return self.atom(TokenType.PLUS)
        elif char == "-":
            return self.atom(TokenType.MINUS)
        elif char == ".":
            return self.atom(TokenType.DOT)
        elif char == "\0":
            return Token(TokenType.END, self.peek())
        else:
            return self.atom(TokenType.UNEXPECTED)

    def identifier(self):
        start_index = self._index
        self.get()
        while self.is_identifier_char(self.peek()):
            self.get()
        return Token(TokenType.IDENTIFIER,
                     self._str[start_index:self._index])

    def number(self):
        start_index = self._index
        self.get()
        while self.is_digit(self.peek()):
            self.get()
        return Token(TokenType.NUMBER,
                     self._str[start_index:self._index])

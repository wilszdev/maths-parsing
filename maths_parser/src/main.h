#ifndef _MAIN_H
#define _MAIN_H

enum class TokenType {
	Plus, Minus, Multiply, Divide, Identifier, Integer
};

struct Token {
	TokenType type;
	char* string;
};

#include <string>
#include <sstream>

class ITreeNode {
public:
	virtual std::string print() = 0;
};

class IBinaryOperator : public ITreeNode {
public:
	virtual std::string print() override {
		std::stringstream ss;
		ss << '(' << left->print() << symbol << right->print() << ')';
		return ss.str();
	}
protected:
	char symbol;
	ITreeNode* left;
	ITreeNode* right;
};

class IUnaryOperator : public ITreeNode {
public:
	virtual std::string print() override {
		std::stringstream ss;
		ss << '(' << symbol << arg->print() << ')';
		return ss.str();
	}
protected:
	char symbol;
	ITreeNode* arg;
};

#endif

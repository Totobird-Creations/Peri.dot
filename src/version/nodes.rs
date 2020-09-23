use std::fmt;
use colored::*;

use super::tokens;
use super::lexer;



#[derive(Debug, Clone)]
pub enum Node {
    NullNode,


    IntNode {
        token: tokens::Token,
        value: i32,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    },
    FloatNode {
        token: tokens::Token,
        value: f32,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    },
    StringNode {
        token: tokens::Token,
        value: String,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    },
    VarAccessNode {
        token: tokens::Token,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    },


    VarInitNode {
        varname: tokens::Token,
        node   : Box<Node>,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    },


    BinaryOpNode {
        left   : Box<Node>,
        optoken: tokens::Token,
        right  : Box<Node>,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    },
    UnaryOpNode {
        optoken: tokens::Token,
        node   : Box<Node>,
        start: lexer::LexerPosition, end: lexer::LexerPosition
    }
}
impl fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Node::NullNode                                              => write!(f, "{}", "NULL".red()),

            Node::IntNode       {token: _, value, start: _, end: _}      => write!(f, "i{}", value),
            Node::FloatNode     {token: _, value, start: _, end: _}      => write!(f, "f{}", value),
            Node::StringNode    {token: _, value, start: _, end: _}      => write!(f, "`{}`", value),
            Node::VarAccessNode {token, start: _, end: _}                => write!(f, "{}", token.value),

            Node::VarInitNode   {varname, node, start: _, end: _}     => write!(f, "({} = {})", varname.value, node),

            Node::BinaryOpNode  {left, optoken, right, start: _, end: _} => write!(f, "({} {} {})", left, optoken, right),
            Node::UnaryOpNode   {optoken, node, start: _, end: _}        => write!(f, "({} {})", optoken, node)
        }
    }
}
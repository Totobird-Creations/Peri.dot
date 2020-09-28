use std::fmt;
use colored::*;

use super::tokens;
use super::lexer;



#[derive(Debug, Clone)]
pub struct Node {
    pub nodevalue: NodeValue,
    pub start: lexer::LexerPosition,
    pub end: lexer::LexerPosition
}
#[derive(Debug, Clone)]
pub enum NodeValue {
    NullNode,


    IntNode {
        token: tokens::Token,
        value: String,
    },
    FloatNode {
        token: tokens::Token,
        value: String,
    },
    StringNode {
        token: tokens::Token,
        value: String,
    },
    VarAccessNode {
        token: tokens::Token,
    },


    VarInitNode {
        varname: tokens::Token,
        node   : Box<Node>,
    },


    IfNode {
        cases: Vec<(Node, Vec<Node>)>,
        elsecase: Option<Vec<Node>>,
    },


    BinaryOpNode {
        left   : Box<Node>,
        optoken: tokens::Token,
        right  : Box<Node>,
    },
    UnaryOpNode {
        optoken: tokens::Token,
        node   : Box<Node>,
    }
}
impl fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.nodevalue {
            NodeValue::NullNode                              => write!(f, "{}", "NULL".red()),

            NodeValue::IntNode       {token: _, value}       => write!(f, "i{}", value),
            NodeValue::FloatNode     {token: _, value}       => write!(f, "f{}", value),
            NodeValue::StringNode    {token: _, value}       => write!(f, "`{}`", value),
            NodeValue::VarAccessNode {token}                 => write!(f, "{}", token.value),

            NodeValue::VarInitNode   {varname, node}         => write!(f, "({} = {})", varname.value, node),

            NodeValue::IfNode        {cases, elsecase} => {
                let mut res = "".to_string();

                for i in 0 .. cases.len() {
                    res += if i == 0 {"if"} else {" elif"};
                    res += format!(" {}", cases[i].0).as_str();
                }

                match elsecase {
                    Some(_) => {
                        res += " else";
                    },
                    None       => {}
                }

                write!(f, "({})", res)
            },

            NodeValue::BinaryOpNode  {left, optoken, right}  => write!(f, "({} {} {})", left, optoken, right),
            NodeValue::UnaryOpNode   {optoken, node}         => write!(f, "({} {})", optoken, node)
        }
    }
}
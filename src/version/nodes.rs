use std::collections::HashMap;

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
    ArrayNode {
        exprs: Vec<Node>
    },
    CallNode {
        varname: Box<Node>,
        args   : Vec<Node>
    },


    VarInitNode {
        varname: tokens::Token,
        node   : Box<Node>,
    },
    VarAssignNode {
        varname: tokens::Token,
        node   : Box<Node>,
    },


    IfNode {
        cases: Vec<(Node, Vec<Node>)>,
        elsecase: Option<Vec<Node>>,
    },
    ForNode {
        varoverwrite: bool,
        varname: tokens::Token,
        iterable: Box<Node>,
        body: Vec<Node>
    },
    WhileNode {
        condition: Box<Node>,
        body: Vec<Node>
    },
    FuncNode {
        args: HashMap<i32, (tokens::Token, String)>,
        returntype: Box<Node>,
        body: Vec<Node>
    },


    BinaryOpNode {
        left   : Box<Node>,
        optoken: tokens::Token,
        right  : Box<Node>,
    },
    UnaryOpNode {
        optoken: tokens::Token,
        node   : Box<Node>,
    },


    TypeNode {
        value: String
    }
}
impl fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.nodevalue {
            NodeValue::NullNode                              => write!(f, "{}", "NULL".red()),
            NodeValue::TypeNode      {value: _}              => write!(f, "{}", "TYPE".red()),

            NodeValue::IntNode       {token: _, value}       => write!(f, "i{}", value),
            NodeValue::FloatNode     {token: _, value}       => write!(f, "f{}", value),
            NodeValue::StringNode    {token: _, value}       => write!(f, "`{}`", value),
            NodeValue::VarAccessNode {token}                 => write!(f, "{}", token.value),
            NodeValue::ArrayNode     {exprs}                 => {
                let mut res = "".to_string();

                for i in 0 .. exprs.len() {
                    res += format!("{}", exprs[i]).as_str();
                    if i < exprs.len() - 1 {
                        res += ", ";
                    }
                }

                write!(f, "[{}]", res)
            },

            NodeValue::VarInitNode   {varname, node}         => write!(f, "(var {} = {})", varname.value, node),
            NodeValue::VarAssignNode {varname, node}         => write!(f, "({} = {})", varname.value, node),
            NodeValue::CallNode      {varname, args: _}      => write!(f, "{}()", varname),

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
            NodeValue::ForNode       {varoverwrite, varname, iterable, body: _} => {
                write!(f, "(for {}{} in {})", if *varoverwrite {"var "} else {""}, varname.value, *iterable)
            },
            NodeValue::WhileNode     {condition, body: _} => {
                write!(f, "(while {})", *condition)
            },
            NodeValue::FuncNode      {args, returntype, body: _} => {
                let mut resargs = "".to_string();

                let mut i = 0;
                for arg in args.keys() {
                    resargs += format!("{}: {}", args[arg].0, args[arg].1).as_str();

                    if i < args.len() - 1 {
                        resargs += ", ";
                    }

                    i += 1
                }

                let returntype = match &returntype.nodevalue {
                    NodeValue::TypeNode {value} => value,
                    _ => panic!("Non TypeNode Stored")
                };

                write!(f, "(func({}): {})", resargs, returntype)
            }

            NodeValue::BinaryOpNode  {left, optoken, right}  => write!(f, "({} {} {})", left, optoken, right),
            NodeValue::UnaryOpNode   {optoken, node}         => write!(f, "({} {})", optoken, node)
        }
    }
}
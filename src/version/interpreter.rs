use std::collections::HashMap;

use super::exceptions::InterpreterException;
use super::lexer;
use super::tokens;
use super::nodes::Node;
use super::types::*;
use super::context::*;



#[derive(Clone)]
pub struct RTResult {
    pub exception: InterpreterException,
    pub value: Type
}
impl RTResult {
    fn register(&mut self, res: RTResult) -> Type {
        if res.exception.failed {
            self.exception = res.exception;
        }
        return res.value;
    }

    pub fn success(&mut self, value: Type) -> RTResult {
        self.value = value;
        return self.clone();
    }

    pub fn failure(&mut self, exception: InterpreterException) -> RTResult {
        self.exception = exception;
        return self.clone();
    }
}



struct Interpreter {

}
impl Interpreter {
    fn visit(&mut self, node: Node, context: &mut Context) -> RTResult {
        match node.clone() {
            Node::NullNode                                         => panic!("NullNode Found"),
            Node::IntNode       {token, value, start, end}         => self.visit_intnode(node, context, token, start, end),
            Node::FloatNode     {token, value, start, end}         => self.visit_floatnode(node, context, token, start, end),
            Node::StringNode    {token, value, start, end}         => self.visit_stringnode(node, context, token, start, end),
            Node::VarAccessNode {token, start, end}                => self.visit_varaccessnode(node, context, token, start, end),
        
            Node::VarInitNode   {varname, node: onode, start, end} => self.visit_varinitnode(node, context, varname, *onode, start, end),

            Node::BinaryOpNode  {left, optoken, right, start, end} => self.visit_binaryopnode(node, context, *left, optoken, *right, start, end),
            Node::UnaryOpNode   {optoken, node: onode, start, end} => self.visit_unaryopnode(node, context, optoken, *onode, start, end)
        }
    }



    fn visit_intnode(&mut self, node: Node, context: &Context, token: tokens::Token, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::IntType(token.value.parse::<i32>().unwrap()),
            start, end, context: context.clone()
        });
    }

    fn visit_floatnode(&mut self, node: Node, context: &Context, token: tokens::Token, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::FloatType(token.value.parse::<f32>().unwrap()),
            start, end, context: context.clone()
        });
    }

    fn visit_stringnode(&mut self, node: Node, context: &Context, token: tokens::Token, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::StringType(token.value.parse::<String>().unwrap()),
            start, end, context: context.clone()
        });
    }

    fn visit_varaccessnode(&mut self, node: Node, context: &mut Context, token: tokens::Token, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        let varname = token.value;
        let value = context.symbols.get(varname.clone());

        match value {
            Some(value) => {
                return res.success(value.value);
            }
            None        => {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "IdentifierException".to_string(),
                    msg: format!("Symbol `{}` is not defined", varname),
                    start: start, end: end, context: Some(context.clone())
                });
            }
        }
    }



    fn visit_varinitnode(&mut self, node: Node, context: &mut Context, token: tokens::Token, onode: Node, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        let varname = token.value;
        let value = res.register(self.visit(onode, context));
        if res.exception.failed {
            return res;
        }

        context.symbols.set(varname, value.clone());
        return res.success(value);
    }



    fn visit_binaryopnode(&mut self, node: Node, context: &mut Context, left: Node, optoken: tokens::Token, right: Node, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        let left = res.register(self.visit(left, context));
        if res.exception.failed {
            return res;
        }
        let right = res.register(self.visit(right, context));
        if res.exception.failed {
            return res;
        }
        let mut result: Type;

        if optoken.token == tokens::TT_PLUS {
            result = res.register(left.plus_op(right));
        } else if optoken.token == tokens::TT_MINUS {
            result = res.register(left.minus_op(right));
        } else if optoken.token == tokens::TT_TIMES {
            result = res.register(left.times_op(right));
        } else if optoken.token == tokens::TT_DIVBY {
            result = res.register(left.divby_op(right));
        } else if optoken.token == tokens::TT_POW {
            result = res.register(left.pow_op(right));
        } else {
            panic!("Interpreter | visit_UnaryOpNode | Invalid operator recieved.");
        }

        if res.exception.failed {
            return res;
        }

        return res.success(
            result.setpos(start, end)
        );
    }

    fn visit_unaryopnode(&mut self, node: Node, context: &mut Context, optoken: tokens::Token, onode: Node, start: lexer::LexerPosition, end: lexer::LexerPosition) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: start.clone(), end: end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: start.clone(), end: end.clone(), context: context.clone()}};
        let mut number = res.register(self.visit(onode, context));
        if res.exception.failed {
            return res;
        }

        if optoken.token == tokens::TT_MINUS {
            number = res.register(number.times_op(Type {value: Value::IntType(-1), start: start.clone(), end: end.clone(), context: context.clone()}));
        } else {
            panic!("Interpreter | visit_UnaryOpNode | Invalid operator recieved.");
        }

        if res.exception.failed {
            return res;
        }

        return res.success(
            number.setpos(start, end)
        );
    }
}



pub fn interpret(nodes: Vec<Node>) -> Vec<RTResult> {
    let mut interpreter = Interpreter {};
    let symbols = SymbolTable {symbols: HashMap::new(), parent: Box::new(None)};
    let context = &mut Context {
        display: "<root>".to_string(),
        parent: Box::from(None),
        parententry: None,
        symbols: symbols
    };
    let mut result = vec![];
    for node in nodes {
        result.push(interpreter.visit(node, context));
        //println!("{:#?}", context.symbols)
    }

    return result;
}

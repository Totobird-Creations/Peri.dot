use super::exceptions::InterpreterException;
use super::tokens;
use super::nodes::*;
use super::types::*;
use super::context::*;



#[derive(Clone)]
pub struct RTResult {
    pub exception: InterpreterException,
    pub value: Type
}
impl RTResult {
    pub fn register(&mut self, res: RTResult) -> Type {
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
        match node.nodevalue.clone() {
            NodeValue::NullNode                             => panic!("NullNode Found"),
            NodeValue::IntNode       {token, value}         => self.visit_intnode(node, context, token, value),
            NodeValue::FloatNode     {token, value}         => self.visit_floatnode(node, context, token, value),
            NodeValue::StringNode    {token, value}         => self.visit_stringnode(node, context, token, value),
            NodeValue::VarAccessNode {token}                => self.visit_varaccessnode(node, context, token),

            NodeValue::VarInitNode   {varname, node: onode} => self.visit_varinitnode(node, context, varname, *onode),

            NodeValue::IfNode        {cases, elsecase}      => self.visit_ifnode(node, context, cases, elsecase),

            NodeValue::BinaryOpNode  {left, optoken, right} => self.visit_binaryopnode(node, context, *left, optoken, *right),
            NodeValue::UnaryOpNode   {optoken, node: onode} => self.visit_unaryopnode(node, context, optoken, *onode)
        }
    }



    fn visit_intnode(&mut self, node: Node, context: &Context, token: tokens::Token, value: String) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::IntType(value.parse::<i128>().unwrap()),
            start: node.start, end: node.end, context: context.clone()
        });
    }

    fn visit_floatnode(&mut self, node: Node, context: &Context, token: tokens::Token, value: String) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::FloatType(value.parse::<f64>().unwrap()),
            start: node.start, end: node.end, context: context.clone()
        });
    }

    fn visit_stringnode(&mut self, node: Node, context: &Context, token: tokens::Token, value: String) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::StrType(value),
            start: node.start, end: node.end, context: context.clone()
        });
    }

    fn visit_varaccessnode(&mut self, node: Node, context: &mut Context, token: tokens::Token) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
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
                    ucmsg: "Symbol `{}` is not defined".to_string(),
                    start: node.start, end: node.end, context: Some(context.clone())
                });
            }
        }
    }



    fn visit_varinitnode(&mut self, node: Node, context: &mut Context, token: tokens::Token, onode: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let varname = token.value;
        let value = res.register(self.visit(onode, context));
        if res.exception.failed {
            return res;
        }

        match context.symbols.get(varname.clone()) {
            Some(value) => {
                if value.readonly {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "IdentifierException".to_string(),
                        msg: format!("Symbol `{}` is read-only", varname),
                        ucmsg: "Symbol `{}` is read-only".to_string(),
                        start: node.start, end: node.end, context: Some(context.clone())
                    });
                }
            },
            None => {}
        }
        
        context.symbols.set(varname, value.clone());
        return res.success(value);
    }



    fn visit_ifnode(&mut self, node: Node, context: &mut Context, cases: Vec<(Node, Vec<Node>)>, elsecase: Option<Vec<Node>>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};

        for i in cases {
            let condition = res.register(self.visit(i.0, context));
            if res.exception.failed {
                return res;
            }

            let condvalue: bool;

            match condition.value {
                Value::BoolType(val) => {
                    condvalue = val
                },
                _                      => {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "TypeException".to_string(),
                        msg: format!("{} can not be interpreted as Bool", condition.gettype()),
                        ucmsg: "{} can not be interpreted as Bool".to_string(),
                        start: node.start, end: node.end, context: Some(context.clone())
                    });
                }
            }

            if condvalue {
                let mut value = Type {
                    value: Value::NullType,
                    start: node.start, end: node.end,
                    context: context.clone()
                };
                for j in i.1 {
                    value = res.register(self.visit(j, context));
                    if res.exception.failed {
                        return res;
                    }
                }
                return res.success(value)
            }
        }

        match elsecase {
            Some(nodes) => {
                let mut value = Type {
                    value: Value::NullType,
                    start: node.start, end: node.end,
                    context: context.clone()
                };
                for i in nodes {
                    value = res.register(self.visit(i, context));
                    if res.exception.failed {
                        return res;
                    }
                }
                return res.success(value)
            },
            None => {}
        }

        return res.success(Type {
            value: Value::NullType,
            start: node.start, end: node.end,
            context: context.clone()
        });
    }



    fn visit_binaryopnode(&mut self, node: Node, context: &mut Context, left: Node, optoken: tokens::Token, right: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
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

        } else if optoken.token == tokens::TT_EQUALEQ {
            result = res.register(left.equaleq_comp(right));
        } else if optoken.token == tokens::TT_NOTEQ {
            result = res.register(left.noteq_comp(right));
        } else if optoken.token == tokens::TT_LSSTHN {
            result = res.register(left.lssthn_comp(right));
        } else if optoken.token == tokens::TT_GRTTHN {
            result = res.register(left.grtthn_comp(right));
        } else if optoken.token == tokens::TT_LSSTHNEQ {
            result = res.register(left.lssthneq_comp(right));
        } else if optoken.token == tokens::TT_GRTTHNEQ {
            result = res.register(left.grtthneq_comp(right));
        } else if optoken.token == tokens::TT_AND {
            result = res.register(left.and_comb(right));
        } else if optoken.token == tokens::TT_XOR {
            result = res.register(left.xor_comb(right));
        } else if optoken.token == tokens::TT_OR {
            result = res.register(left.or_comb(right));
        
        } else {
            panic!("Interpreter | visit_UnaryOpNode | Invalid operator recieved.");
        }

        if res.exception.failed {
            return res;
        }

        return res.success(
            result.setpos(node.start, node.end)
        );
    }

    fn visit_unaryopnode(&mut self, node: Node, context: &mut Context, optoken: tokens::Token, onode: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let mut value = res.register(self.visit(onode, context));
        if res.exception.failed {
            return res;
        }

        if optoken.token == tokens::TT_MINUS {
            match value.value {
                Value::FloatType(_) => value = res.register(value.times_op(Type {value: Value::FloatType(-1.0), start: node.start.clone(), end: node.end.clone(), context: context.clone()})),
                _                   => value = res.register(value.times_op(Type {value: Value::IntType(-1), start: node.start.clone(), end: node.end.clone(), context: context.clone()}))
            }

        } else if optoken.token == tokens::TT_NOT {
            value = res.register(value.equaleq_comp(Type {value: Value::BoolType(false), start: node.start.clone(), end: node.end.clone(), context: context.clone()}));
        } else {
            panic!("Interpreter | visit_UnaryOpNode | Invalid operator recieved.");
        }

        if res.exception.failed {
            return res;
        }

        return res.success(
            value.setpos(node.start, node.end)
        );
    }
}



pub fn interpret(nodes: Vec<Node>) -> Vec<RTResult> {
    let mut interpreter = Interpreter {};
    let symbols = defaultsymbols();

    let context = &mut Context {
        display: "<root>".to_string(),
        parent: Box::from(None),
        parententry: None,
        symbols: symbols
    };
    let mut result = vec![];
    for node in nodes {
        result.push(interpreter.visit(node, context));
    }

    return result;
}

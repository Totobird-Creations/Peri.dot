use std::collections::HashMap;

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



pub struct Interpreter {}
impl Interpreter {
    pub fn visit(&mut self, node: Node, context: &mut Context) -> RTResult {
        match node.nodevalue.clone() {
            NodeValue::NullNode                                              => panic!("NullNode Found"),
            NodeValue::TypeNode {value}                                      => panic!("TypeNode Found: {}", value),

            NodeValue::IntNode       {token, value}                          => self.visit_intnode       (node, context, token, value),
            NodeValue::FloatNode     {token, value}                          => self.visit_floatnode     (node, context, token, value),
            NodeValue::StringNode    {token, value}                          => self.visit_stringnode    (node, context, token, value),
            NodeValue::VarAccessNode {token}                                 => self.visit_varaccessnode (node, context, token),
            NodeValue::ArrayNode     {exprs}                                 => self.visit_arraynode     (node, context, exprs),
            NodeValue::CallNode      {varname, args}                         => self.visit_callnode      (node, context, *varname, args),

            NodeValue::VarInitNode   {varname, node: onode}                  => self.visit_varinitnode   (node, context, varname, *onode),
            NodeValue::VarAssignNode {varname, node: onode}                  => self.visit_varassignnode (node, context, varname, *onode),

            NodeValue::IfNode        {cases, elsecase}                       => self.visit_ifnode        (node, context, cases, elsecase),
            NodeValue::ForNode       {varoverwrite, varname, iterable, body} => self.visit_fornode       (node, context, varoverwrite, varname, *iterable, body),
            NodeValue::WhileNode     {condition, body}                       => self.visit_whilenode     (node, context, *condition, body),
            NodeValue::FuncNode      {args, returntype, body}                => self.visit_funcnode      (node, context, args, returntype, body),

            NodeValue::BinaryOpNode  {left, optoken, right}                  => self.visit_binaryopnode  (node, context, *left, optoken, *right),
            NodeValue::CastOpNode    {casttype, node: onode}                 => self.visit_castopnode    (node, context, casttype, *onode),
            NodeValue::UnaryOpNode   {optoken, node: onode}                  => self.visit_unaryopnode   (node, context, optoken, *onode)
        }
    }



    fn visit_intnode(&mut self, node: Node, context: &Context, _token: tokens::Token, value: String) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let value = match value.parse::<i128>() {
            Ok(value) => value,
            Err(_)  => {
                return res.failure(
                    InterpreterException {
                        failed: true,
                        name: "OverflowException".to_string(),
                        msg: format!("Integer overflowed when converting to Peri.dot type"),
                        ucmsg: "Integer overflowed when converting to Peri.dot type".to_string(),
                        start: node.start, end: node.end, context: Some(context.clone())
                    }
                )
            }
        };
        return res.success(Type {
            value: Value::IntType(value),
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end, context: context.clone()
        });
    }

    fn visit_floatnode(&mut self, node: Node, context: &Context, _token: tokens::Token, value: String) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let value = match value.parse::<f64>() {
            Ok(value) => value,
            Err(_)  => {
                return res.failure(
                    InterpreterException {
                        failed: true,
                        name: "OverflowException".to_string(),
                        msg: format!("Float overflowed when converting to Peri.dot type"),
                        ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                        start: node.start, end: node.end, context: Some(context.clone())
                    }
                )
            }
        };
        if ! value.is_finite() {
            return res.failure(
                InterpreterException {
                    failed: true,
                    name: "OverflowException".to_string(),
                    msg: format!("Float overflowed when converting to Peri.dot type"),
                    ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                    start: node.start, end: node.end, context: Some(context.clone())
                }
            )
        }
        return res.success(Type {
            value: Value::FloatType(value),
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end, context: context.clone()
        });
    }

    fn visit_stringnode(&mut self, node: Node, context: &Context, _token: tokens::Token, value: String) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        return res.success(Type {
            value: Value::StrType(value),
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end, context: context.clone()
        });
    }

    fn visit_varaccessnode(&mut self, node: Node, context: &mut Context, token: tokens::Token) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let varname = token.value;
        let value = context.symbols.get(varname.clone());

        match value {
            Some(mut value) => {
                value.value.modorigin();
                value.value.name = varname.clone();
                return res.success(value.value.setpos(node.start, node.end));
            }
            None => {
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

    fn visit_arraynode(&mut self, node: Node, context: &mut Context, exprs: Vec<Node>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let mut values = vec![];

        for i in exprs {
            let expr = res.register(self.visit(i, context));

            if res.exception.failed {
                return res;
            }

            values.push(expr);
        }

        if values.len() > 0 {
            let arraytype = values[0].gettype().to_string();

            for i in values.clone() {
                if i.gettype().to_string() != arraytype {
                    context.origin = i.clone().context.origin;
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "TypeException".to_string(),
                        msg: format!("Array<{}> may not contain {}", arraytype, i.gettype()),
                        ucmsg: "Array<{}> may not contain {}".to_string(),
                        start: i.start, end: i.end, context: Some(context.clone())
                    });
                }
            }

            return res.success(Type {
                value: Value::ArrayType(values.clone(), arraytype),
                name: "<Anonymous>".to_string(),
                start: node.start, end: node.end, context: context.clone()
            });

        } else {
            let arraytype = Type {
                value: Value::NullType,
                name: "<Anonymous>".to_string(),
                start: node.clone().start, end: node.clone().end, context: context.clone()
            };
            return res.success(Type {
                value: Value::ArrayType(values, arraytype.gettype().to_string()),
                name: "<Anonymous>".to_string(),
                start: node.clone().start, end: node.clone().end, context: context.clone()
            });
        }
    }

    fn visit_callnode(&mut self, node: Node, context: &mut Context, varname: Node, args: Vec<Node>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let mut resargs = vec![];

        let mut func = res.register(self.visit(varname, context));

        if res.exception.failed {
            return res;
        }

        func = func.copy().setpos(node.start, node.end);

        for arg in args {
            resargs.push(res.register(self.visit(arg, context)));
            if res.exception.failed {
                return res;
            }
        }

        let value = res.register(func.call(resargs));

        if res.exception.failed {
            return res;
        }

        return res.success(value);
    }



    fn visit_varinitnode(&mut self, node: Node, context: &mut Context, token: tokens::Token, onode: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let varname = token.value;
        let mut value = res.register(self.visit(onode, context));
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

        value.name = varname.clone();
        
        context.symbols.set(varname, value.clone());
        return res.success(value);
    }

    fn visit_varassignnode(&mut self, node: Node, context: &mut Context, token: tokens::Token, onode: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let varname = token.value;
        let mut assigningvalue = res.register(self.visit(onode, context));
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

                if value.value.gettype() != assigningvalue.gettype() {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "TypeException".to_string(),
                        msg: format!("Can not assign {} to symbol of type {}", assigningvalue.gettype(), value.value.gettype()),
                        ucmsg: "Can not assign {} to symbols of type {}".to_string(),
                        start: assigningvalue.start, end: assigningvalue.end, context: Some(context.clone())
                    });
                }
            },
            None => {}
        }

        assigningvalue.name = varname.clone();
        
        context.symbols.set(varname, assigningvalue.clone());
        return res.success(assigningvalue);
    }



    fn visit_ifnode(&mut self, node: Node, context: &mut Context, cases: Vec<(Node, Vec<Node>)>, elsecase: Option<Vec<Node>>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};

        for i in cases {
            let condition = res.register(self.visit(i.0.clone(), context));
            if res.exception.failed {
                return res;
            }

            let condvalue: bool;

            match condition.value {
                Value::BoolType(val) => {
                    condvalue = val
                },
                _ => {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "TypeException".to_string(),
                        msg: format!("{} can not be interpreted as Bool", condition.gettype()),
                        ucmsg: "{} can not be interpreted as Bool".to_string(),
                        start: i.0.clone().start, end: i.0.clone().end, context: Some(condition.context.clone())
                    });
                }
            }

            if condvalue {
                let mut value = Type {
                    value: Value::NullType,
                    name: "<Anonymous>".to_string(),
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
                    name: "<Anonymous>".to_string(),
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
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end,
            context: context.clone()
        });
    }



    fn visit_fornode(&mut self, node: Node, context: &mut Context, varoverwrite: bool, varname: tokens::Token, iterable: Node, body: Vec<Node>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        
        let iterable = res.register(self.visit(iterable, context));

        if res.exception.failed {
            return res;
        }

        let iterable = match iterable.value {
            Value::ArrayType(value, _) => value,
            _ => {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be interpreted as an Iterable", iterable.gettype()),
                    ucmsg: "{} can not be interpreted as {}".to_string(),
                    start: iterable.start, end: iterable.end, context: Some(context.clone())
                });
            }
        };

        let mut value = Type {
            value: Value::NullType,
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end,
            context: context.clone()
        };

        for i in iterable {
            if ! varoverwrite {
                let itype = context.symbols.get(varname.value.clone());
                match itype {
                    Some(value) => {
                        if value.readonly {
                            return res.failure(InterpreterException {
                                failed: true,
                                name: "TypeException".to_string(),
                                msg: format!("Can not assign to read-only symbol"),
                                ucmsg: "Can not assign to read-only symbol".to_string(),
                                start: varname.start, end: varname.end, context: Some(context.clone())
                            });
                        }

                        if value.value.gettype() != i.gettype() {
                            return res.failure(InterpreterException {
                                failed: true,
                                name: "TypeException".to_string(),
                                msg: format!("Can not assign {} to symbol of type {}", i.gettype(), value.value.gettype()),
                                ucmsg: "Can not assign {} to symbol of type {}".to_string(),
                                start: varname.start, end: varname.end, context: Some(context.clone())
                            });
                        }
                    },
                    None => {
                        return res.failure(InterpreterException {
                            failed: true,
                            name: "TypeException".to_string(),
                            msg: format!("Can not assign to non-existant symbol"),
                            ucmsg: "Can not assign to non-existant symbol".to_string(),
                            start: varname.start, end: varname.end, context: Some(context.clone())
                        });
                    }
                }
            }
            context.symbols.set(varname.value.clone(), i);

            for j in body.clone() {
                value = res.register(self.visit(j, context));
                if res.exception.failed {
                    return res;
                }
            }
        }

        return res.success(value);
    }



    fn visit_whilenode(&mut self, node: Node, context: &mut Context, conditionnode: Node, body: Vec<Node>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};

        let mut value = Type {
            value: Value::NullType,
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end,
            context: context.clone()
        };

        loop {
            let condition = res.register(self.visit(conditionnode.clone(), context));
            let condvalue: bool;

            match condition.value {
                Value::BoolType(val) => {
                    condvalue = val;
                },
                _ => {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "TypeException".to_string(),
                        msg: format!("{} can not be interpreted as Bool", condition.gettype()),
                        ucmsg: "{} can not be interpreted as Bool".to_string(),
                        start: condition.clone().start, end: condition.clone().end, context: Some(condition.context.clone())
                    });
                }
            }

            if ! condvalue {
                break;
            }

            for j in body.clone() {
                value = res.register(self.visit(j, context));
                if res.exception.failed {
                    return res;
                }
            }
        }

        return res.success(value);
    }



    fn visit_funcnode(&mut self, node: Node, context: &mut Context, args: HashMap<i32, (tokens::Token, String)>, returntype: Box<Node>, body: Vec<Node>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};

        let mut argnames = vec![];

        for i in args.keys() {
            if argnames.contains(&args[i].0.value) {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "ParameterException".to_string(),
                    msg: format!("Paramter `{}` is used more than once", args[i].0.value),
                    ucmsg: "Parameter {} is used more than once".to_string(),
                    start: args[i].0.start.clone(), end: args[i].0.end.clone(), context: Some(context.clone())
                });
            }
            argnames.push(args[i].0.value.clone());
        }

        let returntype = match returntype.nodevalue {
            NodeValue::TypeNode {value} => {value},
            _ => panic!("Non TypeNode received")
        };

        let func = Type {
            value: Value::FuncType (
                args,
                returntype,
                body
            ),
            name: "<Anonymous>".to_string(),
            start: node.start, end: node.end,
            context: context.clone()
        };

        return res.success(func);
    }



    fn visit_binaryopnode(&mut self, node: Node, context: &mut Context, left: Node, optoken: tokens::Token, right: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
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

    fn visit_castopnode(&mut self, node: Node, context: &mut Context, casttype: String, onode: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};

        let value = res.register(self.visit(onode, context));

        if res.exception.failed {
            return res;
        }

        let mut result = res.register(value.cast_op(casttype));

        if res.exception.failed {
            return res;
        }

        return res.success(
            result.setpos(node.start, node.end)
        );
    }

    fn visit_unaryopnode(&mut self, node: Node, context: &mut Context, optoken: tokens::Token, onode: Node) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: node.start.clone(), end: node.end.clone(), context: Some(context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}};
        let mut value = res.register(self.visit(onode, context));
        if res.exception.failed {
            return res;
        }

        if optoken.token == tokens::TT_MINUS {
            match value.value {
                Value::FloatType(_) => value = res.register(value.times_op(Type {value: Value::FloatType(-1.0), name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()})),
                _                   => value = res.register(value.times_op(Type {value: Value::IntType(-1), name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}))
            }

        } else if optoken.token == tokens::TT_NOT {
            value = res.register(value.equaleq_comp(Type {value: Value::BoolType(false), name: "<Anonymous>".to_string(), start: node.start.clone(), end: node.end.clone(), context: context.clone()}));
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
        symbols: symbols,
        origin: vec![]
    };
    let mut result = vec![];
    for node in nodes {
        result.push(interpreter.visit(node, context));
    }

    return result;
}

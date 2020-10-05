use std::fmt;
use std::collections::HashMap;
use std::sync::Arc;

use super::lexer;
use super::interpreter::{RTResult, Interpreter};
use super::exceptions::InterpreterException;
use super::context;
use super::nodes;
use super::tokens;



#[derive(Clone)]
pub struct Type {
    pub value: Value,
    pub name: String,
    pub start: lexer::LexerPosition, pub end: lexer::LexerPosition,
    pub context: context::Context
}
#[derive(Clone)]
pub enum Value {
    NullType,

    IntType(i128),
    //      |^^^
    //      > Value

    FloatType(f64),
    //        |^^
    //        > Value

    StrType(String),
    //      |^^^^^
    //      > Value

    BoolType(bool),
    //       |^^^
    //       > Value

    ArrayType(Vec<Type>, String),
    //        |^^^^^^^^  |^^^^^
    //        > Values   > Value Type

    //SequenceType(Vec<Type>),

    //UntypedArrayType(Vec<Type>),

    //TableType(HashMap),

    //EnumerationType,

    //ExceptionType,

    //ModuleType,

    //StructureType,

    //ImplementationType,

    FuncType(HashMap<i32, (tokens::Token, String)>, String, Vec<nodes::Node>),
    //       |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  |^^^^^  |^^^^^^^^^^^^^^^
    //       > Arguments                            |       > Body
    //                                              > Return Type

    BuiltInFuncType(String, HashMap<i32, (String, String)>, String, Arc::<dyn Fn(&mut context::Context, lexer::LexerPosition, lexer::LexerPosition) -> RTResult>)
    //              |^^^^^  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  |^^^^^  |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //              > Name  > Arguments                     |       > Callable
    //                                                      > Return Type
}
impl Type {
    pub fn gettype(&self) -> String {
        match &self.value {
            Value::NullType                    => "Null".to_string(),
            Value::IntType(_)                  => "Int".to_string(),
            Value::FloatType(_)                => "Float".to_string(),
            Value::StrType(_)                  => "Str".to_string(),
            Value::BoolType(_)                 => "Bool".to_string(),
            Value::ArrayType(value, arraytype) => format!("Array<{}, {}>", value.len(), arraytype),
            Value::FuncType(args, returntype, _)  => {
                let mut res = "".to_string();

                let mut i = 0;
                for key in args.keys() {
                    res += args[key].1.as_str();

                    if i < args.len() - 1 {
                        res += ", ";
                    }

                    i += 1;
                }

                format!("Func<[{}], {}>", res, returntype)
            },
            Value::BuiltInFuncType(_, args, returntype, _) => {
                let mut res = "".to_string();

                let mut i = 0;
                for key in args.keys() {
                    res += args[key].1.as_str();

                    if i < args.len() - 1 {
                        res += ", ";
                    }

                    i += 1;
                }

                format!("Func<[{}], {}>", res, returntype)
            }
        }
    }



    pub fn setpos(&mut self, start: lexer::LexerPosition, end: lexer::LexerPosition) -> Type {
        self.start = start;
        self.end = end;
        return self.clone();
    }

    pub fn setcontext(&mut self, context: context::Context) -> Type {
        self.context = context;
        return self.clone();
    }

    pub fn modorigin(&mut self) -> Type {
        self.context.origin = vec![context::Origin {
            start: self.start.clone(), end: self.end.clone(),
            context: self.context.clone()
        }];
        return self.clone();
    }



    pub fn plus_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                let value = match selfvalue.checked_add(othervalue) {
                    Some(value) => value,
                    None        => {
                        let mut context = self.context;
                        context.origin.append(&mut other.context.origin.clone());
                        return res.failure(
                            InterpreterException {
                                failed: true,
                                name: "OverflowException".to_string(),
                                msg: format!("Integer overflowed when converting to Peri.dot type"),
                                ucmsg: "Integer overflowed when converting to Peri.dot type".to_string(),
                                start: self.start, end: self.end, context: Some(context)
                            }
                        )
                    }
                };
                return res.success(Type {
                    value: Value::IntType(value),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(mut selfvalue), Value::FloatType(mut othervalue)) => {
                let a = selfvalue.to_string();
                let a = a.split(".").collect::<Vec<&str>>();
                let a = if a.len() == 1 {0} else {a[1].len()};
                let b = othervalue.to_string();
                let b = b.split(".").collect::<Vec<&str>>();
                let b = if b.len() == 1 {0} else {b[1].len()};
                let len = (10.0 as f64).powf(if a > b {a as f64} else {b as f64});
                selfvalue = selfvalue * len;
                othervalue = othervalue * len;
                let selfvalue = (selfvalue + othervalue) / len;
                if ! selfvalue.is_finite() {
                    let mut context = self.context;
                    context.origin.append(&mut other.context.origin.clone());
                    return res.failure(
                        InterpreterException {
                            failed: true,
                            name: "OverflowException".to_string(),
                            msg: format!("Float overflowed when converting to Peri.dot type"),
                            ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                            start: self.start, end: self.end, context: Some(context)
                        }
                    )
                }
                return res.success(Type {
                    value: Value::FloatType(selfvalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::StrType(selfvalue), Value::StrType(othervalue)) => {
                return res.success(Type {
                    value: Value::StrType(selfvalue + othervalue.as_str()),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::ArrayType(selfvalue, selftype), Value::ArrayType(othervalue, othertype)) => {
                if selftype != othertype {
                    let mut context = self.clone().context;
                    context.origin.append(&mut other.context.origin.clone());
                    return res.failure(
                        InterpreterException {
                            failed: true,
                            name: "TypeException".to_string(),
                            msg: format!("{}<{}> can not be added to {}<{}>", other.gettype(), othertype, self.gettype(), selftype),
                            ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                            start: self.start, end: self.end, context: Some(context)
                        }
                    )
                }
                let mut value = selfvalue.clone();
                let mut othervalue = othervalue;
                value.append(&mut othervalue);
                return res.success(Type {
                    value: Value::ArrayType(value, self.gettype().to_string()),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be added to {}", other.gettype(), self.gettype()),
                    ucmsg: "{} can not be added to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn minus_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                let value = match selfvalue.checked_sub(othervalue) {
                    Some(value) => value,
                    None        => {
                        let mut context = self.context;
                        context.origin.append(&mut other.context.origin.clone());
                        return res.failure(
                            InterpreterException {
                                failed: true,
                                name: "OverflowException".to_string(),
                                msg: format!("Integer overflowed when converting to Peri.dot type"),
                                ucmsg: "Integer overflowed when converting to Peri.dot type".to_string(),
                                start: self.start, end: self.end, context: Some(context)
                            }
                        )
                    }
                };
                return res.success(Type {
                    value: Value::IntType(value),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(mut selfvalue), Value::FloatType(mut othervalue)) => {
                let a = selfvalue.to_string();
                let a = a.split(".").collect::<Vec<&str>>();
                let a = if a.len() == 1 {0} else {a[1].len()};
                let b = othervalue.to_string();
                let b = b.split(".").collect::<Vec<&str>>();
                let b = if b.len() == 1 {0} else {b[1].len()};
                let len = (10.0 as f64).powf(if a > b {a as f64} else {b as f64});
                selfvalue = selfvalue * len;
                othervalue = othervalue * len;
                let selfvalue = (selfvalue - othervalue) / len;
                if ! selfvalue.is_finite() {
                    let mut context = self.context;
                    context.origin.append(&mut other.context.origin.clone());
                    return res.failure(
                        InterpreterException {
                            failed: true,
                            name: "OverflowException".to_string(),
                            msg: format!("Float overflowed when converting to Peri.dot type"),
                            ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                            start: self.start, end: self.end, context: Some(context)
                        }
                    )
                }
                return res.success(Type {
                    value: Value::FloatType(selfvalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be subtracted from {}", other.gettype(), self.gettype()),
                    ucmsg: "{} can not be subtracted from {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn times_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                let value = match selfvalue.checked_mul(othervalue) {
                    Some(value) => value,
                    None        => {
                        let mut context = self.context.clone();
                        context.origin.append(&mut other.context.origin.clone());
                        return res.failure(
                            InterpreterException {
                                failed: true,
                                name: "OverflowException".to_string(),
                                msg: format!("Integer overflowed when converting to Peri.dot type"),
                                ucmsg: "Integer overflowed when converting to Peri.dot type".to_string(),
                                start: self.start, end: self.end, context: Some(context)
                            }
                        )
                    }
                };
                return res.success(Type {
                    value: Value::IntType(value),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                let selfvalue = selfvalue * othervalue;
                if ! selfvalue.is_finite() {
                    let mut context = self.context.clone();
                    context.origin.append(&mut other.context.origin.clone());
                    return res.failure(
                        InterpreterException {
                            failed: true,
                            name: "OverflowException".to_string(),
                            msg: format!("Float overflowed when converting to Peri.dot type"),
                            ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                            start: self.start, end: self.end, context: Some(context)
                        }
                    )
                }
                return res.success(Type {
                    value: Value::FloatType(selfvalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be multiplied by {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be multiplied by {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn divby_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                if othervalue == 0 {
                    let mut context = self.context;
                    context.origin = other.context.origin;
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "OperationException".to_string(),
                        msg: format!("{} divided by zero", selfvalue),
                        ucmsg: "{} divided by zero".to_string(),
                        start: other.start, end: other.end, context: Some(context)
                    });
                }
                let value = match selfvalue.checked_div(othervalue) {
                    Some(value) => value,
                    None        => {
                        let mut context = self.context.clone();
                        context.origin.append(&mut other.context.origin.clone());
                        return res.failure(
                            InterpreterException {
                                failed: true,
                                name: "OverflowException".to_string(),
                                msg: format!("Integer overflowed when converting to Peri.dot type"),
                                ucmsg: "Integer overflowed when converting to Peri.dot type".to_string(),
                                start: self.start, end: self.end, context: Some(context)
                            }
                        )
                    }
                };
                return res.success(Type {
                    value: Value::IntType(value),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                if othervalue == 0.0 {
                    let mut context = self.context.clone();
                    context.origin.append(&mut other.context.origin.clone());
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "OperationException".to_string(),
                        msg: format!("{} divided by zero", selfvalue),
                        ucmsg: "{} divided by zero".to_string(),
                        start: self.start, end: other.end, context: Some(context)
                    });
                }
                let selfvalue = selfvalue / othervalue;
                if ! selfvalue.is_finite() {
                    let mut context = self.context.clone();
                    context.origin.append(&mut other.context.origin.clone());
                    return res.failure(
                        InterpreterException {
                            failed: true,
                            name: "OverflowException".to_string(),
                            msg: format!("Float overflowed when converting to Peri.dot type"),
                            ucmsg: "Float overflowed when converting to Peri.dot type".to_string(),
                            start: self.start, end: self.end, context: Some(context)
                        }
                    )
                }
                return res.success(Type {
                    value: Value::FloatType(selfvalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be divided by {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be divided by {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn pow_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                if othervalue < 0 {
                    let mut context = self.context.clone();
                    context.origin = other.context.origin;
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "OperationException".to_string(),
                        msg: format!("{} raised to negative value {}", selfvalue, othervalue * -1),
                        ucmsg: "{} raised to negative value {}".to_string(),
                        start: other.start, end: other.end, context: Some(context)
                    });
                }
                let value = match selfvalue.checked_pow(othervalue as u32) {
                    Some(value) => value,
                    None        => {
                        let mut context = self.context.clone();
                        context.origin.append(&mut other.context.origin.clone());
                        return res.failure(
                            InterpreterException {
                                failed: true,
                                name: "OverflowException".to_string(),
                                msg: format!("Integer overflowed when converting to Peri.dot type"),
                                ucmsg: "Integer overflowed when converting to Peri.dot type".to_string(),
                                start: self.start, end: self.end, context: Some(context)
                            }
                        )
                    }
                };
                return res.success(Type {
                    value: Value::IntType(value),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::FloatType(selfvalue.powf(othervalue)),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be raised to {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be raised to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn equaleq_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::NullType, Value::NullType) => {
                return res.success(Type {
                    value: Value::BoolType(true),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::StrType(selfvalue), Value::StrType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be compared to {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be compared to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn noteq_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        let value = res.register(self.clone().equaleq_comp(other.clone()));

        if res.exception.failed {
            return res;
        }

        match value.value {
            Value::BoolType(value) => {
                return res.success(Type {
                    value: Value::BoolType(! value),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }
            _ => panic!("Equaleq comparison returned non-boolean value")
        }
    }



    pub fn lssthn_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue < othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue < othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be compared to {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be compared to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn grtthn_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue > othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue > othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be compared to {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be compared to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn lssthneq_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue <= othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue <= othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be compared to {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be compared to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn grtthneq_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue >= othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue >= othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be compared to {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be compared to {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn and_comb(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue && othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be combined with {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be combined with {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn xor_comb(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(!(selfvalue && othervalue) && (selfvalue || othervalue)),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be combined with {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be combined with {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn or_comb(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue || othervalue),
                    name: "<Anonymous>".to_string(),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                let mut context = self.context.clone();
                context.origin.append(&mut other.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be combined with {}", self.gettype(), other.gettype()),
                    ucmsg: "{} can not be combined with {}".to_string(),
                    start: self.start, end: other.end, context: Some(context)
                });
            }

        }
    }



    pub fn gencontext(self) -> context::Context {
        let mut symbols = context::defaultsymbols();
        symbols.parent = Box::new(Some(self.context.symbols.clone()));

        return context::Context {
            display: self.name.to_string(),
            parent: Box::from(Some(self.context.clone())),
            parententry: Some(self.start.clone()),
            symbols: symbols,
            origin: vec![]
        };
    }

    pub fn checkpopargs(self, context: &mut context::Context, args: Vec<Type>, funcargs: HashMap<i32, (String, String)>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: self.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: self.end.clone(), context: self.context.clone()}};

        if args.len() != funcargs.len() {
            return res.failure(InterpreterException {
                failed: true,
                name: "ParameterException".to_string(),
                msg: format!("Function takes {} parameters, {} given", funcargs.len(), args.len()),
                ucmsg: "{} takes {} parameters, {} given".to_string(),
                start: self.start, end: self.end, context: Some(self.context.clone())
            });
        }

        for key in funcargs.keys() {
            if funcargs[key].1 != args[*key as usize].gettype() {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "ParameterException".to_string(),
                    msg: format!("Parameter `{}` must be of type {}, {} given", funcargs[key].0, funcargs[key].1, args[*key as usize].gettype()),
                    ucmsg: "Parameter {} must be of type {}, {} given".to_string(),
                    start: args[*key as usize].start.clone(), end: args[*key as usize].end.clone(), context: Some(args[*key as usize].context.clone())
                });
            }

            context.symbols.set(funcargs[key].0.clone(), args[*key as usize].clone().setcontext(context.clone()));
        }

        return res.success(Type {
            value: Value::NullType,
            name: "<Anonymous>".to_string(),
            start: self.start, end: self.end,
            context: self.context
        })
    }



    pub fn call(self, args: Vec<Type>) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: self.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, name: "<Anonymous>".to_string(), start: self.start.clone(), end: self.end.clone(), context: self.context.clone()}};

        match self.value.clone() {

            Value::FuncType(funcargs, returntype, body) => {
                let mut interpreter = Interpreter {};
                let context = &mut self.clone().gencontext();

                let mut funcargsfix = HashMap::new();

                for key in funcargs.keys() {
                    let value = (funcargs[key].0.value.clone(), funcargs[key].1.clone());
                    funcargsfix.insert(*key, value);
                }

                res.register(self.clone().checkpopargs(context, args, funcargsfix));

                if res.exception.failed {
                    return res;
                }

                let mut value = Type {
                    value: Value::NullType,
                    name: "<Anonymous>".to_string(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: context.clone()
                };
                for i in body {
                    value = res.register(interpreter.visit(i, context));
                    if res.exception.failed {
                        return res;
                    }
                }

                if value.gettype() != returntype {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "ReturnException".to_string(),
                        msg: format!("`{}` must return {}, {} returned", self.name, returntype, value.gettype()),
                        ucmsg: "`{}` must return {}, {} returned".to_string(),
                        start: self.start.clone(), end: self.end.clone(), context: Some(self.context.clone())
                    })
                }

                return res.success(value);
            }

            Value::BuiltInFuncType(name, funcargs, returntype, func) => {
                let context = &mut self.clone().gencontext();
    
                res.register(self.clone().checkpopargs(context, args, funcargs));
    
                if res.exception.failed {
                    return res;
                }
    
                let value = res.register(func(&mut context.clone(), self.start.clone(), self.end.clone()));
    
                if res.exception.failed {
                    return res;
                }

                if value.gettype() != returntype {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "ReturnException".to_string(),
                        msg: format!("`{}` must return {}, {} returned", self.name, returntype, value.gettype()),
                        ucmsg: "`{}` must return {}, {} returned".to_string(),
                        start: self.start.clone(), end: self.end.clone(), context: Some(self.context.clone())
                    })
                }
    
                return res.success(value);
            }

            _ => {
                let mut context = self.context.clone();
                context.origin.append(&mut self.context.origin.clone());
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be called", self.gettype()),
                    ucmsg: "{} can not be called".to_string(),
                    start: self.start, end: self.end, context: Some(context)
                });
            }

        }
    }



    pub fn copy(self) -> Type {
        match self.value.clone() {
            Value::NullType => {
                Type {
                    value: Value::NullType,
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::IntType(value) => {
                Type {
                    value: Value::IntType(
                        value.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::FloatType(value) => {
                Type {
                    value: Value::FloatType(
                        value.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::StrType(value) => {
                Type {
                    value: Value::StrType(
                        value.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::BoolType(value) => {
                Type {
                    value: Value::BoolType(
                        value.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::ArrayType(values, valtype) => {
                Type {
                    value: Value::ArrayType(
                        values.clone(),
                        valtype.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::FuncType(funcargs, returntype, body) => {
                Type {
                    value: Value::FuncType(
                        funcargs.clone(),
                        returntype.clone(),
                        body.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            Value::BuiltInFuncType(name, args, returntype, func) => {
                Type {
                    value: Value::BuiltInFuncType(
                        name.clone(),
                        args.clone(),
                        returntype.clone(),
                        func.clone()
                    ),
                    name: self.name.clone(),
                    start: self.start.clone(), end: self.end.clone(),
                    context: self.context.clone()
                }
            },
            _ => panic!("Illegal copy")
        }
    }
}
impl fmt::Display for Type {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.value {
            Value::NullType              => write!(f, "null"),
            Value::IntType(value)        => write!(f, "{}", value),
            Value::FloatType(value) => {
                let mut value = value.to_string();
                if ! value.contains(".") {
                    value += ".0";
                }
                write!(f, "{}", value)
            },
            Value::StrType(value)        => write!(f, "{}", value),
            Value::BoolType(value)       => write!(f, "{}", if *value {"true"} else {"false"}),
            Value::ArrayType(value, _) => {
                let mut res = "".to_string();
                for i in 0..value.len() {
                    res += format!("{}", value[i]).as_str();
                    if i < value.len() - 1 {
                        res += ", ";
                    }
                }
                write!(f, "[{}]", res)
            },
            Value::FuncType(_, _, _)     => write!(f, "<Func {}>", self.name),
            Value::BuiltInFuncType(name, _, _, _)     => write!(f, "<Built-In Func {}>", name)
        }
    }
}

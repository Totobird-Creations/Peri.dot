use std::fmt;

use super::lexer;
use super::interpreter::RTResult;
use super::exceptions::InterpreterException;
use super::context;



#[derive(Clone, Debug)]
pub struct Type {
    pub value: Value,
    pub start: lexer::LexerPosition, pub end: lexer::LexerPosition,
    pub context: context::Context
}
#[derive(Clone, Debug)]
pub enum Value {
    NullType,
    IntType(i128),
    FloatType(f64),
    StrType(String),
    BoolType(bool)
}
impl Type {
    pub fn gettype(&self) -> &str {
        match self.value {
            Value::NullType   =>   "Null",
            Value::IntType(_) =>   "Int",
            Value::FloatType(_) => "Float",
            Value::StrType(_) =>   "String",
            Value::BoolType(_) =>  "Bool"
        }
    }



    pub fn setpos(&mut self, start: lexer::LexerPosition, end: lexer::LexerPosition) -> Type {
        self.start = start;
        self.end = end;
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
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
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::StrType(selfvalue), Value::StrType(othervalue)) => {
                return res.success(Type {
                    value: Value::StrType(selfvalue + othervalue.as_str()),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
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
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::FloatType(selfvalue.powf(othervalue)),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::NullType, Value::NullType) => {
                return res.success(Type {
                    value: Value::BoolType(true),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::StrType(selfvalue), Value::StrType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue == othervalue),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        let value = res.register(self.clone().equaleq_comp(other.clone()));

        if res.exception.failed {
            return res;
        }

        match value.value {
            Value::BoolType(value) => {
                return res.success(Type {
                    value: Value::BoolType(! value),
                    start: self.start, end: other.end, context: self.context
                });
            }
            _ => panic!("Equaleq comparison returned non-boolean value")
        }
    }



    pub fn lssthn_comp(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue < othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue < othervalue),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue > othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue > othervalue),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue <= othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue <= othervalue),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue >= othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue >= othervalue),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue && othervalue),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(!(selfvalue && othervalue) && (selfvalue || othervalue)),
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
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::BoolType(selfvalue), Value::BoolType(othervalue)) => {
                return res.success(Type {
                    value: Value::BoolType(selfvalue || othervalue),
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
}
impl fmt::Display for Type {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.value {
            Value::NullType           => write!(f, "null"),
            Value::IntType(value)     => write!(f, "{}", value),
            Value::FloatType(value)   => {
                let mut value = value.to_string();
                if ! value.contains(".") {
                    value += ".0";
                }
                write!(f, "{}", value)
            },
            Value::StrType(value)  => write!(f, "{}", value),
            Value::BoolType(value) => write!(f, "{}", if *value {"true"} else {"false"})
        }
    }
}

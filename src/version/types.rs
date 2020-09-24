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
    IntType(i32),
    FloatType(f32),
    StringType(String),
    BooleanType(bool)
}
impl Type {
    fn gettype(&self) -> &str {
        match self.value {
            Value::NullType   =>     "Null",
            Value::IntType(_) =>     "Int",
            Value::FloatType(_) =>   "Float",
            Value::StringType(_) =>  "String",
            Value::BooleanType(_) => "String"
        }
    }



    pub fn setpos(&mut self, start: lexer::LexerPosition, end: lexer::LexerPosition) -> Type {
        self.start = start;
        self.end = end;
        return self.clone();
    }

    /*pub fn setcontext(&mut self, context: context::Context) -> Type {
        self.context = context;
        return self.clone();
    }*/



    pub fn plus_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::IntType(selfvalue + othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::FloatType(selfvalue + othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::StringType(selfvalue), Value::StringType(othervalue)) => {
                return res.success(Type {
                    value: Value::StringType(selfvalue + othervalue.as_str()),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be added to {}", other.gettype(), self.gettype()),
                    start: self.start, end: other.end, context: Some(self.context)
                });
            }

        }
    }



    pub fn minus_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::IntType(selfvalue - othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::FloatType(selfvalue - othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be added to {}", other.gettype(), self.gettype()),
                    start: self.start, end: other.end, context: Some(self.context)
                });
            }

        }
    }



    pub fn times_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::IntType(selfvalue * othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                return res.success(Type {
                    value: Value::FloatType(selfvalue * othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be added to {}", other.gettype(), self.gettype()),
                    start: self.start, end: other.end, context: Some(self.context)
                });
            }

        }
    }



    pub fn divby_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                if othervalue == 0 {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "OperationException".to_string(),
                        msg: format!("{} divided by zero", selfvalue),
                        start: self.start, end: other.end, context: Some(self.context)
                    });
                }
                return res.success(Type {
                    value: Value::IntType(selfvalue / othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (Value::FloatType(selfvalue), Value::FloatType(othervalue)) => {
                if othervalue == 0.0 {
                    return res.failure(InterpreterException {
                        failed: true,
                        name: "OperationException".to_string(),
                        msg: format!("{} divided by zero", selfvalue),
                        start: self.start, end: other.end, context: Some(self.context)
                    });
                }
                return res.success(Type {
                    value: Value::FloatType(selfvalue / othervalue),
                    start: self.start, end: other.end, context: self.context
                });
            }

            (_, _) => {
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be added to {}", other.gettype(), self.gettype()),
                    start: self.start, end: other.end, context: Some(self.context)
                });
            }

        }
    }



    pub fn pow_op(self, other: Type) -> RTResult {
        let mut res = RTResult {exception: InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.start.clone(), end: other.end.clone(), context: Some(self.context.clone())}, value: Type {value: Value::NullType, start: self.start.clone(), end: other.end.clone(), context: self.context.clone()}};
        match (self.value.clone(), other.value.clone()) {

            (Value::IntType(selfvalue), Value::IntType(othervalue)) => {
                return res.success(Type {
                    value: Value::IntType(selfvalue.pow(othervalue as u32)),
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
                return res.failure(InterpreterException {
                    failed: true,
                    name: "TypeException".to_string(),
                    msg: format!("{} can not be added to {}", other.gettype(), self.gettype()),
                    start: self.start, end: other.end, context: Some(self.context)
                });
            }

        }
    }
}
impl fmt::Display for Type {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match &self.value {
            Value::NullType           => write!(f, "Null"),
            Value::IntType(value)     => write!(f, "{}", value),
            Value::FloatType(value)   => {
                let mut value = value.to_string();
                if ! value.contains(".") {
                    value += ".0";
                }
                write!(f, "{}", value)
            },
            Value::StringType(value)  => write!(f, "{}", value),
            Value::BooleanType(value) => write!(f, "{}", if *value {"True"} else {"False"})
        }
    }
}
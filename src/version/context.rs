use std::collections::HashMap;
use std::sync::Arc;

use super::lexer;
use super::types;
use super::interpreter;
use super::exceptions;



#[derive(Clone)]
pub struct Origin {
    pub start  : lexer::LexerPosition,
    pub end    : lexer::LexerPosition,
    pub context: Context
}



#[derive(Clone)]
pub struct Context {
    pub display    : String,
    pub parent     : Box<Option<Context>>,
    pub parententry: Option<lexer::LexerPosition>,
    pub symbols    : SymbolTable,
    pub origin     : Vec<Origin>
}



#[derive(Clone)]
pub struct Symbol {
    pub value: types::Type,
    pub readonly: bool
}



pub fn defaultsymbols() -> SymbolTable {
    let mut symbols = SymbolTable {symbols: HashMap::new(), parent: Box::new(None)};

    symbols.biv("null".to_string(), types::Value::NullType);
    symbols.biv("true".to_string(), types::Value::BoolType(true));
    symbols.biv("false".to_string(), types::Value::BoolType(false));

    let mut arguments = HashMap::new();
    arguments.insert(0, ("message".to_string(), "Str".to_string()));
    fn exec_print(context: &mut Context, start: lexer::LexerPosition, end: lexer::LexerPosition) -> interpreter::RTResult {
        let mut res = interpreter::RTResult {exception: exceptions::InterpreterException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: lexer::LexerPosition {index: 0, line: 0, column: 0, file:"Built-In".to_string(), script: "".to_string(), lines: vec!["".to_string()]}, end: lexer::LexerPosition {index: 0, line: 0, column: 0, file:"Built-In".to_string(), script: "".to_string(), lines: vec!["".to_string()]}, context: Some(context.clone())}, value: types::Type {value: types::Value::NullType, name: "<Anonymous>".to_string(), start: lexer::LexerPosition {index: 0, line: 0, column: 0, file:"Built-In".to_string(), script: "".to_string(), lines: vec!["".to_string()]}, end: lexer::LexerPosition {index: 0, line: 0, column: 0, file:"Built-In".to_string(), script: "".to_string(), lines: vec!["".to_string()]}, context: context.clone()}};

        let message = context.symbols.get("message".to_string()).unwrap().value;
        println!("{}", message);

        let mut value = message.clone();
        value.name = "<Anonymous>".to_string();
        value.setpos(start, end);
        value.setcontext(context.clone());

        return res.success(value);
    }
    symbols.biv("print".to_string(), types::Value::BuiltInFuncType(
        "print".to_string(),
        arguments,
        "Str".to_string(),
        Arc::new(exec_print)
    ));

    return symbols;
}



#[derive(Clone)]
pub struct SymbolTable {
    pub symbols: HashMap<String, Symbol>,
    pub parent : Box<Option<SymbolTable>>
}
impl SymbolTable {
    pub fn get(&mut self, name: String) -> Option<Symbol> {
        match self.symbols.get(name.as_str()) {
            Some(value) => return Some(value.clone()),
            None        => return None
        }
    }

    pub fn set(&mut self, name: String, value: types::Type) {
        self.symbols.insert(
            name,
            Symbol {value, readonly: false}
        );
    }

    pub fn biv(&mut self, name: String, value: types::Value) {
        self.symbols.insert(
            name.clone(),
            Symbol {
                value: types::Type {
                    value: value,
                    name: name,
                    start: lexer::LexerPosition {
                        index: 0, line: 0, column: 0,
                        file: "Built-In".to_string(),
                        script: "".to_string(), lines: vec!["".to_string()]
                    },
                    end: lexer::LexerPosition {
                        index: 0, line: 0, column: 0,
                        file: "Built-In".to_string(),
                        script: "".to_string(), lines: vec!["".to_string()]
                    },
                    context: Context {
                        display: "Built-In".to_string(),
                        parent: Box::new(None),
                        parententry: None,
                        symbols: SymbolTable {
                            parent: Box::new(None),
                            symbols: HashMap::new()
                        },
                        origin: vec![]
                    }
                },
                readonly: true
            }
        );
    }

    /*fn remove(&mut self, name: String) {
        self.symbols.remove(&name);
    }*/
}

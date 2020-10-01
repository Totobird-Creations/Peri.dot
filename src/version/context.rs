use std::collections::HashMap;

use super::lexer;
use super::types;



#[derive(Clone, Debug)]
pub struct Origin {
    pub start  : lexer::LexerPosition,
    pub end    : lexer::LexerPosition,
    pub context: Context
}



#[derive(Clone, Debug)]
pub struct Context {
    pub display    : String,
    pub parent     : Box<Option<Context>>,
    pub parententry: Option<lexer::LexerPosition>,
    pub symbols    : SymbolTable,
    pub origin     : Vec<Origin>
}



#[derive(Clone, Debug)]
pub struct Symbol {
    pub value: types::Type,
    pub readonly: bool
}



pub fn defaultsymbols() -> SymbolTable {
    let mut symbols = SymbolTable {symbols: HashMap::new(), parent: Box::new(None)};

    symbols.biv("null".to_string(), types::Value::NullType);
    symbols.biv("true".to_string(), types::Value::BoolType(true));
    symbols.biv("false".to_string(), types::Value::BoolType(false));

    return symbols;
}



#[derive(Clone, Debug)]
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

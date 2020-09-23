use std::collections::HashMap;

use super::lexer;
use super::types;



#[derive(Clone, Debug)]
pub struct Context {
    pub display    : String,
    pub parent     : Box<Option<Context>>,
    pub parententry: Option<lexer::LexerPosition>,
    pub symbols    : SymbolTable
}



#[derive(Clone, Debug)]
pub struct Symbol {
    pub value: types::Type
}



#[derive(Clone, Debug)]
pub struct SymbolTable {
    pub symbols: HashMap<String, Symbol>,
    pub parent : Box<Option<SymbolTable>>
}
impl SymbolTable {
    pub fn get(&mut self, name: String) -> Option<Symbol> {
        println!("{:#?}", self.symbols);
        match self.symbols.get(name.as_str()) {
            Some(value) => return Some(value.clone()),
            None        => return None
        }
    }

    pub fn set(&mut self, name: String, value: types::Type) {
        self.symbols.insert(
            name,
            Symbol {value}
        );
    }

    /*fn remove(&mut self, name: String) {
        self.symbols.remove(&name);
    }*/
}

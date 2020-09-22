use std::fmt;
use colored::*;

use super::lexer;



pub struct CommandLineException {
    pub name     : String,
    pub msg      : String
}
impl fmt::Display for CommandLineException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}: {}", self.name.red().bold(), self.msg.red())
    }
}



pub struct LexerException {
    pub failed   : bool,
    pub name     : String,
    pub msg      : String,
    pub start    : lexer::LexerPosition,
    pub end      : lexer::LexerPosition
}
impl fmt::Display for LexerException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut exc = "".to_string();
        exc += format!("{}\n", "An exception occured while generating tokens:".blue().bold()).as_str();
        exc += format!("  {} `{}`,\n", "File".green(), self.start.file.green().bold()).as_str();
        exc += format!("  {} {}, {} {}\n", "Line".green(), (self.start.line + 1).to_string().green().bold(), "Column".green(), (self.start.column + 1).to_string().green().bold()).as_str();
        exc += format!("    {}\n", self.start.lines[self.start.line].yellow().bold()).as_str();
        exc += format!("    {}{}\n", " ".repeat(self.start.column), "^".repeat(self.end.column - self.start.column).yellow()).as_str();
        exc += format!("{}: {}", self.name.red().bold(), self.msg.red()).as_str();

        write!(f, "{}", exc)
    }
}



#[derive(Clone)]
pub struct ParserException {
    pub failed   : bool,
    pub name     : String,
    pub msg      : String,
    pub start    : lexer::LexerPosition,
    pub end      : lexer::LexerPosition
}
impl fmt::Display for ParserException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut exc = "".to_string();
        exc += format!("{}\n", "An exception occured while parsing tokens:".blue().bold()).as_str();
        exc += format!("  {} `{}`,\n", "File".green(), self.start.file.green().bold()).as_str();
        exc += format!("  {} {}, {} {}\n", "Line".green(), (self.start.line + 1).to_string().green().bold(), "Column".green(), (self.start.column + 1).to_string().green().bold()).as_str();
        exc += format!("    {}\n", self.start.lines[self.start.line].yellow().bold()).as_str();
        exc += format!("    {}{}\n", " ".repeat(self.start.column), "^".repeat(self.end.column - self.start.column).yellow()).as_str();
        exc += format!("{}: {}", self.name.red().bold(), self.msg.red()).as_str();

        write!(f, "{}", exc)
    }
}



#[derive(Clone)]
pub struct InterpreterException {
    pub failed: bool,
    pub name  : String,
    pub msg   : String,
    pub start : lexer::LexerPosition,
    pub end   : lexer::LexerPosition
}

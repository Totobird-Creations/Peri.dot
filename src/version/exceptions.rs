use std::fmt;
use colored::*;
use md5::{Md5, Digest};

use super::lexer;
use super::context;



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
    pub failed: bool,
    pub name  : String,
    pub msg   : String,
    pub ucmsg : String,
    pub start : lexer::LexerPosition,
    pub end   : lexer::LexerPosition
}
impl fmt::Display for LexerException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut exc = "".to_string();
        exc += format!("{}\n", "An exception occured while generating tokens:".blue().bold()).as_str();
        exc += format!("  {} `{}`,\n", "File".green(), self.start.file.green().bold()).as_str();
        exc += format!("  {} {}, {} {}\n", "Line".green(), (self.start.line + 1).to_string().green().bold(), "Column".green(), (self.start.column + 1).to_string().green().bold()).as_str();
        exc += format!("    {}\n", self.start.lines[self.start.line].yellow().bold()).as_str();
        exc += format!("    {}{}\n", " ".repeat(self.start.column), "^".repeat(self.end.index - self.start.index).yellow()).as_str();
        let mut errorcode = Md5::new();
        errorcode.input(format!("{}{}", self.name, self.ucmsg));
        let errorcode = format!("{:?}", errorcode.result()).replace(", ", "").replace("[", "").replace("]", "");
        let errorcode = errorcode.get(0..5).unwrap();

        exc += format!("[{}{}] {}: {}", "e".red(), errorcode.red().bold(), self.name.red().bold(), self.msg.red()).as_str();

        write!(f, "{}", exc)
    }
}



#[derive(Clone)]
pub struct ParserException {
    pub failed: bool,
    pub name  : String,
    pub msg   : String,
    pub ucmsg : String,
    pub start : lexer::LexerPosition,
    pub end   : lexer::LexerPosition
}
impl fmt::Display for ParserException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut exc = "".to_string();
        exc += format!("{}\n", "An exception occured while parsing tokens:".blue().bold()).as_str();
        exc += format!("  {} `{}`,\n", "File".green(), self.start.file.green().bold()).as_str();
        exc += format!("  {} {}, {} {}\n", "Line".green(), (self.start.line + 1).to_string().green().bold(), "Column".green(), (self.start.column + 1).to_string().green().bold()).as_str();
        exc += format!("    {}\n", self.start.lines[self.start.line].yellow().bold()).as_str();
        exc += format!("    {}{}\n", " ".repeat(self.start.column), "^".repeat(self.end.index - self.start.index).yellow()).as_str();
        let mut errorcode = Md5::new();
        errorcode.input(format!("{}{}", self.name, self.ucmsg));
        let errorcode = format!("{:?}", errorcode.result()).replace(", ", "").replace("[", "").replace("]", "");
        let errorcode = errorcode.get(0..5).unwrap();

        exc += format!("[{}{}] {}: {}", "e".red(), errorcode.red().bold(), self.name.red().bold(), self.msg.red()).as_str();

        write!(f, "{}", exc)
    }
}



#[derive(Clone)]
pub struct InterpreterException {
    pub failed : bool,
    pub name   : String,
    pub msg    : String,
    pub ucmsg  : String,
    pub start  : lexer::LexerPosition,
    pub end    : lexer::LexerPosition,
    pub context: Option<context::Context>
}
impl InterpreterException {
    fn generatetraceback(self) -> String {
        let mut result = "".to_string();
        let mut part: String;
        let mut pos = self.start;
        let mut ctx = self.context;
        let mut context: context::Context;

        loop {
            match ctx {
                Some(value) => {context = value}
                None        => break
            }

            part = format!("  {} `{}`, {} `{}`,\n", "File".green(), pos.file.green().bold(), "In".green(), context.display.green().bold());
            part += format!("  {} {}, {} {}\n", "Line".green(), pos.line.to_string().green().bold(), "Column".green(), pos.column.to_string().green().bold()).as_str();
            result = part + result.as_str();

            match context.parententry {
                Some(value) => {pos = value}
                None        => break
            }
            ctx = *context.parent;
        }

        result = format!("{}\n{}", "Traceback (Most recent call last):".blue().bold(), result.as_str());
        return result;
    }
}
impl fmt::Display for InterpreterException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut exc = "".to_string();
        exc += self.clone().generatetraceback().as_str();
        exc += format!("    {}\n", self.start.lines[self.start.line].yellow().bold()).as_str();
        exc += format!("    {}{}\n", " ".repeat(self.start.column), "^".repeat(self.end.index - self.start.index).yellow()).as_str();
        let mut errorcode = Md5::new();
        errorcode.input(format!("{}{}", self.name, self.ucmsg));
        let errorcode = format!("{:?}", errorcode.result()).replace(", ", "").replace("[", "").replace("]", "");
        let errorcode = errorcode.get(0..5).unwrap();

        exc += format!("[{}{}] {}: {}", "e".red(), errorcode.red().bold(), self.name.red().bold(), self.msg.red()).as_str();

        write!(f, "{}", exc)
    }
}

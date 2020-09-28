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
        let mut pos = self.start.clone();
        let mut ctx = self.context.clone();
        let mut context: context::Context;

        loop {
            match ctx {
                Some(value) => {context = value}
                None        => break
            }

            part = "".to_string();

            if context.origin.len() > 0 {
                part = self.clone().generateorigin(context.origin, 0, vec![])[1..].to_string() + "\n";
            }

            part += format!("  {} `{}`, {} `{}`,\n", "File".green(), pos.file.green().bold(), "In".green(), context.display.green().bold()).as_str();
            part += format!("  {} {}, {} {}\n", "Line".green(), (pos.line + 1).to_string().green().bold(), "Column".green(), (pos.column + 1).to_string().green().bold()).as_str();
            part += format!("    {}\n", self.start.lines[self.start.line].yellow().bold()).as_str();
            part += format!("    {}{}\n", " ".repeat(self.start.column), "^".repeat(self.end.index - self.start.index).yellow()).as_str();
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

    fn generateorigin(self, origin: Vec<context::Origin>, iter: u32, ignore: Vec<bool>) -> String {
        let mut result = "".to_string();

        let mut prefix = "".to_string();
        for i in 0..ignore.clone().len() {
            if ignore[i] {
                prefix += "  ";
            } else {
                prefix += "║ ";
            }
        }

        let mut start: lexer::LexerPosition;
        let mut end: lexer::LexerPosition;
        let mut context: context::Context;
        let mut parent: Vec<context::Origin>;

        let mut part: String;

        for i in 0..origin.len() {
            start = origin[i].start.clone();
            end = origin[i].end.clone();
            context = origin[i].context.clone();
            parent = context.origin.clone();

            let cornertype: &str;
            if i >= origin.len() - 1 {
                cornertype = "╔";
            } else {
                cornertype = "╠";
            }

            part = "".to_string();
            part += format!("  {}{} {}, {} {},\n", (prefix.clone() + cornertype + "═").magenta(), "File".green(), start.file.green().bold(), "In".green(), context.display.green().bold()).as_str();
            part += format!("  {} {} {}, {} {}\n", (prefix.clone() + "║").magenta(), "Line".green(), (start.line + 1).to_string().green().bold(), "Column".green(), (start.column + 1).to_string().green().bold()).as_str();
            part += format!("  {}   {}\n", (prefix.clone() + "║").magenta(), start.lines[start.line].yellow().bold()).as_str();
            part += format!("  {}   {}{}", (prefix.clone() + "║").magenta(), " ".repeat(start.column), "^".repeat(end.index - start.index - 1).yellow()).as_str();

            let mut ig = ignore.clone();
            ig.push(i >= origin.len() - 1);
            result = self.clone().generateorigin(parent, iter + 1, ig).as_str().to_string() + "\n" + part.as_str() + result.as_str();
        }

        return result;
    }
}
impl fmt::Display for InterpreterException {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut exc = self.clone().generatetraceback();

        let mut errorcode = Md5::new();
        errorcode.input(format!("{}{}", self.name, self.ucmsg));
        let errorcode = format!("{:?}", errorcode.result()).replace(", ", "").replace("[", "").replace("]", "");
        let errorcode = errorcode.get(0..5).unwrap();

        exc += format!("[{}{}] {}: {}", "e".red(), errorcode.red().bold(), self.name.red().bold(), self.msg.red()).as_str();

        write!(f, "{}", exc)
    }
}


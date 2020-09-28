use std::fmt;
use colored::*;

use super::lexer;



#[derive(Clone, Debug)]
pub struct Token {
    pub token  : String,
    pub value  : String,
    pub start  : lexer::LexerPosition,
    pub end    : lexer::LexerPosition
}
impl Token {
    pub fn matches(self, token: &str, value: &str) -> bool {
        return (token.to_string() == self.token) && (value.to_string() == self.value)
    }
}
impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let tokenname: ColoredString;

        if [TT_EOL, TT_EOF].contains(&self.token.as_str()) {
            tokenname = self.token.truecolor(68, 73, 75);
        } else if [TT_EQUALEQ, TT_NOTEQ, TT_LSSTHN, TT_LSSTHNEQ, TT_GRTTHN, TT_GRTTHNEQ].contains(&self.token.as_str()) {
            tokenname = self.token.truecolor(192, 0, 0);
        } else if [TT_INT, TT_FLOAT, TT_STRING, TT_IDENTIFIER].contains(&self.token.as_str()) {
            tokenname = self.token.truecolor(0, 192, 0);
        } else if [TT_PLUS, TT_MINUS, TT_TIMES, TT_DIVBY, TT_POW, TT_CAST, TT_NOT].contains(&self.token.as_str()) {
            tokenname = self.token.truecolor(157, 128, 0);
        // Blue
        } else if [TT_EQUALS].contains(&self.token.as_str()) {
            tokenname = self.token.truecolor(0, 255, 255);
        // Magenta
        } else {
            tokenname = self.token.normal()
        }

        if self.value.len() >= 1 {
            let tokenvalue: ColoredString;
            if [TT_INT, TT_FLOAT].contains(&self.token.as_str()) {
                tokenvalue = self.value.truecolor(181, 206, 168);
            } else if [TT_STRING].contains(&self.token.as_str()) {
                tokenvalue = format!("`{}`", self.value.truecolor(206, 145, 145)).normal();
            } else {
                tokenvalue = self.value.normal();
            }

            write!(f, "{}", format!("<{}: {}>", tokenname, tokenvalue))
        } else {
            write!(f, "<{}>", tokenname)
        }
    }
}

pub const TT_INT        : &'static str = "INT";        // \d(_?\d)*
pub const TT_FLOAT      : &'static str = "FLOAT";      // \d(_?\d)*\.\d(_?\d)*
pub const TT_STRING     : &'static str = "STRING";     // ("|').*\1

pub const TT_PLUS       : &'static str = "PLUS";       // \+
pub const TT_MINUS      : &'static str = "MINUS";      // -
pub const TT_TIMES      : &'static str = "TIMES";      // \*
pub const TT_DIVBY      : &'static str = "DIVBY";      // \/
pub const TT_POW        : &'static str = "POW";        // \*\*

pub const TT_EQUALS     : &'static str = "EQUALS";     // =

pub const TT_EQUALEQ    : &'static str = "EQUALEQ";    // ==
pub const TT_NOTEQ      : &'static str = "NOTEQ";      // !=
pub const TT_LSSTHN     : &'static str = "LSSTHN";     // <
pub const TT_LSSTHNEQ   : &'static str = "LSSTHNEQ";   // <=
pub const TT_GRTTHN     : &'static str = "GRTTHN";     // >
pub const TT_CAST       : &'static str = "CAST";       // >>
pub const TT_GRTTHNEQ   : &'static str = "GRTTHNEQ";   // >=

pub const TT_LPAREN     : &'static str = "LPAREN";     // \(
pub const TT_RPAREN     : &'static str = "RPAREN";     // \)
pub const TT_LCURLY     : &'static str = "LCURLY";     // \{
pub const TT_RCURLY     : &'static str = "RCURLY";     // \}

pub const TT_AND        : &'static str = "AND";        // &
pub const TT_XOR        : &'static str = "XOR";        // \|
pub const TT_OR         : &'static str = "OR";         // (&\|)|(\|&)
pub const TT_NOT        : &'static str = "NOT";        // !

pub const TT_KEYWORD    : &'static str = "KEYWORD";    // [A-Za-z_][A-Za-z0-9_]*
pub const TT_IDENTIFIER : &'static str = "IDENTIFIER"; // [A-Za-z_][A-Za-z0-9_]*

pub const TT_EOL        : &'static str = "EOL";        // \n
pub const TT_EOF        : &'static str = "EOF";        // $

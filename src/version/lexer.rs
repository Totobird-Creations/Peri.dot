use std::collections::HashMap;
use std::fmt;

use super::tokens::*;
use super::constants::*;
use super::exceptions::*;



#[derive(Clone, Debug)]
pub struct LexerPosition {
    index  : usize,
    pub line   : usize,
    pub column : usize,
    pub file   : String,
    script : String,
    pub lines  : Vec<String>
}
impl LexerPosition {
    fn advance(&mut self, ch: char) {
        self.index  += 1;
        self.column += 1;

        if ch == '\n' {
            self.line  += 1;
            self.column = 0;
        }
    }

    fn retreat(&mut self, ch: char) {
        self.index  -= 1;
        self.column -= 1;

        if ch == '\n' {
            if self.line >= 1 {
                self.line -= 1;
            }
            let split = self.script.lines().collect::<Vec<&str>>();
            self.index = split[self.line].len() - 1;
        }
    }

    pub fn copy(&mut self) -> LexerPosition {
        return LexerPosition {
            index: self.index.clone(),
            line: self.line.clone(), column: self.column.clone(),
            file: self.file.clone(), script: self.script.clone(),
            lines: self.lines.clone()
        }
    }
}



pub struct LexerResult {
    pub result    : Vec<Token>,
    pub exception : LexerException
}
impl fmt::Display for LexerResult {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut result = "".to_string();
        for i in &self.result {
            result += format!(" {}", i).as_str();
        }
        write!(f, "{}", result)
    }
}

pub struct LexerPartResult {
    pub result    : Token,
    pub exception : LexerException
}



struct Lexer {
    _file   : String,
    script : String,
    pos    : LexerPosition,
    ch     : char,
    chars  : Vec<char>,
    end    : bool,
}
impl Lexer {
    fn checkinit(&mut self) {
        if self.script.len() >= 1 {
            self.ch = self.chars[0];
        } else {
            self.ch = ' ';
            self.end = true;
        }
    }

    fn advance(&mut self) {
        self.pos.advance(self.ch);
        if self.pos.index < self.script.len() {
            self.ch = self.chars[self.pos.index];
        } else {
            self.end = true;
        }
    }

    fn retreat(&mut self) {
        self.pos.retreat(self.ch);
        self.ch = self.chars[self.pos.index]
    }


    fn maketokens<'a>(&mut self) -> LexerResult {
        let mut tokens = vec![];

        while self.end != true {

            if [' ', '\t'].contains(&self.ch) {
                self.advance();


            } else if self.ch == '\n' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                tokens.push(Token{token: TT_EOL.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if DIGITS.contains(self.ch) {
                tokens.push(self.makenumber());


            } else if ['"', '\''].contains(&self.ch) {
                let result = self.makestring(self.ch);

                if result.exception.failed {
                    return LexerResult {result: vec![], exception: result.exception};
                }

                tokens.push(result.result);


            } else if self.ch == '+' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_PLUSEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    tokens.push(Token{token: TT_PLUS.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '-' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_MINUSEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    tokens.push(Token{token: TT_MINUS.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '*' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_TIMESEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else if self.ch == '*' && ! self.end {
                    self.advance();

                    if self.ch == '=' && ! self.end {
                        let mut end = self.pos.copy();
                        end.advance(self.ch);
                        tokens.push(Token{token: TT_POWEQ.to_string(), value: "".to_string(), start: start, end: end});

                        self.advance()

                    } else {
                        tokens.push(Token{token: TT_POW.to_string(), value: "".to_string(), start: start, end: self.pos.copy()});
                    }

                } else {
                    tokens.push(Token{token: TT_TIMES.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '/' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_DIVBYEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    tokens.push(Token{token: TT_DIVBY.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '=' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_EQUALEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    tokens.push(Token{token: TT_EQUALS.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '!' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_NOTEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    let msg = format!("Expected character `=` not found");
                    return LexerResult {result: tokens, exception: LexerException {failed: true, name: "ExpectedCharException".to_string(), msg: msg, start: start, end: self.pos.copy()}};
                }


            } else if self.ch == '<' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_LSSTHNEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()
                } else {
                    tokens.push(Token{token: TT_LSSTHN.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '>' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_GRTTHNEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else if self.ch == '>' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    tokens.push(Token{token: TT_CAST.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    tokens.push(Token{token: TT_GRTTHN.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '(' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                tokens.push(Token{token: TT_LPAREN.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == ')' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                tokens.push(Token{token: TT_RPAREN.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else {
                let start = self.pos.copy();
                let ch    = self.ch;
                self.advance();

                let msg = format!("Illegal character `{}` found", ch);
                return LexerResult {result: vec![], exception: LexerException {failed: true, name: "UnexpectedCharException".to_string(), msg: msg, start: start, end: self.pos.copy()}};
            }
        }

        let mut end = self.pos.copy();
        end.advance(self.ch);
    
        tokens.push(Token{token: TT_EOL.to_string(), value: "".to_string(), start: self.pos.copy(), end: end.copy()});
        tokens.push(Token{token: TT_EOF.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

        return LexerResult {result: tokens, exception: LexerException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}};
    }


    fn makenumber(&mut self) -> Token {
        let mut num: String = "".to_string();
        let mut dots = 0;
        let start = self.pos.copy();

        while (! self.end) && (DIGITS.to_string() + ".").contains(self.ch) {
            if self.ch == '.' {
                if dots >= 1 {break}
                dots += 1;
                num += ".";
            } else {
                num += self.ch.to_string().as_str();
            }

            self.advance();
        }

        self.retreat();
        if self.ch != '.' {
            self.advance()
        }

        if dots == 0 {
            return Token {token: TT_INT.to_string(), value: num, start: start, end: self.pos.copy()}
        } else {
            return Token {token: TT_FLOAT.to_string(), value: num, start: start, end: self.pos.copy()}
        }
    }

    fn makestring(&mut self, quotetype: char) -> LexerPartResult {
        let mut string = String::from("");
        let mut start = self.pos.copy();

        let mut escchars = HashMap::new();
        escchars.insert('\\', "\\");
        escchars.insert('n' , "\n");
        escchars.insert('\n', "\n");
        escchars.insert('t' , "\t");
        escchars.insert('\'', "\'");
        escchars.insert('\"', "\"");

        let mut escaped = false;

        self.advance();

        while (! self.end) && (self.ch != quotetype || escaped) {
            if escaped {
                if ! escchars.contains_key(&self.ch) {
                    let msg = format!("`{}` can not be escaped", self.ch);
                    let token = Token{token: TT_STRING.to_string(), value: string, start: start.copy(), end: self.pos.copy()};
                    return LexerPartResult {result: token, exception: LexerException {failed: true, name: "EscapeException".to_string(), msg: msg, start: start, end: self.pos.copy()}};
                }

                string += match escchars.get(&self.ch) {
                    Some(converted) => converted,
                    None            => " "
                };

                escaped = false;

            } else {
                if self.ch == '\\' {
                    escaped = true;

                } else if self.ch == '\n' {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);

                    let msg = format!("Invalid EOL, expected `{}`", quotetype);
                    let token = Token{token: TT_STRING.to_string(), value: string, start: start.copy(), end: self.pos.copy()};
                    return LexerPartResult {result: token, exception: LexerException {failed: true, name: "SyntaxException".to_string(), msg: msg, start: start, end: self.pos.copy()}};

                } else {
                    string += self.ch.to_string().as_str();

                }
            }
            self.advance();
        }

        if self.end {
            let mut end = self.pos.copy();
            end.advance(self.ch);

            let msg = format!("Invalid EOF, expected `{}`", quotetype);
            let token = Token{token: TT_STRING.to_string(), value: string, start: start.copy(), end: self.pos.copy()};
            return LexerPartResult {result: token, exception: LexerException {failed: true, name: "SyntaxException".to_string(), msg: msg, start: start, end: self.pos.copy()}};
        }

        self.advance();

        let token = Token{token: TT_STRING.to_string(), value: string, start: start, end: self.pos.copy()};
        return LexerPartResult {result: token, exception: LexerException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}};
    }
}



pub fn lex<'a>(file: &str, script: &str) -> LexerResult {
    let file   = file  .to_string();
    let script = script.to_string();
    let lines  = script.split("\n").collect::<Vec<&str>>();
    let lines  = lines.iter().map(|s| s.to_string()).collect();
    let pos    = LexerPosition { index: 0, line: 0, column: 0, file: file.clone(), script: script.clone(), lines: lines };
    let ch     = match script.chars().next() {
        Some(current) => current,
        None          => ' '
    };

    let mut lexer = Lexer {
        _file: file, script: script.clone(),
        pos: pos, ch: ch,
        chars: script.chars().collect(),
        end: false
    };
    lexer.checkinit();
    let result = lexer.maketokens();

    return result;
}

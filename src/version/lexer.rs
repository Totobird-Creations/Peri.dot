use std::collections::HashMap;
use std::fmt;

use super::logger::logger;
use super::tokens::*;
use super::constants::*;
use super::exceptions::*;



#[derive(Clone, Debug, std::hash::Hash, std::cmp::Eq, std::cmp::PartialEq)]
pub struct LexerPosition {
    pub index  : usize,
    pub line   : usize,
    pub column : usize,
    pub file   : String,
    pub script : String,
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

        if ch == '\n' {
            if self.line > 0 {
                self.line -= 1;
            }
            self.column = self.lines[self.line].len();
        } else {
            self.column -= 1;
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
            result += format!("{} ", i).as_str();
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
        self.pos.retreat(self.chars[self.pos.index - 1]);
        self.ch = self.chars[self.pos.index];
        self.end = false;
    }


    fn maketokens<'a>(&mut self) -> LexerResult {
        let mut tokens = vec![];

        while self.end != true {

            if [' ', '\t'].contains(&self.ch) {
                self.advance();


            } else if self.ch == '\n' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: EOL");
                tokens.push(Token{token: TT_EOL.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if DIGITS.contains(self.ch) {
                tokens.push(self.makenumber());


            } else if ['"', '\''].contains(&self.ch) {
                let result = self.makestring(self.ch);

                if result.exception.failed {
                    return LexerResult {result: vec![], exception: result.exception};
                }

                logger.trace("Found token: STRING");
                tokens.push(result.result);


            } else if self.ch == '+' {
                let mut end = self.pos.copy();
                end.advance(self.ch);

                logger.trace("Found token: PLUS");
                tokens.push(Token{token: TT_PLUS.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == '-' {
                let mut end = self.pos.copy();
                end.advance(self.ch);

                logger.trace("Found token: MINUS");
                tokens.push(Token{token: TT_MINUS.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == '*' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '*' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: POW");
                    tokens.push(Token{token: TT_POW.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    logger.trace("Found token: TIMES");
                    tokens.push(Token{token: TT_TIMES.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '/' {
                let mut end = self.pos.copy();
                end.advance(self.ch);

                logger.trace("Found token: DIVBY");
                tokens.push(Token{token: TT_DIVBY.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == '=' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: EQUALEQ");
                    tokens.push(Token {token: TT_EQUALEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    logger.trace("Found token: EQUALS");
                    tokens.push(Token {token: TT_EQUALS.to_string(), value: "".to_string(), start: start, end: self.pos.copy()});
                }


            } else if self.ch == '&' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '|' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: OR");
                    tokens.push(Token {token: TT_OR.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    logger.trace("Found token: AND");
                    tokens.push(Token {token: TT_AND.to_string(), value: "".to_string(), start: start, end: self.pos.copy()});
                }


            } else if self.ch == '|' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '&' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: OR");
                    tokens.push(Token {token: TT_OR.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    logger.trace("Found token: XOR");
                    tokens.push(Token {token: TT_XOR.to_string(), value: "".to_string(), start: start, end: self.pos.copy()});
                }


            } else if self.ch == '!' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: NOTEQ");
                    tokens.push(Token {token: TT_NOTEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                } else {
                    logger.trace("Found token: NOT");
                    tokens.push(Token {token: TT_NOT.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '<' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: LSSTHNEQ");
                    tokens.push(Token{token: TT_LSSTHNEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()
                } else {
                    logger.trace("Found token: LSSTHN");
                    tokens.push(Token{token: TT_LSSTHN.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '>' {
                let start = self.pos.copy();
                self.advance();

                if self.ch == '=' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: GRTTHNEQ");
                    tokens.push(Token{token: TT_GRTTHNEQ.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()

                /*} else if self.ch == '>' && ! self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    logger.trace("Found token: CAST");
                    tokens.push(Token{token: TT_CAST.to_string(), value: "".to_string(), start: start, end: end});

                    self.advance()*/

                } else {
                    logger.trace("Found token: GRTTHN");
                    tokens.push(Token{token: TT_GRTTHN.to_string(), value: "".to_string(), start: start, end: self.pos.copy()})
                }


            } else if self.ch == '(' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: LPAREN");
                tokens.push(Token{token: TT_LPAREN.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == ')' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: RPAREN");
                tokens.push(Token{token: TT_RPAREN.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == '[' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: LSQUARE");
                tokens.push(Token{token: TT_LSQUARE.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == ']' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: RSQUARE");
                tokens.push(Token{token: TT_RSQUARE.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == '{' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: LCURLY");
                tokens.push(Token{token: TT_LCURLY.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == '}' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: RCURLY");
                tokens.push(Token{token: TT_RCURLY.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == ',' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: COMMA");
                tokens.push(Token{token: TT_COMMA.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if self.ch == ':' {
                let mut end = self.pos.copy();
                end.advance(self.ch);
                logger.trace("Found token: COLON");
                tokens.push(Token{token: TT_COLON.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

                self.advance();


            } else if (ALPHABET.to_string() + "_").contains(self.ch) {
                tokens.push(self.makeidentifier());


            } else if self.ch == '#' {
                let res = self.makecomment();

                if res.exception.failed {
                    return LexerResult {
                        result: vec![],
                        exception: res.exception
                    }
                }
                


            } else {
                let start = self.pos.copy();
                let ch    = self.ch;
                self.advance();

                return LexerResult {
                    result: vec![],
                    exception: LexerException {
                        failed: true,
                        name: "UnexpectedCharException".to_string(),
                        msg: format!("Illegal character `{}` found", ch),
                        ucmsg: "Illegal character `{}` found".to_string(),
                        start: start, end: self.pos.copy()
                    }
                };
            }
        }

        let mut end = self.pos.copy();
        end.advance(self.ch);
    
        logger.trace("Found token: EOL");
        tokens.push(Token{token: TT_EOL.to_string(), value: "".to_string(), start: self.pos.copy(), end: end.copy()});
        logger.trace("Found token: EOF");
        tokens.push(Token{token: TT_EOF.to_string(), value: "".to_string(), start: self.pos.copy(), end: end});

        return LexerResult {
            result: tokens,
            exception: LexerException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}
        };
    }


    fn makenumber(&mut self) -> Token {
        let mut num: String = "".to_string();
        let mut dots = 0;
        let start = self.pos.copy();

        while (! self.end) && (DIGITS.to_string() + "._").contains(self.ch) {
            if self.ch == '.' {
                if dots >= 1 {break;}
                dots += 1;
                num += ".";
            } else if self.ch == '_' {
            } else {
                num += self.ch.to_string().as_str();
            }

            self.advance();
        }

        self.retreat();
        if ! ['.', '_'].contains(&self.ch) {
            self.advance();
        }

        if dots == 0 {
            logger.trace("Found token: INT");
            return Token {token: TT_INT.to_string(), value: num, start: start, end: self.pos.copy()};
        } else {
            logger.trace("Found token: FLOAT");
            return Token {token: TT_FLOAT.to_string(), value: num, start: start, end: self.pos.copy()};
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
                    let token = Token{token: TT_STRING.to_string(), value: string, start: start.copy(), end: self.pos.copy()};
                    return LexerPartResult {
                        result: token,
                        exception: LexerException {
                            failed: true,
                            name: "EscapeException".to_string(),
                            msg: format!("`{}` can not be escaped", self.ch),
                            ucmsg: "`{}` can not be escaped".to_string(),
                            start: start,
                            end: self.pos.copy()
                        }
                    };
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

                    let token = Token{token: TT_STRING.to_string(), value: string, start: start.copy(), end: self.pos.copy()};
                    return LexerPartResult {
                        result: token,
                        exception: LexerException {
                            failed: true,
                            name: "SyntaxException".to_string(),
                            msg: format!("Invalid EOL, expected `{}`", quotetype),
                            ucmsg: "Invalid EOL, expected `{}`".to_string(),
                            start: start,
                            end: self.pos.copy()
                        }
                    };

                } else {
                    string += self.ch.to_string().as_str();

                }
            }
            self.advance();
        }

        if self.end {
            let mut end = self.pos.copy();
            end.advance(self.ch);

            let token = Token{token: TT_STRING.to_string(), value: string, start: start.copy(), end: self.pos.copy()};
            return LexerPartResult {
                result: token,
                exception: LexerException {
                    failed: true,
                    name: "SyntaxException".to_string(),
                    msg: format!("Invalid EOF, expected `{}`", quotetype),
                    ucmsg: "Invalid EOF, expected `{}`".to_string(),
                    start: start,
                    end: self.pos.copy()
                }
            };
        }

        self.advance();

        let token = Token{token: TT_STRING.to_string(), value: string, start: start, end: self.pos.copy()};
        return LexerPartResult {result: token, exception: LexerException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}};
    }



    fn makeidentifier(&mut self) -> Token {
        let mut identifier = String::from("");
        let start = self.pos.copy();

        while (! self.end) && ((ALPHABET.to_string() + DIGITS + "_").contains(self.ch)) {
            identifier += self.ch.to_string().as_str();
            self.advance();
        }

        let tokentype: &str;
        if KEYWORDS.contains(&identifier.as_str()) {
            logger.trace("Found token: KEYWORD");
            tokentype = TT_KEYWORD;
        } else if TYPES.contains(&identifier.as_str()) {
            logger.trace("Found token: TYPE");
            tokentype = TT_TYPE;
        } else {
            logger.trace("Found token: IDENTIFIER");
            tokentype = TT_IDENTIFIER;
        }

        return Token {token: tokentype.to_string(), value: identifier, start: start, end: self.pos.copy()};
    }



    fn makecomment(&mut self) -> LexerPartResult {
        self.advance();

        if self.ch == '=' {
            self.advance();

            loop {
                if self.end {
                    let mut end = self.pos.copy();
                    end.advance(self.ch);
                    end.advance(self.ch);
                    return LexerPartResult {result: Token {token: TT_EOL.to_string(), value: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}, exception: LexerException {failed: true, name: "SyntaxException".to_string(), msg: "Unclosed multiline comment".to_string(), ucmsg: "Unclosed multiline comment".to_string(), start: self.pos.copy(), end: end}};
                }

                if self.ch == '#' {
                    let res = self.makecomment();

                    if res.exception.failed {
                        return res
                    }
                }

                if self.ch == '=' {
                    self.advance();
                    
                    if self.ch == '#' {
                        self.advance();

                        break;
                    }
                }

                self.advance()
            }

        } else {
            while (! self.end) && (self.ch != '\n') {
                if self.ch == '#' {
                    let res = self.makecomment();

                    if res.exception.failed {
                        return res
                    }
                }

                self.advance();
            }
        }

        return LexerPartResult {result: Token {token: TT_EOL.to_string(), value: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}, exception: LexerException {failed: false, name: "".to_string(), msg: "".to_string(), ucmsg: "".to_string(), start: self.pos.copy(), end: self.pos.copy()}};
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

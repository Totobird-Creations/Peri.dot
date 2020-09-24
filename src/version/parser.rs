use super::exceptions::ParserException;

use super::tokens::*;
use super::nodes::*;



#[derive(Clone)]
pub struct ParseResult {
    pub exception: ParserException,
    pub node: Node,
    pub advancecount: usize
}
impl ParseResult {
    fn registeradvancement(&mut self) {
        self.advancecount += 1;
    }

    fn register(&mut self, res: ParseResult) -> Node {
        self.advancecount += res.advancecount;
        if res.exception.failed {
            self.exception = res.exception;
        }
        return res.node.clone();
    }

    fn success(&mut self, node: Node) -> ParseResult {
        self.node = node;
        return self.clone();
    }

    fn failure(&mut self, exception: ParserException) -> ParseResult {
        if ! self.exception.failed || self.advancecount == 0 {
            self.exception = exception;
        }
        return self.clone();
    }
}



pub enum ParseResponse {
    Success(Vec<Node>),
    Failed(ParserException)
}



#[derive(Clone)]
struct Parser {
    tokens: Vec<Token>,
    index: usize,
    curtoken: Token
}
impl Parser {
    fn advance(&mut self) -> Token {
        self.index += 1;
        if self.index < self.tokens.len() {
            self.curtoken = self.tokens[self.index].clone();
        }

        return self.curtoken.clone();
    }



    fn parse(&mut self) -> ParseResponse {
        /*let mut res = self.expr();
        let tok = self.tokens[self.index + 1].clone();
        if ! res.exception.failed && tok.token != TT_EOF {
            return res.failure(ParserException {
                failed: true,
                name: "SyntaxException".to_string(),
                msg: "Expected Literal, EOF not found".to_string(),
                start: self.curtoken.start.clone(), end: self.curtoken.end.clone()
            });
        }

        return res;*/

        let mut res = ParseResult {exception: ParserException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.curtoken.start.clone(), end: self.curtoken.end.clone()}, node: Node::NullNode, advancecount: 0};
        let mut nodes = vec![];

        while self.curtoken.token != TT_EOF {
            while self.curtoken.token == TT_EOL {
                res.registeradvancement();
                self.advance();
            }

            if self.curtoken.token == TT_EOF {break}

            nodes.push(res.register(self.expr()));

            if res.exception.failed {
                return ParseResponse::Failed(res.exception);
            }
        }

        return ParseResponse::Success(nodes);
    }



    fn expr(&mut self) -> ParseResult {
        let mut res = ParseResult {exception: ParserException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.curtoken.start.clone(), end: self.curtoken.end.clone()}, node: Node::NullNode, advancecount: 0};
        let start = self.curtoken.start.clone();

        if self.curtoken.clone().matches(TT_KEYWORD, "var") {
            res.registeradvancement();
            self.advance();

            if self.curtoken.token != TT_IDENTIFIER {
                return res.failure(ParserException {
                    failed: true,
                    name: "SyntaxException".to_string(),
                    msg: "Expected IDENTIFIER not found".to_string(),
                    start: self.curtoken.start.clone(), end: self.curtoken.end.clone()
                });
            }
            let varname = self.curtoken.clone();

            res.registeradvancement();
            self.advance();

            if self.curtoken.token != TT_EQUALS {
                return res.failure(ParserException {
                    failed: true,
                    name: "SyntaxException".to_string(),
                    msg: "Expected `=` not found".to_string(),
                    start: self.curtoken.start.clone(), end: self.curtoken.end.clone()
                });
            }

            res.registeradvancement();
            self.advance();

            let expr = res.register(self.expr());
            if res.exception.failed {
                return res;
            }

            return res.success(Node::VarInitNode {
                varname: varname.clone(), node: Box::new(expr),
                start: varname.start.clone(), end: self.curtoken.start.clone()
            });
        }

        return self.arithexpr();
    }



    fn arithexpr(&mut self) -> ParseResult {
        let mut res = ParseResult {exception: ParserException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.curtoken.start.clone(), end: self.curtoken.end.clone()}, node: Node::NullNode, advancecount: 0};
        let start = self.curtoken.start.clone();
        let mut left = res.register(self.factor());
        if res.exception.failed {
            return res;
        }
        let mut optoken: Token;
        let mut right: Node;

        while [
            TT_MINUS, TT_LPAREN, // factor
            TT_INT, TT_FLOAT, TT_STRING   // atom
        ].contains(&self.curtoken.token.as_str())  {
            right = res.register(self.factor());
            if res.exception.failed {
                return res;
            }

            if ! [TT_PLUS, TT_MINUS, TT_TIMES, TT_DIVBY, TT_POW].contains(&self.curtoken.token.as_str()) {
                return res.failure(ParserException {
                    failed: true,
                    name: "SyntaxException".to_string(),
                    msg: "Expected Operation not found".to_string(),
                    start: self.curtoken.start.clone(), end: self.curtoken.end.clone()
                });
            }

            optoken = self.curtoken.clone();
            res.registeradvancement();
            self.advance();

            left = res.success(Node::BinaryOpNode {left: Box::new(left), optoken: optoken, right: Box::new(right), start: start.clone(), end: self.curtoken.end.clone()}).node
        }

        return res.success(left);
    }



    fn factor(&mut self) -> ParseResult {
        //return self.binaryop(self.factor, vec![TT_TIMES, TT_DIVBY], &self.factor);
        let mut res = ParseResult {exception: ParserException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.curtoken.start.clone(), end: self.curtoken.end.clone()}, node: Node::NullNode, advancecount: 0};
        let token = self.curtoken.clone();
        let end = token.end.clone();
        if token.token == TT_LPAREN {
            res.registeradvancement();
            self.advance();

            let expr = res.register(self.expr());
            if res.exception.failed {
                return res;
            }

            if self.curtoken.token != TT_RPAREN {
                return res.failure(ParserException {
                    failed: true,
                    name: "SyntaxException".to_string(),
                    msg: "Expected `)` not found".to_string(),
                    start: self.curtoken.start.clone(), end: self.curtoken.end.clone()
                });
            }

            res.registeradvancement();
            self.advance();

            return res.success(expr);



        } else if [TT_MINUS].contains(&token.token.as_str()) {
            let start = self.curtoken.start.clone();
            res.registeradvancement();
            self.advance();

            let factor = res.register(self.factor());
            if res.exception.failed {
                return res;
            }

            return res.success(Node::UnaryOpNode {optoken: token, node: Box::new(factor), start: start, end: end});


        } else {
            return self.atom();
        }
    }



    fn atom(&mut self) -> ParseResult {
        let mut res = ParseResult {exception: ParserException {failed: false, name: "".to_string(), msg: "".to_string(), start: self.curtoken.start.clone(), end: self.curtoken.end.clone()}, node: Node::NullNode, advancecount: 0};
        let token = self.curtoken.clone();
        let value = token.value.clone();
        let start = token.start.clone();
        let end = token.end.clone();

        if token.token == TT_INT {
            res.registeradvancement();
            self.advance();
            return res.success(Node::IntNode {token: token, value: value.parse::<i32>().unwrap(), start: start, end: end});

        } else if token.token == TT_FLOAT {
            res.registeradvancement();
            self.advance();
            return res.success(Node::FloatNode {token: token, value: value.parse::<f32>().unwrap(), start: start, end: end});

        } else if token.token == TT_STRING {
            res.registeradvancement();
            self.advance();
            return res.success(Node::StringNode {token: token, value: value, start: start, end: end});

        } else if token.token == TT_IDENTIFIER {
            res.registeradvancement();
            self.advance();
            return res.success(Node::VarAccessNode {token: token, start: start, end: end});

        } else {
            return res.failure(ParserException {
                failed: true,
                name: "SyntaxException".to_string(),
                msg: "Expected Literal not found.".to_string(),
                start: self.curtoken.start.clone(), end: self.curtoken.end.clone()
            });
        }
    }
}



pub fn parse(tokens: Vec<Token>) -> ParseResponse {
    let curtoken = tokens[0].clone();
    let mut parser = Parser {
        tokens: tokens,
        index: 0,
        curtoken: curtoken
    };

    let result = parser.parse();
    return result;
}

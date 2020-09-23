use std::process::exit;
use std::fs;

use super::exceptions;
use super::lexer;
use super::parser;
use super::nodes;
use super::interpreter;

pub fn run(file: &str) {
    let script = read(file);

    let result = lexer::lex(file, script.as_str());

    if result.exception.failed {
        println!("{}", result.exception);
        exit(1);
    }

    println!("LEXER RESULT => {}", result);

    let result = parser::parse(result.result);
    let nodesres: Vec<nodes::Node>;

    match result {
        parser::ParseResponse::Success(nodes) => {
            nodesres = nodes.clone();
            for node in nodes {
                println!("PARSER RESULT => {}", node);
            }
        },
        parser::ParseResponse::Failed(error) => {
            println!("{}", error);
            exit(1);
        }
    }

    let results = interpreter::interpret(nodesres);

    for result in results {
        if result.exception.failed {
            println!("{}", result.exception);
            exit(1);
        }

        println!("INTERPRETER RESULT => {}", result.value);
    }
}

fn read(filename: &str) -> String {
    let contents = match fs::read_to_string(filename) {
        Ok(contents) => contents,
        Err(_e)      => {
            let exc = exceptions::CommandLineException {name: "CommandLineException".to_string(), msg: format!("File `{}` was not found", filename)};
            println!("{}", exc);
            exit(1);
        }
    };

    return contents;
}

use std::process::exit;
use std::fs;

use super::exceptions;
use super::lexer;
use super::parser;
use super::interpreter;

pub fn run(file: &str) {
    let script = read(file);

    let result = lexer::lex(file, script.as_str());

    if result.exception.failed {
        println!("{}", result.exception);
        exit(1);
    }

    //println!("{}", result);

    let result = parser::parse(result.result);

    if result.exception.failed {
        println!("{}", result.exception);
        exit(1);
    }

    println!("{}", result.node);

    let result = interpreter::interpret(result.node);

    if result.exception.failed {
        println!("{}", result.exception.name);
        exit(1);
    }

    println!("{}", result.value)
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

use std::process::exit;
use std;
use colored::*;
use md5::{Md5, Digest};

mod version;

fn main() {
    const VERSION: &str = "1.0.0";

    let args: Vec<_> = std::env::args().collect();

    let argslen = args.len();
    if argslen == 1 {
        let filename = "<repl>";
        version::run::run(filename);
        exit(0);

    } else if argslen == 2 {
        if ["-v", "--version"].contains(&args[1].as_str()) {
            logo(VERSION);
            exit(0);

        } else if ["-h", "--help"].contains(&args[1].as_str()) {
            help();
            exit(0);

        } else if args[1].starts_with("-") {
            argumenterror("InvalidArgumentException", &args[1], &args, 1);
            exit(1);

        } else {
            version::run::run(args[1].as_str());
            exit(0);
        }
    } else {
        let mut debug = false;

        let mut found = false;
        let mut i = 0;
        let mut cmd = args.clone();
        for arg in &args[1..] {
            cmd.remove(0);
            i += 1;
            if ! arg.starts_with("-") {
                found = true;
                break
            } else if ["-d", "--debug"].contains(&arg.as_str()) && debug == false {
                debug = true;
            } else {
                argumenterror("InvalidArgumentException", &arg, &args, i);
                exit(1);
            }
        }

        if ! found {
            argumenterror("MissingArgumentException", "Filename", &args, i + 1);
            exit(1);
        }

        println!("FILE={} ARGS={} DEBUG={}", cmd[0], cmd.join(","), debug);
    }
}


fn logo(version: &str) {
    let logo = format!("
 ╔═════════════════════════════════════════════════════════════╗
 ║     _____----_____                                          ║
 ║    / \\ PERI.DOT / \\   Peri.dot - {: <27}║
 ║  _/  /\\ __     /\\  \\_  © 2020 Totobird Creations            ║
 ║ /___/  \\__\\-,  \\ \\___\\                                      ║
 ║ \\‾‾‾\\ \\  '-\\‾‾\\  /‾‾‾/                                      ║
 ║  ‾\\  \\/     ‾‾ \\/  /‾  https://toto-bird.github.io/Peri.dot ║
 ║    \\ / LANGUAGE \\ /                                         ║
 ║     ‾‾‾‾‾----‾‾‾‾‾                                          ║
 ╚═════════════════════════════════════════════════════════════╝
", version);
    let logo = logo.green().bold();

    println!("{}", logo);
}


fn help() {
    let usagelabel    = "Usage".yellow();
    let usage         = "peridot [OPTIONS] ([FILE] [ARGS]*)".yellow().bold();

    let optionslabel  = "Options".blue();

    let helpoption    = format!(
        "{}, {} - {}",
        "-h".green().bold(),
        "--help   ".green().bold(),
        "Display this help message.".green()
    );
    let versionoption    = format!(
        "{}, {} - {}",
        "-v".green().bold(),
        "--version".green().bold(),
        "Display logo and version.".green()
    );
    let debugoption    = format!(
        "{}, {} - {}",
        "-d".green().bold(),
        "--debug  ".green().bold(),
        "Display debug while compiling".green()
    );

    let help         = format!("
{}: {}

{}:
  {}
  {}
  {}
", usagelabel, usage, optionslabel, helpoption, versionoption, debugoption);

    println!("{}", help);
}


fn argumenterror(title: &str, msg: &str, args: &Vec<String>, argnum: i32) {
    let mut argpointer: String = "".to_string();
    let mut pointerfound = false;
    let mut i = -1;
    for arg in args {
        i += 1;
        if i == argnum {
            argpointer += "^".repeat(arg.len()).as_str();
            pointerfound = true;
            break
        }
        argpointer += (" ".repeat(arg.len()) + " ").as_str();
    }

    if ! pointerfound {
        argpointer += "^";
    }

    let homedir = match std::env::current_dir() {
        Ok(path) => format!("{}", path.display()),
        Err(_e)  => format!("{}", "INVALID")
    };

    let mut errorcode = Md5::new();
    errorcode.input(format!("{}{}", title, msg));
    let errorcode = format!("{:?}", errorcode.result()).replace(", ", "").replace("[", "").replace("]", "");
    let errorcode = errorcode.get(0..5).unwrap();

    let error = format!("
{}
  {}, {}:
    {}
      {}
      {}
[{}{}] {}: {}
",
    "Peri.dot encountered an error while reading arguments:".blue().bold(),
    format!("File {}", "<Command Line>".bold()).green(),
    format!("In {}", format!("{}", homedir).bold()).green(),
    format!("Argument {}", format!("{}", argnum + 1).bold()).green(),
    args.join(" ").yellow().bold(),
    argpointer.yellow(),
    "e".red(), errorcode.red().bold(), title.red().bold(), msg.red()
    );
    println!("{}", error)
}

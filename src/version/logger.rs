use colored::*;

pub struct Logger {
    level: u8
}
impl Logger {
    pub fn trace(self, msg: &str) {
        if self.level <= 0 {
            println!("[{}]: {}", "TRACE".bold(), msg)
        }
    }
}

pub const logger: Logger = Logger {
    level: 1
};

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

#[allow(non_upper_case_globals)]
pub const logger: Logger = Logger {
    level: 1
};

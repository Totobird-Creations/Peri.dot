# Peri.dot ([1.1.0](https://github.com/toto-bird/Peri.dot/releases/tag/1.1.0))

![Peri.dot Logo](https://raw.githubusercontent.com/toto-bird/Peri.dot/master/logo.png)

Peri.dot is a strongly typed interpreted language, with type inference, implemented in Python. The file extension is ".peri"


## Setup

This project uses [poetry](https://python-poetry.org/) for dependency management.


```bash
pip install peridot
```

## Usage 

```bash
peridot file.peri
```

## Documentation

[Peri.dot Language Docs](https://toto-bird.github.io/Peri.dot-lang/)

## Running Unit Tests

Unit tests expect pytest.  (`pip install pytest`)
From the top level directory  `pytest`

## Current Features

* Basic REPL
* Types:
    * Null/None: `Null`
    * Numbers: `Int`, `Float`
    * Strings: `Str`
    * Arrays: `Array`
    * Tuples: `Tuple`
    * Dictionaries: `Dict`
    * Booleans: `Bool`
    * Functions: `Function`
    * Built-in functions: `Built-In Function`
    * Exceptions: `Exception`
    * Ids: `Id`
    * Namespaces: `Namespace`
* Types must be explicitely cast:
    * `1 + 1` -> `2`
    * `1 + 1.0` -> `OperationError('Float can not be added to Int')`
* Including other files: `var operations = include('./operations.peri')`
* Variables:
    * Creation/Initialization: `var x = 2`
    * Assignment: `x = 5`
    * Accessing: `x`
* Arithmetic:
    * Addition: `1 + 2`
    * Subtraction: `5 - 1`
    * Multiplication: `10 * 2`
    * Division: `25 / 5`
    * Exponents: `2 ^ 3`
* Global comparisons:
    * Equals: `==`
    * Not Equals: `!=`
* Numeric comparisons:
    * Greater than: `>`
    * Less than: `<`
    * Greater than or equal to: `>=`
    * Less than or equal to `<=`
* Boolean operations: `and`, `or` and `not`
* Functions:
    * Creation: `var add = func(a, b) {a + b}`
    * Calling: `add(2, 6)`
* Built-In Functions:
    * Printing to console: `print('Hello World!')`
    * Testing: `assert(x == 10, 'x is not 10')`
* Exception handler: `var x = handler {10 / 0}`
* Assert / in-peri.dot testing: `assert(x == 9, 'x is not equal to 9')`
* Flow control:
    * If statements: `if (x == 1) {var y = 3} elif (x == 2) {var y = 2} else {var y = 1}`
    * Switch statements: `switch (var x in a) {case (x == 10) {print('10')} else {print('Hmm...')}}`
    * For loops: `for (var i in [True, True, False]) {print(i)}`
    * While loops: `while (x < 100) {x = x + 1}`

## Coming Soon

* Improved repl
* Classes for general use: `var Test = class() {a = 'hello'}`

## Possible Features

* Formatted strings `'Hello World{suffix}'`
* More operations:
    * Add and assign `+=`
    * Subtract and assign `-=`
    etc.

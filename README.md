# Peri.dot ([2.0 Pre 00](https://github.com/toto-bird/Peri.dot/releases/tag/2.0.0-pre-00))

![Peri.dot Logo](https://raw.githubusercontent.com/toto-bird/Peri.dot/master/logo.png)

---

### Pre-Release Notes
- RPN-ish Arithmetic Added
```peridot
# Peri.Py
(1 + 2) * 3 # ((1 + 2) * 3)
1 + 2 * 3   # (1 + (2 * 3))

# Rusty Peri.dot
1 2+ 3*     # ((1 + 2) * 3)
1 (2 3*)+   # (1 + (2 * 3))
```
- Variables Added
  - Initialization
  - Access
```peridot
# Rusty Peri.dot

var x = 10 10+
x # 20
```
- Error codes
```
# Console

# Before
OperationException: 10 raised to negative value 1

# Now
[e24261] OperationException: 10 raised to negative value 1
```
- Origin Added
```
# Console

# Average Error Messages:

  File `test.peri`, In `<root>`,
  Line 15, Column 1
    my_function()
    ^^^^^^^^^^^^^
  File `test.peri`, In `my_function`,
  Line 11, Column 1
    d h+
    ^^^^
[e22410] TypeException: String can not be added to Int


# Peri.dot Error Messages:

  ╔═File test.peri, In <root>,
  ║ Line 10, Column 1
  ║   var my_function = func() -> Str {
  ║                     ^^^^^^^^^^^^^
  File `test.peri`, In `<root>`,
  Line 15, Column 1
    my_function()
    ^^^^^^^^^^^^^
    ╔═File test.peri, In <root>,
    ║ Line 4, Column 9
    ║   var b = "Hello"
    ║           ^^^^^^^
  ╔═File test.peri, In <root>,
  ║ Line 3, Column 9
  ║   var d = c
  ║           ^
  ║ ╔═File test.peri, In <root>,
  ║ ║ Line 1, Column 9
  ║ ║   var a = 10
  ║ ║           ^^
  ╠═File test.peri, In <root>,
  ║ Line 2, Column 9
  ║   var b = a
  ║           ^
  File `test.peri`, In `my_function`,
  Line 11, Column 1
    b d+
    ^^^^
[e22410] TypeException: String can not be added to Int
```

---

[Homepage](https://toto-bird.github.io/Peri.dot-lang/)<br />
```diff
- WARNING: Documentation and Playground are currently outdated (1.1.1)
```
[Documentation](https://toto-bird.github.io/Peri.dot-lang/docs)<br />
[Playground](https://toto-bird.github.io/Peri.dot-lang/playground)<br />
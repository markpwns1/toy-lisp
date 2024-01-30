# Toy Lisp
Just something I made for fun one morning, not a serious thing. A regular old dynamically typed, functional Lisp.

## Features
- Basic error reporting
- Basic standard library
- Minor syntactic sugar
- A REPL

## Example
```cl
> (def fib $ fn [n] $ if (n < 2) n ((fib (n - 1)) + (fib (n - 2))))
> (fib 8)
21.0
```

## Quirks
1. Supports infix functions by automatically calling the 2nd argument as a function if the 1st argument is not a function. For example, `(+ 1 2)` is equivalent to `(1 + 2)` because the language calls `+` when it notices that `1` is not a function.
2. Supports Haskell's pipe operator `$`. For example, `(f (g (h x) y))` is equivalent to `$ f $ g (h x) y`

## Usage
`python main.py` to run the REPL.

## Standard Library
The following are intrinsic functions
- `a - b` - Subtracts `b` from `a`
- `a + b` - Adds `a` and `b`
- `a * b` - Multiplies `a` and `b`
- `a / b` - Divides `a` by `b`
- `a == b` - Returns true if `a` and `b` are equal 
- `a < b` - Returns true if `a` is less than `b`
- `params => body` - Given an array `params` of parameter names and an expression `body`, creates a function. For example: `([a b] => (a + b))`
- `x : xs` - Prepends the `x` to the array `xs`. For example: `(1 : [2 3 4])`
- `if cond true-branch false-branch` - A lazy function that returns `true-branch` if `cond` is true, but returns `false-branch` otherwise. Ex: `(if true (1 + 2) (3 + 4))`
- `def var-name value` - Effectful function that declares a global variable literally named `var-name` and assigns the value `value`
- `head xs` - Returns the first element of `xs`
- `tail xs` - Returns all but the first element of `xs`
- `let-in var-name value body` - Binds `value` to `var-name` within the expression `body`
- `true` - Not a function. Simply equal to true.
- `false` - Not a function. Simply equal to false.

The following is the standard library, written using the intrinsic functions
- `a or b` - Return true if one or more of `a` or `b` are true.
- `a and b` - Returns true if all of `a` and `b` are true.
- `not a` - Returns true if `a` is false.
- `a != b` - Returns false if `a == b` is true.
- `a >= b` - Returns true if `a < b` is false.
- `a > b` - Returns true if `a` is greater than `b`.
- `a <= b` - Returns true if `a` is less than or equal to `b`.
- `a not b` - Returns `~(a | b)`, in logical terms.
- `a nand b` - Returns `~(a & b)`, in logical terms.
- `a xor b` - Returns true if exactly one of `a` or `b` is true.
- `a ^ b` - Returns `a` raised to the power of `b`.
- `fn params body` - An alias for `=>`.
- `null xs` - Returns true if the array `xs` is empty.
- `len xs` - Returns the length of the array `xs`.
- `xs ++ ys` - Concatenates arrays `xs` and `ys`.
- `xs # i` - Returns the element of `xs` at index `i`.

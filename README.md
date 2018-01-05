# ArbitraryPrecision
Python Arbitrary Precision Math Library

## Introduction
`ArbitraryPrecision` is a self-contained "Arbitrary Precision" floating-point arithmetic library for Python. It's in fact a very, very trivial and naive way of implementing arbitrary precision arithmetic: by simply making use of Python's infinite-precision `int` type to store all precision digits, and using scientific notation to denote the numbers.

## Features
* Using Python's infinite precision Integer type to store all digits.
* Using Magic Methods to support `+`, `-`, `*`, `/` operators to arbitrary precision, and integer powers (`**`).
* Transparent conversion to `ArbitraryPrecision` from Python's `float` type.

## Basic Usage
Transparent conversion of regular floats
```python
from ArbitraryPrecision.Core import ArbitraryPrecision
x = ArbitraryPrecision(139.3821)
print(x ** 35)
# 1.11492363879286133208693075295889416674613615046993827630843576437183137124104462687831999531345667699234228240533632570508765725983649638142308781442482015290504141697009801671793404928856585282930568903790334821701e75
print(x ** 35 / 2)
# 5.5746181939643066604346537647944708337306807523496913815421788218591568562052231343915999765672833849617114120266816285254382862991824819071154390721241007645252070848504900835896702464428292641465284451895167410850e74
```

If you type a more-than-float-precision literal number into Python it won't be converted correctly, of course. You have to use scientific notation to tap directly into the internal `ArbitraryPrecision` representation:
```python
pi = ArbitraryPrecision(Base = 31415926535897932384626433833, Exponent = 0, InternalAware = True)
```

Essentially it's scientific notation - the decimal point is after the first digit, then the exponent is specified in the constructor. Note that this argument `Base` is not very well named - I am aware.

## Beware!
I am not a good Python programmer, and this library is a kludge for homework problems. But it does its job well where it's implemented.

You are of course welcome to make contributions!

## History
This library, `ArbitraryPrecision` was written on a beautiful weekend afternoon when I should've been outside enjoying the sun, but instead had to deal with the complexities of Computational Physics homework, which required the high-precision computation of 288-degree polynomials (namely, the Hermite Polynomials)

After the homework has been completed I decided to release this bit of code to Open Source to whoever finds a good use for it.

Happy Coding!
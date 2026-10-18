"""Basic arithmetic parser for a mobile calculator frontend.

Scope:
- addition, subtraction, multiplication, division
- parentheses
- unary minus / plus
- exact results when possible (e.g. 1/3 instead of 0.333...)
- simple UI-friendly normalization of common calculator symbols

This module is intentionally small and safe. It does not use eval().
It is designed to be the first layer before a SymPy-backed calculator app.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from sympy import Rational, SympifyError, factor, simplify
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    rationalize,
    standard_transformations,
)


# Allow common calculator glyphs and normalize them to SymPy-friendly input.
_REPLACEMENTS = {
    "×": "*",
    "·": "*",
    "÷": "/",
    "−": "-",
    "–": "-",
    "—": "-",
    "^": "**",
}


_ALLOWED_CHARS = re.compile(r"^[0-9\s\+\-\*\/\(\)\.,^×·÷−–—]+$")


@dataclass(frozen=True)
class ParseResult:
    raw: str
    normalized: str
    value: Expr
    exact_text: str
    decimal_text: str


_TRANSFORMATIONS = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
    rationalize,
)


def normalize_expression(expr: str) -> str:
    """Convert calculator-style input into a SymPy-friendly expression."""
    if expr is None:
        raise ValueError("Expression cannot be None")

    text = expr.strip()
    if not text:
        raise ValueError("Expression cannot be empty")

    for old, new in _REPLACEMENTS.items():
        text = text.replace(old, new)

    # Remove spaces to simplify validation and parsing.
    text = re.sub(r"\s+", "", text)
    return text


def validate_basic_expression(expr: str) -> None:
    """Reject unsupported characters early.

    This is intentionally strict: only arithmetic is allowed.
    """
    if not _ALLOWED_CHARS.fullmatch(expr):
        raise ValueError(
            "Unsupported characters detected. Allowed: digits, spaces, + - * / ( ) . , ^ and × ÷ · − – —"
        )


def parse_basic_expression(expr: str) -> Expr:
    """Parse basic arithmetic into a SymPy expression.

    Examples:
        1+2*3
        (1+2)/3
        0.5+0.25 -> 3/4
        2(3+4) -> 14
        5÷2 -> 5/2
    """
    normalized = normalize_expression(expr)
    validate_basic_expression(normalized)

    try:
        parsed = parse_expr(
            normalized,
            transformations=_TRANSFORMATIONS,
            evaluate=True,
        )
    except (SyntaxError, SympifyError, TypeError, ValueError) as exc:
        raise ValueError(f"Could not parse expression: {expr!r}") from exc

    return simplify(parsed)


def format_exact(value: Expr) -> str:
    """Return a compact exact string.

    SymPy already prints exact rationals and radicals nicely.
    """
    return str(value)


def format_decimal(value: Expr, digits: int = 12) -> str:
    """Return a decimal approximation for display."""
    if digits < 1:
        raise ValueError("digits must be >= 1")
    return str(value.evalf(digits))


def calculate(expr: str, digits: Optional[int] = None) -> ParseResult:
    """Parse and evaluate one arithmetic expression.

    If digits is provided, decimal_text is computed with that precision.
    """
    normalized = normalize_expression(expr)
    value = parse_basic_expression(expr)
    exact_text = format_exact(value)
    decimal_text = format_decimal(value, digits or 12)
    return ParseResult(
        raw=expr,
        normalized=normalized,
        value=value,
        exact_text=exact_text,
        decimal_text=decimal_text,
    )


if __name__ == "__main__":
    examples = [
        "1+2*3",
        "(1+2)/3",
        "0.5+0.25",
        "2(3+4)",
        "5÷2",
        "-3+4*2",
        "(2+3)^2",
    ]

    for item in examples:
        result = calculate(item)
        print(f"{item} -> exact: {result.exact_text} | decimal: {result.decimal_text}")

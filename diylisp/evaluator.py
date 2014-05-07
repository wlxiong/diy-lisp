# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    print ast
    try:
        if is_atom(ast):
            return ast
        op = ast[0]
        if op == "quote":
            return ast[1]
        elif op == "atom":
            return is_atom(evaluate(ast[1], env))
        elif op == "eq":
            arg1, arg2 = evaluate(ast[1], env), evaluate(ast[2], env)
            if not is_atom(arg1) or not is_atom(arg2) or arg1 != arg2:
                return False
            return True
        elif op == "+":
            return evaluate(ast[1], env) + evaluate(ast[2], env)
        elif op == "-":
            return evaluate(ast[1], env) - evaluate(ast[2], env)
        elif op == "*":
            return evaluate(ast[1], env) * evaluate(ast[2], env)
        elif op == "/":
            return evaluate(ast[1], env) / evaluate(ast[2], env)
        elif op == "mod":
            return evaluate(ast[1], env) % evaluate(ast[2], env)
        elif op == ">":
            return evaluate(ast[1], env) > evaluate(ast[2], env)
        elif op == "if":
            if evaluate(ast[1], env) == True:
                return evaluate(ast[2], env)
            return evaluate(ast[3], env)
        else:
            raise LispError("Unknow operator '%s'" % op)
    except Exception as e:
        raise LispError("%s" % e)

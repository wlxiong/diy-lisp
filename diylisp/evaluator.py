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

def apply(closure, arguments, env):
    evaluated_args = [evaluate(arg, env) for arg in arguments]
    if len(closure.params) != len(evaluated_args):
        raise LispError("wrong number of arguments, expected %d got %d" % \
                        (len(closure.params), len(evaluated_args)))
    extended_env = closure.env.extend(zip(closure.params, evaluated_args))
    return evaluate(closure.body, extended_env)

def list_manip(ast, env):
    """All the list manipulation can be implemented using lambda function.
    """
    op = ast[0]
    if op == 'cons':
        try:
            head, tail = ast[1:]
        except ValueError:
            raise LispError("cons needs exactly two arguments")
        return [evaluate(head, env)] + evaluate(tail, env)
    elif op == 'head':
        if len(ast[1:]) > 1:
            raise LispError("head needs exactly one argument")
        return evaluate(ast[1], env)[0]
    elif op == 'tail':
        if len(ast[1:]) > 1:
            raise LispError("tail needs exactly one argument")
        return evaluate(ast[1], env)[1:]
    elif op == 'empty':
        if len(ast[1:]) > 1:
            raise LispError("empty needs exactly one argument")
        return len(evaluate(ast[1], env)) == 0

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    try:
        if is_symbol(ast):
            return env.lookup(ast)
        if is_integer(ast) or is_boolean(ast):
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
        elif op == "define":
            try:
                symbol, value = ast[1:]
            except ValueError:
                raise LispError("Wrong number of arguments for 'define'")
            if not is_symbol(symbol):
                raise LispError("non-symbol")
            env.set(symbol, evaluate(value, env))
        elif op == "lambda":
            try:
                params, body = ast[1:]
            except ValueError:
                raise LispError("Wrong number of arguments for 'lambda'")
            if not is_list(params):
                raise LispError("params is not a list")
            # if not is_list(body):
            #     raise LispError("body is not a list")
            return Closure(env, params, body)
        elif is_list(op):
            return evaluate([evaluate(op, env)] + ast[1:], env)
        elif is_closure(op):
            try:
                arguments = ast[1:]
            except ValueError:
                arguments = []
            return apply(op, arguments, env)
        elif op in {'cons', 'head', 'tail', 'empty'}:
            return list_manip(ast, env)
        else:
            try:
                arguments = ast[1:]
            except ValueError:
                arguments = []
            func = evaluate(op, env)
            if not is_closure(func):
                raise LispError("not a function")
            return evaluate([func] + arguments, env)
    except Exception as e:
        raise LispError("%s" % e)

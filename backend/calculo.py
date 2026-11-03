import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    factorial_notation,
    function_exponentiation,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


x, y, t = sp.symbols("x y t")

_TRANSFORMACOES = standard_transformations + (
    convert_xor,  
    implicit_multiplication_application,  
    function_exponentiation,
    factorial_notation,  
)

_NOMES_PERMITIDOS = {
    "x": x,
    "y": y,
    "t": t,
    "pi": sp.pi,
    "E": sp.E,
    "oo": sp.oo,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "sec": sp.sec,
    "csc": sp.csc,
    "cot": sp.cot,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
    "log": sp.log,
    "ln": sp.log,
    "exp": sp.exp,
}

_GLOBAIS_PARSER = {
    "__builtins__": {},
    "Integer": sp.Integer,
    "Float": sp.Float,
    "Rational": sp.Rational,
    "factorial": sp.factorial,
}


def interpretar(expressao: str | int | float | sp.Expr) -> sp.Expr:
    if isinstance(expressao, sp.Expr):
        return expressao
    if expressao is None or not str(expressao).strip():
        raise ValueError("Digite uma expressão para calcular.")

    try:
        return parse_expr(
            str(expressao),
            local_dict=_NOMES_PERMITIDOS,
            global_dict=_GLOBAIS_PARSER,
            transformations=_TRANSFORMACOES,
            evaluate=True,
        )
    except (SyntaxError, TypeError, ValueError, NameError)as Execption:
        raise ValueError("Expressão inválida", Execption)


def somar(a, b) -> sp.Expr:
    return sp.simplify(interpretar(a) + interpretar(b))


def subtrair(a, b) -> sp.Expr:
    return sp.simplify(interpretar(a) - interpretar(b))


def multiplicar(a, b) -> sp.Expr:
    return sp.simplify(interpretar(a) * interpretar(b))


def dividir(a, b) -> sp.Expr:
    denominador = interpretar(b)
    if denominador == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return sp.simplify(interpretar(a) / denominador)


def potencia(base, expoente) -> sp.Expr:
    return sp.simplify(interpretar(base) ** interpretar(expoente))


def raiz_quadrada(numero) -> sp.Expr:
    return sp.sqrt(interpretar(numero))


def porcentagem(numero, percentual) -> sp.Expr:
    return sp.simplify(interpretar(numero) * interpretar(percentual) / 100)


def fatorial(numero) -> sp.Expr:
    valor = interpretar(numero)
    if valor.is_integer is False or valor.is_negative is True:
        raise ValueError("O fatorial exige um inteiro pisitivo.")
    return sp.factorial(valor)


def derivada(expressao, variavel: str = "x", ordem: int = 1) -> sp.Expr:
    ordem = int(ordem)
    if ordem < 1:
        raise ValueError("A ordem da derivada deve ser maior que zero.")
    return sp.diff(interpretar(expressao), obter_variavel(variavel), ordem)


def integral_indefinida(expressao, variavel: str = "x") -> sp.Expr:
    return sp.integrate(interpretar(expressao), obter_variavel(variavel))


def integral_definida(expressao, a, b, variavel: str = "x") -> sp.Expr:
    simbolo = obter_variavel(variavel)
    return sp.integrate(interpretar(expressao), (simbolo, interpretar(a), interpretar(b)))


def limite(expressao, ponto, variavel: str = "x", lado: str = "ambos") -> sp.Expr:
    direcoes = {"ambos": "+-", "direita": "+", "esquerda": "-"}
    if lado not in direcoes:
        raise ValueError("O lado deve ser ambos, direita ou esquerda.")
    return sp.limit(
        interpretar(expressao),
        obter_variavel(variavel),
        interpretar(ponto),
        dir=direcoes[lado],
    )


def obter_variavel(nome: str) -> sp.Symbol:
    try:
        return {"x": x, "y": y, "t": t}[nome]
    except KeyError as erro:
        raise ValueError("A variável deve ser x, y ou t.") from erro
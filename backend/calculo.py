import sympy as sp
from sympy.parsing.sympy_parser import convert_xor,factorial_notation,function_exponentiation,implicit_multiplication_application,parse_expr,standard_transformations

# definimos as variaveis possiveis utilizadas nas expressoes, que sao x, y e t
x, y, t = sp.symbols("x y t")
# aqui definimos as transformacoes que serao aplicadas na interpretacao das expressoes, para permitir a interpretacao de expressao com multiplicacao implicita, exponenciacao de funcoes e fatorial
_TRANSFORMACOES = standard_transformations + (
    convert_xor,  
    implicit_multiplication_application,  
    function_exponentiation,
    factorial_notation,  
)
# aqui definimos os nomes permitidos para a interpretacao das expressoes, que sao as variaveis x, y, t e algumas funcoes matematicas
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
    
# aqui estamos verificando se a expressao esta no formato correto que definimos anteriormente, para funcionar com sympy
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

# funcao de soma, que tem como parametro dois valores, sp interpreta para o formato e executa a soma
def somar(a, b) -> sp.Expr:
    return sp.simplify(interpretar(a) + interpretar(b))

# funcao de subtracao, que tem como parametro dois valores, sp interpreta para o formato e executa a subtrai
def subtrair(a, b) -> sp.Expr:
    return sp.simplify(interpretar(a) - interpretar(b))

# funcao de multiplicacao, que tem como parametro dois valores, sp interpreta para o formato e executa a multiplicacao
def multiplicar(a, b) -> sp.Expr:
    return sp.simplify(interpretar(a) * interpretar(b))

# funcao de divisao, que tem como parametro dois valores, sp interpreta para o formato e executa a divisao 
def dividir(a, b) -> sp.Expr:
    denominador = interpretar(b)
    if denominador == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return sp.simplify(interpretar(a) / denominador)

# funcao de potencia, que tem como parametro dois valores, sp interpreta para o formato e executa a potencia (**), e simplifica o resultado
def potencia(base, expoente) -> sp.Expr:
    return sp.simplify(interpretar(base) ** interpretar(expoente))

# funcao de raiz quadrada, que tem como parametro um valor, sp interpreta para o formato e executa a raiz quadrada, e simplifica o resultado
def raiz_quadrada(numero) -> sp.Expr:
    return sp.sqrt(interpretar(numero))

# funcao de porcentagem, que tem como parametro dois valores, sp interpreta para o formato e executa a porcentagem, e simplifica o resultado
def porcentagem(numero, percentual) -> sp.Expr:
    return sp.simplify(interpretar(numero) * interpretar(percentual) / 100)

# funcao de fatorial, que tem como parametro um valor, sp interpreta para o formato e executa o fatorial, e simplifica o resultado
def fatorial(numero) -> sp.Expr:
    valor = interpretar(numero)
    if valor.is_integer is False or valor.is_negative is True:
        raise ValueError("O fatorial exige um inteiro positivo.")
    return sp.factorial(valor)

# funcao de derivada, que tem como parametro uma expressao, uma variavel e a ordem da derivada, sp interpreta para o formato e executa a derivada, e simplifica o resultado
def derivada(expressao, variavel: str = "x", ordem: int = 1) -> sp.Expr:
    ordem = int(ordem)
    if ordem < 1:
        raise ValueError("A ordem da derivada deve ser maior que zero.")
    return sp.diff(interpretar(expressao), obter_variavel(variavel), ordem)

# funcao de integral, que tem como parametro uma expressao, uma variavel e a ordem da integral, sp interpreta para o formato e executa a integral, e simplifica o resultado
def integral_indefinida(expressao, variavel: str = "x") -> sp.Expr:
    return sp.integrate(interpretar(expressao), obter_variavel(variavel))

# funcao de integral definida, que tem como parametro uma expressao, uma variavel e os limites de integracao, sp interpreta para o formato e executa a integral definida, e simplifica o resultado
def integral_definida(expressao, a, b, variavel: str = "x") -> sp.Expr:
    simbolo = obter_variavel(variavel)
    return sp.integrate(interpretar(expressao), (simbolo, interpretar(a), interpretar(b)))

# funcao de limite, que tem como parametro uma expressao, um ponto, uma variavel e o lado do limite, pela direita esquerda ou ambos, sp interpreta para o formato e executa o limite, e simplifica o resultado
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

# funcao de obter a variavel, que tem como parametro o nome da variavel, e retorna o simbolo correspondente
def obter_variavel(nome: str) -> sp.Symbol:
    try:
        return {"x": x, "y": y, "t": t}[nome]
    except KeyError as erro:
        raise ValueError("A variável deve ser x, y ou t.") from erro
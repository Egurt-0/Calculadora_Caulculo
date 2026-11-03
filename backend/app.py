from flask import Flask, render_template, request

from calculo import (
    derivada,
    integral_definida,
    integral_indefinida,
    interpretar,
    limite,
    obter_variavel,
)
app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
    static_url_path=""
)

@app.get("/")
def renderizar(expressao="", resultado="=", dados=None):
    """Renderiza a calculadora mantendo os campos enviados pelo formulário."""
    dados = dados or {}
    return render_template(
        "index.html",
        expressao=expressao,
        resultado=resultado,
        operacao=dados.get("operacao", "avaliar"),
        variavel=dados.get("variavel", "x"),
        valor=dados.get("valor", ""),
        ordem=dados.get("ordem", "1"),
        a=dados.get("a", ""),
        b=dados.get("b", ""),
        ponto=dados.get("ponto", ""),
        lado=dados.get("lado", "ambos"),
    )


def avaliar(expressao, variavel, valor):
    resultado = interpretar(expressao)
    if valor.strip():
        resultado = resultado.subs(obter_variavel(variavel), interpretar(valor))
    return resultado


@app.get("/")
def home():
    return renderizar()

@app.post("/calcular")
def calcular():
    dados = request.form
    expressao = dados.get("expressao", "")
    acao = dados.get("acao")
    tecla = dados.get("tecla")
    operacao = dados.get("operacao", "avaliar")
    resultado = "="
    if tecla:
        expressao += tecla
    elif acao == "limpar":
        expressao = ""
    elif acao == "apagar":
        expressao = expressao[:-1]
    elif acao == "calcular":
        try:
            variavel = dados.get("variavel", "x")
            if operacao == "avaliar":
                resultado = avaliar(expressao, variavel, dados.get("valor", ""))
            elif operacao == "derivada":
                resultado = derivada(expressao, variavel, dados.get("ordem", 1))
            elif operacao == "integral_indefinida":
                resultado = integral_indefinida(expressao, variavel)
            elif operacao == "integral_definida":
                resultado = integral_definida(
                    expressao, dados.get("a", ""), dados.get("b", ""), variavel
                )
            elif operacao == "limite":
                resultado = limite(
                    expressao,
                    dados.get("ponto", ""),
                    variavel,
                    dados.get("lado", "ambos"),
                )
            else:
                raise ValueError("Operação inválida.")
            resultado = str(resultado)
        except (ArithmeticError, KeyError, TypeError, ValueError) as erro:
            resultado = f"Erro: {erro}"
    return renderizar(expressao, resultado, dados)

    
if __name__ == "__main__":
    app.run(debug=True)

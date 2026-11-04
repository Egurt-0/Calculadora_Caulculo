from flask import Flask, render_template, request

# importando tudo o que preciso do arquivo calculo
from calculo import (
    derivada,
    integral_definida,
    integral_indefinida,
    interpretar,
    limite,
    obter_variavel,
)

# aqui definimos a aplicacao flask, que vai renderizar o frontend e receber as requisicoes que o usuario faz pelo frontend, chamando as funcoes do calculo.py para realizar os calculos
app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
    static_url_path=""
)

# funcao de renderizar, que tem como parametro a expressao, o resultado e os dados do formulario, e retorna o formato no index.html com os valores preenchidos
def renderizar(expressao="", resultado="=", dados=None):
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

# funcao de avaliar, que tem como parametro a expressao, a variavel e o valor, e retorna o resultado da avaliacao da expressao com o valor da variavel substituido
def avaliar(expressao, variavel, valor):
    resultado = interpretar(expressao)
    if valor.strip():
        resultado = resultado.subs(obter_variavel(variavel), interpretar(valor))
    return resultado

# rota principal, que renderiza a pagina inicial do frontend
@app.get("/")
def home():
    return renderizar()
# rota de calculo, que recebe os dados do formulario, e chama as funcoes do calculo.py para realizar os calculos, e retorna o resultado para o frontend na posicao certa definida pelo html
@app.post("/calcular")
def calcular():
    dados = request.form
    expressao = dados.get("expressao", "")
    acao = dados.get("acao")
    tecla = dados.get("tecla")
    operacao = dados.get("operacao", "avaliar")
    resultado = "="
    # if e elif de todas as acoes que o usuario pode fazer
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
            # trata os erros que podem ocorrer durante a interpretacao da expressao, e retorna o erro para o frontend
        except (ArithmeticError, KeyError, TypeError, ValueError) as erro:
            resultado = f"Erro: {erro}"
    return renderizar(expressao, resultado, dados)

# faz com que o arquivo so seja executado com um comado direto, e nao imediatamente apos ser importado
if __name__ == "__main__":
    app.run(debug=True) # Debugando antes de rodar o app, para que possamos ver os erros no terminal, e nao apenas no front

from flask import Flask, render_template, request
from calculo import *
app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend",
    static_url_path=""
)

@app.get("/")
def home():
    return render_template("index.html",expressao="",resultado="=")

@app.post("/calcular")
def calcular():
    dados = request.form
    expressao = dados.get("expressao", "")
    acao = dados.get("acao")
    tecla = dados.get("tecla")
    operacao = dados.get("operacao","avaliar")
    resultado = "="
    if tecla:
        expressao+=tecla
    elif acao == "limpar":
        expressao=""
    elif acao == "apagar":
        expressao = expressao[:-1]
    elif acao == expressao:
        try:
            resultado = str(operacao[operacao](expressao, dados))
        except (ValueError, ZeroDivisionError, KeyError) as execption:
            resultado = f"Erro: {execption}"
    return render_template("index.html", expressao=expressao, resultado=resultado)

    
if __name__ == "__main__":
    app.run(debug=True)
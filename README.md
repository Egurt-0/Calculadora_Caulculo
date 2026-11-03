# Calculadora de Cálculo I

Aplicação web em Flask para avaliar expressões e calcular derivadas, integrais e limites com SymPy.

## Recursos

- Avaliação de expressões, com substituição opcional de `x`, `y` ou `t`.
- Derivadas de primeira a quinta ordem.
- Integrais indefinidas e definidas.
- Limites bilaterais e laterais.
- Teclado visual para montar expressões.

## Executar localmente

Requer Python 3.12 ou mais recente.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python backend\app.py
```

Abra `http://127.0.0.1:5000` no navegador.

> Caso o PowerShell bloqueie a ativação do ambiente, execute o `pip` e o `python` usando `venv\Scripts\python.exe`.

## Sintaxe de exemplos

| Cálculo | Expressão | Parâmetros |
| --- | --- | --- |
| Avaliar | `x^2 + sin(x)` | valor: `2` |
| Derivada | `x^3 + 2*x` | variável: `x`, ordem: `1` |
| Integral definida | `x^2` | de: `0`, até: `3` |
| Limite | `sin(x)/x` | ponto: `0` |

As expressões usam a sintaxe do SymPy: `^`, `pi`, `E`, `oo`, `sqrt(...)`, `sin(...)` e similares.

## Estrutura

```text
backend/         Rotas Flask e regras de cálculo
frontend/        Interface HTML e CSS
requirements.txt Dependências do projeto
```

O diretório `venv/` é local e fica ignorado pelo Git.

# Calculadora de Cálculo I

Interface estática (HTML + CSS, sem JavaScript) para derivadas, integrais e limites.
O backend em Python fica por sua conta.

## Abrir localmente

Dê dois cliques em `frontend/index.html`. A página abre no navegador, mas os botões
só funcionam depois que existir um backend respondendo em `/calcular`.

## Estrutura

```
calculadora-calculo/
├── frontend/
│   ├── index.html
│   └── style.css
└── README.md
```

## Como funciona sem JS

Tudo fica dentro de um único `<form action="/calcular" method="post">`.
Cada clique em qualquer botão envia o formulário inteiro para o backend, que devolve
a página atualizada (com a expressão nova ou o resultado).

A troca entre f(x), d/dx, ∫, ∫ₐᵇ e lim é feita só com CSS (`:has()` + radio buttons).

## Campos que chegam no backend (POST /calcular)

| Campo       | Valores                                                                  | Quando usar                    |
|-------------|--------------------------------------------------------------------------|--------------------------------|
| `operacao`  | `avaliar`, `derivada`, `integral_indefinida`, `integral_definida`, `limite` | sempre                         |
| `expressao` | texto, ex: `x^2 + sin(x)`                                                | sempre                         |
| `variavel`  | `x`, `y`, `t`                                                            | sempre                         |
| `valor`     | número (opcional)                                                        | `avaliar`                      |
| `ordem`     | 1 a 5                                                                    | `derivada`                     |
| `a`, `b`    | limites de integração                                                    | `integral_definida`            |
| `ponto`     | número, `oo` ou `-oo`                                                    | `limite`                       |
| `lado`      | `ambos`, `direita`, `esquerda`                                           | `limite`                       |
| `tecla`     | texto a inserir no fim da expressão (`sin(`, `7`, `^2`, `pi`, `oo`...)    | quando um botão do teclado foi clicado |
| `acao`      | `calcular`, `limpar`, `apagar`                                           | `=`, `C`, `⌫` (Enter no visor = `calcular`) |

Só um de `tecla` ou `acao` vem em cada envio. Os valores do teclado já seguem a sintaxe
do SymPy (`pi`, `E`, `oo`, `sqrt(`, `asin(`...); o backend só precisa trocar `^` por `**`.

## O que o backend precisa devolver

A mesma página, preenchendo:

- `value` do `<input id="expressao">` com a expressão atual
- o conteúdo de `<output name="resultado">` com o resultado
- o `checked` no radio da operação que estava selecionada (e os valores dos outros campos)
- os itens `<li>` do `<ol>` em "Histórico" (opcional)

Sugestão: Flask + Jinja2. Configure o Flask para servir a pasta `frontend` na raiz
(`static_folder="frontend", static_url_path=""`, `template_folder="frontend"`) e o
`href="style.css"` funciona tanto abrindo o arquivo direto quanto pelo servidor.

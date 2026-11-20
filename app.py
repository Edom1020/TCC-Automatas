"""
Interfaz web (Flask) para transacciones.py.

No reimplementa el análisis léxico ni el intérprete: importa y llama
directamente a analizar_lexico() e interpretar() del módulo original.
Para obtener el detalle de cada movimiento (saldo acumulado) se captura
la traza que interpretar() ya imprime con mostrar_traza=True, en lugar
de tocar su lógica interna.
"""

import contextlib
import io
import re

from flask import Flask, render_template, request

from transacciones import (
    TEXTO_ENUNCIADO,
    ErrorLexico,
    ErrorSintactico,
    analizar_lexico,
    interpretar,
)

app = Flask(__name__)

# Coincide con las líneas que interpretar() imprime, p.ej.:
#   "  Deposito  +   500   saldo = 500"
PATRON_TRAZA = re.compile(r"^\s*(\S+)\s+([+-])\s*(\d+)\s+saldo = (-?\d+)\s*$")

CLASE_TOKEN = {
    "INICIO_MOV": "tk-fijo",
    "SEP_VALOR": "tk-fijo",
    "FIN_MOV": "tk-fijo",
    "PALABRA": "tk-palabra",
    "NUMERO": "tk-numero",
}


def fmt_dinero(n):
    signo = "-" if n < 0 else ""
    return f"{signo}$ {abs(n):,}".replace(",", ".")


def fmt_monto(signo, valor):
    simbolo = "+ " if signo > 0 else "− "
    return simbolo + f"{valor:,}".replace(",", ".")


def procesar_texto(texto):
    """Ejecuta analizar_lexico()/interpretar() tal cual y arma el contexto
    que necesita la plantilla."""
    contexto = {
        "texto": texto,
        "num_tokens": 0,
        "tokens": [],
        "movs": [],
        "sin_movs": True,
        "hay_error": False,
        "error_titulo": "",
        "error_msg": "",
        "ok": False,
        "saldo_txt": "—",
        "total_dep": "—",
        "total_ret": "—",
    }

    vacio = texto.strip() == ""

    try:
        tokens = analizar_lexico(texto)
    except ErrorLexico as e:
        contexto["hay_error"] = True
        contexto["error_titulo"] = "Error léxico"
        contexto["error_msg"] = str(e)
        return contexto

    contexto["num_tokens"] = len(tokens)
    contexto["tokens"] = [
        {
            "tipo": tok.tipo,
            "lexema": tok.lexema,
            "clase": CLASE_TOKEN.get(tok.tipo, "tk-palabra"),
        }
        for tok in tokens
    ]

    buffer_salida = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer_salida):
            interpretar(tokens, mostrar_traza=True)
    except ErrorSintactico as e:
        contexto["hay_error"] = True
        contexto["error_titulo"] = "Error sintáctico"
        contexto["error_msg"] = str(e)
        return contexto

    movs = []
    total_dep = 0
    total_ret = 0
    for linea in buffer_salida.getvalue().splitlines():
        m = PATRON_TRAZA.match(linea)
        if not m:
            continue
        tipo, signo_txt, valor_txt, saldo_txt = m.groups()
        signo = 1 if signo_txt == "+" else -1
        valor = int(valor_txt)
        saldo = int(saldo_txt)
        if signo > 0:
            total_dep += valor
        else:
            total_ret += valor
        movs.append(
            {
                "n": len(movs) + 1,
                "tipo": tipo,
                "monto": fmt_monto(signo, valor),
                "clase": "monto-pos" if signo > 0 else "monto-neg",
                "saldo": fmt_dinero(saldo),
            }
        )

    saldo_final = movs[-1]["saldo"] if movs else fmt_dinero(0)

    contexto["movs"] = movs
    contexto["sin_movs"] = len(movs) == 0
    contexto["total_dep"] = fmt_dinero(total_dep)
    contexto["total_ret"] = fmt_dinero(total_ret)
    contexto["ok"] = not vacio
    contexto["saldo_txt"] = saldo_final if not vacio else "—"
    return contexto


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        archivo = request.files.get("archivo")
        accion = request.form.get("accion", "procesar")

        if archivo and archivo.filename:
            texto = archivo.read().decode("utf-8", errors="replace")
        elif accion == "ejemplo":
            texto = TEXTO_ENUNCIADO
        elif accion == "limpiar":
            texto = ""
        else:
            texto = request.form.get("texto", "")

        contexto = procesar_texto(texto)
    else:
        contexto = procesar_texto(TEXTO_ENUNCIADO)

    return render_template("index.html", **contexto)


if __name__ == "__main__":
    app.run(debug=True)

"""
TCC Autómatas 2026-2 · CIPA DEV-OPS
Transacciones Bancarias (Saldo Final)

El programa tiene dos autómatas:
  1. Analizador léxico: recorre el texto carácter por carácter y lo convierte en TOKENS.
  2. Intérprete: autómata con historia de estado que recorre los tokens, recuerda
     el tipo del movimiento y, al cerrar cada bloque </mov>, suma o resta el valor.

Uso:
  python transacciones.py                  -> usa el texto del enunciado
  python transacciones.py archivo.txt      -> lee el texto desde un archivo
"""

import sys
from dataclasses import dataclass

TEXTO_ENUNCIADO = (
    "<mov>Tipo: Deposito; Valor: 500</mov>"
    "<mov>Tipo: Retiro; Valor: 200</mov>"
    "<mov>Tipo: Deposito; Valor: 100</mov>"
)

# Tokens fijos (palabras reservadas) que pide el enunciado.
TOKENS_FIJOS = {
    "<mov>Tipo:": "INICIO_MOV",
    "; Valor:": "SEP_VALOR",
    "</mov>": "FIN_MOV",
}


@dataclass
class Token:
    tipo: str      # categoría: INICIO_MOV, SEP_VALOR, FIN_MOV, PALABRA, NUMERO
    lexema: str    # texto exacto reconocido
    posicion: int  # índice donde empieza en el texto (útil para errores)


class ErrorLexico(Exception):
    pass


class ErrorSintactico(Exception):
    pass


# ---------------------------------------------------------------------------
# 1. ANALIZADOR LÉXICO
# ---------------------------------------------------------------------------

def coincide_literal(texto, i, literal):
    """Autómata que intenta reconocer un token fijo desde la posición i.
    Un espacio en el literal acepta uno o más espacios en el texto.
    Devuelve la posición final si lo reconoce, o None si falla."""
    for c in literal:
        if c == " ":
            if i >= len(texto) or not texto[i].isspace():
                return None
            while i < len(texto) and texto[i].isspace():
                i += 1
        elif i < len(texto) and texto[i] == c:
            i += 1
        else:
            return None
    return i


def analizar_lexico(texto):
    """Convierte el texto en una lista de tokens."""
    tokens = []
    i = 0
    while i < len(texto):
        c = texto[i]

        # Los espacios entre tokens no aportan información: se ignoran.
        if c.isspace():
            i += 1
            continue

        # Intentar primero los tokens fijos del enunciado.
        for literal, tipo in TOKENS_FIJOS.items():
            fin = coincide_literal(texto, i, literal)
            if fin is not None:
                tokens.append(Token(tipo, texto[i:fin], i))
                i = fin
                break
        else:
            # Estado "leyendo palabra": letras seguidas (Deposito, Retiro).
            if c.isalpha():
                inicio = i
                while i < len(texto) and texto[i].isalpha():
                    i += 1
                tokens.append(Token("PALABRA", texto[inicio:i], inicio))
            # Estado "leyendo número": dígitos seguidos (500, 200...).
            elif c.isdigit():
                inicio = i
                while i < len(texto) and texto[i].isdigit():
                    i += 1
                tokens.append(Token("NUMERO", texto[inicio:i], inicio))
            else:
                raise ErrorLexico(f"Carácter inesperado '{c}' en la posición {i}")
    return tokens


# ---------------------------------------------------------------------------
# 2. INTÉRPRETE (autómata con historia de estado)
# ---------------------------------------------------------------------------

# Tabla de transiciones: (estado_actual, tipo_de_token) -> estado_siguiente
TRANSICIONES = {
    ("ESPERA_MOV", "INICIO_MOV"): "ESPERA_TIPO",
    ("ESPERA_TIPO", "PALABRA"): "ESPERA_SEP",
    ("ESPERA_SEP", "SEP_VALOR"): "ESPERA_VALOR",
    ("ESPERA_VALOR", "NUMERO"): "ESPERA_FIN",
    ("ESPERA_FIN", "FIN_MOV"): "ESPERA_MOV",
}

# Efecto de cada tipo de movimiento sobre el saldo.
OPERACIONES = {
    "Deposito": +1,
    "Retiro": -1,
}


def interpretar(tokens, mostrar_traza=True):
    """Recorre los tokens con el autómata y devuelve el saldo final."""
    estado = "ESPERA_MOV"
    saldo = 0
    tipo_actual = None   # historia: el tipo leído se recuerda hasta el </mov>
    valor_actual = None

    for tok in tokens:
        siguiente = TRANSICIONES.get((estado, tok.tipo))
        if siguiente is None:
            raise ErrorSintactico(
                f"Token {tok.tipo} '{tok.lexema}' no esperado en el estado {estado} "
                f"(posición {tok.posicion})"
            )

        # Acciones semánticas asociadas a cada transición.
        if tok.tipo == "PALABRA":
            if tok.lexema not in OPERACIONES:
                raise ErrorSintactico(
                    f"Tipo de movimiento desconocido '{tok.lexema}' (posición {tok.posicion})"
                )
            tipo_actual = tok.lexema
        elif tok.tipo == "NUMERO":
            valor_actual = int(tok.lexema)
        elif tok.tipo == "FIN_MOV":
            # Al cerrar el bloque se aplica el movimiento usando lo recordado.
            saldo += OPERACIONES[tipo_actual] * valor_actual
            if mostrar_traza:
                signo = "+" if OPERACIONES[tipo_actual] > 0 else "-"
                print(f"  {tipo_actual:<9} {signo}{valor_actual:>6}   saldo = {saldo}")
            tipo_actual = valor_actual = None

        estado = siguiente

    # Solo se acepta la cadena si el autómata termina en el estado inicial.
    if estado != "ESPERA_MOV":
        raise ErrorSintactico(f"El texto termina incompleto (estado {estado})")
    return saldo


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            texto = f.read()
    else:
        texto = TEXTO_ENUNCIADO

    print("Texto de entrada:")
    print(f"  {texto.strip()}\n")

    try:
        tokens = analizar_lexico(texto)
        print("Tokens identificados:")
        for tok in tokens:
            print(f"  {tok.tipo:<11} '{tok.lexema}'")

        print("\nMovimientos procesados:")
        saldo = interpretar(tokens)
        print(f"\nSaldo final de la cuenta: {saldo}")
    except (ErrorLexico, ErrorSintactico) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

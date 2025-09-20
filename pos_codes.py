#!/usr/bin/env python3
"""
pos_codes.py

Valida códigos POS de 6 caracteres con el patrón:
  - posiciones 0-1: letras mayúsculas A-Z
  - posiciones 2-4: dígitos 0-9, con la restricción de que no hay "00" consecutivos
    dentro de esas tres posiciones (es decir, ni en (2,3) ni en (3,4) puede aparecer "00")
  - posición 5: letra mayúscula A-Z

Funciones:
- is_valid_pos_code(code) -> bool
- generate_valid_codes(limit=None) -> generator (puede usarse con limit para no generar todos)
- main() -> CLI interactivo
- tests() -> pruebas simples al ejecutar el archivo directamente
"""

from typing import Generator, Optional


def is_valid_pos_code(code: str) -> bool:
    """
    Verifica si `code` cumple las reglas del POS.

    Parámetros:
        code: cadena a validar

    Retorna:
        True si es válida, False en caso contrario.
    """
    if not isinstance(code, str):
        return False

    if len(code) != 6:
        return False

    # Posiciones de letras
    if not (code[0].isalpha() and code[0].isupper()):
        return False
    if not (code[1].isalpha() and code[1].isupper()):
        return False
    if not (code[5].isalpha() and code[5].isupper()):
        return False

    # Posiciones de dígitos
    digits = code[2:5]
    if not digits.isdigit() or len(digits) != 3:
        return False

    # Prohibir "00" consecutivos en las posiciones (2,3) y (3,4).
    # Es decir, dentro de 'digits' no puede aparecer la subcadena "00".
    if "00" in digits:
        return False

    # Todo OK
    return True


def generate_valid_codes(limit: Optional[int] = None) -> Generator[str, None, None]:
    """
    Generador de códigos válidos. POR DEFECTO genera todos (17.576.000),
    así que se recomienda usar `limit` para pruebas.

    Parámetros:
        limit: si es None, intenta generar todos (muy costoso). Si es int,
               genera solo hasta `limit` códigos.

    Ejemplo:
        for i, code in enumerate(generate_valid_codes(limit=100)):
            print(code)
    """
    import itertools
    letters = [chr(ord("A") + i) for i in range(26)]
    digits = [str(i) for i in range(10)]

    count = 0
    for L1, L2 in itertools.product(letters, repeat=2):
        for d1 in digits:
            for d2 in digits:
                # Si d1 == '0' and d2 == '0' -> '00' en (2,3) => prohibido
                if d1 == "0" and d2 == "0":
                    continue
                for d3 in digits:
                    # Si d2 == '0' and d3 == '0' -> '00' en (3,4) => prohibido
                    if d2 == "0" and d3 == "0":
                        continue
                    for L3 in letters:
                        code = f"{L1}{L2}{d1}{d2}{d3}{L3}"
                        yield code
                        count += 1
                        if limit is not None and count >= limit:
                            return


def main():
    """
    Interfaz simple por consola: pide códigos (uno por línea) y muestra si son válidos.
    Escribe 'salir' o Ctrl+C para terminar.
    """
    print("Validador de códigos POS (LL DDD L, sin '00' consecutivos en los 3 dígitos)." )
    print("Escribe un código para validar, o 'gen N' para generar N códigos de prueba, o 'salir' para terminar.")
    try:
        while True:
            s = input("> ").strip()
            if s.lower() in {"salir", "exit", "q", "quit"}:
                print("Saliendo.")
                break
            if s.lower().startswith("gen "):
                try:
                    n = int(s.split()[1])
                    print(f"Generando {n} códigos de ejemplo:")
                    for i, code in enumerate(generate_valid_codes(limit=n), start=1):
                        print(f"{i:4d}: {code}")
                except Exception as e:
                    print("Uso: gen N  (ej: gen 10). Error:", e)
                continue

            valid = is_valid_pos_code(s)
            print(f"{s} -> {'VÁLIDO' if valid else 'INVÁLIDO'}")
    except KeyboardInterrupt:
        print("\nInterrupción por teclado. Saliendo.")


def tests():
    """Pruebas básicas rápidas."""
    cases = {
        "AB123C": True,   # válido
        "AZ009B": False,  # '00' en las posiciones 3-4? digits='009' contiene '00' -> inválido
        "AA100Z": False,  # digits='100' contiene '00' en (2,3) del bloque -> inválido
        "AB090C": True,   # '090' tiene '09' y '90' OK, no '00'
        "A9123B": False,  # longitud != 6
        "ab123C": False,  # minúscula en posición 0
        "AB12C3": False,  # posiciones incorrectas
        "AB120C": True,   # digits='120' no tiene '00'
        "XY000Z": False,  # digits='000' -> contiene '00' -> inválido
    }

    ok = True
    for code, expected in cases.items():
        got = is_valid_pos_code(code)
        print(f"Test {code:8s}: esperado={expected}  got={got}")
        if got != expected:
            ok = False

    # Probar que el generador produce solo códigos válidos (limitado a 1000)
    print("\nProbando generador (hasta 1000 códigos)...")
    for i, code in enumerate(generate_valid_codes(limit=1000), start=1):
        if not is_valid_pos_code(code):
            print("Generador produjo código inválido:", code)
            ok = False
            break
    else:
        print("Generador OK para 1000 códigos.")

    print("\nResultado de pruebas:", "OK" if ok else "FALLÓ")


if __name__ == "__main__":
    # Si ejecutas el script directamente, corre las pruebas básicas y luego abre el CLI.
    print("Ejecutando pruebas rápidas...")
    tests()
    print("\nEntrando al modo interactivo (Ctrl+C para salir)." )
    main()

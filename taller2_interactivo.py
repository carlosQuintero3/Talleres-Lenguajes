import re

# --------- Ejercicio 1: Validar contraseñas ---------
def validar_contrasena(password: str) -> bool:
    """
    Reglas:
    - Primer carácter: mayúscula (A-Z)
    - Parte intermedia opcional: minúsculas (a-z)*
    - Parte final obligatoria: dígitos (0-9)+
    """
    patron = r'^[A-Z][a-z]*[0-9]+$'
    return re.fullmatch(patron, password) is not None


# --------- Ejercicio 2: Validar correos ---------
def validar_correo(correo: str) -> bool:
    """
    Reglas:
    - Inicia con >=1 letra minúscula
    - Luego letras o dígitos (a-z, 0-9)*
    - Termina con '@uptc.edu.co'
    """
    patron = r'^[a-z][a-z0-9]*@uptc\.edu\.co$'
    return re.fullmatch(patron, correo) is not None


# --------- Menú interactivo ---------
def main():
    print("=== Taller 2: Validación AFN / AFD ===")
    print("Opciones:")
    print("1. Validar contraseñas (Ejercicio 1)")
    print("2. Validar correos institucionales (Ejercicio 2)")
    print("0. Salir")

    while True:
        opcion = input("\nElige una opción (0-2): ").strip()

        if opcion == "0":
            print("Saliendo del programa. ¡Adiós!")
            break

        elif opcion == "1":
            print("\n--- Validación de contraseñas ---")
            while True:
                pwd = input("Escribe una contraseña (o 'salir' para volver al menú): ").strip()
                if pwd.lower() == "salir":
                    break
                if validar_contrasena(pwd):
                    print("✅ VÁLIDA según las reglas.")
                else:
                    print("❌ INVÁLIDA.")

        elif opcion == "2":
            print("\n--- Validación de correos ---")
            while True:
                correo = input("Escribe un correo (o 'salir' para volver al menú): ").strip()
                if correo.lower() == "salir":
                    break
                if validar_correo(correo):
                    print("✅ VÁLIDO según las reglas.")
                else:
                    print("❌ INVÁLIDO.")

        else:
            print("⚠️ Opción no válida. Intenta otra vez.")


if __name__ == "__main__":
    main()

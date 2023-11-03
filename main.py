
import AnalizadorSemantico


while True:
    print("Elija una opción")
    print("\t1 - Codigo Incorrecto (incorrecto.txt)")
    print("\t2 - Codigo Correcto (correcto.txt)")
    print("\t3 - Salir")
    opcion = input()
    if opcion == "1":
        analizar2 = AnalizadorSemantico.AnalizadorSemantico()
        analizar2.leyendoCodigo("incorrecto.txt")
    elif opcion == "2":
        analizar = AnalizadorSemantico.AnalizadorSemantico()
        analizar.leyendoCodigo("correcto.txt")
    elif opcion == "3":
        break

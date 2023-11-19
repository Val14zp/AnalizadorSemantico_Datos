
import AnalizadorSemantico


<<<<<<< Updated upstream
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
=======
    nombre_archivo = "incorrecto.txt"
    archivo = Archivo.Archivo(nombre_archivo)
    archivo.ver_listas_palabras()
    symbol_table.procesar_lineas(archivo.leer_y_dividir_lineas())
    """
    symbol_table.buscar_variable_en_tabla_simbolos("x")
    symbol_table.buscar_variable_en_tabla_simbolos("s")
    symbol_table.buscar_variable_en_tabla_simbolos("funcion")
    symbol_table.buscar_variable_en_tabla_simbolos("n")
    symbol_table.buscar_variable_en_tabla_simbolos("v")
    symbol_table.buscar_variable_en_tabla_simbolos("w")
    symbol_table.buscar_variable_en_tabla_simbolos("prueba")

    symbol_table.eliminar("x")
    symbol_table.eliminar("s")
    symbol_table.eliminar("funcion")
    symbol_table.eliminar("n")
    symbol_table.eliminar("v")
    symbol_table.eliminar("w")
    symbol_table.eliminar("prueba")
    """
if __name__ == "__main__":
    main()
>>>>>>> Stashed changes

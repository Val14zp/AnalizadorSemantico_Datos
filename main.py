import AnalizadorSemantico
import TablaSimbolos
import Archivo

def main():
    print("Este es el programa principal.")
    symbol_table = TablaSimbolos.TablaSimbolos()

    nombre_archivo = "correcto.txt"
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
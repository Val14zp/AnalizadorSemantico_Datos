import TablaSimbolos
import Archivo

def main():
    print("Este es el programa principal.")
    symbol_table = TablaSimbolos.TablaSimbolos()

    nombre_archivo = "incorrecto.txt"
    archivo = Archivo.Archivo(nombre_archivo)
    archivo.ver_listas_palabras()
    symbol_table.procesar_lineas(archivo.leer_y_dividir_lineas())
    symbol_table.encontrar_errores(archivo.leer_y_dividir_lineas())

if __name__ == "__main__":
    main()
class Archivo:
    """Gestor para leer archivos."""

    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def leer_y_dividir_lineas(self):
        """Lee el archivo y separa cada linea en palabras."""
        try:
            with open(self.nombre_archivo, 'r', encoding="utf=8") as archivo:
                lineas = archivo.readlines()
                palabras_por_linea = []

                for linea in lineas:
                    palabras = linea.split()
                    palabras_por_linea.append(palabras)

                return palabras_por_linea

        except FileNotFoundError:
            print(f"El archivo '{self.nombre_archivo}' no se encontró.")
            return []

    def ver_listas_palabras(self):
        """Ver las listas de palabras de cada una de las lineas leidas del archivo."""
        lineas_divididas = self.leer_y_dividir_lineas()

        for i, palabras in enumerate(lineas_divididas):
            print(f"Línea {i + 1}: {palabras}")

    
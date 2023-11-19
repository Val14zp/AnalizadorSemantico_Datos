class Variable:
    """Es el objeto que se inserta en la tabla de simbolos."""

    def __init__(self, tipo, nombre, valor):
        self.tipo = tipo
        self.nombre = nombre
        self.valor = valor
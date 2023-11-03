
class Variable:
    def __init__(self, tipo, nombre):
        self.nombre = nombre
        self.tipo = tipo
        self.id = ""
        self.linea = 0


class AnalizadorSemantico:
    def __init__(self):
        self.hashGlobal = {}
        self.reservada = {'void': "void", 'int': "int", 'float': "float", 'string': "string",
                          'if': "if", 'while': "while", 'return': "return"}
        self.especiales = {'+': "+", '-': "-", ';': ";", '*': "*", ',': ",", '/': "/", '=': "=", '==': "==", '!=': "!=",
                           '<': "<", '>': ">", ')': ")", '{': "{", '}': "}", '(': "("}

    def guardarEnHashGlobal(self, var):
        self.hashGlobal[var.nombre] = var

    @staticmethod
    def esString(s):
        if s == '':
            return False
        return s[0] == -30 and s[s.size() - 1] == -99 or \
               s[0] == 34 and s[s.size() - 1] == 34 or \
               s[0] == 39 and s[s.size() - 1] == 39

    @staticmethod
    def esNumero(n):
        return n.replace('.', '', 1).isdigit()

    @staticmethod
    def es_flotante(variable):
        try:
            float(variable)
            return True
        finally:
            return False

    def leyendoCodigo(self, codigo):
        self._leyendoCodigo(codigo)

    @staticmethod
    def _leyendoCodigo(codigo):
        contador = 1
        archivo = open(codigo, "r", encoding="utf=8")
        linea = archivo.readlines()  # una lista de lineas
        archivo.close()
        for i in linea:
            print(contador, " " + i)
            contador += 1

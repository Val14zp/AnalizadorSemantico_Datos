
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
        self.pila = []

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

    def _leyendoCodigo(self, codigo):
        contador = 1
        archivo = open(codigo, "r", encoding="utf=8")
        linea = archivo.readlines()  # una lista de lineas
        archivo.close()
        for i in linea:
            palabras = i.split()  # Divide la línea en palabras
            for palabra in palabras: # Un ciclo que recorre cada palabra en la lista de palabras
                if palabra not in self.hashGlobal: # Si no está en la hashmap entra en el condicional
                    if palabra in self.reservada:
                        if self.pila: # Si hay pila es porque ya se realizó una operación anteriormente
                            if self.pila[-1] in self.reservada: # Quiere decir que hubo doble declaración
                                print("Error - Linea " + str(contador) + ": Declaración de tipos incorrecta.")
                        else:
                            self.pila.append(palabra) # Si no hay pila se agrega en ella para saber si es posible una posible declaración
                    elif palabra in self.especiales:
                        if self.pila:
                            if self.pila[-1] in self.hashGlobal: # Verifica que antes de un caracter especial haya una variable
                                self.pila.append(palabra)
                            else:
                                print("Error - Linea: " + str(contador) + ": uso de carácteres especiales incorrecto.")
                        else:
                            print("Error - Linea: " + str(contador) + ": uso de carácteres especiales incorrecto.")
                    else:
                        if self.pila:
                            if self.pila[-1] in self.reservada: # Verifica que el anterior sea una declaración de tipo
                                variable = Variable(self.pila[-1],palabra) # Crea una variable con el tipo almacenado en la pila y con el nombre de la misma
                                self.guardarEnHashGlobal(variable) # La guarda en la tabla hash
                                self.pila.pop() # Eliminamos el contenido de la pila
                                self.pila.append(variable) # Agregamos la variable a la pila para posibles usos a futuro
                            else:
                                print("Error - Linea: " + str(contador) + ": '" + palabra + "' no está declarado.")
                else: # Dado que la palabra si está en la tabla hash se procede
                    variable = self.hashGlobal.get(palabra) # Se obtiene la palabra de la tabla
                    if self.pila: # Se verifica que exista una pila para realizar validaciones
                        if self.pila[-1] in self.especiales:
                            if self.pila[-2].tipo != variable.tipo: # Verifica que la operación sea posible en caso contrario no lo hará
                                self.pila.pop()
                                self.pila.pop()
                                print("Error - Linea " + str(contador) + ": Operación con tipos distintos")
                            else:
                                self.pila.pop()
                                self.pila.pop()
                        if palabra == "0":
                            if pila[-1] == '/':
                                print("Error - Linea " + str(contador) + ": División entre 0.") # Error en caso de división entre 0


            contador += 1


analizador = AnalizadorSemantico()
analizador.leyendoCodigo("correcto.txt")

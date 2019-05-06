# Lenguajes de programacion
# Juan Manuel Alvarez Duque
# Nicolas Campuzano Angulo
# Taller 1 Analizador lexico para lenguaje SL 
# 5/6/2019
# Se requiere un archivo "./test.txt" para su funcionamiento.

import sys

keywords = [
  "and", "constantes", "hasta", "matriz", "paso", "registro", "sino", "vector", "archivo",
  "desde", "inicio", "mientras", "subrutina", "repetir", "tipos", "caso", "eval", "lib",
  "not", "programa", "retorna", "var", "const", "fin", "libext", "or", "ref", "si", "variables",
  "numerico", "cadena", "logico",
  
  "dim", "imprimir", "cls", "leer", "set_ifs", "abs", "arctan", "ascii", "cos", "dec",
  "eof", "exp", "get_ifs", "inc", "int", "log", "lower", "mem", "ord", "paramval",
  "pcount", "pos", "random", "sec", "set_stdin", "set_stdout", "sin", "sqrt",
  "str", "strdup", "strlen", "substr", "tan", "upper", "val",

]
column = 0
row = 0
startingTokenColumn = 0
startingTokenRow = 0
allTokens = []
lines = None
word = ""
throwError = False
errorCol = 0
errorRow = 0
escape = False

class Token:
    ttk = -1
    l = -1
    c = -1
    lexema = ""
    def __init__ (self, _ttk,_c,_l,_lexema = None):
        self.ttk = _ttk
        self.l = _l
        self.c = _c
        self.lexema = _lexema

    def __str__(self):
        if self.lexema == None:
            return (str("<" + str(self.ttk) + "," + str(self.l) + "," + str(self.c) +  ">"))        
        else:
            return (str("<"+ str(self.ttk) + ","+str(self.lexema)+ "," + str(self.l) + "," + str(self.c) + ">"))
          

def skipToNextLine():
    global column, row
    column = -1 ##Tiene que ser -1 para que la siguiente llamada lo haga 0 (TENER CUIDADO)
    row += 1

def isAlphaOrUnderscoreOrNi(stringToCheck):
    return stringToCheck.isalpha() or stringToCheck == "_" or stringToCheck == "ñ" or stringToCheck == "Ñ"

def isAlnumOrUnderscoreOrNi(stringToCheck):
    ##TODO: no permitir caracteres acentuados
    ## áéíóú deberian dar falso
    return stringToCheck.isalnum() or stringToCheck == "_" or stringToCheck == "ñ" or stringToCheck == "Ñ"


def obtenerCaracterSiguiente():
    global column, row, lines
    if not lines:
        with open("test.txt","r", encoding="utf-8") as f:
            lines = f.readlines()
            return lines[0][0]
    column += 1
    if len(lines[row]) <= column:
        column = 0
        row += 1
        if len(lines) <= row:
            return None
    return lines[row][column]

def noAvanzar():
    global column, row,lines
    if(column == 0):
        row = row - 1
        column = len(lines[row])-1
    else:
        column = column-1
        
def main():
    global allTokens, throwError, errorCol, errorRow
    c = obtenerCaracterSiguiente()
    estado = 0
    while (estado != -1):
        estado = delta(estado,c)
        if(c == None):
            break
        c = obtenerCaracterSiguiente()
    print(*allTokens, sep = "\n")
    if(throwError):
        print(">>> Error lexico(linea:"+str(errorRow+1)+",posicion:"+str(errorCol+1)+")")
           
def delta(estadoActual, caracterLeido):
    global allTokens, column, row, escape, startingTokenColumn, startingTokenRow, word, throwError, errorCol, errorRow
    
    if(estadoActual == 0): ##Ningun Token actualmente en lectura
        startingTokenColumn = column
        startingTokenRow = row
        if(caracterLeido == None):
            return -1
        elif(caracterLeido == "/"):
            return 1
        elif(caracterLeido == "\\"):
            return 3
        
        ##3 maneras de hacer una cadena
        elif(caracterLeido == "\""): 
            word = "\""
            return 4
        elif(caracterLeido == "'"): 
            word = "'"
            return 5
        elif(caracterLeido == "“"):
            word = "“"
            return 6
        ##
        #numeros
        elif(caracterLeido.isdecimal()):
            word = caracterLeido
            return 7
        ##ids y palabras reservadas
        
        elif(isAlphaOrUnderscoreOrNi(caracterLeido)):
            word = caracterLeido
            return 9

        elif(caracterLeido == "<"):
            word = caracterLeido
            return 10
        elif(caracterLeido == ">"):
            word = caracterLeido
            return 11

        elif(caracterLeido == "="):
            word = caracterLeido
            return 12
        
        ##Triviales
        ##TODO: Estos dos primeros no son realmente triviales, 5+3 son 3 tokens, +3 es un token
        elif(caracterLeido == "+"):
            allTokens.append(Token("tk_suma",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "-"):
            allTokens.append(Token("tk_resta",startingTokenColumn+1,startingTokenRow+1))
            return 0
        ##
        elif(caracterLeido == "*"):
            allTokens.append(Token("tk_mult",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "^"):
            allTokens.append(Token("tk_exp",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "%"):
            allTokens.append(Token("tk_mod",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "{"):
            allTokens.append(Token("tk_llave_izq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "}"):
            allTokens.append(Token("tk_llave_der",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "("):
            allTokens.append(Token("tk_par_izq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ")"):
            allTokens.append(Token("tk_par_der",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "["):
            allTokens.append(Token("tk_brac_izq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "]"):
            allTokens.append(Token("tk_brac_der",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ":"):
            allTokens.append(Token("tk_dospuntos",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ";"):
            allTokens.append(Token("tk_pyq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ","):
            allTokens.append(Token("tk_coma",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "."):
            allTokens.append(Token("tk_punto",startingTokenColumn+1,startingTokenRow+1))
            return 0
        ##End Triviales

        elif(caracterLeido == " " or caracterLeido == "\n" or caracterLeido == "\t"):
            return 0
        else:
            # print(caracterLeido)
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        
    if(estadoActual == 1): #El anterior fue un /
        if(caracterLeido == "/"): # //
            skipToNextLine()
            return 0
        elif(caracterLeido == "*"): # /*
            return 2
        else: # / (division)
            noAvanzar() ##Tuvimos que leer un caracter de mas para saber que era este, nos "regresamos" 1 caracter
            allTokens.append(Token("tk_division",startingTokenColumn+1,startingTokenRow+1))
            return 0
            
    if(estadoActual == 2): #Anteriores fueron /*
        if(caracterLeido == "*"):
            return 3
        else: return 2
        
    if(estadoActual == 3): #Anteriores /* y *
        if(caracterLeido == "/"):
            return 0
        else:
            return 2 ##Si el * no estaba seguido de /
        
    if(estadoActual == 4): #Inicio de Cadena Anterior "
        if(caracterLeido == None):
          throwError = True
          errorCol = startingTokenColumn
          errorRow = startingTokenRow
          return -1
        if(caracterLeido == "\"" and not escape):#Fin de cadena "
            word = word + "\""
            allTokens.append(Token("tk_cadena",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido == "\\" ):
            escape = True
            word = word + caracterLeido
            return 4
        else: #Continuacion de cadena
            escape = False
            word = word + caracterLeido
            return 4
        
    if(estadoActual == 5): #Inicio de Cadena Anterior '
        if(caracterLeido == None):
          throwError = True
          errorCol = startingTokenColumn
          errorRow = startingTokenRow
          return -1
        if(caracterLeido == "'" and not escape):#Fin de cadena '
            word = word + "'"
            allTokens.append(Token("tk_cadena",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido == "\\" ):
            escape = True
            word = word + caracterLeido
            return 5
        else: #Continuacion de cadena
            escape = False
            word = word + caracterLeido
            return 5
        
    if(estadoActual == 6): #Inicio de Cadena Anterior “
        if(caracterLeido == None):
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        if(caracterLeido == "”" and not escape):#Fin de cadena ”
            word = word + "”"
            allTokens.append(Token("tk_cadena",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido == "\\" ):
            escape = True
            word = word + caracterLeido
            return 6
        else: #Continuacion de cadena
            escape = False
            word = word + caracterLeido
            return 6
        
    if(estadoActual == 7): # Inicio de Numero
        if(caracterLeido == None):
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        elif(caracterLeido.isdecimal()):
            word = word + caracterLeido
            return 7
        elif(caracterLeido == "."): #Numero Decimal
            return 8
        elif(caracterLeido == 'e' or caracterLeido == 'E'):
            word = word + caracterLeido
            return 14
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
            
    if(estadoActual == 8):# Inicio numero con punto decimal
        if(caracterLeido == None):
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            allTokens.append(Token("tk_punto",column+1,row+1))
            return 0
        elif(caracterLeido.isdecimal()):
            word = word + "."
            word = word + caracterLeido
            return 13
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            allTokens.append(Token("tk_punto",column+1,row+1))
            return 0
        
    if(estadoActual == 9): # Inicio identificador o palabra reservada
        if(caracterLeido == None):
            if word in keywords:
                allTokens.append(Token(word,startingTokenColumn+1,startingTokenRow+1))
                return 0
            else:
                allTokens.append(Token("id",startingTokenColumn+1,startingTokenRow+1, word))
                return 0
        if(len(word) > 32):
            noAvanzar()
            allTokens.append(Token("id",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(isAlnumOrUnderscoreOrNi(caracterLeido)):
            word = word + caracterLeido
            return 9
        else:
            noAvanzar()
            if word in keywords:
                allTokens.append(Token(word,startingTokenColumn+1,startingTokenRow+1))
                return 0
            else:
                allTokens.append(Token("id",startingTokenColumn+1,startingTokenRow+1, word))
                return 0
            
    if(estadoActual == 10): #Anterior fue <
        if(caracterLeido == ">"):
            allTokens.append(Token("tk_distinto",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "="):
            allTokens.append(Token("tk_menorigual",startingTokenColumn+1,startingTokenRow+1))
            return 0
        else:
            noAvanzar()
            allTokens.append(Token("tk_menor",startingTokenColumn+1,startingTokenRow+1))
            return 0
        
    if(estadoActual == 11): #Anterior fue <
        if(caracterLeido == "="):
            allTokens.append(Token("tk_mayorigual",startingTokenColumn+1,startingTokenRow+1))
            return 0
        else:
            noAvanzar()
            allTokens.append(Token("tk_mayor",startingTokenColumn+1,startingTokenRow+1))
            return 0
    if(estadoActual == 12):
        if(caracterLeido == "="):
            allTokens.append(Token("tk_igualdad",startingTokenColumn+1,startingTokenRow+1))
            return 0
        else:
            noAvanzar()
            allTokens.append(Token("tk_asig",startingTokenColumn+1,startingTokenRow+1))
            return 0
        
    if(estadoActual == 13):# Continuacion numero con punto decimal
        if(caracterLeido == None):
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido.isdecimal()):
            word = word+caracterLeido
            return 13
        elif(caracterLeido == 'e' or caracterLeido == 'E'):
            word = word + caracterLeido
            return 14
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
    if(estadoActual == 14): #Notacion cientifica
      if(caracterLeido == None):
        throwError = True
        errorCol = startingTokenColumn
        errorRow = startingTokenRow
        return -1
      if(caracterLeido == '+' or caracterLeido == '-'):
            word = word + caracterLeido
            return 14
      elif(caracterLeido.isdecimal()):
            word = word+caracterLeido
            return 15
      throwError = True
      errorCol = startingTokenColumn
      errorRow = startingTokenRow
      return -1
    if(estadoActual == 15): # Despues del e+/-num
        if(caracterLeido == None):
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido.isdecimal()):
            word = word + caracterLeido
            return 15
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0

if __name__ == "__main__":  
    main()
            
            


    
        

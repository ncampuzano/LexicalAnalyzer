keywords = [
  "and", "constantes", "hasta", "matriz", "paso", "registro", "sino", "vector", "archivo",
  "desde", "inicio", "mientras", "subrutina", "repetir", "tipos", "caso", "eval", "lib",
  "not", "programa", "retorna", "var", "const", "fin", "libext", "or", "ref", "si", "variables",
  
  "dim", "imprimir", "cls", "leer", "set_ifs", "abs", "arctan", "ascii", "cos", "dec",
  "eof", "exp", "get_ifs", "inc", "int", "log", "lower", "mem", "ord", "paramval",
  "pcount", "pos", "random", "sec", "set_stdin", "set_stdout", "sin", "sqrt",
  "str", "strdup", "strlen", "substr", "tan", "upper", "val",

  
]

def main():
  with open("test.txt", "r") as f:
    lines = f.readlines()
  column = 0
  row = 0
  for line in lines:
    row += 1
    column = 0
    word = ""
    for letter in line:
      column += 1
      if isAlnumOrUnderscore(letter):
        word += letter
      else: 
        if word in keywords:
          print("<" + word + "," + str(row) + "," + str(column - len(word))  + ">")
        elif word:
          print("<id," + word + "," + str(row) + "," + str(column - len(word))  + ">")
        word = ""

def isAlnumOrUnderscore(stringToCheck):
  return stringToCheck.isalnum() or stringToCheck == "_"

if __name__ == "__main__":  
  main()

keywords = [
  "and", "constantes", "hasta", "matriz", "paso", "registro", "sino", "vector", "archivo",
  "desde", "inicio", "mientras", "subrutina", "repetir", "tipos", "caso", "eval", "lib",
  "not", "programa", "retorna", "var", "const", "fin", "libext", "or", "ref", "si", "variables"
]

def isLetter(letter):
  return (letter >= 65 and letter <= 90) or (letter >= 97 and letter <= 122)

def main():
  f = open("test.txt", "r")
  lines = f.readlines()
  column = 0
  row = 0
  for line in lines:
    row += 1
    column = 0
    word = ""
    for letter in line:
      column += 1
      if letter.isspace(): # If there is a space character
        if word in keywords and isReserved:
          print("<" + word + "," + str(row) + "," + str(column - len(word))  + ">")
        isReserved = True
        word = ""
      elif letter.isalpha():
        word += letter
      else:
        isReserved = False
if __name__ == "__main__":  
  main()
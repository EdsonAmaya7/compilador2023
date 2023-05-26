from tokenize import Token
import pandas as pd #libreria para hacer dataframes de la matriz estados y tabla sintactica

# producciones de mi gramatica
producciones = {
                1:["DECLARACIONVARIABLES", "MAIN", "DECLARACIONFUNCIONES"],
                2:["{", "VARIABLES", "}"],
                3:["TIPO", "LISTAVARIABLES", ";", "VARIABLES"], 4:["ε"],
                5:["identificador", "LISTAVARIABLESPRIMA"], 6:[";", "LISTAVARIABLES"], 7:["ε"], 8:["main", "-", ">", "BLOQUE"], 9:["integer"],
                10:["string"], 11:["boolean"],
                12:["list"], 13:["DECLARAFUNCION", "DECLARACIONFUNCIONES"], 14:["ε"],
                15:["TIPO", "identificador", "PARAMETROS", "BLOQUE", "RETURN", "DECLARAFUNCION"], 16:["ε"], 17:["{", "INSTRUCCIONES", "}"],
                18:["(", "LISTAPARAMETROS", ")"], 19:["identificador", "LISTAPARAMETROSPRIMA"],
                20:["ε"], 21:[",", "LISTAPARAMETROS"], 22:["ε"],
                23:["return", "LISTARETURN"], 24:["identificador", "LISTARETURNPRIMA"],
                25:["LISTARETURN"], 
                26:["ε"],
                27:["INSTRUCCION", "INSTRUCCIONES"],
                28:["ε"],
                29:["identificador", ":=>", "LLAMADAFUNCION"], 30:["identificador" ,":=>", "EXPARITM"],
                31:["while", "BOOLEXP", "BLOQUE"],
                32:["do", "BLOQUE", "cycle", "BOOLEXP"], 33:["repeat", "BLOQUE", "condition", "BOOLEXP"],
                34:["if", "BOOLEXP", "BLOQUE", "ELSEIF", "ELSE"], 35:["for", "identificador", "int", "RANGO", "BLOQUE"],
                36:["print", "(", "VARIABLESIMPRIMIR", ")"], 37:["call", "identificador", "(", "LISTAPARAMETROS", ")"], 38:["FUNCION_BUILT_IN"],
                39:["lengthiness", "(", "identificador", ")"],
                40:["isinteger", "(", "identificador", ")"],
                41:["isreal", "(", "identificador", ")"],
                42:["convertintger", "(", "identificador", ")"],
                43:["convertfloat", "(", "identificador", ")"], 44:["read", "(", ")"],
                45:["getabs", "(", "EXPARITM", ")"], 46:["getstr", "(", "EXPARITM", ")"], 47:["power", "(", "EXPARITM", ")"],
                48:["round","(", "EXPARITM", ")"], 49:["getsum", "(", "identificador", ")"], 
                50:["getmin", "(", "identificador", ")"],
                51:["getmax", "(", "identificador", ")"], 52:["identificador", "VARIABLESPRIMA"],
                53:["texto", "VARIABLESPRIMA"],
                54:[",", "VARIABLESIMPRIMIR"],
                55:["ε"], 56:["otherif", "BOOLEXP", "BLOQUE", "ELSEIF"], 57:["ε"], 58:["ε"], 59:["other", "BLOQUE"], 60:["range", "(", "VALOR1", ")"], 61:["EXPARITM", "VALOR2"],
                62:["ε"], 63:[";", "EXPARITM", "VALOR3"],
                64:["ε"], 65:[";", "EXPARITM"],
                66:["BOOLTERM", "BOOLEXP_PRIMA"], 67:["||", "BOOLTERM", "BOOLEXP_PRIMA"],
                68:["ε"], 69:["BOOLFACTOR", "BOOLTERM_PRIMA"],
                70:["&%&", "BOOLFACTOR", "BOOLTERM_PRIMA"], 71:["ε"],
                72:["~", "BOOLFACTOR"],
                73:["(", "RELTERM", "RELTERMP", ")"],
                74:["RELTERM", "RELTERM"],
                75:["OPERADOR", "RELTERM"],
                76:["ε"],
                77:["EXPARITM"],
                78:["TERMINO", "EXPPRIMA"],
                79:[":+", "TERMINO", "EXPPRIMA"],
                80:[":-", "TERMINO", "EXPPRIMA"],
                81:["ε"],
                82:["FACTOR", "TERMPRIMO"],
                83:[":*", "FACTOR", "TERMPRIMO"],
                84:[":/", "FACTOR", "TERMPRIMO"],
                85:["ε"],
                86:["identificador"],
                87:["numero"],
                88:["<:"],
                89:[":>"],
                90:["<:="],
                91:[":>="],
                92:["=:="],
                93:["!:="]
                }

# Diccionario de simbolos NO TERMINALES para acceder a la columna de la tabla sintactica
NT = { 
      "P":0, 
      "DECLARACIONVARIABLES":1, 
      "VARIABLES":2, 
      "LISTAVARIABLES":3, 
      "LISTAVARIABLESPRIMA":4, 
      "MAIN":5, 
      "TIPO":6, 
      "DECLARACIONFUNCIONES":7, 
      "DECLARAFUNCION":8, 
      "BLOQUE":9, 
      "PARAMETROS":10,
      "LISTAPARAMETROS":11,
      "LISTAPARAMETROSPRIMA":12,
      "RETURN":13,
      "LISTARETURN":14,
      "LISTARETURNPRIMA":15,
      "INSTRUCCIONES":16,
      "INSTRUCCION":17,
      "LLAMADAFUNCION":18,
      "FUNCION_BUILT_IN":19,
      "VARIABLESIMPRIMIR":20,
      "VARIABLEPRIMA":21,
      "ELSEIF":22,
      "ELSE":23,
      "RANGO":24,
      "VALOR1":25,
      "VALOR2":26,
      "VALOR3":27,
      "BOOLEXP":28,
      "BOOLEXP_PRIMA":29,
      "BOOLTERM":30,
      "BOOLTERM_PRIMA":31,
      "BOOLFACTOR":32,
      "RELTERMP":33,
      "RELTERM":34,
      "EXPARITM":35,
      "EXPRIMA":36,
      "TERMINO":37,
      "TERMPRIMO":38,
      "FACTOR":39,
      "OPERADOR":40,
      
      }

'''Errors = {
          -1:"Se esperaba ---> begin", #P
          -2:"Se esperaba ---> { = if for while repeat cases print read end $", #VARIABLES
          -3:"Se esperaba ---> } identificador", #DECLARACION 
          -4:"Se esperaba ---> integer real string bolean list", #TIPO
          -5:"Se esperaba ---> identificador", #LISTA
          -6:"Se esperaba ---> , :", #LISTAPRIMA
          -7:"Se esperaba ---> , : =", #EXTRA
          -8:"Se esperaba ---> [ numero", #NUMERO_LISTA_NUMEROS
          -9:"Se esperaba ---> [", #LISTA_NUMEROS
          -10:"Se esperaba ---> numero", #NUMEROS
          -11:"Se esperaba ---> , : ]", #LISTANUMERO
          -12:"Se esperaba ---> } =  if for while repeat cases print read break end", #ESTATUTOS
          -13:"Se esperaba ---> = if for while repeat cases print read break do", #ESTATUTO
          -14:"Se esperaba ---> else", #ELSE
          -15:"Se esperaba ---> [ ( identificador numero ", #ESTATUTO1
          -16:"Se esperaba ---> [ identificador", #ESTATUTO2
          -17:"Se esperaba ---> identificador", #INCREDECRE
          -18:"Se esperaba ---> [ identificador", #LISTAORANGO
          -19:"Se esperaba ---> [", #LISTAVALORES
          -20:"Se esperaba ---> identificador numero", #LISTA_VALORES
          -21:"Se esperaba ---> identificador numero", #IDENTIFICADOROVALOR
          -22:"Se esperaba ---> , ]", #LISTAVALORESPRIMA
          -23:"Se esperaba ---> ++ --", #SIGNO
          -24:"Se esperaba ---> } case", #LISTACASES
          -25:"Se esperaba ---> ( ~! identificador numero", #CONDICION
          -26:"Se esperaba ---> <= >= > < || &&", #OPERADOR
          -27:"Se esperaba ---> ( identificador numero", #EXPRESION
          -28:"Se esperaba ---> ; ) . = + - <= >= > < || && identificador numero", #EXPPRIMA
          -29:"Se esperaba ---> ( identificador numero", #TERMINO
          -30:"Se esperaba ---> ; ) . = + - <= >= > < || && * / identificador numero", #TERMPRIMO
          -31:"Se esperaba ---> ( identificador numero", #FACTOR
          -32:"Se esperaba ---> =" #ASIGNACION
          }'''

stack = ["$", "P"] #iniciio mi stack_sintactico
tabla_tokens = []
tokens = []

tokens_reservadas = {"identificador":300, "main":301, "integer":302, "string":303, "boolean":304, "list":305,
                     "return":306, "while":307, "do":308, "cycle":309, "repeat":310, "condiction":311, "if":312,
                     "for":313, "in":314, "print":315, "call":316, "lengthiness":317, "isinteger":318, "isreal":319,
                     "convertfloat":320,"read":321,"getsum":322,"getmin":323,"getmax":324,"texto":325,"otherif":326,
                     "other":327,"range":328}

tabla_identificadores = []


archivo = open("archivo_mido.txt", "r") # para leer el archivo del programa fuente

matriz = pd.read_excel("MatrizSintactica.xlsx") # data_frame de la matriz de estados

#reccorro cada linea del archvio fuente
texto = ""
for linea in archivo.readlines():
    texto += linea

texto = texto.replace("\n", "")


#estados finales del automata
estados_finales = { - 1: "reconoce {", -2: "reconoce }", -3:"punto y coma ;", -4:'reconoce -->',
                   -5: 'parentesis abierto ( ', -6:'parentesis cierra )', -7:'coma , ', -8:'reconoce :=>', -9:'reconoce :+',
                   -10: 'reconoce :-', -11: 'reconoce :/', -12:'reconoce :*', -13:'reconoce :>=',
                   -14: 'reconoce :>', -15:'reconoce ||', -16:'reconoce &%&', -17:'reconoce ~', -18:'reconoce <:=',
                   -19:'reconoce <:', -20: 'reconoce =:=', -21:'reconoce !:=', -22: 'reconoce identificador', -23: 'reconoce numero enteero',
                   -24: 'reconoce numero con punto decimal', -25:'reconoce numero decimal con notacion cientifica',
                   -26: 'reconoce numero entero con punto decimal', -27:'reconoce texto comilla simple', -28: 'reconoce comillas dobles',
                   -29: 'reconoce comentarios', -30: 'reconoce comentario bloquee', 100: 'reconoce error'}

reservadas = ["identificador", "main", "integer", "string", "boolean", "list",
                     "return", "while", "do", "cycle", "repeat", "condiction", "if",
                     "for", "in", "print", "call", "lengthiness", "isinteger", "isreal",
                     "convertfloat","read","getsum","getmin","getmax","texto","otherif",
                     "other","range"]
##qu
stack_lex = []

caracter = 0 # indice del caracter en el texto
fila = 0
estado = 0
contenido = [] # lista aux para comparar identificador y palabra reservada ó número
num_texto = 0

indice = 0
while caracter < len(texto):
    # se accede a la matriz con la fila y el caracter, caso especial la letra e
    if(texto[caracter] == " "):
        estado = matriz.loc[fila, "espacio"]
    else:
        estado = matriz.loc[fila, "digito" if texto[caracter].isdigit() else "letra" if texto[caracter].isalpha() else texto[caracter]]
    
    if estado in estados_finales: # verifica si ha llegado a un estado final
        if estado == -22: #se llego al estado de identificadores, ahora comprueba si es una pal_reservada
            if "".join(contenido) in reservadas:
                print("Reconoce palabra reservada", f"'{''.join(contenido)}'")
                tabla_tokens.append({"Tipo":"Palabra reservada", "Token":f"{''.join(contenido)}", "Número":tokens_reservadas[f"{''.join(contenido)}"]})
                estado = fila = 0
                caracter -= 1
                contenido = []
            else:
                print(estados_finales[estado], f"{''.join(contenido)}")
                indice += 1
                tabla_identificadores.append({"Indice": indice, "Identificador":f"{''.join(contenido)}", "Tipo-Dato":None, "Valor": None})
                tabla_tokens.append({"Tipo":"Identificador", "Token":f"{''.join(contenido)}", "Número":indice})
                caracter -= 1
                estado = fila = 0
                contenido = []

        elif ((estado == -23) or (estado == -24) or (estado == -25) or (estado == -26)): # este estado reconoce los números
            if "." not in f"{''.join(contenido)}" and "e" not in f"{''.join(contenido)}":
                print("Número Entero", f"{''.join(contenido)}#")
                estado = fila = 0
                contenido = []
            if "." in f"{''.join(contenido)}" and "e" not in f"{''.join(contenido)}":
                print("Decimal", f"{''.join(contenido)}#")
                estado = fila = 0
                contenido = []
            if "e" in f"{''.join(contenido)}" and "." not in f"{''.join(contenido)}":
                print("Número con notación", f"{''.join(contenido)}#")
                estado = fila =0
                contenido = []
            if "." in f"{''.join(contenido)}" and "e" in f"{''.join(contenido)}":
                print("Decimal con notacion", f"{''.join(contenido)}#")
                estado = fila = 0
                contenido = []
        else:
            print(estados_finales[estado])
            estado = fila = 0
            if(contenido == "<:"):
                caracter -= 1
            contenido = []
    else:
        fila = estado
        if texto[caracter] != " ":
            contenido.append(texto[caracter])
    caracter += 1

# for token in tabla_tokens:
#     print(token)

tb_tok = pd.DataFrame(tokens, columns = ["Tipo", "Token", "Token_númerico"]) # mi tabla de tokens

print(tb_tok)



# for identificador in tabla_identificadores:
#     print(identificador)


df = pd.read_excel("MatrizSintactica.xlsx") # leemos la tabla sintactica con la libreria de pandas
stack_lex = stack_lex[::-1]
comparacion = list(tb_tok["Token"][::-1])

# ciclo while para comprobar los topes de los stack y hacer el pop y push hasta que queden vacias
while len(stack_lex) != 0:
    
    print(f"Stack_lexico:{stack}")
    print(f"Entrada: {comparacion}")
    
    if stack[-1] != stack_lex[-1]: #Compara el tope del stack lexico y el de la entrada
        pro = df.loc[NT[stack.pop()], stack_lex[-1]] #accede a la matriz para saber que produccion debe de aplicar
        print(f"Se aplica la produccion: {pro}") if pro >= 1 else print("\n.")
        
        #if pro <= -1:
            #print(Errors[pro]) # te indica que es lo que esperaba
            #break
    else:
            
        for i in producciones[pro][::-1]: #hace los push en el stack_lexico
            stack.append(i) #push de la lista de la producciones 
    
    if len(stack_lex) == 1:
        break
    
    if stack[-1] == stack_lex[-1]: #si los topes son iguales hace el pop en ambos stacks
        stack.pop()
        comparacion.pop()
        stack_lex.pop()
    
    if stack[-1] == "ε": #si se encuentra epsilon hace el pop
        stack.pop()
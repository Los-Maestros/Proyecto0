#%%
# Buenas tardes :D

# -------------------
# Variables
# -------------------

funciones = {}

variables = {}

caracteres = ['{', '}', '(', ')', ';', ',']

c_simple = {'jump':[[2],[]], 
    'walk':[[1,2],['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']], 
    'leap':[[1,2],['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']], 
    'turn':[[1],['left', 'right', 'around']], 
    'turnto':[[1],['north', 'south', 'west', 'east']], 
    'drop':[[1],[]], 
    'get':[[1],[]], 
    'grab':[[1],[]], 
    'letGo':[[1],[]], 
    'nop':[[0],None]}

cond_def = {
    'facing' : ['north', 'south', 'west', 'east'],
    'can' : list(c_simple.keys()),
    'not' : ['facing', 'can', 'not']
    }


# -------------------
# CARGA DE DATOS
# -------------------

def lector(file):
    archivo = open(file, 'r')
    texto = archivo.read().replace('\n',' ')
    lista = lector2(texto)
    return lista

def lector2(texto):
    respuesta = []
    palabra = ''
    cont = 0
    
    for letra in texto:
        if letra not in caracteres and letra != ' ':
            palabra += letra
        
        else:
            if palabra:
                respuesta.append(palabra)
            if letra in caracteres:
                respuesta.append(letra)
            palabra = '' 
            
        #? Se verifica si los parentesis se cierran
        if letra == '{' or letra == '(':
            cont += 1
        if letra == '}' or letra == ')':
            cont -= 1  
            
    assert not cont, 'Hay parentesis que no se cierran'
    return respuesta

# ------------------
# VERIFICADORES
# ------------------

def complemeto_llave(archivo):
    cont = 0
    for i,j in enumerate(archivo):
        if j == '{':
            cont += 1
        elif j == '}':
            if not cont:
                return i
            cont -= 1

def parametros(lista, nombre):
    char = lista.pop(0)
    comas = 0
    while char != ')':
        if char != ',':
            comas +=1
            assert char not in caracteres, f'Función {nombre} con parametros {char}' #? Se verifica que no sea un caracter especial la variable
            
            if nombre not in funciones:
                funciones[nombre] = []
            funciones[nombre].append(char)
        char = lista.pop(0)   
        comas -= 1 
    assert not comas, f'Función {nombre} con malos parametros'
    return lista
         
def cont_parametros(texto):
    cont = 0
    pos = 2
    while texto[pos] != ')':
        if  texto[pos] != ',':
            cont += 1
        pos += 1
    return cont

# diccionarios con las variables y funciones construidas por el usuario
variables_parametro = {}
funciones_parametro = {}

def construir_parametros(lista):
    r = []
    c = 0
    while lista[c] != ')':
        if lista[c] != ',':
            r.append(lista[c])
        c += 1
    return r,c

def analizar_bloque(bloque_completo, funcion, status):
    error = ''
    # analiza un bloque de codigo
    p_final = complemeto_llave(bloque_completo)
    bloque = bloque_completo[:p_final]
    while len(bloque) > 1 and status:
        if bloque[0] in c_simple.keys():
            bloque, status, error = analizar_c_simple(bloque, status, error, funciones_parametro, funcion)                        
        elif bloque[0] == 'if':
            bloque, status, error = analizar_if(bloque, status, error, funciones_parametro, funcion)
        elif bloque[0] == 'while':
            bloque, status, error = analizar_while(bloque, status, error, funciones_parametro, funcion)
        elif bloque[0] == 'repeat':
            bloque, status, error = analizar_repeat(bloque, status, error, funciones_parametro, funcion)
        elif bloque[0] in funciones_parametro.keys():
            bloque, status, error = analizar_funcion_parametro(bloque, status, error, funciones_parametro)
        else:
            error = 'Funcion en bloque no encontrada'
            status = False
        if len(bloque)>1:
            if bloque[0] == ';' and bloque[1] == '}':
                error = 'Bloque ',funcion,' mal construido'
                status = False
            else:
                bloque = bloque[1:]
        else:
            bloque = bloque[1:]
    if status:
        bloque_final = bloque_completo[p_final+1:]
    return bloque_final, status, error
    
def analizar_c_simple(bloque, status, error, funciones_parametro, funcion):
    # analizar una funcion simple
    error = ''
    if (bloque[0] == 'nop') and (bloque[1] ==  '(') and bloque[2] ==  ')':
        bloque = bloque[3:]
    else:
        num_parameters = c_simple[bloque[0]][0]
        parametros, pf = construir_parametros(bloque[2:])
        if len(parametros) not in num_parameters:
            error = 'Funcion ',funcion,' con extra/menos parametros'
            status = False
        else:
            if len(parametros) == 1:
                if bloque[0] == 'turn' or bloque[0] == 'turnto':
                    if parametros[0] not in (c_simple[bloque[0]][1]):
                        error = 'Parametro ',parametros,' en la funcion ', bloque[0], ' no valido'
                        status = False
                else:
                    if parametros[0] not in funciones_parametro[funcion] and parametros[0] not in variables_parametro.keys() and not(parametros[0].isdigit()):
                        error = 'Parametro ',parametros,' en la funcion ', bloque[0], ' no valido'
                        status = False
            elif funcion == 'jump':
                if parametros[0] not in funciones_parametro[funcion] and not(parametros[0].isdigit()):
                    error = 'Parametros ',parametros,' en la funcion ', bloque[0], ' no valido'
                    status = False
                elif parametros[1] not in funciones_parametro[funcion] and not(parametros[1].isdigit()):
                    error = 'Parametros ',parametros,' en la funcion ', bloque[0], ' no valido'
                    status = False
            elif funcion == 'walk' or funcion == 'leap':
                if parametros[0] not in funciones_parametro[funcion] and parametros[0] not in variables_parametro.keys() and not(parametros[0].isdigit()):
                    error = 'Parametros ',parametros,' en la funcion ', bloque[0], ' no valido'
                    status = False
                elif parametros[1] not in (c_simple[bloque[0]][1]):
                    error = 'Parametros ',parametros,' en la funcion ', bloque[0], ' no valido'
                    status = False
        if status:
            bloque = bloque[3+pf:]
    return bloque, status, error

def analizar_if(bloque, status, error, funciones_parametro, funcion):
    # loop IF
    error = ''
    if bloque[1] in cond_def.keys():
        if bloque[1] == 'not':
            if not(bloque[2] == '(' and bloque[3] in cond_def.keys()):
                error = 'Parametro de condicion ',bloque[3],' no valido'
                status = False
            else:
                bloque = bloque[2:]
        if bloque[1] == 'facing':
            if not(bloque[2] == '(' and bloque[4] == ')' and bloque[3] in cond_def[bloque[1]]):
                error = 'Parametro de condicion ',bloque[3],' no valido'
                status = False
            else:
                bloque = bloque[5:]
        elif bloque[1] == 'can':
            if not(bloque[2] == '(' and bloque[3] in c_simple.keys()):
                error = 'Parametro de condicion ',bloque[3],' no valido'
                status = False
            else:
                bloque = bloque[3:]
                bloque, status, error = analizar_c_simple(bloque, status, error, funciones_parametro, funcion)
        if bloque[1] == '{':
            bloque = bloque[2:]
            bloque, status, error = analizar_bloque(bloque, status, funcion)
        else:
            error = 'Sintaxis no valida'
            status = False
    else:
        error = 'Condicion ',bloque[1],' no valida'
        status = False
    if bloque[0] == 'else':
        bloque = bloque[1:]
        bloque, status, error = analizar_bloque(bloque, status, funcion)
    else:
        error = 'Sintaxis no valida'
        status = False
    return bloque, status, error

def analizar_while(bloque, status, error, funciones_parametro, funcion):
    # loop WHILE
    error = ''
    if bloque[1] in cond_def.keys():
        if bloque[1] == 'not':
            if not(bloque[2] == '(' and bloque[3] in cond_def.keys()):
                error = 'Parametro de condicion ',bloque[3],' no valido'
                status = False
            else:
                bloque = bloque[2:]
        if bloque[1] == 'facing':
            if not(bloque[2] == '(' and bloque[4] == ')' and bloque[3] in cond_def[bloque[1]]):
                error = 'Parametro de condicion ',bloque[3],' no valido'
                status = False
            else:
                bloque = bloque[5:]
        elif bloque[1] == 'can':
            if not(bloque[2] == '(' and bloque[3] in c_simple.keys()):
                error = 'Parametro de condicion ',bloque[3],' no valido'
                status = False
            else:
                bloque = bloque[3:]
                bloque, status, error = analizar_c_simple(bloque, status, error, funciones_parametro, funcion)
        if bloque[1] == '{':
            bloque = bloque[2:]
            # hasta aca todo iba bien
            print(bloque,'bloque en while')
            bloque, status, error = analizar_bloque(bloque, status, funcion)
        else:
            error = 'Sintaxis no valida'
            status = False
    return bloque, status, error

def analizar_repeat(bloque, status, error, funciones_parametro, funcion):
    # loop REPEAT
    error = ''
    if bloque[1] not in funciones_parametro[funcion] and bloque[1] not in variables_parametro.keys() and not(parametros[0].isdigit()):
        error = 'Parametro ',bloque[1],' en la funcion ', bloque[0], ' no valido'
        status = False
    else:
        if bloque[2] == 'times':
            bloque = bloque[4:]
            bloque, status, error = analizar_bloque(bloque, status, funcion)
        else:
            error = 'Sintaxis no valida'
            status = False
    return bloque, status, error

def analizar_funcion_parametro(bloque, status, error, funciones_parametro):
    error = ''
    num_parameters = funciones_parametro[bloque[0]]
    parametros, pf = construir_parametros(bloque[2:])
    if len(parametros) == num_parameters:
        error = 'Funcion ',bloque[0],' con extra/menos parametros'
        status = False
    else:
        varfunc = bloque[0]
        for i in parametros:
            if i not in variables_parametro.keys() and not(i.isdigit()) and (i+varfunc) not in variables_parametro.keys():
                error = 'Parametro ',i,' en la funcion ', bloque[0], ' no valido'
                status = False
            else:
                bloque = bloque[3+pf:]
        print(bloque)
    return bloque, status, error

def analizar(lista):
    status = True
    c = 0
    error = ''
    car = ['{', '}', '(', ')', ';', ',']
    while len(lista) > c and status:
        palabra = lista[c]
        print(lista[c:], 'Lista final')
        if palabra == 'defVar':
            # CHEQUEO PARA VARIABLES
            if((lista[c+1] not in car) and (lista[c+2] not in car)):
                variables_parametro[lista[c+1]] = lista[c+2]
                c += 3
            else:
                error = 'Variable mal declarada'
                status = False
        elif palabra == 'defProc':
            # CHEQUEO PARA FUNCIONES
            funcion = lista[c+1]
            if(lista[c+2]=='('):
                funciones_parametro[funcion] = []
                while (lista[c+3] != ')') and status:
                    if lista[c+3] != ',':
                        funciones_parametro[funcion] += [lista[c+3]]
                    if lista[c+3] == ',' and lista[c+4] == ',':
                        error = 'Funcion ',funcion,' con malos parametros'
                        status = False
                    c += 1
                c += 3
                for i in funciones_parametro[funcion]:
                    variables_parametro[i+funcion]='0'
            else:
                error = 'Funcion ',funcion,' mal declarada'
                status = False
            if lista[c+1] == '{':
                p_final = complemeto_llave(lista[c+2:])
                bloque = lista[c+2:c+3+p_final]
                while len(bloque) > 1 and status:
                    print(bloque, 'Bloque')
                    if bloque[0] in c_simple.keys():
                        bloque, status, error = analizar_c_simple(bloque, status, error, funciones_parametro, funcion)                        
                    elif bloque[0] == 'if':
                        bloque, status, error = analizar_if(bloque, status, error, funciones_parametro, funcion)
                    elif bloque[0] == 'while':
                        bloque, status, error = analizar_while(bloque, status, error, funciones_parametro, funcion)
                    elif bloque[0] == 'repeat':
                        bloque, status, error = analizar_repeat(bloque, status, error, funciones_parametro, funcion)
                    else:
                        error = 'Bloque ',funcion,' no encontrada'
                        status = False
                    if len(bloque)>1:
                        if bloque[0] == ';' and bloque[1] == '}':
                            error = 'Bloque ',funcion,' mal construido'
                            status = False
                        else:
                            bloque = bloque[1:]
                    else:
                        bloque = bloque[1:]
                # Terminamos de chequear el bloque de la funcion
                c += 3 + p_final
            else:
                error = 'Funcion ',funcion,' mal declarada'
                status = False
            for i in funciones_parametro[funcion]:
                del variables_parametro[i+funcion]
        elif palabra == '{':
            funcion = 'none'
            bloque = lista[c+1:]
            bloque, status, error = analizar_bloque(bloque, status, funcion)
            c += 3 + p_final
        else:
            error = 'Funcion ',funcion,' mal declarada'
            status = False
    if len(error) > 0:
        print('FALSE || Error :', error)
    else:
        print('TRUE || El programa es correcto')
    return status

# print(lector('Practica.txt'))
analizar(lector('Practica.txt'))
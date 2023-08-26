#%%
# Buenas tardes :D
funciones = [
    'jump', 'walk', 'leap', 'turn', 'turnto', 'drop', 'get', 'grab', 'letGo', 'nop', 'facing'
]

variables = {}

extras = [
    'if', 'else', 'while', 'repeat', 'times', 'can', 'not'
]

caracteres = ['{', '}', '(', ')', ';', ',']


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
         


variables_parametro = {}
funciones_parametro = {}

c_simple = {
    
    'jump':[[2],[]], 
    'walk':[[1,2],['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']], 
    'leap':[[1,2],['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']], 
    'turn':[[1],['left', 'right', 'around']], 
    'turnto':[[1],['north', 'south', 'west', 'east']], 
    'drop':[[1],[]], 
    'get':[[1],[]], 
    'grab':[[1],[]], 
    'letGo':[[1],[]], 
    'nop':[[0],None]
    
    }

cond_def = {
    'facing':[[1],['north', 'south', 'west', 'east']],
    'can':[[1],[c_simple.keys()]],
    'not':[[1],['facing', 'can', 'not']]
    }

def construir_parametros(lista):
    r = []
    c = 0
    pf = 0
    while lista[c] != ')':
        if lista[c] != ',':
            r.append(lista[c])
        pf += 1
    return r,pf
        

def analizar(lista):
    status = True
    c = 0
    error = ''
    car = ['{', '}', '(', ')', ';', ',']
    while len(lista) > c and status:
        palabra = lista[c]
        if palabra == 'defVar':
            if((lista[c+1] not in car) and (lista[c+2] not in car)):
                variables_parametro[lista[c+1]] = lista[c+2]
                c += 3
            else:
                error = 'Variable mal declarada'
                status = False
        elif palabra == 'defProc':
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
            else:
                error = 'Funcion ',funcion,' mal declarada'
                status = False
            if lista[c+1] == '{':
                p_final = complemeto_llave(lista[c+2:])
                bloque = lista[c+2:c+3+p_final]
                print(bloque)
                print(funciones_parametro)
                print(variables_parametro)
                cb = 0
                while len(bloque) > 1 and status:
                    if bloque[0] in c_simple.keys():
                        # es una funcion simple
                        if (bloque[0] == 'nop') and (bloque[1] ==  '(') and bloque[2] ==  ')':
                            bloque = bloque[3:]
                        else:
                            num_parameters = c_simple[bloque[0]][0]
                            parametros, pf = construir_parametros(bloque[1:])
                            if len(parametros) > num_parameters:
                                error = 'Funcion ',funcion,' con extra parametros'
                                status = False
                            else:
                                if len(parametros) == 1:
                                    if 'turn' in parametros or 'turnto' in parametros:
                                        pass
                                    else:
                                        if (c_simple[bloque[1]][1][0]==0) and not(i.isdigit()):
                                            error = 'Parametro ',i,' en la funcion ', funcion, ' no valido'
                                            status = False
                                else:
                                    if (len(c_simple[bloque[1]][0][0])>1) and (i not in c_simple[bloque[1]][1]):
                                        error = 'Parametro ',i,' en la funcion ', funcion, ' no valido'
                                        status = False
                                    if i not in funciones_parametro:
                                        error = 'Parametro ',i,' en la funcion ', funcion, ' no valido'
                                        status = False
                                
                            
                    elif bloque[0] == 'if':
                        # es un if
                        pass
                    elif bloque[0] == 'while':
                        # es un while
                        pass
                    elif bloque[0] == 'repeat':
                        # es un repeat
                        pass
                    else:
                        error = 'Bloque ',funcion,' no encontrada'
                        status = False
                    if bloque[0] == ';' and bloque[1] == '}':
                        error = 'Bloque ',funcion,' mal construido'
                        status = False
                    else:
                        bloque = bloque[1:]
                # Terminamos de chequear el bloque
                c += 1 + p_final
            else:
                error = 'Funcion ',funcion,' mal declarada'
                status = False
            # chequear loops
        elif palabra == '{':
            # chequear la ejecucion de fin funciones_parametro
            pass
        
            
    if len(error) > 0:
        print('Error en', lista[c], ':', error)
    else:
        print('El programa es correcto')

# print(lector('Practica.txt'))
analizar(lector('Practica.txt'))


# ------------------
# PROGRAMA
# ------------------

def task(archivo):
    error = False
    while archivo and not error:
        palabra = archivo.pop(0)
        
        if palabra == 'defVar':
            nombre = archivo.pop(0)
            valor = archivo.pop(0)
            
            assert nombre not in caracteres, 'Variable mal declarada'
            assert valor not in caracteres, 'Valor mal declarado'
            variables[nombre] = valor
        
        elif palabra == 'defProc':
            nombre = archivo.pop(0)
            funciones.append(nombre)
            archivo.pop(0)
            parametros(archivo, nombre)
            
        elif palabra == '{':
            pos_final = complemeto_llave(archivo)
            bloque = archivo[:pos_final]
            # bla bla bla
            archivo = archivo[pos_final+1:]
    
    




# -------------------------------
# EJEMPLO
# -------------------------------

def handle_go( u ):
    print( "going %d units" % int(u))

def handle_rotate( direc ):
    print( "rotating %s" % direc.lower() )

def handle_drill():
    print( "drilling" )

def find_matching_brace(body):
    nest = 0
    for i, n in enumerate(body):
        if n == '{':
            nest += 1
        if n == '}':
            if not nest:
                return i
            nest -= 1


def process(body):
    while body:
        verb = body.pop(0)
        if verb == "GO":
            handle_go( body.pop(0) )
            assert body.pop(0) == 'UNITS'
        elif verb == "ROTATE":
            handle_rotate(body.pop(0))
        elif verb == "DRILL":
            handle_drill()
        elif verb == "REPEAT":
            count = body.pop(0)
            assert body.pop(0)=="TIMES"
            assert body.pop(0)=="{"
            closing = find_matching_brace(body)
            newbody = body[0:closing]
            print("repeat", count, closing, newbody)
            for _ in range(int(count)):
                process(newbody[:])
            body = body[closing+1:]
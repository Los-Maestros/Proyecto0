#%%
# Buenas tardes :D
funciones = [
    'jump', 'walk', 'leap', 'turn', 'turnto', 'drop', 'get', 'grab', 'letGo', 'nop', 'facing'
]

variables = [
    'north', 'south', 'east', 'west'
]

extras = [
    'if', 'else', 'while', 'repeat', 'times', 'can', 'not'
]



# -------------------
# CARGA DE DATOS
# -------------------

def lector(file):
    archivo = open(file, 'r')
    texto = archivo.read().replace('\n',' ')
    lista = lector2(texto)
    return lista

def lector2(texto):
    caracteres = ['{', '}', '(', ')', ';', ',']
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

def parametros(lista, var):
    char = lista.pop(0)
    while char != ')':
        if char != ',':
            var.append(char)
        char = lista.pop(0)
    return lista
         


variables_parametro = []
funciones_parametro = {}
c_simple = {'jump':['2',[0,0]], 
                 'walk':['1 or 2',[0,['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']]], 
                 'leap':['1 or 2',[0,['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']]], 
                 'turn':['1',['left', 'right', 'around']], 
                 'turnto':['1',['north', 'south', 'west', 'east']], 
                 'drop':['1',[0]], 
                 'get':['1',[0]], 
                 'grab':['1',[0]], 
                 'letGo':['1',[0]], 
                 'nop':['0',None],}
cond_def = {'facing':['1',['north', 'south', 'west', 'east']],
                     'can':['1',[c_simple.keys()]],
                     'not':['1',['facing', 'can', 'not']]}


def analizar(lista):
    status = True
    c = 0
    error = ''
    car = ['{', '}', '(', ')', ';', ',']
    while len(lista) > c and status:
        palabra = lista[c]
        if palabra == 'defVar':
            if((lista[c+1] not in car) and (lista[c+2] not in car)):
                c += 3
                variables_parametro.append(lista[c])
            else:
                error = 'Variable mal declarada'
                status = False
        elif palabra == 'defProc':
            funcion = lista[c+1]
            if(lista[c+2]=='('):
                funciones_parametro[funcion] = []
                while (lista[c+3] != ')') and status:
                    if lista[c+3] != ',':
                        funciones_parametro[lista[c+1]]=[lista[c+3]]
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
                bloque = lista[c+1:c+3+p_final]
                print(bloque)
                cb = 0
                while len(bloque) > 1 and status:
                    if bloque[0] in c_simple.keys():
                        # es una funcion simple
                        if (bloque[0] == 'nop') and (bloque[1] ==  '(') and bloque[2] ==  ')':
                            bloque = bloque[3:]
                        else:
                            num_parameters = c_simple[bloque[0]][0]
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
                # Terminamos de chequear el bloque
                c += 1 + p_final
            else:
                error = 'Funcion ',funcion,' mal declarada'
                status = False
            # chequear loops
        elif palabra == '{':
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
    while archivo:
        palabra = archivo.pop(0)
        
        if palabra == 'defVar':
            variable = archivo.pop(0)
            variables.append(variable)
        
        elif palabra == 'defProc':
            nombre = archivo.pop(0)
            funciones.append(nombre)
            archivo.pop(0)
            parametros(archivo, variables)
            
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
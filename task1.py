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
    cont = 1
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
    
    
print(lector('Practica.txt'))



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
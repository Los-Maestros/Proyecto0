# -------------------
# Variables
# -------------------

funciones = {}

variables = {}

caracteres = ['{', '}', '(', ')', ';', ',']

funciones_simple = {
    
    'jump': [[2],['int', 'int']], 
    'walk': [[1,2],['int', ['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']]], 
    'leap' : [[1,2],['int', ['front', 'right', 'left', 'back', 'north', 'south', 'west', 'east']]], 
    'turn' : [[1],[['left', 'right', 'around']]], 
    'turnto' : [[1],[['north', 'south', 'west', 'east']]], 
    'drop' : [[1],['int']], 
    'get' : [[1],['int']], 
    'grab' : [[1],['int']], 
    'letGo' : [[1],['int']], 
    'nop' : [[0]]
}

condicionales = {
    'facing' : ['north', 'south', 'west', 'east'],
    'can' : list(funciones_simple.keys()),
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
            
    assert not cont, 'Hay parentesis que no se cierran.'
    return respuesta


# ------------------
# AYUDAS
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

def complemeto_parentesis(archivo):
    cont = 0
    for i,j in enumerate(archivo):
        if j == '(':
            cont += 1
        elif j == ')':
            cont -= 1
            if not cont:
                return i

def entero(variable):
    if variable.isdigit():
        return 'int'
    return variable


# ------------------
# PARAMETROS
# ------------------

def lista_parametros(texto):
    texto.pop(0)
    palabra = texto.pop(0)
    parametros = []
    comas = 1
    cero_comas = True

    while palabra != ')':
        if palabra != ',':
            comas -=1
            verificar_caracter(palabra)
            var = verificar_variable(palabra)
            parametros.append(var)
        else:
            comas += 1
            
        palabra = texto.pop(0)
        cero_comas = False

    if cero_comas:
        comas -= 1 
    assert not comas, f'La función tiene mas/menos comas que parametros.'
    return parametros


def agregar_parametros(lista, nombre):
    char = lista.pop(0)
    comas = 1
    cero_comas = True
    
    if nombre not in funciones:
        funciones[nombre] = [[],[]]
    
    while char != ')':
        if char != ',':
            comas -=1
            verificar_caracter(char)
            funciones[nombre][0].append(char)
        
        else:
            comas += 1 
        char = lista.pop(0)  
        cero_comas = False
        
    funciones[nombre][1] = len(funciones[nombre][0])*[None]
    if cero_comas:
        comas -= 1 
    assert not comas, f'Función \"{nombre}\" con malos parametros.'
    return lista
         
         
# ------------------
# VERIFICADORES
# ------------------

def verificar_variable(valor):
    if valor in variables:
        valor_final = variables[valor]
    else:
        valor_final = entero(valor)
    return valor_final


def verificar_caracter(char):
    assert char not in caracteres, f'Los parametros de una función son un caracter \"{char}\".'


def verificar_condicional(archivo, condicional, esFuncion):
    pos_final = complemeto_parentesis(archivo)
    lst_parametro = archivo[1:pos_final]
    parametro = lst_parametro.pop(0)
    assert parametro in condicionales[condicional], f'El tipo de parametro de \"{condicional}\", es erroneo.'
    
    if condicional == 'not':
        verificar_condicional(lst_parametro, parametro, esFuncion)
        
    elif condicional == 'can':
        verificar_funcion_simple(lst_parametro, parametro, esFuncion) 
    
    return pos_final
    
    
def verificar_funcion_simple(bloque, funcion, esFuncion):
    lst_parametros = lista_parametros(bloque)
    assert len(lst_parametros) in funciones_simple[funcion][0], f'La cantidad de parametros de la función \"{funcion}\", es erronea.'
    
    if len(lst_parametros):
        tipo1 = lst_parametros[0] in funciones_simple[funcion][1][0]
        if esFuncion:
            existe1 = lst_parametros[0] in funciones[esFuncion][0] 
            
            if existe1:
                tipo = funciones_simple[funcion][1][0]
                numero = funciones[esFuncion][0].index(lst_parametros[0])
                funciones[esFuncion][1][numero] = tipo
            
            resultado1 = existe1 or tipo1
        else:
            resultado1 = tipo1
            
        try:
            tipo2 = lst_parametros[1] in funciones_simple[funcion][1][1]
            
            if esFuncion:
                existe2 = lst_parametros[1] in funciones[esFuncion][0]
                resultado2 = existe2 or tipo2
                
                if existe2:
                    tipo = funciones_simple[funcion][1][1]
                    numero = funciones[esFuncion][0].index(lst_parametros[1])
                    funciones[esFuncion][1][numero] = tipo
            
            else:
                resultado2 = tipo2
                
        except:
            resultado2 = True
        
        assert resultado1 and resultado2, f'La función \"{funcion}\", tiene un tipo de parametro erroneo.'
    
    return bloque


def verificar_puntocoma(bloque):
    if len(bloque) > 0:
        punto_coma = bloque.pop(0)
        if punto_coma == ';' and bloque[-1] != ';':
            return True
        return False
    return True


# ------------------
# PROGRAMA
# ------------------

def bloques(archivo, esFuncion = ''):
    pos_final = complemeto_llave(archivo)
    bloque = archivo[:pos_final]
    
    while bloque:
        pal = bloque.pop(0)

        if pal in funciones_simple:
            verificar_funcion_simple(bloque, pal, esFuncion)
        
        elif pal == 'while' or  pal == 'if':
            condicional = bloque.pop(0)
            assert condicional in condicionales, 'Despues de un while/if tiene que ir una condicional.'
            
            pos_f = verificar_condicional(bloque, condicional, esFuncion)
            bloque = bloque[pos_f+1:]
            assert bloque.pop(0) == '{', 'Despues de la condicional tiene que ir un bloque.'
            pos_f = bloques(bloque, esFuncion)
            bloque = bloque[pos_f+1:]
            
            if pal == 'if':
                assert bloque.pop(0) == 'else', 'No puede haber un else, sin if.'
                assert bloque.pop(0) == '{', 'Despues de un else, tiene que ir un bloque.'
                pos_f = bloques(bloque, esFuncion)
                bloque = bloque[pos_f+1:]  
                        
        elif pal == 'repeat':
            valor = verificar_variable(bloque.pop(0))
            assert valor == 'int', f'La variable \"{valor}\", tiene que ser un entero.'
            assert bloque.pop(0) == 'times', 'Despues del valor tiene que ir times.'
            assert bloque.pop(0) == '{', 'Despues de un times, tiene que ir un bloque.'
            pos_f = bloques(bloque, esFuncion)
            bloque = bloque[pos_f+1:]
            
        elif pal in funciones:
            lst_parametros = lista_parametros(bloque) 
            assert len(lst_parametros) == len(funciones[pal][0]), f'La cantidad de parametros ingresados de la función {pal}, es erronea.'
        
            if not esFuncion:
                for i, j in enumerate(lst_parametros):
                    
                    assert funciones[pal][1][i] is None or j in funciones[pal][1][i], f'El tipo de variable de la funcion {pal}, no coincide.'
            
        else:
            assert False, 'Hay algo dentro de un bloque de codigo que no deberia ir ahí.'
               
        assert verificar_puntocoma(bloque), f'Los ; estan mal puestos en una función.'
    return pos_final
    

def task(archivo):
    
    while archivo:
        palabra = archivo.pop(0)
        
        if palabra == 'defVar':
            nombre = archivo.pop(0)
            valor = entero(archivo.pop(0))
            
            assert nombre not in caracteres, f'Variable \"{nombre}\" mal declarada.'
            assert valor not in caracteres, f'Valor \"{valor}\" mal declarado.'
            variables[nombre] = valor
        
        elif palabra == 'defProc':
            nombre = archivo.pop(0)
            archivo.pop(0)
            agregar_parametros(archivo, nombre)
            assert archivo.pop(0) == '{', f'Función \"{nombre}\" mal delarada.'
            pos_final = bloques(archivo, nombre)
            archivo = archivo[pos_final+1:]
            
        elif palabra == '{':
            pos_final = bloques(archivo)
            archivo = archivo[pos_final+1:]
            
        else:
            assert False, 'Hay algo fuera de un bloque de codigo que no deberia ir ahí.'
            
    return True

# ------------------
# INICAR APLICACION
# ------------------

if __name__ == '__main__':
    print('\n¡¡Bienvenido al verificador de Sintaxis!!\n')
    # nombre_archivo = input('Ingrese el nombre del archivo que quiere analizar -> ')
    archivo = lector('pruebas.txt')
    verificado = task(archivo)
    
    if verificado:
        print(f'\nLa sintaxis del archivo ola es correcto :D')
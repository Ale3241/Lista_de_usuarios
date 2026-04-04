# Ejercicio:
# Lista de usuarios(diccionarios), permitir agregar varios usuarios, mostrar cuantos hay

import json
import pandas as pd
import os
import time as t

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

#Funcion para poner un input y que valide que efectivamente es un numero existente, sin simbolos ni letras
def input_int_manager(message):
    while True:
        try:
            number = input(message)
            if number.lower() == 'salir':
                return 'salir'
            number = int(number)
            break
        except ValueError:
            print('Ingresa un numero valido...')
    return number


#Leer si existe el archivo sino lo crea vacio
try:
    with open('lista_usuarios.json', 'r') as f:
        usuarios = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    usuarios = []



def key(indice=None):
    while True:
        limpiar()
        print('Que informacion deseas agregara el usuario?\n' +
        '(Escribe por Ej. nombre, edad, correo, etc, ti "titulo" de lo que desees agregar.\n')

        key = input('> ')

        exist = False

        if indice is None:
            return key
        
        for k in usuarios[indice]:
            if k == key.title():
                print(f'CUIDADO!!\n' +
                f'La llave "{k}" ya esta definida con el valor "{usuarios[indice][k]}", esta se estara actualizando si continuas!!')
                exist = True
                break
        if exist == True:
            while True:
                decision = input('Deseas actualizarla? (Si/No) \n> ')
                if decision.lower() in ['si', 's']:
                    return key
                elif decision.lower() in ['n', 'no']:
                    break
                else:
                    print('No es una opcion valida...')
        else:
            return key



def value():
    limpiar()
    value = input('\nDame el valor de esa informacion: ')
    return value


def agregar_usuario(indice=None):
    
    usuario = {}

    k = key(indice) if indice is not None else key()
    v = value()

    usuario[k.title()] = v.title()

    while True:
        repeat = input('Deseas agregar mas informacion al usuario? (si o no): ')

        match repeat.lower():
            case 'si'|'s':
                k = key(indice) if indice is not None else key()
                v = value()
                usuario[k.title()] = v.title()
            
            case 'no'|'n':
                break

            case _:
                print('Escribe si o no(s/n)...')

    return usuario


def seleccion_id_usuario(accion):
    while True:
        limpiar()
        print('Lista de usuarios:')
        carga_usuarios()
        i_usuario = input_int_manager(f'selecciona el ID del usuario que deseas {accion} o escriba "Salir": ')
        
        if i_usuario == 'salir':
            return 'salir'
        
        if not i_usuario - 1 in range(len(usuarios)):
            print('No existe ese ID...')
            t.sleep(1)
        else:
            print(f'\nUsuario seleccionado: #{i_usuario} {usuarios[i_usuario - 1]}')
            return i_usuario - 1


def loading(txt):
    for seconds in range(3, 0, -1):
        limpiar()
        print(txt, seconds)
        t.sleep(.8)



def editar():
    while True:
        indice = seleccion_id_usuario('editar')
        if indice == 'salir':
            loading('Saliendo...')
            return 
        print('Quieres hacerlo "denuevo" o simplemente "seguir" agregando mas informacion?')
        tipo_edicion = input('> ')

        if 'denuevo' in tipo_edicion.lower():
            usuario = agregar_usuario()
            usuarios[indice] = usuario
            break
        elif 'seguir' in tipo_edicion.lower():
            usuario = agregar_usuario(indice)
            usuarios[indice].update(usuario)
            break
        elif tipo_edicion.lower() == 'salir':
            loading('Saliendo...')
            return
        else:
            print('Escribe "Denuevo" o "Seguir" para seleccionar el tipo de edicion...')
            t.sleep(1.5)

    print('\nUsuario editado con exito!\n')
    input('Preisonar cualquier tecla...')


def carga_usuarios():
    for usuario in range(len(usuarios)):
        print(f'El usuario #{usuario + 1} es: ', usuarios[usuario])
    print()


def mostrar():
    limpiar()
    if usuarios:
        print(f'Cantidad: {len(usuarios)}')
        print('Los usuarios agregados son:\n')
        carga_usuarios()
    else:
        print('No hay usuarios agregados...')


def eliminar():
    
    indice = seleccion_id_usuario('eliminar')
    if indice == 'salir':
        loading('Saliendo...')
        return 
    while True:
        desicion = input('Estas seguro que deseas eliminar este usuario? (si/no)\n>')
        
        if desicion.lower() in ['si', 's']:
            loading('Eliminando...')
            del usuarios[indice]
            print('USUARIO ELIMINADO CORRECTAMENTE!!')
            break
        elif desicion.lower() in ['n', 'no']:
            loading('Saliendo al menu...')
            break
        else:
            print('OPCION INVALIDA!!')
            
            
def buscar():
    opciones = {}
    for u in range(len(usuarios)):
        for k in usuarios[u]:
            opciones[k] = opciones.get(k, 0) + 1

    while True:
        limpiar()
        print('Escribe por cual vas a buscar:')        
        for o in opciones:
            print(f'{o}({opciones[o]})')
            
        opcion = input('> ').strip().title()
        encontrados = False

        if opcion in opciones:

            print(f'Estos son los usuarios cque contienen "{opcion}":\n')
            
            for u in usuarios:
                if u.get(opcion):
                    print(u)

            filtro = input('\nDame el valor que deseas buscar:').strip().title()

            print(f'\nResultados para {opcion} = {filtro}:\n')
            for u in usuarios:
                if str(u.get(opcion)) == filtro:
                    print(u)
                    encontrados = True

            if not encontrados:
                print('No se ha encontrado ningun usuario...')
                t.sleep(1.5)
            
            input('')
            break
        else:    
            print('Esa opcion no existe...')
            t.sleep(1.5)
        
    


#GUARDAR DATOS EN UN ARCHIVO JSON
def guardar():
    limpiar()
    with open('lista_usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=4)
    loading('Guardando...')
    print('CAMBIOS GUARDADOS CON EXITO!')
    t.sleep(1)

def print_w_time(message):
    print('No hay usuarios para ', message)
    t.sleep(1.5)


def importar_xlsx():
    df = pd.DataFrame(usuarios)
    loading('Importando...')
    df.to_excel("Lista_usuarios.xlsx", index=False)
    limpiar()
    print('Importado con exito!')
    t.sleep(1)


#MENU - MATCH
while True:
    limpiar()
    print('Bienvenido al programa de lista de usuarios!\n')
    print('Elige una opcion\n',
        '1.Agregar\n',
        '2.Editar\n',
        '3.Mostrar\n',
        '4.Guardar\n',
        '5.Importar(xlsx)\n',
        '6.Eliminar\n',
        '7.Buscar\n',
        '8.Salir\n')

    option = input('Accion > ')
    print()

    match option.lower():
        case '1' | 'agregar':
            usuario = agregar_usuario()
            usuarios.append(usuario)
        

        case '2' | 'editar':
            if not usuarios:
                print_w_time('editar')
            else:
                editar()


        case '3' | 'mostrar':
            mostrar()
            input('Preisonar cualquier tecla...')
            

        case '4' | 'guardar':
            guardar()


        case '5' | 'importar':
            importar_xlsx()


        case '6' | 'eliminar':
            if not usuarios:
                print_w_time('eliminar')
            else:
                eliminar()
                
                
        case '7' | 'buscar':
            if not usuarios:
                print_w_time('buscar')
            else:
                buscar()


        case '8' | 'salir':
            break


        case _:
                print('Elige una opcion valida...')
                t.sleep(1.2)
"""
Script para realizar una copia de seguridad de los archivos a subir a desarrollo y subirlos
"""
import sys
import os
from ftplib import FTP
import time

menu_actions = {}

ORIGINFOLDER = "C:\\SUBIDAS"
BACKUPFOLDER = "C:\\backupftp"
USUARIOFTP = "poner aqu tu usuario"
CLAVEFTP = "poner aqui tu clave de acceso"



#=====================
#        MENU
#=====================

def main_menu():
    """
    Crea el menu principal
    """
    os.system('cls')

    print "Elige una opcion de menu"
    print "1. Subir a carpeta bin"
    print "2. Subir a carpeta languages"
    print "\n0. Salir"
    eleccion = raw_input(" >> ")
    exec_menu(eleccion)

def exec_menu(eleccion):
    """
    Realiza la llmada a las funciones de los diferentes menus
    """
    os.system('cls')
    ch = eleccion.lower()
    if ch == '':
        menu_actions[ch]()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Eleccion invalida, intenta de nuevo\n"
            menu_actions['main_menu']()
    return

def menu1():
    """
    Asigna el path de destino y llama a la rutina que los sube
    """
    pathftp = 'poner aqui path carpeta bin'
    crear_backup(pathftp)

def menu2():
    """
    Asigna el path de destino y llama a la rutina que los sube
    """
    pathftp = 'poner aqui path carpeta languages'
    crear_backup(pathftp)

def crear_backup(path):
    """
    Realiza un backup de los archivos que se van a subir a la carpeta del ftp
    de desarrollo, realiza la subida y borra los archivos situados en la carpeta de subida
    """
    os.system('cls')
    archivos = os.listdir(ORIGINFOLDER)
    numarchivosasubir = len(archivos)
    if numarchivosasubir > 0:
        existecarpeta = os.path.exists(BACKUPFOLDER)
        if not existecarpeta:
            os.mkdir(BACKUPFOLDER)

        locbackupfolder = BACKUPFOLDER + "\\" + time.strftime("%Y%m%d%H%M%S", time.localtime())
        os.mkdir(locbackupfolder)
        os.chdir(locbackupfolder)
        print "Creando la carpeta para el backup\n" + locbackupfolder
        locftp = FTP('heraeveriliondev.cloudapp.net')
        locftp.login(user=USUARIOFTP, passwd=CLAVEFTP)
        locftp.cwd(path)
        archivos_borrar = []

        for archivo in archivos:
            try:
                archivolocal = open(archivo, 'wb')
                locftp.retrbinary('RETR ' + archivo, archivolocal.write, 1024)
            except IOError:
                print "Error: no puedo abrir el archivo\n"
            else:
                archivos_borrar.append(archivo)
                archivolocal.close()
                print "Copiando archivo " + locbackupfolder + "\\" + archivo + "\n"


        for archivo in archivos_borrar:
            try:
                
                os.remove(ORIGINFOLDER + "\\" + archivo)
            except IOError:
                print "Error al borrar el archivo " + ORIGINFOLDER + "\\" + archivo + "\n"
            else:
                print "Borrado archivo " + ORIGINFOLDER + "\\" + archivo + "\n"
        
        locftp.quit()

        print "Pulse una tecla para continuar."
        raw_input(" >> ")
    else:
        print "No hay archivos para subir"


def back():
    """
    Esta funcion llama a la funcion main_menu
    """
    menu_actions['main_menu']()

def salir():
    """
    Sale del programa
    """
    sys.exit()

menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': salir
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            exec_menu(sys.argv[1])
        except KeyError:
            print "Eleccion invalida, intenta de nuevo\n"
            menu_actions['main_menu']()
    else:
        main_menu()

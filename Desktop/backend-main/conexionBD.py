
# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector


def connectionBD():
    mydb = mysql.connector.connect(
        host="localhost",
        user="alansillo",
        passwd="alansito661",
        database="victoryapi"
    )
    return mydb
    '''       
    if mydb:
        return ("Conexion exitosa")
    else:
        return ("Error en la conexion a BD")
    '''

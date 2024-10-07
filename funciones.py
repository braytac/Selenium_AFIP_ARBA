#!/usr/bin/env python
# coding: utf-8

# In[71]:


from pathlib import Path
import sqlite3
from sqlite3 import Error
from datetime import date

database = Path('FacturasAFIP.db')

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None 


def create_table(conn, sql):
    """
    Crear tabla
    """
    cur = conn.cursor()
    cur.execute('DROP TABLE facturas')
    conn.commit()
    cur.execute(sql)
    conn.commit()
    cur.close()


def create_tables(conn,database):
 
    tabla_facturas = """ CREATE TABLE IF NOT EXISTS facturas (
                                        id integer PRIMARY KEY,
                                        destinatario text NOT NULL,
                                        cuit text NOT NULL,
                                        concepto text NOT NULL,
                                        monto real,
                                        desde text,
                                        hasta text
                                    ); """
 
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create projects table
        print("Creando tabla Facturas")
        create_table(conn, tabla_facturas)
        # create tasks table
    else:
        print("Error! cannot create the database connection.")

def eliminar_registro(conn, nro):
    cur = conn.cursor()
    cur.execute("DELETE FROM facturas WHERE nro_comprobante=?", (nro,))
    conn.commit()
    #cur.execute("update sqlite_sequence set seq=0 where name='facturas'")
    #cur = conn.cursor()
    #cur.execute("VACUUM")
    cur.close()
        
def limpiar_db(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM facturas")
    conn.commit()
    #cur.execute("update sqlite_sequence set seq=0 where name='facturas'")
    #cur = conn.cursor()
    #cur.execute("VACUUM")
    cur.close()

def insertar_factura(conn, datos):
    """
    Guardar nueva factura
    :param conn:
    :param datos:
    :return: facturas id
    """
    fecha_factura = date.today().strftime("%Y-%m-%d")
    sql = "INSERT INTO facturas ( \
                                    nro_comprobante, \
                                    cuit,destinatario, \
                                    monto, \
                                    concepto, \
                                    desde, \
                                    hasta, \
                                    fecha_factura)\
              VALUES (?,?,?,?,?,?,?,'"+fecha_factura+"')"
    cur = conn.cursor()
    cur.execute(sql, datos)
    conn.commit()
    cur.close()    
    return cur.lastrowid

def consulta_factura(conn, sql):
    #sql = """ SELECT * FROM facturas WHERE strftime( '%m', desde )='10' """
    cur = conn.cursor()
    cur.execute(sql)
    r = cur.fetchall()
    cur.close()    
    return r

def guardar_factura(conn, factura_campos):
    # guardar nueva factura
    factura_id = insertar_factura(conn, factura_campos) 
    return factura_id
        

# Si lo estoy ejecutando como programa principal
# y no es un módulo de otro programa
#if __name__ == '__main__':
#    guardar_factura()


#create_tables(conn,database)
#limpiar_db(conn)
#eliminar_registro(conn,'1')

def mostrar_facturas(conn):
    sql = """ SELECT nro_comprobante,destinatario,monto,fecha_factura,desde,hasta FROM facturas ORDER BY nro_comprobante ASC """
    facturas = consulta_factura(conn, sql)
    
    # Imprimir encabezado de las columnas, que son: "Nº comp.", Destinatario, Monto, Fecha, factura,  Desde, Hasta,  teniendo en cuenta la longitud de los datos a mostrar en el for
    columna1 = "Nº comp.".ljust(10)
    columna2 = "Destinatario".ljust(45)
    columna3 = "Monto".ljust(10)
    columna4 = "Fecha Factura".ljust(15)
    columna5 = "Desde".ljust(15)
    columna6 = "Hasta".ljust(15)
    print(columna1+columna2+"\t"+columna3+"\t"+columna4+"\t"+columna5+"\t"+columna6)



    for factura in facturas:
        
        nroFactura = str(factura[0])
        entidad = str(factura[1])
        monto = str(factura[2])

        # rellenar nro de factura a 5 caracteres con espacios a la derecha
        nroFactura = nroFactura.ljust(10)
        # rellenar entidad a 45 caracteres con espacios a la derecha
        entidad = entidad.ljust(45)
        # rellenar monto a 10 caracteres con espacios a la derecha
        monto = monto.rjust(10)


        print(nroFactura+
              entidad+
              monto+"\t"+
              str(factura[3])+"\t"+
              str(factura[4])+"\t"+
              str(factura[5]))


def mostrar_montos_DDJJ(conn):
    sql = """SELECT sum(monto) AS monto,strftime('%m/%Y',fecha_factura) AS periodo FROM facturas 
          GROUP BY periodo 
          ORDER BY hasta ASC """

    ddjjs = consulta_factura(conn, sql)
    print("\nMENSUALES\n__________________________\nPeríodo\t  Monto Facturado\n")
    for ddjj in ddjjs:

        print(str(ddjj[1])+"\t|  "+
              str(ddjj[0]))

    sql = """SELECT sum(monto) AS monto,strftime('%Y',fecha_factura) AS periodo FROM facturas 
          GROUP BY periodo 
          ORDER BY hasta ASC """

    ddjjs = consulta_factura(conn, sql)
    print("\nANUALES\n__________________________\nPeríodo\t  Monto\n")
    for ddjj in ddjjs:

        print(str(ddjj[1])+"\t|  "+
              str(ddjj[0]))  

def mostrar_ingresos_mes(conn):
    sql = """SELECT sum(monto) AS monto,strftime('%m/%Y',hasta) AS periodo FROM facturas 
          GROUP BY periodo 
          ORDER BY hasta ASC """

    ddjjs = consulta_factura(conn, sql)
    print("\nMENSUALES\n__________________________\nPeríodo\t  Monto\n")
    for ddjj in ddjjs:

        print(str(ddjj[1])+"\t|  "+
              str(ddjj[0]))

    sql = """SELECT sum(monto) AS monto,strftime('%Y',hasta) AS periodo FROM facturas 
          GROUP BY periodo 
          ORDER BY hasta ASC """

    ddjjs = consulta_factura(conn, sql)
    print("\nANUALES\n__________________________\nPeríodo\t  Monto\n")
    for ddjj in ddjjs:

        print(str(ddjj[1])+"\t|  "+
              str(ddjj[0]))              
              
#        nro_comprobante,destinatario,monto,desde,hasta
#conn = create_connection(database)
"""
factura_campos = ('30677980032',
                  'FUNDACION DE LA FACULTAD DE INGENIERIA',
                  '5000',
                  'Mantenimiento DB y carga de personal en lectores biométricos',
                  '2019-03-01',
                  '2019-03-01')
guardar_factura(conn,factura_campos)
"""
#mostrar_facturas(conn)
#conn.close()

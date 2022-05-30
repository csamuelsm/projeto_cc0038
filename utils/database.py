from flask import abort
import mysql.connector
import os

conn = None

def start_conn(host = "mysql04-farm2.uni5.net",
            user = "bessapontes23", password = "6qSLjgbR",
            database = "bessapontes23"):
    global conn
    if conn is not None and conn.is_connected():
        return conn
    try:
        conn = mysql.connector.connect(host = host,
            user = user,
            password = password,
            database = database)
    except mysql.connector.Error as error:
        print("Falha ao se conectar no banco de dados: {}".format(error))
        abort(500)

def get_conn():
    global conn
    return conn

def close_conn():
    global conn
    if conn is not None:
        conn.close()
        conn = None

def get_cobras():
    # função que retorna o nome científico das cobras no banco
    global coon
    start_conn()
    cursor = conn.cursor()

    query = ("SELECT COBRA.idCOBRA, COBRA.familia, COBRA.especie, COBRA_NOME_POP.nome FROM COBRA "
            "INNER JOIN COBRA_NOME_POP ON COBRA.idCOBRA = COBRA_NOME_POP.idCOBRA "
            "ORDER BY familia;")
    cursor.execute(query)

    cobras = []
    for id, familia, especie, nome_pop in cursor:
        cobras.append("{} {}".format(familia, especie))
<<<<<<< HEAD
        print(nome_pop)


=======
        
>>>>>>> f47ce8c624e8665a1b373bf359f1302420bd0bdf
    cursor.close()
    close_conn()
    return cobras

def get_cobras_info():
    cobras = get_cobras()
    cobras_info = {}
    for cobra in cobras:
        for filename in os.listdir("./static/serpentesFotos/{}".format(cobra)):
            if cobra not in cobras_info.keys():
                cobras_info[cobra] = []
            cobras_info[cobra].append(filename)
    return cobras_info

def insert_registro(localizacao, informacao_adc,
                    dateTime, localizacao_lat = '',
                    localizacao_log = '', isImg = 0):
    global coon
    start_conn()
    cursor = conn.cursor()
    idRegistro = None
    try:
        insert_query = """INSERT INTO REGISTRO (localizacao, localizacao_lat, localizacao_log, imagem, informacao_adc, data_hora)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (localizacao, localizacao_lat, localizacao_log, isImg, informacao_adc, dateTime)
        cursor.execute(insert_query, values)
        print(cursor.rowcount, "Registro salvo com sucesso")
        conn.commit()
        idRegistro = cursor.lastrowid
    except mysql.connector.Error as error:
        print("Falha ao inserir o registro no banco de dados: {}".format(error))
    finally:
        cursor.close()
        close_conn()
    return idRegistro

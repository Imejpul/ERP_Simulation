import pymysql


# ----------------------------------CONEXIÓN CON BD


def conectar_bd():
    db = pymysql.connect(host="127.0.0.1", user="root", db="practica3", port=3306)
    # Preparar el cursor
    cursor = db.cursor()
    # Ejecutar SQL de prueba
    cursor.execute("SELECT VERSION()")
    # Recuperar una fila usando fetchone()
    dato = cursor.fetchone()
    print("Versión de BD: % s " % dato)

    return db


def desconectar_bd(db):
    db.close()


# --------------------------------CREACION TABLAS


def crear_tabla_compra(cursor):
    # Eliminar tabla (drop) si ya existe
    cursor.execute("DROP TABLE IF EXISTS COMPRA")

    # SQL para crear tabla
    sql = """CREATE TABLE COMPRA (
                NUM_ORD CHAR(20) NOT NULL,
                DPTO_SOLCT CHAR(20),
                PROD1 CHAR(20),
                CANT_PROD1 INT,
                PROD2 CHAR(20),
                CANT_PROD2 INT)"""
    cursor.execute(sql)


def crear_tabla_venta(cursor):
    # Eliminar tabla (drop) si ya existe
    cursor.execute("DROP TABLE IF EXISTS VENTA")

    # SQL para crear tabla
    sql = """CREATE TABLE VENTA (
                NUM_FACT INT NOT NULL,
                CLIENTE CHAR(20),
                PROD1 CHAR(20),
                CANT_PROD1 INT,
                IMP_PROD1 FLOAT,
                PROD2 CHAR(20),
                CANT_PROD2 INT,
                IMP_PROD2 FLOAT)"""
    cursor.execute(sql)


# producción
def crear_tabla_objetivo(cursor):
    # Eliminar tabla (drop) si ya existe
    cursor.execute("DROP TABLE IF EXISTS OBJETIVO")

    # SQL para crear tabla
    sql = """CREATE TABLE OBJETIVO (
                MES_ANYO CHAR(20) NOT NULL,
                UDS_OBJ INT,
                DIAS_LAB INT,
                TURNOS INT)"""
    cursor.execute(sql)


# finanzas
def crear_tabla_balance(cursor):
    # Eliminar tabla (drop) si ya existe
    cursor.execute("DROP TABLE IF EXISTS BALANCE")

    # SQL para crear tabla
    sql = """CREATE TABLE BALANCE (
                MES_ANYO CHAR(20) NOT NULL,
                INGRESOS FLOAT,
                GASTOS FLOAT,
                IMP_SOC INT)"""
    cursor.execute(sql)


def crear_tabla_usuario(cursor):
    # Eliminar tabla (drop) si ya existe
    cursor.execute("DROP TABLE IF EXISTS USUARIO")

    # SQL para crear tabla
    sql = """CREATE TABLE USUARIO (
                    NOM_USER CHAR(20) NOT NULL,
                    USER_PASS CHAR(20),
                    ROL INT)"""
    cursor.execute(sql)


# --------------------------------INSERTAR USUARIOS INICIALES


def carga_usuarios_iniciales(nombre, user_pass, rol, db):
    cursor = db.cursor()

    # Consulta SQL para insertar datos de un empleado
    sql = """INSERT INTO USUARIO(NOM_USER,USER_PASS, ROL) VALUES\
          ('%s', '%s', '%d' )"""\
          % (nombre, user_pass, rol)
    print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


# -------------------------------SET UP INICIAL


def set_up_inicial():
    bd = conectar_bd()
    cursor = bd.cursor()

    crear_tabla_usuario(cursor)
    crear_tabla_compra(cursor)
    crear_tabla_venta(cursor)
    crear_tabla_objetivo(cursor)  # producción
    crear_tabla_balance(cursor)  # finanzas

    # Inserción usuarios Administradores
    carga_usuarios_iniciales('ivan', '123', 5, bd)
    carga_usuarios_iniciales('ekaitz', '369', 5, bd)

    # Inserción usuarios departamentos
    carga_usuarios_iniciales('eric', '789', 1, bd)  # Compras
    carga_usuarios_iniciales('isa', '147', 2, bd)  # Ventas
    carga_usuarios_iniciales('david', '258', 3, bd)  # Producción
    carga_usuarios_iniciales('jose', '369', 4, bd)  # Finanzas

    desconectar_bd(bd)


set_up_inicial()

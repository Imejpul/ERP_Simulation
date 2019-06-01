import csv
import pymysql

# --------------------------------GESTIÓN ARCHIVOS

# Ruta a ventas (para ventas y finanzas)
ruta_ventas = './datos_ventas/facturas.csv'

# Ruta a usuarios (para gestión_usuarios y login)
ruta_usuarios = './datos_usuarios/usuarios.csv'


def lectura_datos(ruta_archivo):
    datos = []

    # Control excepciones
    try:
        with open(ruta_archivo) as csvfichero:
            reader = csv.reader(csvfichero, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

            csvfichero.seek(0)

            for fila in reader:
                datos.append(fila)

    except IOError:
        print("Error al intentar cargar datos..")

    return datos


def escritura_datos(ruta_archivo, datos, tipo_escritura):
    fichero = open(ruta_archivo, tipo_escritura)

    # Control excepciones
    try:
        with fichero:
            writer = csv.writer(fichero)
            writer.writerows(datos)
            return True
    except IOError:
        print("Error al intentar guardar datos..")
        return False


# -----------------------------LÓGICA NEGOCIO


def compras():
    ruta_compras = './datos_compras/ordenesCompra.csv'

    def crear_orden_compra():

        departamento_solicitante = input("Introduzca departamento que solicita: ")
        numero_orden = input("Introduzca número orden (ver -mostrar ordenes compra-): ")

        prod1 = input("Introduzca producto 1: ")
        prod2 = input("Introduzca producto 2: ")

        cant_prod1 = input("Introduzca cantidad producto 1: ")
        cant_prod2 = input("Introduzca cantidad producto 2: ")

        orden_creada = False

        # controlamos que campos vacíos tomen valor guión bajo ( _ )

        if departamento_solicitante == '':
            departamento_solicitante = '_'

        if numero_orden == '':
            numero_orden = '_'

        if prod1 == '':
            prod1 = '_'

        if prod2 == '':
            prod2 = '_'

        if cant_prod1 == '':
            cant_prod1 = '_'

        if cant_prod2 == '':
            cant_prod2 = '_'

        # procedimiento para almacenar datos (BD o Archivo)

        if numero_orden != '_':
            datos = [numero_orden, departamento_solicitante, prod1, prod2, int(cant_prod1), int(cant_prod2)]
            # orden_creada = escritura_datos(ruta_compras, datos, 'a')
            insertar_datos_tabla_compra(datos)
            orden_creada = True
        else:
            print("¡Debe dar algún valor a número orden! (3 dígitos numéricos enteros -> 123 p.ej.) \n")

        if orden_creada:
            print("¡Orden creada! \n")
        else:
            print("¡Error al crear orden! ")
            print("Saliendo de crear orden compra.. \n")

    def editar_orden_compra():

        orden_tst = False
        index = -1
        orden_modificada = False

        num_orden = input("Introduzca número orden de compra (ver -Mostrar órdenes de compra-): ")

        # carga de datos desde BD y almacenar en variables

        # datos = lectura_datos(ruta_compras)
        datos = cargar_datos_tabla('COMPRA')

        for fila in datos:
            for campo in fila:
                if campo == num_orden:
                    index = datos.index(fila)
                    orden_tst = True

        if orden_tst:

            departamento = datos[index][1]
            prod1 = datos[index][2]
            prod2 = datos[index][4]
            cant_prod1 = datos[index][3]
            cant_prod2 = datos[index][5]

            print("departamento: " + departamento)
            print("producto 1: " + prod1)
            print("producto 2: " + prod2)
            print("cantidad producto 1: " + str(cant_prod1))
            print("cantidad producto 2: " + str(cant_prod2) + "\n")

            print(
                "Datos a modificar en orden de compra: \n"
                "---> 1. Departamento \n"
                "---> 2. Producto 1 \n"
                "---> 3. Producto 2 \n"
                "---> 4. Cant.Producto 1 \n"
                "---> 5. Cant.Producto 2 \n"
                "---> 6. salir ")
            op_ord_compra = input("Introduzca nº: ")

            if op_ord_compra == '1':

                nuevo_departamento = input("Nuevo valor departamento: ")
                # datos[index][1] = nuevo_departamento

                # escritura_datos(ruta_compras, datos, 'w')
                actualizar_tupla_tabla('COMPRA', 'DPTO_SOLCT', nuevo_departamento, 'NUM_ORD', datos[index][0])
                orden_modificada = True

            elif op_ord_compra == '2':

                nuevo_prod1 = input("Nuevo valor producto 1: ")

                # escritura_datos(ruta_compras, datos, 'w')
                actualizar_tupla_tabla('COMPRA', 'PROD1', nuevo_prod1, 'NUM_ORD', datos[index][0])
                orden_modificada = True

            elif op_ord_compra == '3':

                nuevo_prod2 = input("Nuevo valor producto 2: ")
                # datos[index][3] = nuevo_prod2

                # escritura_datos(ruta_compras, datos, 'w')
                actualizar_tupla_tabla('COMPRA', 'PROD2', nuevo_prod2, 'NUM_ORD', datos[index][0])
                orden_modificada = True

            elif op_ord_compra == '4':

                nueva_cant_prod1 = input("Nuevo valor a cantidad producto 1: ")
                # datos[index][4] = nueva_cant_prod1

                # escritura_datos(ruta_compras, datos, 'w')
                actualizar_tupla_tabla('COMPRA', 'CANT_PROD1', nueva_cant_prod1, 'NUM_ORD', datos[index][0])
                orden_modificada = True

            elif op_ord_compra == '5':

                nueva_cant_prod2 = input("Nuevo valor a cantidad producto 2: ")
                # datos[index][5] = nueva_cant_prod2

                # escritura_datos(ruta_compras, datos, 'w')
                actualizar_tupla_tabla('COMPRA', 'CANT_PROD2', nueva_cant_prod2, 'NUM_ORD', datos[index][0])
                orden_modificada = True

            elif op_ord_compra == '6':
                orden_modificada = False
            else:
                print("¡Introduzca valor válido! (1 al 6)")

        if orden_modificada:
            print("¡Orden modificada! \n")
        else:
            print("¡Error al modificar orden! ")
            print("Saliendo de editar orden compra.. \n")

    def anular_orden_compra():

        num_orden = input("Introduzca número orden de compra (ver -Mostrar órdenes de compra-): ")

        ord_tst = False
        orden_anulada = False
        index = -1

        # eliminar en BD orden equivalente a num_orden
        # datos = lectura_datos(ruta_compras)
        datos = cargar_datos_tabla('COMPRA')

        for fila in datos:
            for campo in fila:
                if campo == num_orden:
                    index = datos.index(fila)
                    ord_tst = True

        if ord_tst:
            # eliminamos tupla si existe en nuestra BD
            # datos.remove(datos[index])
            borrar_tupla_tabla('COMPRA', 'NUM_ORD', datos[index][0])
            orden_anulada = True

            # reescribimos el archivo de usuarios
            escritura_datos(ruta_compras, datos, 'w')

        if orden_anulada:
            print("Orden anulada! \n")
        else:
            print("¡Error al anular orden! ")
            print("Saliendo de anular orden compra.. \n")

    def mostrar_ordenes_compra():
        # datos = lectura_datos(ruta_compras)
        datos = cargar_datos_tabla('COMPRA')

        for orden in datos:
            print(orden)

        print("¡ordenes cargadas! \n")

    opcompras = '0'
    while opcompras != '5':
        print(
            "Menú del departamento de Compras: \n"
            "---> 1. Crear orden de compra \n"
            "---> 2. Editar orden de compra \n"
            "---> 3. Anular orden de compra \n"
            "---> 4. Mostrar órdenes de compra \n"
            "---> 5. salir \n")
        opcompras = input("Introduzca nº: ")
        print("\n")

        if opcompras == '1':
            crear_orden_compra()
        elif opcompras == '2':
            editar_orden_compra()
        elif opcompras == '3':
            anular_orden_compra()
        elif opcompras == '4':
            mostrar_ordenes_compra()
        elif opcompras == '5':
            print("saliendo de compras.. \n")
        else:
            print("¡Introduzca valor válido! (1 al 5) \n")


def ventas():
    def crear_factura_venta():

        factura_creada = False

        num_factura = input("Introduzca número factura: ")
        cliente = input("Introduzca cliente: ")

        prod1 = input("Introduzca producto 1: ")
        if prod1 != '':
            imp_prod1 = input("Introduzca importe producto 1: ")
            cant_prod1 = input("Introduzca cantidad producto 1: ")

            if imp_prod1 == '' or cant_prod1 == '':
                imp_prod1 = '0'
                cant_prod1 = '1'

        # Control posibles valores vacíos
        else:
            prod1 = '_'
            imp_prod1 = '0'
            cant_prod1 = '0'

        prod2 = input("Introduzca producto 2: ")
        if prod2 != '':
            imp_prod2 = input("Introduzca importe producto 2: ")
            cant_prod2 = input("Introduzca cantidad producto 2: ")

            if imp_prod2 == '' or cant_prod2 == '':
                imp_prod2 = '0'
                cant_prod2 = '1'

        # Control posibles valores vacíos
        else:
            prod2 = '_'
            imp_prod2 = '0'
            cant_prod2 = '0'

        if cliente == '':
            cliente = '_'

        # control posible fallos en cálculo total
        '''try:
            total = (int(cant_prod1) * float(imp_prod1)) + (int(cant_prod2) * float(imp_prod2))
        except:
            total = 'N/D'
        '''

        # procedimiento para almacenar datos (BD o Archivo)
        if num_factura != '':
            # datos = [[num_factura, cliente, prod1, imp_prod1, cant_prod1, prod2, imp_prod2, cant_prod2, total]]
            # factura_creada = escritura_datos(ruta_ventas, datos, 'a')
            datos = [int(num_factura), cliente, prod1, int(cant_prod1), float(imp_prod1), prod2, int(cant_prod2),
                     float(imp_prod2)]
            insertar_datos_tabla_venta(datos)
            factura_creada = True
        else:
            print("¡Debe dar algún valor a número factura! (Preferente: 3 dígitos numéricos enteros -> 123 p.ej.) \n")

        if factura_creada:
            print("¡Factura creada! \n")
        else:
            print("¡Error al crear factura! ")
            print("Saliendo de crear factura.. \n")

    def editar_factura_venta():

        factura_tst = False
        index = -1
        factura_modificada = False

        num_factura = int(input("Introduzca número factura (acceda a -Mostrar facturas- primero): "))

        # carga de datos desde BD y almacenar en variables
        # datos = lectura_datos(ruta_ventas)
        datos = cargar_datos_tabla('VENTA')

        for fila in datos:
            for campo in fila:
                if campo == num_factura:
                    index = datos.index(fila)
                    factura_tst = True

        if factura_tst:

            cliente = datos[index][1]

            prod1 = datos[index][2]
            imp_prod1 = datos[index][4]
            cant_prod1 = datos[index][3]

            prod2 = datos[index][5]
            imp_prod2 = datos[index][7]
            cant_prod2 = datos[index][6]

            # total = datos[index][8]

            print("Cliente: " + cliente)
            print("Prod1: " + prod1)
            print("Importe prod1: " + str(imp_prod1))
            print("Cantidad prod1: " + str(cant_prod1))
            print("Prod2: " + prod2)
            print("Importe prod2: " + str(imp_prod2))
            print("Cantidad prod2: " + str(cant_prod2))
            # print("Total: " + total + "\n")

            print(
                "Datos a modificar en orden de compra:+ \n"
                "---> 1. Cliente \n"
                "---> 2. Producto 1 \n"
                "---> 3. Importe producto 1 \n"
                "---> 4. Cantidad producto 1 \n"
                "---> 5. Producto 2 \n"
                "---> 6. Importe producto 2 \n"
                "---> 7. Cantidad producto 2 \n"
                "---> 8. salir \n")
            op_edit_fact = input("Introduzca nº: ")
            print("\n")

            if op_edit_fact == '1':
                cliente = input("Nuevo cliente: ")

                # datos[index][1] = cliente

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'CLIENTE', cliente, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '2':
                prod1 = input("Nuevo producto 1: ")

                # datos[index][1] = prod1

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'PROD1', prod1, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '3':
                imp_prod1 = input("Nuevo importe producto 1: ")

                # datos[index][1] = imp_prod1

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'IMP_PROD1', imp_prod1, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '4':
                cant_prod1 = input("Nueva cantidad producto 1: \n")

                # datos[index][1] = cant_prod1

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'CANT_PROD1', cant_prod1, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '5':
                prod2 = input("Nuevo producto 2: ")

                # datos[index][1] = prod2

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'PROD2', prod2, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '6':
                imp_prod2 = input("Nuevo importe producto 2: ")

                # datos[index][1] = imp_prod2

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'IMP_PROD2', imp_prod2, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '7':
                cant_prod2 = input("Nueva cantidad producto 2: \n")

                # datos[index][1] = cant_prod2

                # escritura_datos(ruta_ventas, datos, 'w')
                actualizar_tupla_tabla('VENTA', 'CANT_PROD2', cant_prod2, 'NUM_FACT', datos[index][0])
                factura_modificada = True

            elif op_edit_fact == '8':
                factura_modificada = False
            else:
                print("¡Introduzca valor válido! (1 al 8)")

        if factura_modificada:
            print("¡Factura modificada! \n")
        else:
            print("¡Error al modificar factura! ")
            print("Saliendo de editar factura.. \n")

    def anular_factura_venta():

        factura_tst = False
        factura_anulada = False
        index = -1

        num_factura = input("Introduzca número factura (acceda a -Mostrar facturas- primero): ")

        datos = lectura_datos(ruta_ventas)

        for fila in datos:
            for campo in fila:
                if campo == num_factura:
                    index = datos.index(fila)
                    factura_tst = True

        # eliminar en BD orden equivalente a num_orden
        if factura_tst:
            # eliminamos tupla del usuario si el usuario existe en nuestra BD
            # datos.remove(datos[index])
            borrar_tupla_tabla('VENTA', 'NUM_FACT', datos[index][0])
            factura_anulada = True

            # reescribimos el archivo de usuarios
            # escritura_datos(ruta_ventas, datos, 'w')

        if factura_anulada:
            print("Factura anulada! \n")
        else:
            print("¡Error al anular factura! ")
            print("Saliendo de anular factura.. \n")

    def mostrar_facturas():
        # datos = lectura_datos(ruta_ventas)
        datos = cargar_datos_tabla('VENTA')

        for factura in datos:
            print(factura)

        print("¡facturas cargadas! \n")

    opventas = '0'
    while opventas != '5':
        print(
            "Menú del departamento de Ventas: \n"
            "---> 1. Crear factura de venta \n"
            "---> 2. Editar factura de venta \n"
            "---> 3. Anular factura de venta \n"
            "---> 4. Mostrar facturas de ventas \n"
            "---> 5. salir \n")

        opventas = input("Introduzca nº: ")
        print("\n")

        if opventas == '1':
            crear_factura_venta()
        elif opventas == '2':
            editar_factura_venta()
        elif opventas == '3':
            anular_factura_venta()
        elif opventas == '4':
            mostrar_facturas()
        elif opventas == '5':
            print("saliendo de ventas.. \n")
        else:
            print("¡Introduzca valor válido! (1 al 5) \n")


def produccion():
    ruta_produccion = './datos_produccion/objetivosAnyo.csv'

    def crear_obj_mens():
        cant_obj = input("Introduzca cantidad de unidades objetivo: ")
        mes = input("Introduzca mes a aplicar objetivo: ")

        # controlamos que campos vacíos tomen valor guión bajo ( _ )
        if cant_obj == '':
            cant_obj = '_'

        # procedimiento para almacenar datos (BD o Archivo)
        objetivo_creado = False

        if mes != '':
            # datos = [[mes, cant_obj, '_', '_']]
            # objetivo_creado = escritura_datos(ruta_produccion, datos, 'a')

            datos = [mes, int(cant_obj), 0, 0]
            insertar_datos_tabla_objetivo(datos)

            objetivo_creado = True
        else:
            print("¡Debe dar un valor válido para mes!")

        if objetivo_creado:
            print("¡Objetivo creado! \n")
        else:
            print("¡Error al crear objetivo! ")
            print("Saliendo de crear objetivo.. \n")

    def editar_obj_mens():

        objt_tst = False
        index = -1
        objetivo_editado = False

        mes_objetivo = input("Introduzca mes de objetivos: \n")

        # procedimiento para almacenar datos (BD o Archivo)
        # datos = lectura_datos(ruta_produccion)
        datos = cargar_datos_tabla('OBJETIVO')

        for fila in datos:
            for campo in fila:
                if campo == mes_objetivo:
                    index = datos.index(fila)
                    objt_tst = True

        if objt_tst:

            objetivo = datos[index][1]

            print("Cantidad objetivo para el mes seleccionado: " + str(objetivo))

            nuevo_obj = input("Introduzca nueva cantidad para mes seleccionado: \n")

            if nuevo_obj == '':
                nuevo_obj = '_'

            # datos[index][1] = nuevo_obj
            # escritura_datos(ruta_produccion, datos, 'w')

            actualizar_tupla_tabla('OBJETIVO', 'UDS_OBJ', nuevo_obj, 'MES_ANYO', datos[index][0])
            objetivo_editado = True

        if objetivo_editado:
            print("¡Objetivo editado! \n")
        else:
            print("¡Error al editar objetivo! ")
            print("Saliendo de editar objetivo.. \n")

    def anular_obj_mens():

        objt_tst = False
        objetivo_anulado = False
        index = -1

        mes_objetivo = input("Introduzca mes de objetivos: \n")

        # procedimiento para almacenar datos (BD o Archivo)
        # datos = lectura_datos(ruta_produccion)
        datos = cargar_datos_tabla('OBJETIVO')

        for fila in datos:
            for campo in fila:
                if campo == mes_objetivo:
                    index = datos.index(fila)
                    objt_tst = True

        if objt_tst:
            # datos.remove(datos[index])

            # escritura_datos(ruta_produccion, datos, 'w')

            borrar_tupla_tabla('OBJETIVO', 'MES_ANYO', datos[index][0])
            objetivo_anulado = True

        if objetivo_anulado:
            print("¡Objetivo anulado! \n")
        else:
            print("¡Error al anular objetivo! ")
            print("Saliendo de anular objetivo.. \n")

    def crear_cal_mens():

        cal_tst = False
        index = -1

        mes = input("Introduzca mes a aplicar calendario: ")
        dias_laborables = input("Introduzca cantidad días laborables: ")
        turnos_trabajo = input("Introduzca cantidad turnos por mes: ")

        if dias_laborables == '':
            dias_laborables = '_'

        if turnos_trabajo == '':
            turnos_trabajo = '_'

        # procedimiento para almacenar datos (BD o Archivo)
        calendario_creado = False

        # datos = lectura_datos(ruta_produccion)
        datos = cargar_datos_tabla('OBJETIVO')

        if mes != '':
            for fila in datos:
                for campo in fila:
                    if campo == mes:
                        index = datos.index(fila)
                        cal_tst = True

        if cal_tst:
            # datos[index][2] = dias_laborables
            # datos[index][3] = turnos_trabajo

            # escritura_datos(ruta_produccion, datos, 'w')

            actualizar_tupla_tabla('OBJETIVO', 'DIAS_LAB', int(dias_laborables), 'MES_ANYO', datos[index][0])
            actualizar_tupla_tabla('OBJETIVO', 'TURNOS', int(turnos_trabajo), 'MES_ANYO', datos[index][0])

            calendario_creado = True

        if calendario_creado:
            print("¡Calendario creado! \n")
        else:
            print("¡Error al crear calendario! ")
            print("Saliendo de crear calendario.. \n")

    def editar_cal_mens():

        cal_tst = False
        index = -1

        mes_objetivo = input("Introduzca mes: ")

        # procedimiento para almacenar datos (BD o Archivo)
        # datos = lectura_datos(ruta_produccion)
        datos = cargar_datos_tabla('OBJETIVO')

        for fila in datos:
            for campo in fila:
                if campo == mes_objetivo:
                    index = datos.index(fila)
                    cal_tst = True

        if cal_tst:
            dias_lab = datos[index][2]
            turnos = datos[index][3]

            print("Cantidad días laborables para el mes seleccionado: " + str(dias_lab))
            print("Cantidad turnos para el mes seleccionado: " + str(turnos) + " \n")

        op = input("Desea cambiar los días (1), los turnos (2) o ambos (3): ")
        if op == '1':
            nuevo_dias = input("Introduzca nueva cantidad días laborables para mes seleccionado: ")

            # datos[index][2] = nuevo_dias
            # escritura_datos(ruta_produccion, datos, 'w')

            actualizar_tupla_tabla('OBJETIVO', 'DIAS_LAB', int(nuevo_dias), 'MES_ANYO', datos[index][0])

            cal_mens_editado = True

        elif op == '2':
            nuevo_turnos = input("Introduzca nueva cantidad turnos para mes seleccionado: ")

            # datos[index][3] = nuevo_turnos
            # escritura_datos(ruta_produccion, datos, 'w')

            actualizar_tupla_tabla('OBJETIVO', 'TURNOS', int(nuevo_turnos), 'MES_ANYO', datos[index][0])

            cal_mens_editado = True

        elif op == '3':
            nuevo_dias = input("Introduzca nueva cantidad días laborables para mes seleccionado: ")
            nuevo_turnos = input("Introduzca nueva cantidad turnos para mes seleccionado: ")

            # datos[index][2] = nuevo_dias
            # datos[index][3] = nuevo_turnos

            # escritura_datos(ruta_produccion, datos, 'w')

            actualizar_tupla_tabla('OBJETIVO', 'DIAS_LAB', int(nuevo_dias), 'MES_ANYO', datos[index][0])
            actualizar_tupla_tabla('OBJETIVO', 'TURNOS', int(nuevo_turnos), 'MES_ANYO', datos[index][0])

            cal_mens_editado = True
        else:
            print("¡Debe elegir un valor correcto (del 1 al 3)!")
            cal_mens_editado = False

        # carga en BD

        if cal_mens_editado:
            print("¡objetivo editado! \n")
        else:
            print("¡Error al editar objetivo! ")
            print("Saliendo de editar objetivo.. \n")

    def anular_cal_mens():

        cal_tst = False
        cal_mens_anulado = False
        index = -1

        mes_objetivo = input("Introduzca mes: \n")

        # procedimiento para almacenar datos (BD o Archivo)
        # datos = lectura_datos(ruta_produccion)
        datos = cargar_datos_tabla('OBJETIVO')

        for fila in datos:
            for campo in fila:
                if campo == mes_objetivo:
                    index = datos.index(fila)
                    cal_tst = True

        if cal_tst:
            # datos[index][2] = '_'
            # datos[index][3] = '_'

            # escritura_datos(ruta_produccion, datos, 'w')
            actualizar_tupla_tabla('OBJETIVO', 'DIAS_LAB', 0, 'MES_ANYO', datos[index][0])
            actualizar_tupla_tabla('OBJETIVO', 'TURNOS', 0, 'MES_ANYO', datos[index][0])

            cal_mens_anulado = True

        if cal_mens_anulado:
            print("¡Calendario mes anulado! \n")
        else:
            print("¡Error al editar calendario mes! ")
            print("Saliendo de calendario mes.. \n")

    def mostrar_obj_mens():
        # datos = lectura_datos(ruta_produccion)
        datos = cargar_datos_tabla('OBJETIVO')

        for objetivo in datos:
            print(objetivo)

        print("¡producción cargada! \n")

    opprod = '0'
    while opprod != '8':
        print(
            "Menú del departamento de Producción: \n"
            "---> 1. Crear objetivo mensual de producción \n"
            "---> 2. Editar objetivo mensual de producción \n"
            "---> 3. Anular objetivo mensual de producción \n"
            "---> 4. Crear calendario mensual producción \n"
            "---> 5. Editar calendario mensual producción \n"
            "---> 6. Anular calendario mensual producción \n"
            "---> 7. Mostrar objetivos mensuales de producción \n"
            "---> 8. salir \n")

        opprod = input("Introduzca nº: ")
        print("\n")

        if opprod == '1':
            crear_obj_mens()
        elif opprod == '2':
            editar_obj_mens()
        elif opprod == '3':
            anular_obj_mens()
        elif opprod == '4':
            crear_cal_mens()
        elif opprod == '5':
            editar_cal_mens()
        elif opprod == '6':
            anular_cal_mens()
        elif opprod == '7':
            mostrar_obj_mens()
        elif opprod == '8':
            print("saliendo de producción.. \n")
        else:
            print("¡Introduzca valor válido! (1 al 8) \n")


def finanzas():
    ruta_finanzas = './datos_finanzas/balancesAnyo.csv'
    sociedades = 29  # 29% impuesto sociedades

    def crear_balance():

        balance_creado = False
        ingresos = 0
        gastos = 0
        # beneficio_neto = 0
        # beneficio_bruto = 0

        mes = input("Introduzca mes de balance: ")

        try:
            ingresos = float(input("Introduzca monto total de ingresos: "))
            gastos = float(input("Introduzca monto total de gastos: "))

            # beneficio_bruto = ingresos - gastos
            # beneficio_neto = beneficio_bruto - (beneficio_bruto * sociedades)

        except:
            print("Debe dar valores válidos (Ingresos y gastos -> numéricos)")

        # BD

        if mes != '':
            # datos = [[mes, ingresos, gastos, sociedades, beneficio_bruto, beneficio_neto]]
            # escritura_datos(ruta_finanzas, datos, 'a')
            datos = [mes, ingresos, gastos, sociedades]
            insertar_datos_tabla_balance(datos)
            balance_creado = True

        if balance_creado:
            print("¡Balance creado! \n")
        else:
            print("¡Error al crear balance! ")
            print("Saliendo de crear balance.. \n")

    def editar_balance():

        bal_editado = False
        bal_tst = False
        index = -1

        mes = input("Introduzca mes de balance a editar: ")

        # BD
        # datos = lectura_datos(ruta_finanzas)
        datos = cargar_datos_tabla('BALANCE')

        for fila in datos:
            for campo in fila:
                if campo == mes:
                    index = datos.index(fila)
                    bal_tst = True

        if bal_tst:

            ingresos = float(datos[index][1])
            gastos = float(datos[index][2])

            print("Monto ingresos total para el mes seleccionado: " + str(ingresos))
            print("Monto gastos total para el mes seleccionado: " + str(gastos))

            op = input("Desea cambiar los ingresos (1), los gastos (2) o ambos(3): ")
            if op == '1':
                nuevo_ingresos = input("Introduzca nueva cantidad ingresos para mes seleccionado: \n")

                if nuevo_ingresos != '':

                    '''
                    # Recálculo beneficios
                    beneficio_bruto = float(nuevo_ingresos) - gastos
                    beneficio_neto = beneficio_bruto - (beneficio_bruto * sociedades)

                    datos[index][1] = nuevo_ingresos
                    datos[index][4] = beneficio_bruto
                    datos[index][5] = beneficio_neto

                    bal_editado = escritura_datos(ruta_finanzas, datos, 'w')
                    '''

                    actualizar_tupla_tabla('BALANCE', 'INGRESOS', nuevo_ingresos, 'MES_ANYO', datos[index][0])
                    bal_editado = True
                else:
                    print("Debe dar valores válidos (Ingresos y gastos -> numéricos)")

            elif op == '2':
                nuevo_gastos = input("Introduzca nueva cantidad gastos para mes seleccionado: \n")

                if nuevo_gastos != '':

                    '''
                    # Recálculo beneficios
                    beneficio_bruto = ingresos - float(nuevo_gastos)
                    beneficio_neto = beneficio_bruto - (beneficio_bruto * sociedades)

                    datos[index][2] = nuevo_gastos
                    datos[index][4] = beneficio_bruto
                    datos[index][5] = beneficio_neto

                    bal_editado = escritura_datos(ruta_finanzas, datos, 'w')
                    '''

                    actualizar_tupla_tabla('BALANCE', 'GASTOS', nuevo_gastos, 'MES_ANYO', datos[index][0])
                    bal_editado = True
                else:
                    print("Debe dar valores válidos (Ingresos y gastos -> numéricos)")

            elif op == '3':
                nuevo_ingresos = input("Introduzca nueva cantidad ingresos para mes seleccionado: ")
                nuevo_gastos = input("Introduzca nueva cantidad gastos para mes seleccionado: ")

                if nuevo_gastos != '' and nuevo_ingresos != '':

                    '''
                    # Recálculo beneficios
                    beneficio_bruto = float(nuevo_ingresos) - float(nuevo_gastos)
                    beneficio_neto = beneficio_bruto - (beneficio_bruto * sociedades)

                    datos[index][1] = nuevo_ingresos
                    datos[index][2] = nuevo_gastos
                    datos[index][4] = beneficio_bruto
                    datos[index][5] = beneficio_neto

                    bal_editado = escritura_datos(ruta_finanzas, datos, 'w')
                    '''

                    actualizar_tupla_tabla('BALANCE', 'INGRESOS', nuevo_ingresos, 'MES_ANYO', datos[index][0])
                    actualizar_tupla_tabla('BALANCE', 'GASTOS', nuevo_gastos, 'MES_ANYO', datos[index][0])
                    bal_editado = True

                else:
                    print("Debe dar valores válidos (Ingresos y gastos -> numéricos)")
            else:
                print("¡Debe elegir un valor correcto (del 1 al 3)!")

        if bal_editado:
            print("¡Balance editado! \n")
        else:
            print("¡Error al editar balance! ")
            print("Saliendo de editar balance.. \n")

    def anular_balance():

        bal_tst = False
        balance_anulado = False
        index = -1

        mes = input("Introduzca mes de balance: ")

        # BD
        # datos = lectura_datos(ruta_finanzas)
        datos = cargar_datos_tabla('BALANCE')

        for fila in datos:
            for campo in fila:
                if campo == mes:
                    index = datos.index(fila)
                    bal_tst = True

        if bal_tst:
            # datos.remove(datos[index])
            # balance_anulado = escritura_datos(ruta_finanzas, datos, 'w')
            borrar_tupla_tabla('BALANCE', 'MES_ANYO', datos[index][0])
            balance_anulado = True

        if balance_anulado:
            print("¡Balance anulado! \n")
        else:
            print("¡Error al anular balance! ")
            print("Saliendo de anular balance.. \n")

    def mostrar_balances():

        # datos = lectura_datos(ruta_finanzas)
        datos = cargar_datos_tabla('BALANCE')

        for objetivo in datos:
            print(objetivo)

        print("¡Balances cargados! \n")

    def mostrar_facturas_fin():
        # datos = lectura_datos(ruta_ventas)
        datos = cargar_datos_tabla('VENTA')

        for factura in datos:
            print(factura)

        print("¡facturas cargadas! \n")

    opfin = '0'
    while opfin != '6':
        print(
            "Menú del departamento de Finanzas: \n"
            "---> 1. Crear balance \n"
            "---> 2. Editar balance \n"
            "---> 3. Anular balance \n"
            "---> 4. Mostrar facturas venta \n"
            "---> 5. Mostrar balances\n"
            "---> 6. salir \n")

        opfin = input("Introduzca nº: ")
        print("\n")

        if opfin == '1':
            crear_balance()
        elif opfin == '2':
            editar_balance()
        elif opfin == '3':
            anular_balance()
        elif opfin == '4':
            mostrar_facturas_fin()
        elif opfin == '5':
            mostrar_balances()
        elif opfin == '6':
            print("saliendo de finanzas.. \n")
        else:
            print("¡Introduzca valor válido! (1 al 6) \n")


# ------------------------------------LÓGICA ERP


def gestion_usuarios():
    def alta_usuario():
        user = str(input("Introduzca nombre de usuario: "))
        contrasenya = str(input("Introduzca contraseña: "))
        rol = int(input("Introduzca rol -> 1 al 5: "))

        user_creado = False

        if user == '':
            user = '_'

        if contrasenya == '':
            contrasenya = '_'

        if rol == '':
            rol = '_'

        # BD
        if user != '_':
            datos = [user, contrasenya, rol]
            # user_creado = escritura_datos(ruta_usuarios, datos, 'a')
            insertar_datos_tabla_usuario(datos)
            user_creado = True
        else:
            print("Debe dar algún valor a usuario")

        if user_creado:
            print("¡Usuario creado! \n")
        else:
            print("¡Error al crear usuario! ")
            print("Saliendo de crear usuario.. \n")

    def baja_usuario():
        user = input("Introduzca nombre de usuario: ")

        user_tst = False
        user_eliminado = False
        index = -1

        # Aquí comprobación de datos con BD. Cargamos variable ROL
        # datos = lectura_datos(ruta_usuarios)
        datos = cargar_datos_tabla('USUARIO')

        for fila in datos:
            for campo in fila:
                if campo == user:
                    index = datos.index(fila)
                    user_tst = True

        if user_tst:
            # eliminamos tupla del usuario si el usuario existe en nuestra BD
            # datos.remove(datos[index])
            borrar_tupla_tabla('USUARIO', 'NOM_USER', datos[index][0])
            user_eliminado = True

            # reescribimos el archivo de usuarios
            # escritura_datos(ruta_usuarios, datos, 'w')

        if user_eliminado:
            print("¡Usuario eliminado! \n")
        else:
            print("¡Error al eliminar usuario! ")
            print("Saliendo de eliminar usuario.. \n")

    def modificar_usuario():

        user_tst = False
        index = -1
        usuario_editado = False

        user = input("Introduzca nombre de usuario: ")

        # Aquí comprobación de datos con BD. Cargamos variable ROL
        # datos = lectura_datos(ruta_usuarios)
        datos = cargar_datos_tabla('USUARIO')

        for fila in datos:
            for campo in fila:
                if campo == user:
                    index = datos.index(fila)
                    user_tst = True

        if user_tst:

            contrasenya = datos[index][1]
            rol = datos[index][2]

            user_cargado = True

            print("Usuario: " + user)
            print("Contraseña: " + contrasenya)
            print("Rol: " + str(rol) + "\n")

            op = input("Desea cambiar el usuario (1), la contraseña (2), el rol (3) o todos (4): ")
            if op == '1':
                nuevo_user = input("Introduzca nuevo usuario: ")
                # datos[index][0] = nuevo_user
                actualizar_tupla_tabla('USUARIO', 'NOM_USER', nuevo_user, 'NOM_USER', datos[index][0])

                # escritura_datos(ruta_usuarios, datos, 'w')
                usuario_editado = True

            elif op == '2':
                nueva_pass = input("Introduzca nueva contraseña: ")
                # datos[index][1] = nueva_pass
                actualizar_tupla_tabla('USUARIO', 'USER_PASS', nueva_pass, 'NOM_USER', datos[index][0])

                # escritura_datos(ruta_usuarios, datos, 'w')
                usuario_editado = True

            elif op == '3':
                nuevo_rol = input("Introduzca nuevo rol: ")
                # datos[index][2] = nuevo_rol
                actualizar_tupla_tabla('USUARIO', 'ROL', nuevo_rol, 'NOM_USER', datos[index][0])

                # escritura_datos(ruta_usuarios, datos, 'w')
                usuario_editado = True

            elif op == '4':
                nuevo_user = input("Introduzca nuevo usuario: ")
                # datos[index][0] = nuevo_user
                actualizar_tupla_tabla('USUARIO', 'NOM_USER', nuevo_user, 'NOM_USER', datos[index][0])

                nueva_pass = input("Introduzca nueva contraseña: ")
                # datos[index][1] = nueva_pass
                actualizar_tupla_tabla('USUARIO', 'USER_PASS', nueva_pass, 'NOM_USER', nuevo_user)

                nuevo_rol = input("Introduzca nuevo rol: ")
                # datos[index][2] = nuevo_rol
                actualizar_tupla_tabla('USUARIO', 'ROL', nuevo_rol, 'NOM_USER', nuevo_user)

                # escritura_datos(ruta_usuarios, datos, 'w')
                usuario_editado = True

            else:
                print("¡Debe elegir un valor correcto (del 1 al 4)!")
                usuario_editado = False

        else:
            user_cargado = False

        if user_cargado and usuario_editado:
            print("¡Usuario modificado! \n")
        else:
            print("¡Error al modificar usuario! ")
            print("Saliendo de modificar usuario.. \n")

    def ver_usuarios():
        # datos = lectura_datos(ruta_usuarios)
        datos = cargar_datos_tabla('USUARIO')

        for usuario in datos:
            print(usuario)

        print("¡Usuarios cargados! \n")

    opgest = '0'
    while opgest != '5':
        print(
            "Menú gestión usuarios: \n"
            "---> 1. Alta usuario \n"
            "---> 2. baja usuario \n"
            "---> 3. modificar usuario \n"
            "---> 4. Ver usuarios \n"
            "---> 5. salir \n")

        opgest = input("Introduzca nº: ")
        print("\n")

        if opgest == '1':
            alta_usuario()
        elif opgest == '2':
            baja_usuario()
        elif opgest == '3':
            modificar_usuario()
        elif opgest == '4':
            ver_usuarios()
        elif opgest == '5':
            print("saliendo de gestión usuarios.. \n")
        else:
            print("¡Introduzca valor válido! (1 al 5) \n")


def menu_admin():
    opcion = '0'
    while opcion != '6':
        print(
            "Elige departamento: \n"
            "---> 1. Compras \n"
            "---> 2. Ventas (Facturación) \n"
            "---> 3. Producción (Gestión mensual objetivos)\n"
            "---> 4. Finanzas \n"
            "---> 5. Gestión Usuarios \n"
            "---> 6. salir \n")

        opcion = input("Introduzca nº: ")
        print("\n")

        if opcion == '1':
            compras()
        elif opcion == '2':
            ventas()
        elif opcion == '3':
            produccion()
        elif opcion == '4':
            finanzas()
        elif opcion == '5':
            gestion_usuarios()
        elif opcion == '6':
            print("saliendo de menú admin.. \n")
        else:
            print("¡Introduzca valor válido! (1 al 6) \n")


def login():
    rol = ''
    user_tst = False
    pass_tst = False
    index = -1
    pass_almacenada = ''

    print("Bienvenido a ERP Solutions: \n")

    user = input("Introduzca nombre de usuario: ")

    contrasenya = input("Introduzca contraseña: ")

    # Aquí comprobación de datos con BD. Cargamos variable ROL
    # datos = lectura_datos(ruta_usuarios) -> ERP CON ARCHIVOS CSV
    datos = cargar_datos_tabla('USUARIO')

    if datos:
        for fila in datos:
            for campo in fila:
                if campo == user:
                    index = datos.index(fila)
                    user_tst = True

    if user_tst:
        pass_almacenada = datos[index][1]

    if contrasenya == pass_almacenada:
        pass_tst = True
        rol = str(datos[index][2])

    # Determinamos que menú mostrar según ROL
    if user_tst and pass_tst:
        if rol == '1':
            compras()
        elif rol == '2':
            ventas()
        elif rol == '3':
            produccion()
        elif rol == '4':
            finanzas()
        elif rol == '5':
            menu_admin()
    elif datos:
        print("\n")
        print("¡Usuario o contraseña erróneo!")


# ----------------------------------CONEXIÓN CON BD


def conectar_bd():
    db = pymysql.connect(host="127.0.0.1", user="root", db="practica3", port=3306)
    # Preparar el cursor
    cursor = db.cursor()

    '''
    # Ejecutar SQL de prueba
    cursor.execute("SELECT VERSION()")
    # Recuperar una fila usando fetchone()
    dato = cursor.fetchone()
    print("Versión de BD: % s " % dato)
    '''

    return db


def desconectar_bd(db):
    db.close()


# --------------------------------RECUPERAR DATOS DESDE BD


def cargar_datos_tabla(tabla):
    # Conexión con BD
    bd = conectar_bd()
    cursor = bd.cursor()

    # SQL para cargar tabla
    sql = "SELECT * FROM %s" % tabla
    try:
        cursor.execute(sql)

        datos = cursor.fetchall()

    except:

        print("Error: no se han podido recuperar datos")
        datos = []

    # Desconexión de la BD
    desconectar_bd(bd)

    return datos


# ------------------------------INSERTAR DATOS EN BD

def insertar_datos_tabla_usuario(datos):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para insertar datos
    sql = """INSERT INTO USUARIO(NOM_USER, USER_PASS, ROL) VALUES\
          ('%s', '%s', '%d')""" \
          % (datos[0], datos[1], datos[2])
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


def insertar_datos_tabla_compra(datos):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para insertar datos
    sql = """INSERT INTO COMPRA(NUM_ORD, DPTO_SOLCT, PROD1, CANT_PROD1, PROD2, CANT_PROD2) VALUES\
          ('%s', '%s', '%s', '%d', '%s', '%d' )""" \
          % (datos[0], datos[1], datos[2], datos[4], datos[3], datos[5])
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


def insertar_datos_tabla_venta(datos):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para insertar datos
    sql = """INSERT INTO VENTA(NUM_FACT, CLIENTE, PROD1, CANT_PROD1, IMP_PROD1, PROD2, CANT_PROD2, IMP_PROD2) VALUES\
          ('%d', '%s', '%s', '%d', '%f', '%s', '%d', '%f' )""" \
          % (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7])
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


# PRODUCCIÓN
def insertar_datos_tabla_objetivo(datos):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para insertar datos
    sql = """INSERT INTO OBJETIVO(MES_ANYO, UDS_OBJ, DIAS_LAB, TURNOS) VALUES\
          ('%s', '%d', '%d', '%d')""" \
          % (datos[0], datos[1], datos[2], datos[3])
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


# FINANZAS
def insertar_datos_tabla_balance(datos):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para insertar datos
    sql = """INSERT INTO BALANCE(MES_ANYO, INGRESOS, GASTOS, IMP_SOC) VALUES\
          ('%s', '%f', '%f', '%d')""" \
          % (datos[0], datos[1], datos[2], datos[3])
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


# -----------------------------BORRAR DATOS EN BD


def borrar_tupla_tabla(tabla, clave, valor):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para borrar datos
    sql = "DELETE FROM %s WHERE %s = '%s'" % (tabla, clave, valor)
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


# ..............................ACTUALIZAR DATOS EN BD

def actualizar_tupla_tabla(tabla, campo, valor_campo, clave, valor_clave):
    db = conectar_bd()
    cursor = db.cursor()

    # Consulta SQL para borrar datos
    sql = "UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(tabla, campo, valor_campo, clave, valor_clave)
    # print(sql)

    try:
        # Ejecutar el comando SQL
        cursor.execute(sql)
        # Aceptar cambios con commit
        db.commit()
    except:
        # Rollback en caso de haber algún error
        db.rollback()


login()

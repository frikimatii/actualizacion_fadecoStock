import sqlite3
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def sort_column_alpha(tree, col, reverse):
    items = [(tree.set(item, col), item) for item in tree.get_children("")]
    items.sort(reverse=reverse)

    # Reorganiza los elementos en la tabla
    for index, (val, item) in enumerate(items):
        tree.move(item, "", index)

    # Cambia la dirección de la ordenación
    tree.heading(col, command=lambda: sort_column_alpha(tree, col, not reverse))



def sort_column_alphanumeric(tree, col, reverse):
    items = [(tree.set(item, col), item) for item in tree.get_children("")]
    items.sort(key=lambda x: (float('inf') if x[0].isalpha() else float(x[0]), x[0]), reverse=reverse)

    # Reorganiza los elementos en la tabla
    for index, (_, item) in enumerate(items):
        tree.move(item, "", index)

    # Cambia la dirección de la ordenación para el próximo clic
    tree.heading(col, command=lambda: sort_column_alphanumeric(
        tree, col, not reverse))


def obtener_color_fondo(cantidad):
    if cantidad < 10:
        return "#ff6868"
    elif cantidad > 50:
        return "#87ff79"
    else:
        return ""
    

def mostrar_datos(treeview, table, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT piezas, cantidad FROM {table}")
    datos = cursor.fetchall()
    conn.close()

    # Limpiar la tabla antes de agregar nuevos datos
    for item in treeview.get_children():
        treeview.delete(item)

    # Agregar elementos a la lista con cantidades y aplicar colores
    for pieza, cantidad in datos:
        color_fondo = obtener_color_fondo(cantidad)
        treeview.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
        
    tabla_personalizada = {
    "armado_final": "Armado Final",
    "buen_hombre_pulido": "Stock Buen Hombre",
    "carmelo_pulido": "Stock Carmelo",
    "chapa": "Chapa",
    "maxi_pulido": "Stock Maxi",
    "pieza_retocadas": "Piezas Retocadas",
    "piezas_del_fundicion": "Piezas del Fundición",
    "piezas_del_motor_final": "Piezas del Motor Final",
    "piezas_finales_defenitivas": "Piezas Terminadas",
    "producto_final": "Producto Final",
    "soldador_stock": "Stock En Bruto",
}
    table_seleccionada = ["armado_final", "buen_hombre_pulido", "carmelo_pulido", "chapa", "maxi_pulido", "pieza_retocadas", "piezas_del_fundicion", "piezas_del_motor_final", "piezas_finales_defenitivas", "producto_final", "soldador_stock"]
    for tabla in table_seleccionada:
    # Obtén el texto personalizado correspondiente al nombre original de la tabla
        texto_personalizado = tabla_personalizada.get(tabla, table)
        txt = texto_personalizado
        info.config(text=txt) 


def sort_column(tree, col, reverse):
    items = [(float(tree.set(item, col)), item) for item in tree.get_children("")]
    items.sort(reverse=reverse)

    # Reorganiza los elementos en la tabla
    for index, (val, item) in enumerate(items):
        tree.move(item, "", index)

    # Cambia la dirección de la ordenación
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


def sort_column_numeric(tree, col, reverse):
    items = [(float(tree.set(item, col)), item)
             for item in tree.get_children("")]
    items.sort(reverse=reverse)

    # Reorganiza los elementos en la tabla
    for index, (val, item) in enumerate(items):
        tree.move(item, "", index)

    # Cambia la dirección de la ordenación para el próximo clic
    tree.heading(col, command=lambda: sort_column_numeric(
        tree, col, not reverse))



            
#Acrualizar Piezas (agregar)
def actualizar_pieza(lista_predefinida, entrada_cantidad, res, table, funcion, tree, info):
    actualizar_pieza = lista_predefinida.get()
    entrada_actualizar = entrada_cantidad.get()
    

    if entrada_actualizar.strip().isdigit():
        entrada_actualizar = int(entrada_actualizar)

        if entrada_actualizar < 0:
            res.config(text="La Cantidad NO puede ser Negativa")
        else:
            # Mostrar una ventana de confirmación
            confirmacion = messagebox.askyesno("Confirmar", f"¿Desea Agregar la cantidad de {entrada_actualizar} {actualizar_pieza} ?")

            if confirmacion:
                conn = sqlite3.connect("basedatospiezas.db")
                cursor = conn.cursor()
                cursor.execute(
                    f"SELECT cantidad FROM {table} WHERE piezas=?", (actualizar_pieza,)
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is not None:
                    cantidad_actual = cantidad_actual[0]
                    nueva_cantidad = cantidad_actual + entrada_actualizar
                    cursor.execute(
                        f"UPDATE {table} SET cantidad=? WHERE piezas=?", (nueva_cantidad, actualizar_pieza)
                    )
                    conn.commit()
                    conn.close()
                    mostrar_datos(tree, table, info)  # Llama a la función para mostrar los datos actualizados
                    res.insert(
                        0,
                        f"Carga exitosa: Usted cargó {entrada_actualizar} {actualizar_pieza}:",
                    )
                else:
                    res.insert(
                        0, f"La Pieza {actualizar_pieza} no se puede modificar"
                    )
    else:
        res.insert(0, "La cantidad ingresada no es un número válido")
        
    entrada_cantidad.delete(0, 'end')
        
        
#eliminar_piez(combox, cantida list tabla , funcion , arbol)
def eliminar_pieza(
    lista_predefinida_eliminar, entrada_cantidad_eliminar, res, table, funcion, tree, info
):
    pieza_eliminar = lista_predefinida_eliminar.get()
    cantidad_eliminar = entrada_cantidad_eliminar.get()

    try:
        cantidad_eliminar = int(cantidad_eliminar)
        if cantidad_eliminar < 0:
            raise ValueError("La cantidad no puede ser negativa.")
    except :
        res.insert(0, f"Error Ingrese un numero")
        return

    # Mostrar una ventana de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea eliminar {cantidad_eliminar} unidades de {pieza_eliminar}?")

    if confirmacion:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                f"SELECT cantidad FROM {table} WHERE piezas=?", (pieza_eliminar,)
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]
                if cantidad_eliminar <= cantidad_actual:
                    nueva_cantidad = cantidad_actual - cantidad_eliminar
                    if nueva_cantidad >= 0:
                        cursor.execute(
                            f"UPDATE {table} SET cantidad=? WHERE piezas=?",
                            (nueva_cantidad, pieza_eliminar),
                        )
                        res.insert(
                            0,
                            f" Descarga exitosa: se eliminaron {cantidad_eliminar} unidades de {pieza_eliminar}.",
                        )
                    else:
                        res.insert(0, f"No se puede eliminar la cantidad especificada de {pieza_eliminar}.")
                else:
                    res.insert(0, f"No hay suficientes unidades de {pieza_eliminar} en el stock.")
            else:
                res.insert(0, f"La pieza {pieza_eliminar} no se puede encontrar en la tabla {table}.")
        except sqlite3.Error as e:
            res.insert(0, f"Error en la base de datos: {e}")
        finally:
            conn.commit()
            conn.close()
            
        entrada_cantidad_eliminar.delete(0, 'end')
    
    
    # ---------------funciones de stock de chapas _________________________________________________
    
def mostrar_datos_chapa(tree1, table, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT piezas, cantidad, modelo, tipo_de_base FROM {table}")
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)

    subtitulo_text = "Stock Completo"
    subtitulo.config(text=subtitulo_text)


def consulta_de_piezas(tabla, tipo_de_base, modelo, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM chapa WHERE tipo_de_base = 'acero_dulce' AND modelo IN (?, ?) UNION SELECT piezas, cantidad FROM chapa WHERE tipo_de_base = ? AND modelo = ?;",
        ("pieza", modelo, tipo_de_base, modelo),
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for dato in datos:
        tabla.insert("", "end", values=dato)

    subtitulo_text = f"Mostrando {tipo_de_base} {modelo}"
    subtitulo.config(text=subtitulo_text)


def consulta_de_piezas_eco(tabla, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM chapa WHERE especial = 'eco' ",
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for dato in datos:
        tabla.insert("", "end", values=dato)

    subtitulo_text = f"Mostrando Eco"
    subtitulo.config(text=subtitulo_text)

def consulta_cabezales(tabla, tipo_de_base, modelo, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM chapa WHERE tipo_de_base = ? AND modelo = ? AND piezas IN ('chapa_U_cabezal', 'tapa_cabezal', 'bandeja_cabezal')",
        (tipo_de_base, modelo),
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for dato in datos:
        tabla.insert("", "end", values=dato)

    subtitulo_text = f"Mostrando {tipo_de_base} {modelo}"
    subtitulo.config(text=subtitulo_text)


def stock_chapa(tabla, tipo_de_base, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad, modelo FROM chapa WHERE tipo_de_base = ?",
        (tipo_de_base,),
    )
    datos = cursor.fetchall()
    conn.close()

    for item in tabla.get_children():
        tabla.delete(item)
    for dato in datos:
        tabla.insert("", "end", values=dato)

    subtitulo_text = f"Mostrando {tipo_de_base}"
    subtitulo.config(text=subtitulo_text)


#agregado de chapa
def agregar_pieza_chapas(
    tipo_var, lista_agregar_chapa, cantidad_agregar, arbol, tabla, lista_acciones, info
):
    tipo = "acero" if tipo_var.get() == 1 else "pintura"
    pieza = lista_agregar_chapa.get()
    cantidad = cantidad_agregar.get()

    if pieza == "":
        lista_acciones.insert(0, "Elige un tipo de chapa.")
        return
    
    if not cantidad.isdigit() or int(cantidad) < 1:
        lista_acciones.insert(0, "Ingrese una cantidad válida.")
    else:
        # Confirmación antes de realizar cambios en la base de datos
        confirmacion = messagebox.askyesno(
            "Confirmar", 
            f"¿Estás seguro de agregar {cantidad} unidades de {pieza} de {tipo}?"
        )
        if confirmacion:
            try:
                with sqlite3.connect("basedatospiezas.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT cantidad FROM chapa WHERE tipo_de_base = ? AND piezas = ?",
                        (tipo, pieza),
                    )
                    resultado = cursor.fetchone()

                    if resultado is not None:
                        cantidad_existente = resultado[0]
                        cantidad_nueva = cantidad_existente + int(cantidad)
                        cursor.execute(
                            "UPDATE chapa SET cantidad = ? WHERE tipo_de_base = ? AND piezas = ?",
                            (cantidad_nueva, tipo, pieza),
                        )
                    else:
                        cursor.execute(
                            "INSERT INTO chapa (tipo_de_base, piezas, cantidad) VALUES (?, ?, ?)",
                            (tipo, pieza, int(cantidad)),
                        )
                    conn.commit()
                    # Mostrar datos después de la inserción o actualización
                    mostrar_datos(arbol, tabla, info)
                    cantidad_agregar.delete(0, 'end')

            except sqlite3.Error as e:
                lista_acciones.insert(0, f"ERROR EN LA BASE DE DATOS: {str(e)}")
            else:
                lista_acciones.insert(
                    0, f"Carga exitosa: Agregó {cantidad} de {pieza}, de {tipo}"
                )

#eliminar pieza de chapa 
def eliminar_pieza_chapas(
    tipo_var, lista_eliminar_chapa, cantidad_eliminar, arbol, tabla, lista_acciones, info
):
    tipo = tipo_var.get()
    if tipo == 1:
        tipo = "acero"
    elif tipo == 2:
        tipo = "pintura"
    pieza = lista_eliminar_chapa.get()
    cantidad = cantidad_eliminar.get()
    
    if tipo == "":
        lista_acciones.insert(0, "Elige un tipo de chapa.")
        return

    if not cantidad.isdigit() or int(cantidad) < 1:
        lista_acciones.insert(0, "Ingrese una cantidad válida.")
        return

    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT cantidad FROM chapa WHERE tipo_de_base = ? AND piezas = ?",
            (tipo, pieza),
        )
        resultado = cursor.fetchone()

        if resultado is not None:
            cantidad_existente = resultado[0]
            if cantidad_existente >= int(cantidad):
                # Confirmación antes de eliminar piezas
                confirmacion = messagebox.askyesno(
                    "Confirmar", 
                    f"¿Estás seguro de eliminar {cantidad} unidades de {pieza} de {tipo}?"
                )
                if not confirmacion:
                    return  # Si el usuario cancela, no se eliminan las piezas
                
                cantidad_nueva = cantidad_existente - int(cantidad)
                cursor.execute(
                    "UPDATE chapa SET cantidad = ? WHERE tipo_de_base = ? AND piezas = ?",
                    (cantidad_nueva, tipo, pieza),
                )
                conn.commit()
                cantidad_eliminar.delete(0, 'end')
                lista_acciones.insert(
                    0, f"Eliminación exitosa: Eliminó {cantidad} de {pieza} de {tipo}"
                )
            else:
                lista_acciones.insert(
                    0, "No hay suficiente cantidad para eliminar."
                )
        else:
            lista_acciones.insert(
                0, f"La pieza {pieza} no existe en la base de datos."
            )
    except sqlite3.Error as e:
        lista_acciones.insert(0, "ERROR EN LA BASE DE DATOS:", e)
    finally:
        if conn:
            conn.close()
        mostrar_datos(arbol, tabla, info)




def agregar_portaeje(entrada_agregar_porta_eje, tree, tabla, lista_acciones):
    entrada_actualizar = entrada_agregar_porta_eje.get()

    if entrada_actualizar.strip().isdigit():
        entrada_actualizar = int(entrada_actualizar)

        if entrada_actualizar < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM chapa WHERE piezas = 'portaeje' ")
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]
                nueva_cantidad = cantidad_actual + entrada_actualizar
                cursor.execute(
                    f"UPDATE chapa SET cantidad=? WHERE piezas = 'portaeje' ",
                    (nueva_cantidad,),
                )
                conn.commit()
                conn.close()
                mostrar_datos(tree, tabla)
                lista_acciones.insert(
                    0, f"Carga de ejes: {entrada_actualizar}")

            else:
                lista_acciones.insert(0, "Cantidada ingresada invalida")

    else:
        lista_acciones.insert(0, "Ingrese un numero Valido")


def eliminar_portaeje(entrada_eliminar_porta_eje, tree, tabla, lista_acciones):
    entrada_eliminar = entrada_eliminar_porta_eje.get()

    if entrada_eliminar.strip().isdigit():
        entrada_eliminar = int(entrada_eliminar)

        if entrada_eliminar < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM chapa WHERE piezas = 'portaeje' ")
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]
                if cantidad_actual >= entrada_eliminar:
                    nueva_cantidad = cantidad_actual - entrada_eliminar
                    cursor.execute(
                        f"UPDATE chapa SET cantidad=? WHERE piezas = 'portaeje'",
                        (nueva_cantidad,),
                    )
                    conn.commit()
                    conn.close()
                    mostrar_datos(tree, tabla)
                    lista_acciones.insert(
                        0, f"Eliminación de ejes: {entrada_eliminar}")
                else:
                    lista_acciones.insert(
                        0, "No hay suficiente cantidad para eliminar."
                    )
            else:
                lista_acciones.insert(0, "Cantidad ingresada inválida")
    else:
        lista_acciones.insert(0, "Ingrese un número válido")


def calcular_maquinas(maquina, lista_acciones):
    try:
        conn = sqlite3.connect(
            "basedatospiezas.db"
        )  # Reemplaza con el nombre de tu base de datos
        cursor = conn.cursor()

        # Consulta las cantidades de las piezas en la base de datos
        cantidades = {}
        for pieza, cantidad in maquina.items():
            cursor.execute(
                "SELECT cantidad FROM chapa WHERE piezas = ?", (pieza,))
            resultado = cursor.fetchone()
            if resultado is not None:
                cantidad_disponible = resultado[0]
                cantidades[pieza] = cantidad_disponible

        # Calcula la cantidad máxima de máquinas que se pueden armar
        cantidad_maquinas = min(cantidades.values()) // min(maquina.values())
        return lista_acciones.insert(
            0, f"Se pueden armar {cantidad_maquinas} máquinas de acero 330."
        )

    except sqlite3.Error as e:
        print("ERROR EN LA BASE DE DATOS:", e)
        return 0  # En caso de error, devuelve 0 máquinas



def agregar_piezas_faltantes(
    lista_agregar_v_p, cantidad_agregar_v_p, arbol, lista_acciones, tabla, info
):
    pieza_seleccionada = lista_agregar_v_p.get()
    cantidad_ingregar = cantidad_agregar_v_p.get()

    if not pieza_seleccionada:
        lista_acciones.insert(0, "Elige un tipo de Pieza.")
        return

    try:
        cantidad_ingregar = int(cantidad_ingregar)
        if cantidad_ingregar < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            # Ventana de confirmación antes de ejecutar la carga
            confirmacion = messagebox.askyesno(
                "Confirmar", 
                f"¿Estás seguro de agregar {cantidad_ingregar} unidades de {pieza_seleccionada}?"
            )
            if confirmacion:
                conn = sqlite3.connect("basedatospiezas.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT cantidad FROM chapa WHERE piezas=?", (pieza_seleccionada,)
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is not None:
                    cantidad_actual = cantidad_actual[0]
                    nueva_cantidad = cantidad_actual + cantidad_ingregar
                    cursor.execute(
                        "UPDATE chapa SET cantidad=? WHERE piezas=?",
                        (nueva_cantidad, pieza_seleccionada),
                    )
                    conn.commit()
                    conn.close()
                    mostrar_datos(arbol, tabla, info)
                    lista_acciones.insert(
                        0,
                        f"Carga exitosa: Usted cargó {cantidad_ingregar} {pieza_seleccionada}:",
                    )
                    cantidad_agregar_v_p.delete(0, 'end')
                else:
                    lista_acciones.insert(
                        0, f"La Pieza {pieza_seleccionada} no se puede modificar"
                    )
    except ValueError:
        lista_acciones.insert(0, "La cantidad ingresada no es un número válido")        
        
from tkinter import messagebox

def eliminar_piezas_faltante(
    pieza_seleccionada, cantidad_eliminar, arbol, lista_acciones, tabla, info
):
    try:
        if not pieza_seleccionada:
            lista_acciones.insert(0, "Elige un tipo de pieza.")
            return

        if cantidad_eliminar.strip().isdigit():
            cantidad_eliminar = int(cantidad_eliminar)

            if cantidad_eliminar < 0:
                lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
            else:
                # Ventana de confirmación antes de eliminar las piezas
                confirmacion = messagebox.askyesno(
                    "Confirmar", 
                    f"¿Estás seguro de eliminar {cantidad_eliminar} unidades de {pieza_seleccionada}?"
                )
                if confirmacion:
                    conn = sqlite3.connect("basedatospiezas.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT cantidad FROM chapa WHERE piezas=?", (pieza_seleccionada,)
                    )
                    cantidad_actual = cursor.fetchone()

                    if cantidad_actual is not None:
                        cantidad_actual = cantidad_actual[0]

                        if cantidad_actual >= cantidad_eliminar:
                            nueva_cantidad = cantidad_actual - cantidad_eliminar
                            cursor.execute(
                                "UPDATE chapa SET cantidad=? WHERE piezas=?",
                                (
                                    nueva_cantidad,
                                    pieza_seleccionada,
                                ),
                            )
                            conn.commit()
                            conn.close()
                            mostrar_datos(arbol, tabla, info)
                            lista_acciones.insert(
                                0,
                                f"Eliminación exitosa: Usted eliminó {cantidad_eliminar} de {pieza_seleccionada}",
                            )
                            cantidad_eliminar.delete(0, 'end')
                        else:
                            lista_acciones.insert(
                                0, "No hay suficiente cantidad para eliminar."
                            )
                    else:
                        lista_acciones.insert(
                            0, f"La Pieza {pieza_seleccionada} no se puede modificar"
                        )
        else:
            raise ValueError("La cantidad ingresada no es un número válido")
    except Exception as e:
        lista_acciones.insert(0, f"Error al eliminar piezas: {str(e)}")


def mostrar_stock_soldador(tabla):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        cursor.execute("SELECT modelo, tipo , cantidad FROM soldador_stock ")
        stock_disponible = cursor.fetchall()

        # Limpiar la tabla antes de llenarla
        tabla.delete(*tabla.get_children())

        if stock_disponible:
            for modelo, tipo, cantidad in stock_disponible:
                tabla.insert("", "end", values=(
                    "Soldador", cantidad, modelo, tipo))
        else:
            print("No hay stock disponible para el soldador.")

        conn.close()

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")


def calcular_maquinas_posibles_eco(base_eco, lista_acciones):
    try:
        # Usamos la sentencia "with" para abrir la conexión, lo que asegura que se cierre correctamente incluso si ocurre un error
        with sqlite3.connect("basedatospiezas.db") as conn:
            cursor = conn.cursor()

            # Consulta SQL para obtener las cantidades de las piezas eco
            cursor.execute("SELECT piezas, cantidad FROM chapa WHERE especial = 'eco'")
            cantidades_disponibles = dict(cursor.fetchall())

            # Verificar si todas las piezas del modelo base están presentes en las cantidades disponibles
            for pieza in base_eco:
                if pieza not in cantidades_disponibles:
                    lista_acciones.insert(0, f"La pieza '{pieza}' no está disponible en la base de datos.")
                    return

            # Verificar si hay suficientes cantidades para armar las máquinas
            cantidades_minimas = {pieza: cantidades_disponibles[pieza] // cantidad_base for pieza, cantidad_base in base_eco.items()}  # Corregimos el cálculo aquí
            cantidad_bases = min(cantidades_minimas.values(), default=0)

            if cantidad_bases > 0:
                lista_acciones.insert(0, f"Se pueden armar {cantidad_bases} máquinas Eco.")
            else:
                lista_acciones.insert(0, "No hay piezas suficientes para armar las máquinas.")

    except sqlite3.Error as e:
        lista_acciones.insert(0, "Error en la base de datos: " + str(e))
        
#

def calcular_maquinas_posibles(base_modelo, tipo_base, modelo, lista_acciones):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        cantidades = {}

        for pieza, cantidad in base_modelo.items():
            cursor.execute(
                "SELECT cantidad FROM chapa WHERE tipo_de_base = ? AND modelo = ? AND piezas = ?",
                (tipo_base, modelo, pieza),
            )
            resultado = cursor.fetchone()

            if resultado is not None:
                cantidad_disponible = resultado[0]
                cantidades[pieza] = cantidad_disponible

        if len(cantidades) == len(base_modelo):
            cantidad_bases = min(cantidades.values()
                                 ) // min(base_modelo.values())
            lista_acciones.insert(
                0, f"Se pueden armar {cantidad_bases} máquinas {tipo_base} {modelo}.")
        else:
            lista_acciones.insert(
                0, "No hay piezas suficientes para armar las máquinas."
            )

        conn.close()

    except sqlite3.Error as e:
        lista_acciones.insert(0, "Error en la base de datos.")





def is_positive_integer(value):
    try:
        num = int(value)
        return num >= 0
    except ValueError:
        return False


def eliminar_cantidad_de_piezas(
    combocaja_soldador, entrada_cantidad_soldador, tabla, subtitulo, lista_acciones
):
    cantidad_str = entrada_cantidad_soldador.get()
    tipo = combocaja_soldador

    # Verifica si la cantidad ingresada es un número
    if not cantidad_str.isdigit():
        mensaje_error = "Error: La cantidad debe ser un número entero."
        print(mensaje_error)
        lista_acciones.insert(0, mensaje_error)
        return

    cantidad = int(cantidad_str)  # Convierte la cantidad a un entero
    
        # Ventana de confirmación antes de eliminar las piezas
    confirmacion = messagebox.askyesno(
        "Confirmar", 
        f"¿Estás seguro de enviar {cantidad} unidades del tipo {tipo} al soldador?"
    )
    if not confirmacion:
        lista_acciones.insert(0, "Eliminación cancelada por el usuario.")
        return


    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    # Obtiene información sobre la cantidad actual de las piezas
    cantidad_actual_por_pieza = {}

    if tipo == "Inox 330":
        lista_1 = ["chapa_principal_330", "lateral_front_330", "lateral_atras_330"]
        lista_2 = ["planchuela_330", "varilla_330"]
        lista_3 = [ "portaeje"]

        for pieza in lista_1:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero' AND modelo = 330 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_2:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 330 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_3:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        # Verifica si es posible eliminar la cantidad deseada de todas las piezas
        eliminacion_posible = all(
            cantidad_actual_por_pieza[pieza] >= cantidad
            for pieza in lista_1 + lista_2 + lista_3
        )

        if not eliminacion_posible:
            mensaje_error = (
                "Error: NO hay Base Suficiente en la fabrica"
            )
            print(mensaje_error)
            lista_acciones.insert(0, mensaje_error)
            return

        # Si la eliminación es posible, procede con la actualización
        for pieza in lista_1:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero' AND modelo = 330 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_2:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 330 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_3:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        cursor.execute(
            "UPDATE soldador_stock SET cantidad = cantidad + ? WHERE modelo = '330' AND tipo = 'inox'",
            (cantidad,),
        )
        lista_acciones.insert(0, f"Se envio {cantidad} bases al soldador acero 330")
        conn.commit()
        consulta_de_piezas(tabla, "acero", "330", subtitulo)

    elif tipo == "Inox 300":
        lista_1 = ["chapa_principal_300", "lateral_front_300", "lateral_atras_300"]
        lista_2 = ["planchuela_300", "varilla_300"]
        lista_3 = ["", "portaeje"]

        for pieza in lista_1:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero' AND modelo = 300 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_2:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 300 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_3:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        # Verifica si es posible eliminar la cantidad deseada de todas las piezas
        eliminacion_posible = all(
            cantidad_actual_por_pieza[pieza] >= cantidad
            for pieza in lista_1 + lista_2 + lista_3
        )

        if not eliminacion_posible:
            mensaje_error = (
                "Error: No es posible eliminar la cantidad deseada de piezas."
            )
            print(mensaje_error)
            lista_acciones.insert(0, mensaje_error)
            return

        # Si la eliminación es posible, procede con la actualización
        for pieza in lista_1:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero' AND modelo = 300 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_2:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 300 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_3:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        cursor.execute(
            "UPDATE soldador_stock SET cantidad = cantidad + ? WHERE modelo = '300' AND tipo = 'inox'",
            (cantidad,),
        )
        lista_acciones.insert(0, f"Se envio {cantidad} bases al soldador acero 300")
        conn.commit()
        consulta_de_piezas(tabla, "acero", "300", subtitulo)

    elif tipo == "Pintada 330":
        lista_1 = ["chapa_principal_330", "lateral_front_330", "lateral_atras_330"]
        lista_2 = ["planchuela_330", "varilla_330"]
        lista_3 = ["portaeje"]

        for pieza in lista_1:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'pintura' AND modelo = 330 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_2:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 330 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_3:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        # Verifica si es posible eliminar la cantidad deseada de todas las piezas
        eliminacion_posible = all(
            cantidad_actual_por_pieza[pieza] >= cantidad
            for pieza in lista_1 + lista_2 + lista_3
        )

        if not eliminacion_posible:
            mensaje_error = (
                "Error: No es posible eliminar la cantidad deseada de piezas."
            )
            print(mensaje_error)
            lista_acciones.insert(0, mensaje_error)
            return

        # Si la eliminación es posible, procede con la actualización
        for pieza in lista_1:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'pintura' AND modelo = 330 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_2:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 330 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_3:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        cursor.execute(
            "UPDATE soldador_stock SET cantidad = cantidad + ? WHERE modelo = '330' AND tipo = 'pintada'",
            (cantidad,),
        )
        lista_acciones.insert(0, f"Se envio {cantidad} bases al soldador pintura 330")
        conn.commit()
        consulta_de_piezas(tabla, "pintura", "330", subtitulo)

    elif tipo == "Pintada 300":
        lista_1 = ["chapa_principal_300", "lateral_front_300", "lateral_atras_300"]
        lista_2 = ["planchuela_300", "varilla_300"]
        lista_3 = ["portaeje"]

        for pieza in lista_1:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'pintura' AND modelo = 300 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_2:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 300 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_3:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        # Verifica si es posible eliminar la cantidad deseada de todas las piezas
        eliminacion_posible = all(
            cantidad_actual_por_pieza[pieza] >= cantidad
            for pieza in lista_1 + lista_2 + lista_3
        )

        if not eliminacion_posible:
            mensaje_error = (
                "Error: No es posible eliminar la cantidad deseada de piezas."
            )
            print(mensaje_error)
            lista_acciones.insert(0, mensaje_error)
            return

        # Si la eliminación es posible, procede con la actualización
        for pieza in lista_1:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'pintura' AND modelo = 300 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_2:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 300 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_3:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        cursor.execute(
            "UPDATE soldador_stock SET cantidad = cantidad + ? WHERE modelo = '300' AND tipo = 'pintada'",
            (cantidad,),
        )
        lista_acciones.insert(0, f"Se envio {cantidad} bases al soldador de pintada 300")
        conn.commit()
        consulta_de_piezas(tabla, "pintura", "300", subtitulo)

    elif tipo == "Inox 250":
        lista_1 = ["chapa_principal_250", "lateral_front_250", "lateral_atras_250"]
        lista_2 = ["planchuela_250", "varilla_250"]
        lista_3 = [ "portaeje"]

        for pieza in lista_1:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero' AND modelo = 250 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_2:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 250 AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        for pieza in lista_3:
            cursor.execute(
                """
            SELECT cantidad FROM chapa
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        # Verifica si es posible eliminar la cantidad deseada de todas las piezas
        eliminacion_posible = all(
            cantidad_actual_por_pieza[pieza] >= cantidad
            for pieza in lista_1 + lista_2 + lista_3
        )

        if not eliminacion_posible:
            mensaje_error = (
                "Error: No es posible eliminar la cantidad deseada de piezas."
            )
            print(mensaje_error)
            lista_acciones.insert(0, mensaje_error)
            return

        # Si la eliminación es posible, procede con la actualización
        for pieza in lista_1:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero' AND modelo = 250 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_2:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE tipo_de_base = 'acero_dulce' AND modelo = 250 AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        for pieza in lista_3:
            cantidad_restante = cantidad_actual_por_pieza[pieza] - cantidad
            cursor.execute(
                """
            UPDATE chapa
            SET cantidad = ?
            WHERE modelo = 'pieza' AND piezas = ?
            """,
                (cantidad_restante, pieza),
            )

        cursor.execute(
            "UPDATE soldador_stock SET cantidad = cantidad + ? WHERE modelo = '250' AND tipo = 'inox'",
            (cantidad,),
        )
        lista_acciones.insert(0, f"Se envio {cantidad} bases al soldador de Inox 250")
        conn.commit()
        consulta_de_piezas(tabla, "acero", "250", subtitulo)

        
    elif tipo == "Eco":
        def actualizar_piezas_eco(cursor, lista_piezas, cantidad):
            for pieza in lista_piezas:
                cursor.execute(
                    """
                    UPDATE chapa
                    SET cantidad = cantidad - ?
                    WHERE especial = 'eco' AND piezas = ?
                    """,
                    (cantidad, pieza),
                )

        lista_1 = ["chapa_principal_330", "lateral_front_eco", "lateral_atras_330"]
        lista_2 = ["planchuela_330", "varilla_330"]
        lista_3 = ["portaeje"]

        lista_total = lista_1 + lista_2 + lista_3

        cantidad_actual_por_pieza = {}

        for pieza in lista_total:
            cursor.execute(
                """
                SELECT cantidad FROM chapa
                WHERE especial = 'eco' AND piezas = ?
                """,
                (pieza,),
            )
            cantidad_actual = cursor.fetchone()
            if cantidad_actual:
                cantidad_actual_por_pieza[pieza] = cantidad_actual[0]

        eliminacion_posible = all(
            cantidad_actual_por_pieza[pieza] >= cantidad for pieza in lista_total
        )

        if not eliminacion_posible:
            mensaje_error = "Error: No es posible eliminar la cantidad deseada de piezas."
            print(mensaje_error)
            lista_acciones.insert(0, mensaje_error)
            return

        for lista_piezas in [lista_1, lista_2, lista_3]:
            actualizar_piezas_eco(cursor, lista_piezas, cantidad)

        cursor.execute(
            """
            UPDATE soldador_stock
            SET cantidad = cantidad + ?
            WHERE modelo = 'eco' AND tipo = 'inox'
            """,
            (cantidad,),
        )

        conn.commit()
        
        lista_acciones.insert(0, f"Se enviaron {cantidad} bases al soldador de la Eco")
    entrada_cantidad_soldador.delete(0, 'end') ############

        
    conn.close()


def bases_soldador_terminadas(
    combocaja_terminadas, entrada_cantidad_terminadas, lista_acciones, tabla_chapa
):
    tipo = combocaja_terminadas
    cantidad_str = entrada_cantidad_terminadas.get()

    # Verifica si la cantidad ingresada es un número
    if not cantidad_str.isdigit():
        mensaje_error = "Error: La cantidad debe ser un número entero."
        print(mensaje_error)
        lista_acciones.insert(0, mensaje_error)
        return

    cantidad = int(cantidad_str)  # Convierte la cantidad a un entero

    # Ventana de confirmación antes de eliminar las piezas
    confirmacion = messagebox.askyesno(
        "Confirmar", 
        f"¿Estás seguro de resivir {cantidad} unidades del tipo {tipo} del soldador?"
    )
    if not confirmacion:
        lista_acciones.insert(0, "Eliminación cancelada por el usuario.")
        return


    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        if tipo == "Inox 330":
            # Obtén la cantidad actual de la base de datos para  330
            cursor.execute(
                "SELECT cantidad FROM soldador_stock WHERE tipo = 'inox' AND modelo = '330'"
            )
            cantidad_actual = cursor.fetchone()

            # Verifica si hay suficientes bases disponibles
            if cantidad_actual is None:
                mensaje_error = "No hay registros para Inox 330 en la base de datos."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            cantidad_actual = cantidad_actual[0]

            if cantidad_actual < cantidad:
                mensaje_error = f"No hay suficientes bases de  330 en el Soldador. Cantidad actual: {cantidad_actual}."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            # Actualiza la cantidad en la base de datos soldador_stock
            nueva_cantidad_soldador = max(0, cantidad_actual - cantidad)
            cursor.execute(
                """
                UPDATE soldador_stock
                SET cantidad = ?
                WHERE tipo = 'inox' AND modelo = '330'
            """,
                (nueva_cantidad_soldador,),
            )

            # Actualiza la cantidad en la tabla piezas_del_fundicion
            cursor.execute(
                """
                UPDATE piezas_del_fundicion
                SET cantidad = cantidad + ?
                WHERE piezas = 'inox_330'
            """,
                (cantidad,),
            )

            # Muestra un mensaje de éxito y agrega la acción a la lista
            mensaje_exito = f"Se han terminado {cantidad} bases de Inox 330."
            print(mensaje_exito)
            lista_acciones.insert(0, mensaje_exito)
            mostrar_stock_soldador(tabla_chapa)

        if tipo == "Inox 300":
            # Obtén la cantidad actual de la base de datos para Inox 300
            cursor.execute(
                "SELECT cantidad FROM soldador_stock WHERE tipo = 'inox' AND modelo = '300'"
            )
            cantidad_actual = cursor.fetchone()

            # Verifica si hay suficientes bases disponibles
            if cantidad_actual is None:
                mensaje_error = "No hay registros para Inox 300 en la base de datos."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            cantidad_actual = cantidad_actual[0]

            if cantidad_actual < cantidad:
                mensaje_error = f"No hay suficientes bases de Inox 300 disponibles. Cantidad actual: {cantidad_actual}."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            # Actualiza la cantidad en la base de datos soldador_stock
            nueva_cantidad_soldador = max(0, cantidad_actual - cantidad)
            cursor.execute(
                """
                UPDATE soldador_stock
                SET cantidad = ?
                WHERE tipo = 'inox' AND modelo = '300'
            """,
                (nueva_cantidad_soldador,),
            )

            # Actualiza la cantidad en la tabla piezas_del_fundicion
            cursor.execute(
                """
                UPDATE piezas_del_fundicion
                SET cantidad = cantidad + ?
                WHERE piezas = 'inox_300'
            """,
                (cantidad,),
            )

            # Muestra un mensaje de éxito y agrega la acción a la lista
            mensaje_exito = f"Se han terminado {cantidad} bases de Inox 300."
            print(mensaje_exito)
            lista_acciones.insert(0, mensaje_exito)
            mostrar_stock_soldador(tabla_chapa)
            
        elif tipo == "Pintada 330":
            # Obtén la cantidad actual de la base de datos para Inox 330
            cursor.execute(
                "SELECT cantidad FROM soldador_stock WHERE tipo = 'pintada' AND modelo = '330'"
            )
            cantidad_actual = cursor.fetchone()

            # Verifica si hay suficientes bases disponibles
            if cantidad_actual is None:
                mensaje_error = "No hay registros para pintada 330 en la base de datos."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            cantidad_actual = cantidad_actual[0]

            if cantidad_actual < cantidad:
                mensaje_error = f"No hay suficientes bases de pintada 330 disponibles. Cantidad actual: {cantidad_actual}."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            # Actualiza la cantidad en la base de datos soldador_stock
            nueva_cantidad_soldador = max(0, cantidad_actual - cantidad)
            cursor.execute(
                """
                UPDATE soldador_stock
                SET cantidad = ?
                WHERE tipo = 'pintada' AND modelo = '330'
            """,
                (nueva_cantidad_soldador,),
            )

            # Actualiza la cantidad en la tabla piezas_del_fundicion
            cursor.execute(
                """
                UPDATE piezas_del_fundicion
                SET cantidad = cantidad + ?
                WHERE piezas = 'base_pintada_330'
            """,
                (cantidad,),
            )

            # Muestra un mensaje de éxito y agrega la acción a la lista
            mensaje_exito = f"Se han terminado {cantidad} bases de Pintada 330."
            print(mensaje_exito)
            lista_acciones.insert(0, mensaje_exito)
            mostrar_stock_soldador(tabla_chapa)


        elif tipo == "Pintada 300":
            # Obtén la cantidad actual de la base de datos para Inox 300
            cursor.execute(
                "SELECT cantidad FROM soldador_stock WHERE tipo = 'pintada' AND modelo = '300'"
            )
            cantidad_actual = cursor.fetchone()

            # Verifica si hay suficientes bases disponibles
            if cantidad_actual is None:
                mensaje_error = "No hay registros para pintada 300 en la base de datos."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            cantidad_actual = cantidad_actual[0]

            if cantidad_actual < cantidad:
                mensaje_error = f"No hay suficientes bases de pintada 300 disponibles. Cantidad actual: {cantidad_actual}."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            # Actualiza la cantidad en la base de datos soldador_stock
            nueva_cantidad_soldador = max(0, cantidad_actual - cantidad)
            cursor.execute(
                """
                UPDATE soldador_stock
                SET cantidad = ?
                WHERE tipo = 'pintada' AND modelo = '300'
            """,
                (nueva_cantidad_soldador,),
            )

            # Actualiza la cantidad en la tabla piezas_del_fundicion
            cursor.execute(
                """
                UPDATE piezas_del_fundicion
                SET cantidad = cantidad + ?
                WHERE piezas = 'base_pintada_300'
            """,
                (cantidad,),
            )

            # Muestra un mensaje de éxito y agrega la acción a la lista
            mensaje_exito = f"Se han terminado {cantidad} bases de Pintada 300."
            print(mensaje_exito)
            lista_acciones.insert(0, mensaje_exito)
            mostrar_stock_soldador(tabla_chapa)
            
        elif tipo == "Inox 250":
            # Obtén la cantidad actual de la base de datos para Inox 300
            cursor.execute(
                "SELECT cantidad FROM soldador_stock WHERE tipo = 'inox' AND modelo = '250'"
            )
            cantidad_actual = cursor.fetchone()

            # Verifica si hay suficientes bases disponibles
            if cantidad_actual is None:
                mensaje_error = "No hay registros para acero 250 en la base de datos."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            cantidad_actual = cantidad_actual[0]

            if cantidad_actual < cantidad:
                mensaje_error = f"No hay suficientes bases de acero 250 disponibles. Cantidad actual: {cantidad_actual}."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            # Actualiza la cantidad en la base de datos soldador_stock
            nueva_cantidad_soldador = max(0, cantidad_actual - cantidad)
            cursor.execute(
                """
                UPDATE soldador_stock
                SET cantidad = ?
                WHERE tipo = 'inox' AND modelo = '250'
            """,
                (nueva_cantidad_soldador,),
            )

            # Actualiza la cantidad en la tabla piezas_del_fundicion
            cursor.execute(
                """
                UPDATE piezas_del_fundicion
                SET cantidad = cantidad + ?
                WHERE piezas = 'inox_250'
            """,
                (cantidad,),
            )

            # Muestra un mensaje de éxito y agrega la acción a la lista
            mensaje_exito = f"Se han terminado {cantidad} bases de Pintada 250."
            print(mensaje_exito)
            lista_acciones.insert(0, mensaje_exito)
            mostrar_stock_soldador(tabla_chapa)

        elif tipo == "Eco":
            # Obtén la cantidad actual de la base de datos para Inox eci
            cursor.execute(
                "SELECT cantidad FROM soldador_stock WHERE tipo = 'inox' AND modelo = 'eco'"
            )
            cantidad_actual = cursor.fetchone()

            # Verifica si hay suficientes bases disponibles
            if cantidad_actual is None:
                mensaje_error = "No hay registros para acero Eco en la base de datos."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            cantidad_actual = cantidad_actual[0]

            if cantidad_actual < cantidad:
                mensaje_error = f"No hay suficientes bases de acero Eco disponibles. Cantidad actual: {cantidad_actual}."
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)
                return

            # Actualiza la cantidad en la base de datos soldador_stock
            nueva_cantidad_soldador = max(0, cantidad_actual - cantidad)
            cursor.execute(
                """
                UPDATE soldador_stock
                SET cantidad = ?
                WHERE tipo = 'inox' AND modelo = 'eco'
            """,
                (nueva_cantidad_soldador,),
            )

            # Actualiza la cantidad en la tabla piezas_del_fundicion
            cursor.execute(
                """
                UPDATE piezas_del_fundicion
                SET cantidad = cantidad + ?
                WHERE piezas = 'inox_eco' AND modelo = 'eco'
            """,
                (cantidad,),
            )

            # Muestra un mensaje de éxito y agrega la acción a la lista
            mensaje_exito = f"Se han terminado {cantidad} bases de Eco."
            print(mensaje_exito)
            lista_acciones.insert(0, mensaje_exito)
            mostrar_stock_soldador(tabla_chapa)


        entrada_cantidad_terminadas.delete(0, 'end') 
        # Guarda los cambios en la base de datos
        conn.commit()

    except Exception as e:
        # Manejo de errores
        mensaje_error = f"Error: {e}"
        print(mensaje_error)
        lista_acciones.insert(0, mensaje_error)

    finally:
        # Cierra la conexión a la base de datos
        conn.close()


def armar_cabezales_inox(cantidad_cabezales, lista_acciones):
    # Mostrar mensaje de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea armar {cantidad_cabezales} cabezales inox?")
    if not confirmacion:
        lista_acciones.insert(0, "Se canceló la operación de armado de cabezales.")
        return
    
    try:
        with sqlite3.connect("basedatospiezas.db") as conn:
            cursor = conn.cursor()

            cabezales_inox = {"chapa_U_cabezal", "tapa_cabezal", "bandeja_cabezal"}

            piezas_faltantes = {}

            for pieza in cabezales_inox:
                cursor.execute("SELECT cantidad FROM chapa WHERE modelo = 'cabezal' AND piezas = ?", (pieza,))
                cantidad_disponible = cursor.fetchone()

                if cantidad_disponible:
                    cantidad_disponible = int(cantidad_disponible[0])
                    cantidad_necesaria = int(cantidad_cabezales)
                    cantidad_faltante = max(0, cantidad_necesaria - cantidad_disponible)

                    if cantidad_faltante > 0:
                        piezas_faltantes[pieza] = cantidad_faltante
                    else:
                        cursor.execute("UPDATE chapa SET cantidad = cantidad - ? WHERE modelo = 'cabezal' AND piezas = ?",
                                       (cantidad_necesaria, pieza))
                        conn.commit()

            if not piezas_faltantes:
                cursor.execute("UPDATE piezas_del_fundicion SET cantidad = cantidad + ? WHERE modelo = 'cabezal' AND piezas = 'cabezal_inox'",
                               (cantidad_cabezales,))
                conn.commit()
                lista_acciones.insert(0, f"Se agregaron {cantidad_cabezales} cabezales inox ")
            else:
                lista_acciones.insert(0, "No hay suficientes piezas para armar los cabezales Inox. Faltan las siguientes piezas:")
                for pieza, cantidad_faltante in piezas_faltantes.items():
                    lista_acciones.insert(1, f"{pieza}: {cantidad_faltante} unidades.")

            cantidad_cabezales.delete(0, 'end')
    except sqlite3.Error as e:
        lista_acciones.insert(0, f"Error en la base de datos: {str(e)}")
        
        
#250import sqlite3
def armar_cabezales_250(cantidad_cabezales, lista_acciones):
    # Mostrar mensaje de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea armar {cantidad_cabezales} cabezales 250?")
    if not confirmacion:
        lista_acciones.insert(0, "Se canceló la operación de armado de cabezales 250.")
        return
    
    try:
        with sqlite3.connect("basedatospiezas.db") as conn:
            cursor = conn.cursor()

            cabezales_250 = {"chapa_U_cabezal_250", "tapa_cabezal_250", "bandeja_cabezal_250"}

            piezas_faltantes = {}

            for pieza in cabezales_250:
                cursor.execute("SELECT cantidad FROM chapa WHERE modelo = 'cabezal' AND piezas = ?", (pieza,))
                cantidad_disponible = cursor.fetchone()

                if cantidad_disponible:
                    cantidad_disponible = int(cantidad_disponible[0])
                    cantidad_necesaria = int(cantidad_cabezales)
                    cantidad_faltante = max(0, cantidad_necesaria - cantidad_disponible)

                    if cantidad_faltante > 0:
                        piezas_faltantes[pieza] = cantidad_faltante
                    else:
                        cursor.execute("UPDATE chapa SET cantidad = cantidad - ? WHERE modelo = 'cabezal' AND piezas = ?",
                                       (cantidad_necesaria, pieza))
                        conn.commit()
                else:
                    lista_acciones.insert(0, f"No se encontró la pieza {pieza} en la base de datos.")
                    return

            if not piezas_faltantes:
                cursor.execute("UPDATE piezas_del_fundicion SET cantidad = cantidad + ? WHERE modelo = 'cabezal' AND piezas = 'cabezal_250'",
                               (cantidad_cabezales,))
                conn.commit()
                lista_acciones.insert(0, f"Se agregaron {cantidad_cabezales} cabezales 250 ")
            else:
                lista_acciones.insert(0, "No hay suficientes piezas para armar los cabezales. Faltan las siguientes piezas:")
                for pieza, cantidad_faltante in piezas_faltantes.items():
                    lista_acciones.insert(1, f"{pieza}: {cantidad_faltante} unidades.")
                    
            cantidad_cabezales.delete(0, 'end')
    except sqlite3.Error as e:
        lista_acciones.insert(0, f"Error en la base de datos: {str(e)}")
    

def armar_cabezales_pint(cantidad_cabezales, lista_acciones):
    # Mostrar mensaje de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea armar {cantidad_cabezales} cabezales para pintura?")
    if not confirmacion:
        lista_acciones.insert(0, "Se canceló la operación de armado de cabezales para pintura.")
        return
    
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    # Define the required pieces for the cabezal
    cabezales_inox = {"chapa_U_cabezal", "tapa_cabezal", "bandeja_cabezal"}

    # Check if there are enough pieces available
    piezas_faltantes = {}
    for pieza in cabezales_inox:
        cursor.execute("SELECT cantidad FROM chapa WHERE tipo_de_base = 'pintura' AND piezas = ?", (pieza,))
        cantidad_disponible = cursor.fetchone()

        if cantidad_disponible:
            cantidad_disponible = int(cantidad_disponible[0])
            cantidad_necesaria = int(cantidad_cabezales)
            cantidad_faltante = max(0, cantidad_necesaria - cantidad_disponible)

            if cantidad_faltante > 0:
                piezas_faltantes[pieza] = cantidad_faltante
            else:
                # Deduct the used quantity from the "chapa" table
                cursor.execute("UPDATE chapa SET cantidad = cantidad - ? WHERE tipo_de_base = 'pintura' AND piezas = ?",
                               (cantidad_necesaria, pieza))
                conn.commit()

    if not piezas_faltantes:
        # Update the "piezas_del_fundidor" table
        cursor.execute("UPDATE piezas_del_fundicion SET cantidad = cantidad + ? WHERE modelo = 'cabezal' AND piezas = 'cabezal_pintura'",
                       (cantidad_cabezales,))
        conn.commit()
        lista_acciones.insert(0, f"Se agregaron {cantidad_cabezales} cabezales para pintura")
        
    else:
        lista_acciones.insert(0, "No hay suficientes piezas para armar los cabezales de pintura. Faltan las siguientes piezas:")
        for pieza, cantidad_faltante in piezas_faltantes.items():
           lista_acciones.insert(1, f"{pieza}: {cantidad_faltante} unidades.")

    conn.close()
    cantidad_cabezales.delete(0, 'end')



def mostrar_bases_en_bruto(tree1, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad, modelo FROM piezas_del_fundicion WHERE modelo = '330' OR modelo = '300' OR modelo = '250' OR modelo = 'eco'"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)

    subtitulo_text = "Bases En Bruto"
    subtitulo.config(text=subtitulo_text)


def mostrar_cabezales_en_bruto(tree1, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM piezas_del_fundicion WHERE modelo = 'cabezal' "
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)

    subtitulo_text = "Cabezales en Bruto"
    subtitulo.config(text=subtitulo_text)


# --------------------------------funciiones de piezas fundidor --------------------------------------------------------


def mostrar_datos_materias(material, tabla, res, sub):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM piezas_del_fundicion WHERE material = ? ",
        (material,),
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for pieza, cantidad in datos:
        color_fondo = obtener_color_fondo(cantidad)
        tabla.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
    res.insert(0, f"Stock de {material}")
    sub_text = f"Mostrando {material}"
    sub.config(text=sub_text)

def mostrar_plastico(material, tabla, res, sub):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE tipo = ? ",
        (material,),
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for pieza, cantidad in datos:
        color_fondo = obtener_color_fondo(cantidad)
        tabla.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
    res.insert(0, f"Stock de {material}")
    
    sub_text = f"Mostrando {material}"
    sub.config(text=sub_text)

def mostrar_shop(material, tabla, res, sub):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE mecanizado = ? ",
        (material,),
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for pieza, cantidad in datos:
        color_fondo = obtener_color_fondo(cantidad)
        tabla.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
    res.insert(0, f"Stock de {material}")
    sub_text = f"Mostrando {material}"
    sub.config(text=sub_text)

def mostrar_chapa_cortada(tabla, res, sub):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad, piezas FROM piezas_del_fundicion WHERE material= 'chapa_cortada' AND mecanizado = 'cortado'")
    datos = cursor.fetchall()
    conn.close()
    for item in tabla.get_children():
        tabla.delete(item)
    for cantidad , pieza in datos:
        color_fondo = obtener_color_fondo(cantidad)
        tabla.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
    res.insert(0, f"Stock de Chapa Cortada")
    sub_text = f"Mostrando Chapa Cortada"
    sub.config(text=sub_text)

def mostrar_piezas_cortadas(tabla, res, sub):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    
    # Corrige la consulta SQL
    cursor.execute("""
        SELECT piezas, SUM(cantidad) AS cantidad_cortada
        FROM piezas_del_fundicion
        WHERE piezas IN ('teletubi_eco','guia_U', 'eje_rectificado', 'varilla_brazo_330', 'varilla_brazo_300', 'varilla_brazo_250', 'tubo_manija', 'tubo_manija_250', 'cuadrado_regulador', 'palanca_afilador', 'eje_corto', 'eje_largo', 'caja_soldada_eco', 'buje_eje_eco')
        GROUP BY piezas

    """)
    
    datos = cursor.fetchall()
    conn.close()
    
    # Limpia la tabla antes de agregar nuevos datos
    for item in tabla.get_children():
        tabla.delete(item)
    
    # Agrega los datos a la tabla
    for pieza, cantidad in datos:
        color_fondo = obtener_color_fondo(cantidad)
        tabla.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
    
    res.insert(0, f"Stock de Piezas Cortada")
    
    sub_text = f"Mostrando Piezas Cortadas"
    sub.config(text=sub_text)
    
    
def mostrar_tornillo_guia_rueditas(tabla, res, sub):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    
    # Corrige la consulta SQL
    cursor.execute("""
        SELECT piezas, SUM(cantidad) AS cantidad_cortada
        FROM piezas_del_fundicion
        WHERE piezas IN ('tornillo_guia', 'rueditas', 'tornillo_teletubi_eco')
        GROUP BY piezas
    """)
    
    datos = cursor.fetchall()
    conn.close()
    
    # Limpia la tabla antes de agregar nuevos datos
    for item in tabla.get_children():
        tabla.delete(item)
    
    # Agrega los datos a la tabla
    for pieza, cantidad in datos:
        color_fondo = obtener_color_fondo(cantidad)
        tabla.insert("", tk.END, values=(pieza, cantidad), tags=(color_fondo,))
    
    res.insert(0, f"Stock de Tornillo/ Rueditas")
    
    sub_text = f"Mostrando Varios"
    sub.config(text=sub_text)
    
#envio de a provedores
def enviar_piezas_a_pulido(
    pieza,
    cantidad,
    tabla,
    tree,
    lista_acciones,
    info,
):
    pieza_seleccionada = pieza.get()
    cantidad_ingresada = cantidad.get()

    if not cantidad_ingresada.isdigit() or int(cantidad_ingresada) < 0:
        lista_acciones.insert(0, "Ingrese una Cantidad Válida")
        return

    if int(cantidad_ingresada) == 0:
        lista_acciones.insert(0, "No hay piezas para enviar a pulido.")
        return

    # Mostrar una ventana de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea enviar {cantidad_ingresada} piezas de {pieza_seleccionada} a pulido?")

    if confirmacion:
        conn = None
        cursor = None

        try:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT cantidad FROM {tabla} WHERE piezas = ?", (
                    pieza_seleccionada,)
            )
            resultado = cursor.fetchone()
            cantidad_existente = resultado[0] if resultado else 0

            nueva_cantidad = cantidad_existente + int(cantidad_ingresada)

            # Iniciar una transacción
            conn.execute("BEGIN")

            # Actualizar la tabla donde envías las piezas a pulido
            cursor.execute(
                f"UPDATE {tabla} SET cantidad = ? WHERE piezas = ?",
                (nueva_cantidad, pieza_seleccionada),
            )

            # Reducir la cantidad en la tabla de stock en bruto
            cursor.execute(
                f"SELECT cantidad FROM piezas_del_fundicion WHERE piezas = ?",
                (pieza_seleccionada,),
            )
            resultado_stock_bruto = cursor.fetchone()
            cantidad_stock_bruto = resultado_stock_bruto[0] if resultado_stock_bruto else 0

            if int(cantidad_ingresada) > cantidad_stock_bruto:
                lista_acciones.insert(0, "No hay suficientes piezas en stock para enviar la cantidad especificada a pulido.")
                conn.rollback()
                return

            nueva_cantidad_stock_bruto = cantidad_stock_bruto - int(cantidad_ingresada)
            cursor.execute(
                f"UPDATE piezas_del_fundicion SET cantidad = ? WHERE piezas = ?",
                (nueva_cantidad_stock_bruto, pieza_seleccionada),
            )

            # Confirmar la transacción
            conn.commit()

        except sqlite3.Error as e:
            # Revertir la transacción en caso de error
            if conn:
                conn.rollback()
            lista_acciones.insert(0, f"Error en la base de datos: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        mostrar_datos(tree, tabla, info)

        lista_acciones.insert(0, f"{cantidad_ingresada} piezas de {pieza_seleccionada} han sido enviadas a pulido.")
    cantidad.delete(0, 'end')

#mover a pulidas a resibidasd
def mover_piezas_a_stock_pulidas(
    pieza, cantidad, tabla_carmelo, tabla_stock_pulidas, arbol, lista_acciones, info
):
    pieza_seleccionada = pieza.get()
    cantidad_ingresada = cantidad.get()

    if not cantidad_ingresada.isdigit() or int(cantidad_ingresada) < 0:
        lista_acciones.insert(0, "Ingrese una Cantidad Válida")
        return

    # Mostrar una ventana de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea resivir {cantidad_ingresada} piezas de {pieza_seleccionada} al stock de piezas pulidas?")

    if confirmacion:
        conn = None
        cursor = None

        try:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT cantidad FROM {tabla_carmelo} WHERE piezas = ?",
                (pieza_seleccionada,),
            )
            resultado = cursor.fetchone()
            cantidad_existente = resultado[0] if resultado else 0

            if int(cantidad_ingresada) > cantidad_existente:
                lista_acciones.insert(
                    0, "No hay suficientes piezas en el Pulidor"
                )
                return

            # Iniciar una transacción
            conn.execute("BEGIN")

            # Actualizar la tabla de Carmelo reduciendo la cantidad
            nueva_cantidad_carmelo = cantidad_existente - int(cantidad_ingresada)
            cursor.execute(
                f"UPDATE {tabla_carmelo} SET cantidad = ? WHERE piezas = ?",
                (nueva_cantidad_carmelo, pieza_seleccionada),
            )

            # Actualizar la tabla de Stock Pulidas aumentando la cantidad
            cursor.execute(
                f"SELECT cantidad FROM {tabla_stock_pulidas} WHERE piezas = ?",
                (pieza_seleccionada,),
            )
            resultado_stock_pulidas = cursor.fetchone()
            cantidad_stock_pulidas = (
                resultado_stock_pulidas[0] if resultado_stock_pulidas else 0
            )

            nueva_cantidad_stock_pulidas = cantidad_stock_pulidas + \
                int(cantidad_ingresada)
            cursor.execute(
                f"UPDATE {tabla_stock_pulidas} SET cantidad = ? WHERE piezas = ?",
                (nueva_cantidad_stock_pulidas, pieza_seleccionada),
            )

            # Confirmar la transacción
            conn.commit()

        except sqlite3.Error as e:
            # Revertir la transacción en caso de error
            if conn:
                conn.rollback()
            lista_acciones.insert(0, f"Error en la base de datos: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        mostrar_datos(arbol, tabla_carmelo, info)

        lista_acciones.insert(
            0,
            f"{cantidad_ingresada} pieza de {pieza_seleccionada} han sido movidas a Stock Pulidas.",
        )
    cantidad.delete(0, 'end')


def mostrar_datos_especifico(tabla, modelo, arbol, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas, cantidad FROM {tabla} WHERE modelo =  ?", (modelo,))
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    text = f"Mostrando Lista {modelo}"
    info.config(text=text)


def agregar_a_lista_tarea(caja_texto, lista_tarea):
    texto = caja_texto.get(
        "1.0", "end-1c"
    )  # Obtiene el texto desde la posición 1.0 hasta el final, excluyendo el último carácter (que es un salto de línea)

    if (
        texto.strip()
    ):  # Verifica que el texto no esté vacío después de eliminar espacios en blanco
        lista_tarea.insert(0, texto)  # Agrega el texto a la lista
        # Borra el contenido de la caja de texto
        caja_texto.delete("1.0", tk.END)


def mostrar(tree1, tabla, mecanizado, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.execute(
        f"SELECT piezas, cantidad FROM {tabla} WHERE mecanizado = ?", (
            mecanizado,)
    )
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)
    
    if tabla == "piezas_del_fundicion":
        text = "Stock en Bruto"
    elif tabla == "piezas_finales_defenitivas":
        text = "Stock en Fabrica"
    elif tabla == "pieza_retocadas":
        if mecanizado == "niquelado":
            text= "Stock En Niquelado"
        elif mecanizado == "pintor":
            text= "Stock En Pintura"
    
    info.config(text=text)
    


#pintura 
def envios_de_bruto_a_pulido(
    lista_piezas, cantidad_a_niquelar, lista_acciones, arbol, mecanizado
):
    pieza = lista_piezas
    cantidad = cantidad_a_niquelar.get()

    if cantidad.strip().isdigit():
        cantidad = int(cantidad)

        if cantidad < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM piezas_del_fundicion WHERE mecanizado = ? AND piezas = ?",
                (
                    mecanizado,
                    pieza,
                ),
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]

                # Verificar si hay suficientes piezas en la primera tabla
                if cantidad_actual >= cantidad:
                    # Solicitar confirmación al usuario antes de realizar cambios en la base de datos
                    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de enviar al Pintor {cantidad} unidades de {pieza}?")
                    if confirmacion:
                        nueva_cantidad = cantidad_actual - cantidad
                        cursor.execute(
                            "UPDATE piezas_del_fundicion SET cantidad=? WHERE mecanizado = ? AND piezas = ?",
                            (
                                nueva_cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )
                        conn.commit()

                        # Nueva consulta para actualizar otra tabla
                        cursor.execute(
                            "UPDATE pieza_retocadas SET cantidad = cantidad + ? WHERE mecanizado = ? AND piezas = ?",
                            (
                                cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )

                        conn.commit()
                        conn.close()
                        lista_acciones.insert(0, f"Carga {pieza}: {cantidad} unidades")
                        cantidad_a_niquelar.delete(0, 'end')

                else:
                    lista_acciones.insert(0, "No hay suficientes piezas disponibles")
            else:
                lista_acciones.insert(0, "Cantidad ingresada inválida")
    else:
        lista_acciones.insert(0, "Ingrese un número válido")
        
        

def envios_pulido_a_fabrica(
    lista_piezas, cantidad_a_niquelar, lista_acciones, arbol, mecanizado
):
    pieza = lista_piezas
    cantidad = cantidad_a_niquelar.get()

    if cantidad.strip().isdigit():
        cantidad = int(cantidad)

        if cantidad < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM pieza_retocadas WHERE mecanizado = ? AND piezas = ?",
                (
                    mecanizado,
                    pieza,
                ),
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]

                # Verificar si hay suficientes piezas en la primera tabla
                if cantidad_actual >= cantidad:
                    # Solicitar confirmación al usuario antes de realizar cambios en la base de datos
                    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de resivir {cantidad} unidades de {pieza} a la fábrica?")
                    if confirmacion:
                        nueva_cantidad = cantidad_actual - cantidad
                        cursor.execute(
                            "UPDATE pieza_retocadas SET cantidad=? WHERE mecanizado = ? AND piezas = ?",
                            (
                                nueva_cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )
                        conn.commit()

                        # Nueva consulta para actualizar otra tabla
                        cursor.execute(
                            "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE mecanizado = ? AND piezas = ?",
                            (
                                cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )

                        conn.commit()
                        conn.close()
                        lista_acciones.insert(0, f"Carga {pieza}: {cantidad} unidades")
                        cantidad_a_niquelar.delete(0, 'end')

                else:
                    lista_acciones.insert(0, "No hay suficientes piezas disponibles")
            else:
                lista_acciones.insert(0, "Cantidad ingresada inválida")
    else:
        lista_acciones.insert(0, "Ingrese un número válido")

#niquelado

def envios_de_bruto_a_niquelar(
    lista_piezas, cantidad_a_niquelar, lista_acciones, arbol, mecanizado
):
    pieza = lista_piezas
    cantidad = cantidad_a_niquelar.get()

    if not cantidad.strip().isdigit():
        lista_acciones.insert(0, "Ingrese una cantidad válida.")
        return

    cantidad = int(cantidad)

    if cantidad < 0:
        lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        return

    conn = None
    cursor = None

    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT cantidad FROM piezas_del_fundicion WHERE mecanizado = ? AND piezas = ?",
            (mecanizado, pieza,),
        )
        cantidad_actual = cursor.fetchone()

        if cantidad_actual is not None:
            cantidad_actual = cantidad_actual[0]
            nueva_cantidad = cantidad_actual - cantidad

            if nueva_cantidad < 0:
                lista_acciones.insert(0, "No se pueden enviar más piezas de las disponibles en stock.")
                return

            # Solicitar confirmación al usuario antes de realizar cambios en la base de datos
            confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de enviar {cantidad} unidades de {pieza} a niquelar?")
            if not confirmacion:
                return  # Si el usuario no confirma, salir de la función sin hacer cambios

            # Actualizar la tabla de piezas_del_fundicion
            cursor.execute(
                "UPDATE piezas_del_fundicion SET cantidad=? WHERE mecanizado = ? AND piezas = ?",
                (nueva_cantidad, mecanizado, pieza,),
            )
            conn.commit()

            # Actualizar la tabla de piezas_retocadas
            cursor.execute(
                "UPDATE pieza_retocadas SET cantidad = cantidad + ? WHERE mecanizado = ?  AND piezas = ?",
                (cantidad, mecanizado, pieza,),
            )
            conn.commit()

            lista_acciones.insert(0, f"Carga {pieza}: {cantidad} unidades")
            cantidad_a_niquelar.delete(0, 'end')
        else:
            lista_acciones.insert(0, "Cantidad ingresada inválida")
    except sqlite3.Error as e:
        lista_acciones.insert(0, f"Error en la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def envios_de_niquelado_a_fabrica(
    lista_piezas, cantidad_a_niquelar, lista_acciones, arbol, mecanizado
):
    pieza = lista_piezas
    cantidad = cantidad_a_niquelar.get()

    if not cantidad.strip().isdigit():
        lista_acciones.insert(0, "Ingrese una cantidad válida.")
        return

    cantidad = int(cantidad)

    if cantidad < 0:
        lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        return

    conn = None
    cursor = None

    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT cantidad FROM pieza_retocadas WHERE mecanizado = ? AND piezas = ?",
            (mecanizado, pieza,),
        )
        cantidad_actual = cursor.fetchone()

        if cantidad_actual is not None:
            cantidad_actual = cantidad_actual[0]
            nueva_cantidad = cantidad_actual - cantidad

            if nueva_cantidad < 0:
                lista_acciones.insert(0, "No se pueden enviar más piezas de las disponibles en stock.")
                return

            # Solicitar confirmación al usuario antes de realizar cambios en la base de datos
            confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de resivir {cantidad} unidades de {pieza} a la fábrica?")
            if not confirmacion:
                return  # Si el usuario no confirma, salir de la función sin hacer cambios

            # Actualizar la tabla de pieza_retocadas
            cursor.execute(
                "UPDATE pieza_retocadas SET cantidad=? WHERE mecanizado = ? AND piezas = ?",
                (nueva_cantidad, mecanizado, pieza,),
            )
            conn.commit()

            # Actualizar la tabla de piezas_finales_defenitivas
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE mecanizado = ?  AND piezas = ?",
                (cantidad, mecanizado, pieza,),
            )
            conn.commit()

            lista_acciones.insert(0, f"Carga {pieza}: {cantidad} unidades")
            cantidad_a_niquelar.delete(0, 'end')

        else:
            lista_acciones.insert(0, "Cantidad ingresada inválida")
    except sqlite3.Error as e:
        lista_acciones.insert(0, f"Error en la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#cabezalesimport 
def envios_de_bruto_cabezal(
    lista_piezas, cantidad_a_niquelar, lista_acciones, arbol, mecanizado
):
    pieza = lista_piezas
    cantidad = cantidad_a_niquelar.get()

    if cantidad.strip().isdigit():
        cantidad = int(cantidad)

        if cantidad < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM piezas_del_fundicion WHERE mecanizado = ? AND piezas = ?",
                (
                    mecanizado,
                    pieza,
                ),
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]

                # Verificar si hay suficientes piezas en la primera tabla
                if cantidad_actual >= cantidad:
                    # Solicitar confirmación al usuario antes de realizar cambios en la base de datos
                    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de enviar a {cantidad} unidades de {pieza} al pintura?")
                    if confirmacion:
                        nueva_cantidad = cantidad_actual - cantidad
                        cursor.execute(
                            "UPDATE piezas_del_fundicion SET cantidad=? WHERE mecanizado = ? AND piezas = ?",
                            (
                                nueva_cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )
                        conn.commit()

                        # Nueva consulta para actualizar otra tabla
                        cursor.execute(
                            "UPDATE pieza_retocadas SET cantidad = cantidad + ? WHERE mecanizado = ? AND piezas = ?",
                            (
                                cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )

                        conn.commit()
                        conn.close()
                        lista_acciones.insert(0, f"Carga {pieza}: {cantidad} unidades")
                        cantidad_a_niquelar.delete(0, 'end')

                else:
                    lista_acciones.insert(0, "No hay suficientes piezas disponibles")
            else:
                lista_acciones.insert(0, "Cantidad ingresada inválida")
    else:
        lista_acciones.insert(0, "Ingrese un número válido")


def envios_pulido_a_fabrica_cabezal(
    lista_piezas, cantidad_a_niquelar, lista_acciones, arbol, mecanizado
):
    pieza = lista_piezas
    cantidad = cantidad_a_niquelar.get()

    if cantidad.strip().isdigit():
        cantidad = int(cantidad)

        if cantidad < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM pieza_retocadas WHERE mecanizado = ? AND piezas = ?",
                (
                    mecanizado,
                    pieza,
                ),
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]

                # Verificar si hay suficientes piezas en la primera tabla
                if cantidad_actual >= cantidad:
                    # Solicitar confirmación al usuario antes de realizar cambios en la base de datos
                    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de resivir {cantidad} unidades de {pieza} a la fábrica?")
                    if confirmacion:
                        nueva_cantidad = cantidad_actual - cantidad
                        cursor.execute(
                            "UPDATE pieza_retocadas SET cantidad=? WHERE mecanizado = ? AND piezas = ?",
                            (
                                nueva_cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )
                        conn.commit()

                        # Nueva consulta para actualizar otra tabla
                        cursor.execute(
                            "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE mecanizado = ? AND piezas = ?",
                            (
                                cantidad,
                                mecanizado,
                                pieza,
                            ),
                        )

                        conn.commit()
                        conn.close()
                        lista_acciones.insert(0, f"Carga {pieza}: {cantidad} unidades")
                        cantidad_a_niquelar.delete(0, 'end')

                else:
                    lista_acciones.insert(0, "No hay suficientes piezas disponibles")
            else:
                lista_acciones.insert(0, "Cantidad ingresada inválida")
    else:
        lista_acciones.insert(0, "Ingrese un número válido")


# -------------------------------------Funciones Mecanizado------------------------------------------------------------


def mostrar_datos_torno(arbol, tabla, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas, cantidad FROM {tabla} WHERE mecanizado = 'torno' AND piezas NOT IN ('caja_torneado_330', 'caja_torneado_300', 'caja_torneado_250')"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    if tabla == "piezas_del_fundicion":
        txt = "Mostrar Datos: Pieza en Bruto "
    elif tabla == "piezas_finales_defenitivas":
        txt = "Mostrar Datos: Piezas Terminadas"
    
    info.config(text=txt)
        
        
def mostrar_datos_(arbol):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas, cantidad FROM piezas_del_fundicion WHERE piezas IN ('caja_torneado_330', 'caja_torneado_300', 'caja_torneado_250', 'cubre_300', 'teletu_300')"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)


def actualizar_pieza_torno(lista_predefinida, entrada_cantidad, res, table, tree, info):
    actualizar_pieza = lista_predefinida.get()
    entrada_actualizar = entrada_cantidad.get()

    if entrada_actualizar.strip().isdigit():
        entrada_actualizar = int(entrada_actualizar)

        if entrada_actualizar < 0:
            res.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            # Mostrar mensaje de confirmación
            confirmacion = messagebox.askyesno("Confirmar", f"¿Desea actualizar la cantidad de {entrada_actualizar} de la pieza {actualizar_pieza}?")
            if not confirmacion:
                res.insert(0, "Se canceló la operación de actualización de piezas.")
                return
            
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT cantidad FROM piezas_del_fundicion WHERE piezas=?",
                (actualizar_pieza,),
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]

                # Verifica si hay suficientes piezas disponibles
                if cantidad_actual >= entrada_actualizar:
                    nueva_cantidad = max(
                        0, cantidad_actual - entrada_actualizar)
                    cursor.execute(
                        f"UPDATE piezas_del_fundicion SET cantidad=? WHERE piezas=?",
                        (nueva_cantidad, actualizar_pieza),
                    )
                    conn.commit()

                    if actualizar_pieza == "teletubi_eco":
                        # Descuenta la cantidad deseada de "teletubi_eco"
                        cursor.execute(
                            "UPDATE piezas_del_fundicion SET cantidad = cantidad - ? WHERE piezas = ?",
                            (entrada_actualizar, "teletubi_eco"),
                        )
                        conn.commit()
                        # Actualiza la cantidad de "teletubi_doblado_eco"
                        cursor.execute(
                            "UPDATE piezas_del_fundicion SET cantidad = cantidad + ? WHERE piezas = ?",
                            (entrada_actualizar, "teletubi_doblado_eco"),
                        )
                        conn.commit()
                    else:
                        # Actualiza la cantidad de la pieza en la tabla correspondiente
                        cursor.execute(
                            "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = ?",
                            (entrada_actualizar, actualizar_pieza),
                        )
                        conn.commit()

                    conn.close()
                    mostrar_datos(
                        tree, table, info
                    )  # Llama a la función para mostrar los datos actualizados
                    res.insert(
                        0,
                        f"Carga exitosa: Usted cargó {entrada_actualizar} {actualizar_pieza}:",
                    )
                else:
                    conn.close()
                    res.insert(
                        0,
                        f"No hay suficientes piezas de {actualizar_pieza} disponibles.",
                    )
            else:
                conn.close()
                res.insert(
                    0, f"La Pieza {actualizar_pieza} no se puede modificar")
    else:
        res.insert(0, "La cantidad ingresada no es un número válido")
    entrada_cantidad.delete(0, 'end')



def actualizar_caja_torno(lista_predefinida, entrada_cantidad, res, tree):
    actualizar_pieza = lista_predefinida.get()
    entrada_actualizar = entrada_cantidad.get()

    try:
        if entrada_actualizar.strip().isdigit():
            entrada_actualizar = int(entrada_actualizar)

            if entrada_actualizar < 0:
                res.insert(0, "La Cantidad NO puede ser Negativa")
            else:
                conn = sqlite3.connect("basedatospiezas.db")
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT cantidad FROM piezas_del_fundicion WHERE piezas=?",
                    (actualizar_pieza,),
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is not None:
                    cantidad_actual = cantidad_actual[0]

                    if cantidad_actual >= entrada_actualizar:
                        nueva_cantidad = max(
                            0, cantidad_actual - entrada_actualizar)

                        cursor.execute(
                            "UPDATE piezas_del_fundicion SET cantidad=? WHERE piezas=?",
                            (nueva_cantidad, actualizar_pieza),
                        )
                        conn.commit()
                        cantidad_a_actualizar = entrada_cantidad.get()
                        cursor.execute(
                            "UPDATE torno SET cantidad = cantidad + ? WHERE piezas = ?",
                            (cantidad_a_actualizar, actualizar_pieza),
                        )
                        conn.commit()
                        cursor.execute(
                            "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = ?",
                            (cantidad_a_actualizar, actualizar_pieza),
                        )
                        conn.commit()
                        conn.close()
                        mostrar_datos(tree, "torno")
                        res.insert(
                            0,
                            f"Carga exitosa: Usted cargó {entrada_actualizar} {actualizar_pieza}:",
                        )
                    else:
                        res.insert(
                            0,
                            f"No hay suficientes piezas de {actualizar_pieza} disponibles.",
                        )
                else:
                    res.insert(
                        0, f"La Pieza {actualizar_pieza} no se puede modificar")
        else:
            res.insert(0, "La cantidad ingresada no es un número válido")
    except Exception as e:
        res.insert(0, f"Error: {e}")


def mostrar_piezas_torno_terminado(arbol, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE piezas IN ( 'manchon', 'manchon_250', 'eje_250', 'eje', 'rueditas', 'tornillo_guia', 'carros', 'movimientos', 'carros_250', 'buje_eje_eco');"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    info.config(text="Mostrar Datos: Piezas Terminadas")


def pulido_cabezal(entrada_agregar_porta_eje, lista_acciones):
    entrada_actualizar = entrada_agregar_porta_eje.get()

    if entrada_actualizar.strip().isdigit():
        entrada_actualizar = int(entrada_actualizar)

        if entrada_actualizar < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "SELECT cantidad FROM piezas_del_fundicion WHERE piezas = 'cabezal_inox'"
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is not None:
                    cantidad_actual = cantidad_actual[0]
                    nueva_cantidad = cantidad_actual - entrada_actualizar

                    cursor.execute(
                        "UPDATE piezas_del_fundicion SET cantidad= cantidad  - ? WHERE piezas = 'cabezal_inox'",
                        (entrada_actualizar,),
                    )
                    conn.commit()
                    cursor.execute(
                        "UPDATE piezas_finales_defenitivas SET cantidad= cantidad + ? WHERE piezas = 'cabezal_inox'",
                        (entrada_actualizar,),
                    )

                    conn.commit()
                    lista_acciones.insert(
                        0, f"Cabezales Pulidos: {entrada_actualizar}")
                else:
                    lista_acciones.insert(0, "Cantidad ingresada inválida")

            except Exception as e:
                # Manejo de errores
                mensaje_error = f"Error: {e}"
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)

            finally:
                conn.close()

    else:
        lista_acciones.insert(0, "Ingrese un número válido")


def de_enbruto_a_torneado(piezas, cantidad, lista_acciones):
    pieza = piezas.get()
    cantidad_texto = cantidad.get()  # Obtener el valor ingresado como texto

    if not cantidad_texto.isdigit():
        lista_acciones.insert(0, "Ingrese una cantidad válida (número entero positivo).")
        return

    cantidad = int(cantidad_texto)

    if cantidad <= 0:
        lista_acciones.insert(0, "La cantidad debe ser un número entero positivo.")
        return

    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        # Definir un diccionario para mapear piezas a las correspondientes en bruto
        piezas_enbruto = {
            "caja_torneado_330": "caja_330",
            "caja_torneado_300": "caja_300",
            "caja_torneado_250": "caja_250",
            "cubre_300" : "cubrecuchilla_300",
            "teletu_300" : "teletubi_300"
        }

        if pieza in piezas_enbruto:
            pieza_enbruto = piezas_enbruto[pieza]

            # Obtener la cantidad actual de piezas en bruto
            cursor.execute(
                f"SELECT cantidad FROM piezas_del_fundicion WHERE piezas = ?",
                (pieza_enbruto,),
            )
            cantidad_actual_enbruto = cursor.fetchone()

            if cantidad_actual_enbruto is not None:
                cantidad_actual_enbruto = cantidad_actual_enbruto[0]

                # Verificar si hay suficientes piezas en bruto disponibles
                if cantidad_actual_enbruto >= cantidad:
                    # Mostrar mensaje de confirmación
                    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea torneado {cantidad} {pieza_enbruto}?")
                    if not confirmacion:
                        lista_acciones.insert(0, "Se canceló la operación de torneado.")
                        return
                    
                    # Actualizar la cantidad de cajas en bruto
                    nueva_cantidad_enbruto = max(
                        0, cantidad_actual_enbruto - cantidad)
                    cursor.execute(
                        f"UPDATE piezas_del_fundicion SET cantidad = ? WHERE piezas = ?",
                        (nueva_cantidad_enbruto, pieza_enbruto),
                    )

                    # Actualizar la cantidad de cajas tornadas
                    cursor.execute(
                        f"UPDATE piezas_del_fundicion SET cantidad = cantidad + ? WHERE piezas = ?",
                        (cantidad, pieza),
                    )

                    lista_acciones.insert(
                        0, f"Se han Torneado {cantidad} {pieza_enbruto}.")
                    lista_acciones.insert(0, f"Se agregaron {cantidad} {pieza}")
                else:
                    lista_acciones.insert(
                        0, f"No hay suficientes piezas de {pieza_enbruto} en bruto disponibles.")
            else:
                lista_acciones.insert(
                    0, f"No se encontró la pieza en bruto correspondiente para {pieza}.")
        else:
            lista_acciones.insert(
                0, f"No se encontró la correspondencia en bruto para {pieza}.")

        conn.commit()

    except sqlite3.Error as e:
        # Manejo de errores y rollback en caso de error
        lista_acciones.insert(0, f"Error en la base de datos: {e}")
        conn.rollback()

    finally:
        conn.close()
        
    cantidad.delete(0, 'end')  # Limpiar el contenido del Entry después de la acción



def mostrar_cajas_bruto(arbol):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas, cantidad FROM piezas_del_fundicion WHERE piezas IN ('caja_330', 'caja_300', 'caja_250', 'cubrecuchilla_300', 'teletubi_300')"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)


def varilla_para_soldar(entrada_cantidad, varilla_tipo , lista_acciones):
    if varilla_tipo == "varilla_330":
        tipo = "330"
    elif varilla_tipo == "varilla_300":
        tipo = "300"
    elif varilla_tipo == "varilla_250":
        tipo = "250"
        
    entrada_actualizar = entrada_cantidad.get()

    if entrada_actualizar.strip().isdigit():
        entrada_actualizar = int(entrada_actualizar)

        if entrada_actualizar < 0:
            lista_acciones.insert(0, "La Cantidad NO puede ser Negativa")
        else:
            # Mostrar mensaje de confirmación
            confirmacion = messagebox.askyesno("Confirmar", f"¿Desea actualizar la cantidad de varillas soldadas: {entrada_actualizar} para el tipo {varilla_tipo}?")
            if not confirmacion:
                lista_acciones.insert(0, "Se canceló la operación de actualización de varillas soldadas.")
                return
            
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()

            try:
                cursor.execute(
                    f"SELECT cantidad FROM chapa WHERE piezas = 'varilla_{tipo}'"
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is not None:
                    cantidad_actual = cantidad_actual[0]
                    nueva_cantidad = cantidad_actual - entrada_actualizar

                    cursor.execute(
                        f"UPDATE chapa SET cantidad= cantidad  - ? WHERE piezas = 'varilla_{tipo}'",
                        (entrada_actualizar,),
                    )
                    conn.commit()
                    cursor.execute(
                        f"UPDATE piezas_finales_defenitivas SET cantidad= cantidad + ? WHERE piezas = 'varilla_carro_{tipo}'",
                        (entrada_actualizar,),
                    )

                    conn.commit()
                    lista_acciones.insert(
                        0, f"Varillas Soldadas: {entrada_actualizar}")
                else:
                    lista_acciones.insert(0, "Cantidad ingresada inválida")

            except Exception as e:
                # Manejo de errores
                mensaje_error = f"Error: {e}"
                print(mensaje_error)
                lista_acciones.insert(0, mensaje_error)

            finally:
                conn.close()
                entrada_cantidad.delete(0, 'end')

    else:
        lista_acciones.insert(0, "Ingrese un número válido")
    pass 


def mostrar_datos_mecanizado(arbol, info, piezas, tipo, tabla):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    # Utiliza marcadores de posición para evitar problemas de sintaxis y seguridad
    placeholders = ",".join(["?" for _ in piezas])
    
    # Consulta SQL con marcadores de posición
    query = f"SELECT piezas, cantidad FROM {tabla} WHERE piezas IN ({placeholders})  "
    
    cursor.execute(query, piezas)
    datos = cursor.fetchall()
    conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    txt = f"Mostrar Datos: chapas"
    info.config(text=txt)
    piezas_a_augeriar_lista = ["cuadrado_regulador"]


def varilla_soldador(arbol, info, piezas, tipo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    
    cursor.execute(f"SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE piezas IN ('varilla_carro_330', 'varilla_carro_300', 'varilla_carro_250')")
    datos = cursor.fetchall()
    conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    txt = f"Mostrar Datos: {tipo}"
    info.config(text=txt)


# --------------------------------------Armado de motores-----------------------------------------------------------

"""

def mostrar_motores(arbol):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE piezas = 'motores_220w'"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)


def mostrar_pieza_motores(arbol):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE sector = 'armado_de_caja'"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)


def armado_de_motor(modelo, cantidad, lista_acciones):
    tipo = modelo.get()
    cantidad_ = int(cantidad.get())  # Asegurarse de convertir la cantidad a un entero

    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    if tipo == 1:
        motores_finales = [
            "caja_torneado_330",
            "eje",
            "manchon",
            "ruleman_6005",
            "ruleman_6205",
            "corona_330",
            "seguer",
            "sinfin",
            "motor",
        ]
    elif tipo == 2:
        motores_finales = [
            "caja_torneado_300",
            "eje",
            "manchon",
            "ruleman_6005",
            "ruleman_6205",
            "corona_300",
            "seguer",
            "sinfin",
            "motor",
        ]
    else:
        lista_acciones.insert(0, "modelo NO valido")

    # Verificar si hay suficientes piezas en la base de datos
    for pieza in motores_finales:
        cursor.execute(
            "SELECT cantidad FROM piezas_del_fundicion WHERE piezas = ?", (pieza,)
        )
        cantidad_disponible = cursor.fetchone()[0]

        if cantidad_disponible < cantidad_:
            lista_acciones.insert(0, f"NO hay suficiente {pieza} para ensamblar")
            conn.close()

    # Si hay suficientes piezas, calcular la cantidad máxima de armado de motor
    for pieza in motores_finales:
        cursor.execute(
            "UPDATE piezas_del_fundicion SET cantidad = cantidad - ? WHERE piezas = ?",
            (cantidad_, pieza),
        )

    conn.commit()
    conn.close()

    lista_acciones.insert(
        f"Se ensamblaron {cantidad_} unidades del motor {tipo} correctamente."
    )


def cantida_posible_motores(piezas, lista_acciones, base_modelo=None):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    cantidades = {}

    try:
        for pieza in piezas:
            cursor.execute(
                "SELECT cantidad FROM piezas_finales_defenitivas WHERE piezas = ?",
                (pieza,),
            )
            resultado = cursor.fetchone()

            if resultado is not None:
                cantidad_disponible = resultado[0]
                cantidades[pieza] = cantidad_disponible

        if base_modelo is not None and len(cantidades) == len(base_modelo):
            cantidad_bases = min(cantidades.values()) // min(base_modelo.values())
            lista_acciones.insert(0, f"Se pueden armar {cantidad_bases} máquinas.")
        else:
            lista_acciones.insert(
                0, "No hay piezas suficientes para armar las máquinas."
            )
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def armado_de_motor(modelo, cantidad, lista_acciones):
    tipo = modelo.get()
    cantidad_ = int(cantidad.get())  # Asegurarse de convertir la cantidad a un entero

    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    if tipo == 1:
        motores_finales = [
            "caja_torneado_330",
            "eje",
            "manchon",
            "ruleman_6005",
            "ruleman_6205",
            "corona_330",
            "seguer",
            "sinfin",
            "motor",
        ]
    elif tipo == 2:
        motores_finales = [
            "caja_torneado_300",
            "eje",
            "manchon",
            "ruleman_6005",
            "ruleman_6205",
            "corona_300",
            "seguer",
            "sinfin",
            "motor",
        ]
    else:
        lista_acciones.insert(0, "modelo NO valido")

    # Verificar si hay suficientes piezas en la base de datos
    for pieza in motores_finales:
        cursor.execute(
            "SELECT cantidad FROM piezas_del_fundicion WHERE piezas = ?", (pieza,)
        )
        cantidad_disponible = cursor.fetchone()[0]

        if cantidad_disponible < cantidad_:
            lista_acciones.insert(0, f"NO hay suficiente {pieza} para ensamblar")
            conn.close()

    # Si hay suficientes piezas, calcular la cantidad máxima de armado de motor
    for pieza in motores_finales:
        cursor.execute(
            "UPDATE piezas_del_fundicion SET cantidad = cantidad - ? WHERE piezas = ?",
            (cantidad_, pieza),
        )

    conn.commit()
    conn.close()

    lista_acciones.insert(
        f"Se ensamblaron {cantidad_} unidades del motor {tipo} correctamente."
    )


def cajas_terminadas(entry_cantidad, modelo, lista_acciones):
    try:
        cantidad = int(entry_cantidad.get())
    except ValueError:
        lista_acciones.insert(0, "Error: Ingrese un número válido.")
        return

    modelo_opcion = modelo.get()

    modelos_disponibles = {
        1: { 
            "caja_torneado_330": 1,
            "eje": 1,
            "manchon": 1,
            "ruleman_6005": 1,
            "ruleman_6205": 2,
            "corona_330": 1,
            "seguer": 1,
            "sinfin": 1,
            "motores_220w": 1,
        },
        2: {
            "caja_torneado_300": 1,
            "eje": 1,
            "manchon": 1,
            "ruleman_6005": 1,
            "ruleman_6205": 2,
            "corona_300": 1,
            "seguer": 1,
            "sinfin": 1,
            "motores_220w": 1,
        },
        3: {
            "caja_torneado_250": 1,
            "eje_250": 1,
            "manchon_": 1,
            "ruleman_6005": 1,
            "ruleman_6205": 2,
            "corona_250": 1,
            "seguer": 1,
            "sinfin": 1,
            "motores250_220w": 1,
        },
    }

    if modelo_opcion not in modelos_disponibles:
        lista_acciones.insert(0, "Error: Opción de modelo no válida.")
        return

    modelo_dict = modelos_disponibles[modelo_opcion]
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        piezas_faltantes = []

        for pieza, cantidad_modelo in modelo_dict.items():
            cursor.execute(
                "SELECT cantidad FROM piezas_finales_defenitivas WHERE piezas = ? AND modelo = ?",
                (pieza, modelo_opcion),
            )
            resultado = cursor.fetchone()

            if resultado is not None:
                cantidad_actual = resultado[0]
                nueva_cantidad = cantidad_actual - (cantidad_modelo * cantidad)

                if nueva_cantidad < 0:
                    piezas_faltantes.append((pieza, abs(nueva_cantidad)))
                else:
                    # Actualizar la cantidad en la base de datos
                    cursor.execute(
                        "UPDATE piezas_finales_defenitivas SET cantidad = ? WHERE piezas = ? AND modelo = ?",
                        (nueva_cantidad, pieza, modelo_opcion),
                    )

        if piezas_faltantes:
            mensaje = f"Operación Cancelada. Piezas faltantes: {', '.join([f'{pieza} ({cantidad})' for pieza, cantidad in piezas_faltantes])}"
            lista_acciones.insert(0, mensaje)
        else:
            # Realizar las actualizaciones necesarias según el modelo
            if modelo_opcion == 1:
                cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'cajamotor_final_330' AND modelo = ?", (cantidad, modelo_opcion))
                print("330")
            elif modelo_opcion == 2:
                cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'cajamotor_final_300' AND modelo = ?", (cantidad, modelo_opcion))
                print("300")
            elif modelo_opcion == 3:
                cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'cajamotor_final_250' AND modelo = ?", (cantidad, modelo_opcion))
                print("250")
            else:
                lista_acciones.insert(0, "Error: Opción de modelo no válida.")

            lista_acciones.insert(
                0,
                "Operación Completada con Éxito. Todas las piezas se han actualizado.",
            )

        conn.commit()

    except sqlite3.Error as e:
        lista_acciones.insert(0, f"Error al actualizar la base de datos: {e}")

    finally:
        conn.close()
 
"""


def mostrar_pieza(arbol, piezas, res):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE piezas = '{piezas}'"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    text = "Mostrar Cantidad De Motore"
    res.config(text=text)

def mostrar_motores(arbol, res):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE piezas IN ('motores_220w', 'motores250_220w', 'motores_eco')"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    text = "Mostrar Cantidad De Motore"
    res.config(text=text)

def mostrar_piezas_armados(arbol, sector, res):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas ,cantidad, modelo FROM piezas_finales_defenitivas WHERE sector = '{sector}'"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    text = "Mostrar Cantidad De Piezas Para Motores"
    res.config(text=text)

def mostrar_piezas_por_modelo(arbol, pieza):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas ,cantidad, modelo FROM piezas_finales_defenitivas WHERE sector = 'armado_de_caja' AND  pieza = ? ", (
            pieza)
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

def mostrar_piezas_modelo(arbol, modelos, res, tipo):
    # Conectar a la base de datos
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    # Limpiar los datos existentes en el treeview
    for item in arbol.get_children():
        arbol.delete(item)

    # Iterar sobre los modelos y ejecutar la consulta para cada uno
    for tipo_motor in modelos:
        cursor.execute(
            "SELECT piezas, cantidad , modelo FROM piezas_finales_defenitivas WHERE piezas = ?",
            (tipo_motor,)
        )
        datos = cursor.fetchall()

        # Insertar los nuevos datos en el treeview
        for dato in datos:
            arbol.insert("", "end", values=dato)

    # Cerrar la conexión a la base de datos
    conn.close()

    text = f"Cantidad de piezas {tipo}"
    res.config(text=text)

def ensamblar_motor_terminado(modelo_seleccionado, cantidad_motores, res):

    motores_terminado = {
        1: {
            "caja_torneado_330": 1,
            "eje": 1,
            "manchon": 1,
            "ruleman_6005": 1,
            "ruleman_6205": 2,
            "corona_330": 1,
            "seguer": 1,
            "sinfin": 1,
            "motores_220w": 1,
            "oring": 1,
            "ruleman6000": 1

            
        },
        2: {
            "caja_torneado_300": 1,
            "eje": 1,
            "manchon": 1,
            "ruleman_6005": 1,
            "ruleman_6205": 2,
            "corona_300": 1,
            "seguer": 1,
            "sinfin": 1,
            "motores_220w": 1,
            "oring": 1,
            "ruleman6000": 1
        },
        3: {
            "caja_torneado_250": 1,
            "eje_250": 1,
            "manchon_250": 1,
            "ruleman_6004": 1,
            "ruleman_6204": 2,
            "corona_250": 1,
            "seguer": 1,
            "sinfin": 1,
            "motores250_220w": 1,
            "oring": 1,
            "ruleman6000": 1

        }
    }

    # Conectar a la base de datos usando 'with' statement
    with sqlite3.connect("basedatospiezas.db") as conn:
        cursor = conn.cursor()

        try:
            # Obtener las piezas necesarias para el modelo seleccionado
            piezas_necesarias = motores_terminado.get(modelo_seleccionado, {})

            if not piezas_necesarias:
                raise ValueError(
                    res.insert(0, f"No se encontró información para el modelo {modelo_seleccionado}."))

            # Verificar si hay suficientes piezas en el inventario
            cantidad = int(cantidad_motores.get())

            for pieza, cantidad_necesaria in piezas_necesarias.items():
                cursor.execute(
                    "SELECT cantidad FROM piezas_finales_defenitivas WHERE piezas = ?",
                    (pieza,)
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is None or cantidad_actual[0] < cantidad_necesaria * cantidad:
                    raise ValueError(
                         res.insert(0, f"No hay suficientes {pieza} en el inventario."))

            # Mostrar mensaje de confirmación
            confirmacion = messagebox.askyesno("Confirmar", f"¿Desea ensamblar {cantidad} motores del modelo {modelo_seleccionado}?")
            if not confirmacion:
                res.insert(0, "Se canceló la operación de ensamblado.")
                return

            # Restar la cantidad necesaria de cada pieza en el inventario
            for pieza, cantidad_necesaria in piezas_necesarias.items():
                cursor.execute(
                    "UPDATE piezas_finales_defenitivas SET cantidad = cantidad - ? WHERE piezas = ?",
                    (cantidad_necesaria * cantidad, pieza)
                )
                #cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE mecanizado = 'armado_caja' AND modelo = ?", (cantidad_motores, modelo))
            

            # Commit para aplicar los cambios
            conn.commit()

            if modelo_seleccionado in [1, 2, 3]:
                if modelo_seleccionado == 1:
                    nombre_pieza = "cajamotor_final_330"
                    txt = "Motor 330"
                elif modelo_seleccionado == 2:
                    nombre_pieza = "cajamotor_final_300"
                    txt = "Motor 300"
                elif modelo_seleccionado == 3:
                    nombre_pieza = "cajamotor_final_250"
                    txt = "Motor 250"

                cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = ?", (cantidad, nombre_pieza))

                if cantidad == 1:
                    res.insert(0, f"Se agregó {cantidad} motor terminado {txt}")
                else:
                    res.insert(0, f"Se agregaron {cantidad} motores terminados {txt}")
            else:
                res.insert(0, "Modelo no reconocido")

            conn.commit()
            cantidad_motores.delete(0, "end")
            
        except sqlite3.Error as e:
            # Imprimir el error y hacer rollback en caso de error
            res.insert(0, f"Error en la base de datos: {e}")
            conn.rollback()

        except ValueError as ve:
            print(ve)

def motores_terminados(arbol, res):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE mecanizado = 'armado_caja'"
    )
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    text = "Mostrar: Motores terminados "
    res.config(text=text)
    
    
    
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# -----------------------------------Pre Armado---------------------------


def stock_prearmado(arbol, res):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE sector = 'pre_armado'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    text = "Mostrar: Piezas PreArmado"
    res.config(text=text)


base_pre_inox_armada330 = {
    "inox_330": 1,
    "aro_numerador": 1,
    "espiral": 1,
    "perilla_numerador": 1,
    "tapita_perilla": 2,
    "patas": 4,
    "movimientos_final": 1,
    "eje_rectificado": 1,
    "resorte_movimiento": 1,
    "tornillo_guia": 1,
    "guia_U": 1,
    "teclas": 1,
    "cable_220w": 1,
    "varilla_carro_330": 1,
    "carros_final": 1,
    "rueditas": 4,
    "resorte_carro": 2,
    "cajamotor_final_330": 1,
    "capacitores": 1,
}

base_pre_inox_armada300 = {
    "inox_300": 1,
    "aro_numerador": 1,
    "espiral": 1,
    "perilla_numerador": 1,
    "tapita_perilla": 2,
    "patas": 4,
    "movimientos_final": 1,
    "eje_rectificado": 1,
    "resorte_movimiento": 1,
    "tornillo_guia": 1,
    "guia_U": 1,
    "teclas": 1,
    "cable_220w": 1,
    "varilla_carro_300": 1,
    "carros_final": 1,
    "rueditas": 4,
    "resorte_carro": 2,
    "cajamotor_final_300": 1,
    "capacitores": 1,
}

base_pre_inox_armada250 = {
    "inox_250": 1,
    "aro_numerador": 1,
    "espiral": 1,
    "perilla_numerador": 1,
    "tapita_perilla": 2,
    "patas": 4,
    "movimientos_final": 1,
    "eje_rectificado": 1,
    "resorte_movimiento": 1,
    "tornillo_guia": 1,
    "guia_U": 1,
    "teclas": 1,
    "cable_220w": 1,
    "varilla_carro_250": 1,
    "carros_250_final": 1,
    "rueditas": 4,
    "cajamotor_final_250": 1,
    "capacitores_250": 1,
}

base_pre_pintada_armada330 = {
    "base_pintada_330": 1,
    "aro_numerador": 1,
    "espiral": 1,
    "perilla_numerador": 1,
    "tapita_perilla": 2,
    "patas": 4,
    "movimientos_final": 1,
    "eje_rectificado": 1,
    "resorte_movimiento": 1,
    "tornillo_guia": 1,
    "guia_U": 1,
    "teclas": 1,
    "cable_220w": 1,
    "varilla_carro_330": 1,
    "carros_final": 1,
    "rueditas": 4,
    "resorte_carro": 2,
    "cajamotor_final_330": 1,
    "capacitores": 1,
    "bandeja_330" : 1
}

base_pre_pintada_armada300 = {
    "base_pintada_300": 1,
    "aro_numerador": 1,
    "espiral": 1,
    "perilla_numerador": 1,
    "tapita_perilla": 2,
    "patas": 4,
    "movimientos_final": 1,
    "eje_rectificado": 1,
    "resorte_movimiento": 1,
    "tornillo_guia": 1,
    "guia_U": 1,
    "teclas": 1,
    "cable_220w": 1,
    "varilla_carro_300": 1,
    "carros_final": 1,
    "rueditas": 4,
    "resorte_carro": 2,
    "cajamotor_final_300": 1,
    "capacitores": 1,
    "bandeja_300" : 1
}


def mostrar_por_pieza(arbol, modelo, res):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE sector = 'pre_armado' AND modelo = '{modelo}'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    text = f"Mostrar: Piezas {modelo}"
    res.config(text=text)


def maquinas_pre_armadas_disponibles(
    cantidad_maquinas, base_pre_armada, inventario_piezas
):
    # Inicializar la lista de piezas faltantes
    piezas_faltantes = []

    for pieza, cantidad_necesaria in base_pre_armada.items():
        if pieza not in inventario_piezas:
            # Si falta una pieza en el inventario, agregar a la lista de piezas faltantes
            piezas_faltantes.append(
                (pieza, cantidad_necesaria * cantidad_maquinas))
        else:
            cantidad_inventario = inventario_piezas[pieza]
            maquinas_posibles_con_pieza = cantidad_inventario // cantidad_necesaria

            # Verificar si la cantidad de piezas en inventario es suficiente
            if maquinas_posibles_con_pieza < cantidad_maquinas:
                piezas_faltantes.append(
                    (
                        pieza,
                        cantidad_necesaria
                        * (cantidad_maquinas - maquinas_posibles_con_pieza),
                    )
                )

    return piezas_faltantes


def conectar_base_datos_y_calcular_maquinas(cantidad_maquinas, base_pre_armada, res):
    # Conectar a la base de datos
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        # Ejecutar una consulta para obtener la cantidad de cada pieza en el inventario
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas")
        resultados = cursor.fetchall()

        # Crear un diccionario con la información del inventario
        inventario_piezas = dict(resultados)

        # Calcular las piezas faltantes para la cantidad de máquinas especificada
        piezas_faltantes = maquinas_pre_armadas_disponibles(
            cantidad_maquinas, base_pre_armada, inventario_piezas
        )

        if not piezas_faltantes:
            res.insert(0, f"Se pueden armar {cantidad_maquinas} máquinas pre-armadas.")
        else:
            res.insert(0, 
                f"No hay suficientes piezas para armar {cantidad_maquinas} máquinas pre-armadas. Piezas faltantes:"
            )
            for pieza, cantidad_faltante in piezas_faltantes:
                res.insert(0, f"{pieza}: {cantidad_faltante}")

    except sqlite3.Error as e:
        res.insert(0, f"Error al obtener datos de la base de datos: {e}")

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

#conectar_base_datos_y_calcular_maquinas(5, base_pre_inox_armada330)

def actualizar_inventario(res, cantidad_maquinas, tipo_maquina, ensamblar=True):
    cantidad_maquinas = int(cantidad_maquinas)
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        # Obtener el inventario actual de piezas
        cursor.execute("SELECT piezas, cantidad FROM piezas_finales_defenitivas")
        resultados = cursor.fetchall()
        inventario_piezas = dict(resultados)

        # Definir la base pre-armada según el tipo de máquina
        if tipo_maquina == "inox_330":
            base_pre_armada = base_pre_inox_armada330
        elif tipo_maquina == "inox_300":
            base_pre_armada = base_pre_inox_armada300
        elif tipo_maquina == "inox_250":
            base_pre_armada = base_pre_inox_armada250
        elif tipo_maquina == "pintada_330":
            base_pre_armada = base_pre_pintada_armada330
        elif tipo_maquina == "pintada_300":
            base_pre_armada = base_pre_pintada_armada300
        else:
            res.insert(0, f"Tipo de máquina no reconocido: {tipo_maquina}")
            return inventario_piezas, []

        # Verificar si hay suficientes piezas disponibles antes de realizar el descuento
        piezas_faltantes = []
        for pieza, cantidad_necesaria in base_pre_armada.items():
            if inventario_piezas[pieza] < cantidad_necesaria * cantidad_maquinas:
                piezas_faltantes.append(
                    (
                        pieza,
                        cantidad_necesaria * cantidad_maquinas - inventario_piezas[pieza],
                    )
                )

        if piezas_faltantes:
            res.insert(0, "No hay suficientes piezas para ensamblar la cantidad deseada de máquinas.")
            # Imprimir las piezas que faltan en la consola
            res.insert(1, f"Piezas faltantes para ensamblar {cantidad_maquinas} máquinas {tipo_maquina}:")
            for pieza, cantidad_faltante in piezas_faltantes:
                res.insert(1, f"Faltan {pieza}: {cantidad_faltante}")

            return inventario_piezas, piezas_faltantes

        # Mostrar mensaje de confirmación
        accion = "ensamblar" if ensamblar else "eliminar"
        confirmacion = messagebox.askyesno("Confirmar", f"¿Desea {accion} {cantidad_maquinas} máquinas {tipo_maquina}?")
        if not confirmacion:
            res.insert(0, f"Se canceló la operación de {accion} máquinas.")
            return inventario_piezas, []

        # Actualizar el inventario según sea necesario
        for pieza, cantidad_necesaria in base_pre_armada.items():
            if ensamblar:
                inventario_piezas[pieza] -= cantidad_necesaria * cantidad_maquinas
                if inventario_piezas[pieza] < 0:
                    inventario_piezas[pieza] = 0
            else:
                inventario_piezas[pieza] += cantidad_necesaria * cantidad_maquinas

        # Actualizar la base de datos con el nuevo inventario
        for pieza, cantidad_actualizada in inventario_piezas.items():
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = ? WHERE piezas = ?",
                (cantidad_actualizada, pieza),
            )

        # Incrementar la cantidad de la base pre-armada según el tipo de máquina
        if tipo_maquina == "inox_330":
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'base_pre_armada330inox'",
                (cantidad_maquinas,),
            )
        elif tipo_maquina == "inox_300":
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'base_pre_armada300inox'",
                (cantidad_maquinas,),
            )
        elif tipo_maquina == "inox_250":
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'base_pre_armada250inox'",
                (cantidad_maquinas,),
            )
        elif tipo_maquina == "pintada_330":
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'base_pre_armada330pint'",
                (cantidad_maquinas,),
            )
        elif tipo_maquina == "pintada_300":
            cursor.execute(
                "UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'base_pre_armada300pint'",
                (cantidad_maquinas,),
            )
        else:
            res.insert(0,"Error al actualizar.")

        # Confirmar los cambios en la base de datos
        conn.commit()

        # Imprimir un mensaje indicando si se ensamblaron o eliminaron las máquinas
        accion = "ensamblaron" if ensamblar else "eliminaron"

        res.insert(0,f"{cantidad_maquinas} máquinas {tipo_maquina} se {accion}. Inventario actualizado en la base de datos.")

    except sqlite3.Error as e:
        res.insert(0,f"Error al actualizar el inventario en la base de datos: {e}")
        piezas_faltantes = []

    finally: 
        conn.close()
        cantidad_maquinas.delete(0, "end")

def stock_prebases(arbol):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE mecanizado = 'prearmado'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)


def ensamblar_maquinas(cantidad_ensamblar_entry, lista_acciones):

    maquinas_mes = 0

    cantidad_ensamblada = cantidad_ensamblar_entry.get()

    # Validamos que la cantidad ingresada sea un número válido
    try:
        cantidad_ensamblada = int(cantidad_ensamblada)
    except ValueError:
        lista_acciones.insert(0, "Ingrese una Cantidad Válida")
        return

    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Pieza, Cantidad FROM piezas_de_330")
    stock = cursor.fetchall()

    cantidades_requeridas = {
        "Base": 1,
        "Motor": 1,
        "Teletubi": 1,
        "Cuchilla": 1,
        "Vela": 1,
        "CubreCuchilla": 1,
        "Cabezal": 1,
        "Planchada": 1,
        "Brazo": 1,
        "Tapa_afilador": 1,
        "Afilador": 1,
        "Patas": 4
    }

    for pieza, cantidad in stock:
        if pieza in cantidades_requeridas:
            cantidades_requerida = cantidades_requeridas[pieza] * \
                cantidad_ensamblada
            if cantidad < cantidades_requerida:
                lista_acciones.insert(
                    0, "No hay suficientes {pieza} en el stock para ensamblar {cantidad_ensamblada} máquinas.")
                conn.close()
                return

    # Si hay suficientes piezas, ensamblar las máquinas y actualizar las cantidades en la base de datos
    for pieza, cantidad in stock:
        if pieza in cantidades_requeridas:
            cantidad_requerida = cantidades_requeridas[pieza] * \
                cantidad_ensamblada
            nueva_cantidad = cantidad - cantidad_requerida
            cursor.execute(
                "UPDATE piezas_de_330 SET Cantidad=? WHERE Pieza=?", (nueva_cantidad, pieza))

    # Actualizar el contador de máquinas ensambladas

    maquinas_mes += cantidad_ensamblada

    # Crear una etiqueta para mostrar la cantidad total de máquinas ensambladas en el mes
    lista_acciones.insert(0, "Maquinas Terminadas en el mes: {maquinas_mes}")

    # Mostrar la cantidad total de máquinas ensambladas
    lista_acciones.insert( 0, "Se Armaron {cantidad_ensamblada} máquinas \h Total del mes: {maquinas_mes}")

    conn.commit()
    conn.close()
    mostrar_datos()

def bases_terminados(arbol, res):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE mecanizado = 'prearmado'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    text = "Mostrar: Piezas PreArmado"
    res.config(text=text)


#-----------------------armado-afilador----------------------------------------------

def mostrar_pieza_afilador(arbol, res ):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE sector = 'afilador'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        res.insert(0, f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
        text = "Mostrar Pieza de Afiladores"
        res.config(text=text)

#enviar piezas a roman 
def mostrar_pieza_afilador_roman(arbol, res ):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad FROM piezas_afiladores_roman"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        res.insert(0, f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
        text = "Mostrar Pieza En Roman"
        res.config(text=text)

def mostrar_afilador_final(arbol, res):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad FROM piezas_finales_defenitivas WHERE piezas = 'afilador_final'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        res.insert(0, f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
    
    text = "Mostrar Afiladores Terminados"
    res.config(text=text)
    


def armado_final_afiladores_y_agregar_cantidad(cantidad_ingresada_widget, res):
    cantidad_ingresada = cantidad_ingresada_widget.get()  # Obtener el valor ingresado por el usuario
    cantidad_ingresada_int = int(cantidad_ingresada)  # Convertirlo a entero si es necesario

    cantidad_piezas = {
        "capuchon_afilador": 2,
        "carcaza_afilador": 1,
        "eje_corto": 1,
        "eje_largo": 1,
        "ruleman608": 2,
        "palanca_afilador": 1,
        "resorte_palanca": 1,
        "resorte_empuje": 2
    }

    with sqlite3.connect("basedatospiezas.db") as conn:
        cursor = conn.cursor()

        try:
            piezas_suficientes = True

            for pieza, cantidad_pieza in cantidad_piezas.items():
                cursor.execute("SELECT cantidad FROM piezas_afiladores_roman WHERE piezas = ?", (pieza,))
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is None or cantidad_actual[0] < cantidad_ingresada_int * cantidad_pieza:
                    messagebox.showerror("Error", f"No hay suficiente cantidad de {pieza} en lo de roman")
                    piezas_suficientes = False
                    break

            if piezas_suficientes:
                confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas armar {cantidad_ingresada_int} unidades de afiladores?")
                if confirmacion:
                    for pieza, cantidad_pieza in cantidad_piezas.items():
                        cantidad_restante = cantidad_actual[0] - cantidad_ingresada_int * cantidad_pieza
                        cursor.execute("UPDATE piezas_afiladores_roman SET cantidad = ? WHERE piezas = ?", (cantidad_restante, pieza))

                    cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'afilador_final'", (cantidad_ingresada_int,))
                    conn.commit()
                    messagebox.showinfo("Éxito", f"Roman armó {cantidad_ingresada_int} unidades de afiladores")
            
            # Limpiar el contenido del Entry después de la acción
            cantidad_ingresada_widget.delete(0, 'end')
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error en la base de datos: {e}")
            conn.rollback()

        except ValueError as ve:
            messagebox.showerror("Error", ve)

# '''''''''''''''''''''''''''''''''''''''''''''''ARmado Final''''''''''''''''''''''

def mostrar_piezas_finales(arbol, res):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas ,cantidad, modelo FROM piezas_finales_defenitivas WHERE sector = 'armado_final'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        
    text = "Mostrar: Piezas Finales"
    res.config(text=text)

def mostrar_piezas_i330(arbol, res, modelo, tipo):
    
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad, modelo FROM piezas_finales_defenitivas WHERE piezas IN ({seq}) AND sector = 'armado_final'"
            .format(seq=','.join(['?']*len(modelo))),
            tuple(modelo)
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
    finally:
        conn.close()

    for item in arbol.get_children():
        arbol.delete(item)

    for dato in datos:
        arbol.insert("", "end", values=dato)
        

    text = f"Mostrar: Piezas Seleccionadas {tipo}"
    res.config(text=text)


#'''''''''''''''''''armado'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def consulta_bases_terminadas(arbol, mostrar):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad , modelo FROM piezas_finales_defenitivas WHERE mecanizado = 'prearmado'")
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    subtitulo_text = "Mostrar Datos: Bases Terminadas"
    mostrar.config(text=subtitulo_text)


def consulta_insumos(arbol, mostrar):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad, modelo FROM piezas_finales_defenitivas WHERE sector = 'armado_final' AND mecanizado = 'shop'")
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    subtitulo_text = "Mostrar Datos: Insumos"
    mostrar.config(text=subtitulo_text)


def consulta_piezas(arbol, mostrar):
    try:
        with sqlite3.connect("basedatospiezas.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT piezas, cantidad, modelo FROM piezas_finales_defenitivas WHERE sector = 'armado_final' AND mecanizado IN ('pulido', 'niquelado')")
            datos = cursor.fetchall()

        # Borrar todos los elementos existentes en el Treeview
        for item in arbol.get_children():
            arbol.delete(item)

        # Insertar los nuevos datos en el Treeview
        for dato in datos:
            arbol.insert("", "end", values=dato)

        subtitulo_text = "Mostrar Datos: Piezas"
        mostrar.config(text=subtitulo_text)
    except sqlite3.Error as e:
        # Manejo de errores: Imprimir el error o realizar alguna acción adecuada.
        print(f"Error SQLite: {e}")


def consulta_afiladores(arbol, mostrar):
    try:
        with sqlite3.connect("basedatospiezas.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT piezas, cantidad, modelo FROM piezas_finales_defenitivas WHERE piezas = 'afilador_final'")
            datos = cursor.fetchall()

        # Borrar todos los elementos existentes en el Treeview
        for item in arbol.get_children():
            arbol.delete(item)

        # Insertar los nuevos datos en el Treeview
        for dato in datos:
            arbol.insert("", "end", values=dato)

        subtitulo_text = "Mostrar Datos: Piezas"
        mostrar.config(text=subtitulo_text)
    except sqlite3.Error as e:
        # Manejo de errores: Imprimir el error o realizar alguna acción adecuada.
        print(f"Error SQLite: {e}")

i330 = {
    "brazo_330": 1,#
    "cubrecuchilla_330": 1,#
    "velero": 1,#
    "perilla_brazo": 1,#
    "cabezal_inox": 1,#
    "teletubi_330": 1,
    "cuchilla_330": 1,#
    "cuadrado_regulador_final": 1,#
    "vela_final_330": 1,#
    "cubre_motor_rectangulo": 1,
    "cubre_motor_cuadrado": 1,
    "planchada_final_330": 1,#
    "varilla_brazo_330": 1,#
    "resorte_brazo": 1,#
    "tapa_afilador": 1,#
    "pipas": 2,#
    "tubo_manija": 1,#
    "afilador_final": 1,#
    "perilla_cubrecuchilla": 2,#
    "perilla_afilador": 1,#
    "base_afilador_330": 1,
    "base_pre_armada330inox": 1,#
    "piedra_afilador": 1,#
    "pinche_frontal" : 1,#
    "pinche_lateral" : 1,#
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligro": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1,
    "fadeco_330_4estrella": 1
}

i300 = {
    "brazo_300": 1,
    "cubre_300": 1,
    "velero": 1,
    "perilla_brazo": 1,
    "cabezal_inox": 1,
    "teletu_300": 1,
    "cuchilla_300": 1,
    "cuadrado_regulador_final": 1,
    "vela_final_300": 1,
    "cubre_motor_rectangulo": 1,
    "cubre_motor_cuadrado": 1,
    "planchada_final_300": 1,
    "varilla_brazo_300": 1,
    "resorte_brazo": 1,
    "tapa_afilador": 1,
    "pipas": 2,
    "tubo_manija": 1,
    "afilador_final": 1,
    "perilla_cubrecuchilla": 2,
    "perilla_afilador": 1,
    "base_afilador_300": 1,
    "base_pre_armada300inox": 1,
    "piedra_afilador": 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1 ,
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligro": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1,
    "fadeco_300_4estrella": 1
}

i250 = {
    "brazo_250": 1,
    "cubrecuchilla_250": 1,
    "velero": 1,
    "perilla_brazo": 1,
    "cabezal_250": 1,
    "teletubi_250": 1,
    "cuchilla_250": 1,
    "cuadrado_regulador_final": 1,
    "vela_final_250": 1,
    "cubre_motor_rectangulo": 1,
    "planchada_final_250": 1,
    "varilla_brazo_250": 1,
    "resorte_brazo": 1,
    "tapa_afilador_250": 1,
    "pipas": 2,
    "tubo_manija_250": 1,
    "afilador_final": 1,
    "perilla_cubrecuchilla": 2,
    "perilla_afilador": 1,
    "base_afilador_250": 1,
    "base_pre_armada250inox": 1,
    "piedra_afilador": 1,
    "capuchon_250": 1 ,
    "pinche_frontal_250" : 1,
    "pinche_lateral_250" : 1 ,
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligro": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1,
    "fadeco_250_2estrella": 1
}

p330 = {
    "brazo_330": 1,
    "cubrecuchilla_330": 1,
    "velero": 1,
    "perilla_brazo": 1,
    "cabezal_pintura": 1,
    "teletubi_330": 1,
    "cuchilla_330": 1,
    "cuadrado_regulador_final": 1,
    "vela_final_330": 1,
    "cubre_motor_rectangulo": 1,
    "cubre_motor_cuadrado": 1,
    "planchada_final_330": 1,
    "varilla_brazo_330": 1,
    "resorte_brazo": 1,
    "tapa_afilador": 1,
    "pipas": 2,
    "tubo_manija": 1,
    "afilador_final": 1,
    "perilla_cubrecuchilla": 2,
    "perilla_afilador": 1,
    "base_afilador_330": 1,
    "base_pre_armada330pint": 1,
    "piedra_afilador": 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1,
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligro": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1,
    "fadeco_330_3estrella": 1
}

p300 = {
    "brazo_300": 1,
    "cubre_300": 1,
    "velero": 1,
    "perilla_brazo": 1,
    "cabezal_pintura": 1,
    "teletu_300": 1,
    "cuchilla_300": 1,
    "cuadrado_regulador_final": 1,
    "vela_final_300": 1,
    "cubre_motor_rectangulo": 1,
    "cubre_motor_cuadrado": 1,
    "planchada_final_300": 1,
    "varilla_brazo_300": 1,
    "resorte_brazo": 1,
    "tapa_afilador": 1,
    "pipas": 2,
    "tubo_manija": 1,
    "afilador_final": 1,
    "perilla_cubrecuchilla": 2,
    "perilla_afilador": 1,
    "base_afilador_300": 1,
    "base_pre_armada300pint": 1,
    "piedra_afilador": 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1,
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligro": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1,
    "fadeco_300_3estrella": 1
}


def armado_de_maquinas(cantidad_maquinas, tipo_seleccionado, result):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'armado_final' OR sector = 'contro_calidad'")
    filas = cursor.fetchall()
    base_de_datos = {pieza: cantidad for pieza, cantidad in filas}

    piezas_faltantes = []

    # Utiliza diccionarios específicos para cada tipo
    tipos_piezas = {
        'inox_330': i330,
        'inox_300': i300,
        'inox_250': i250,
        'pintada_330': p330,
        'pintada_300': p300,
        # ... (add more types as needed)
    }

    # Obtén el diccionario específico para el tipo seleccionado
    tipo_a_ensamblar = tipos_piezas.get(tipo_seleccionado)

    if tipo_a_ensamblar is None:
        text2 = (f"Tipo {tipo_seleccionado} no reconocido.")
        result.insert(0, text2)
        conn.close()
        return

    # Actualiza el diccionario para reflejar la cantidad de máquinas
    tipo_a_ensamblar = {pieza: cantidad * int(cantidad_maquinas)
                        for pieza, cantidad in tipo_a_ensamblar.items()}

    # Verifica si hay suficientes piezas disponibles
    piezas_disponibles = True
    for pieza, cantidad_necesaria in tipo_a_ensamblar.items():
        cursor.execute("SELECT cantidad FROM piezas_finales_defenitivas WHERE (sector = 'armado_final' OR sector = 'control_calidad') AND piezas = ?", (pieza,))
        cantidad_disponible = cursor.fetchone()

        if cantidad_disponible:
            cantidad_disponible = int(cantidad_disponible[0])
            cantidad_faltante = max(
                0, cantidad_necesaria - cantidad_disponible)

            if cantidad_faltante > 0:
                piezas_faltantes.append((pieza, cantidad_faltante))
                piezas_disponibles = False

    if piezas_disponibles:
        # Si todas las piezas están disponibles, resta las cantidades
        for pieza, cantidad_necesaria in tipo_a_ensamblar.items():
            cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad - ? WHERE (sector = 'armado_final' OR sector = 'control_calidad') AND piezas = ?",
               (cantidad_necesaria, pieza))
            conn.commit()

        cursor.execute(f"UPDATE producto_final SET cantidad = cantidad + ? WHERE piezas = ?",
                       (int(cantidad_maquinas), tipo_seleccionado))
        conn.commit()

        # Mostrar messagebox para confirmar los cambios
        confirmacion = messagebox.askyesno("Confirmar", f"¿Desea agregar {cantidad_maquinas} máquinas {tipo_seleccionado}?")
        if confirmacion:
            text3 = f"Se agregaron {cantidad_maquinas} máquinas {tipo_seleccionado}."
            result.insert(0, text3)
        else:
            text4 = "Se canceló la operación de armado de máquinas."
            result.insert(0, text4)
    else:
        # Si alguna pieza falta, muestra un mensaje
        text4 = "No se pueden armar las máquinas. Faltan las siguientes piezas:"
        result.insert(0, text4)
        for pieza, cantidad_faltante in piezas_faltantes:
            result.insert(0, f"{pieza}: {cantidad_faltante} unidades.")

    conn.close()
    

def mostrar_maquinas_teminadas(arbol,res):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piezas, cantidad, modelo  FROM producto_final ")
    datos = cursor.fetchall()
    conn.close()
    for item in arbol.get_children():
        arbol.delete(item)
    for dato in datos:
        arbol.insert("", "end", values=dato)

    subtitulo_text = "Mostrar Datos: Maquinas Terminadas"
    res.config(text=subtitulo_text)




#999999999999999999posivilidades969699999999999999999999


###############################################Armado FInal ########################################


def maquinas_dis(modelo_maquina):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'armado_final' " )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return -1
    finally:
        conn.close()

    if modelo_maquina == "inox 330":
        piezas_necesarias = i330
    elif modelo_maquina == "inox 300":
        piezas_necesarias = i300
    elif modelo_maquina == "inox 250":
        piezas_necesarias = i250
    elif modelo_maquina == "pint 330":
        piezas_necesarias = p330
    elif modelo_maquina == "pint 300":
        piezas_necesarias = p300
    
    cantidad_minima = float('inf')
    for pieza, cantidad_necesaria in piezas_necesarias.items():
        for dato in datos:
            if dato[0] == pieza:
                cantidad_disponible = dato[1]
                cantidad_posible = cantidad_disponible // cantidad_necesaria
                cantidad_minima = min(cantidad_minima, cantidad_posible)

    return cantidad_minima

def mostrar_maquinas_disponibles(modelo_maquina, label_muestra):
    total_maquinas = maquinas_dis(modelo_maquina)
    label_muestra.config(text=f"{total_maquinas}")

def obtener_maquina_final():
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'armado_final'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return {}
    finally:
        conn.close()

    cantidades_disponibles = {}
    for pieza, cantidad in datos:
        cantidades_disponibles[pieza] = cantidad

    return cantidades_disponibles


def verificar_posibilidad_maquina_teminada(cantidad_deseada, modelo_seleccionado):
    # Obtener la base según el modelo
    maquina_final = {
        "inoxidable 330": i330,
        "inoxidable 300": i300,
        "inoxidable 250": i250,
        "pintada 330": p330,
        "pintada 300": p300
    }

    tipo_de_modelo = maquina_final.get(modelo_seleccionado)

    if tipo_de_modelo is None:
        print(f"Modelo '{modelo_seleccionado}' no reconocido.")
        return False, {}

    # Obtener las cantidades de piezas disponibles desde la base de datos
    cantidades_disponibles = obtener_maquina_final()

    # Verificar si es posible armar la cantidad deseada
    cantidad_minima = float('inf')
    piezas_faltantes = {}

    for pieza, cantidad_necesaria in tipo_de_modelo.items():
        cantidad_disponible = cantidades_disponibles.get(pieza, 0)

        # Calcular la cantidad máxima que se puede armar sin exceder las cantidades disponibles
        cantidad_maxima_posible = cantidad_disponible // cantidad_necesaria

        cantidad_minima = min(cantidad_minima, cantidad_maxima_posible)

        # Calcular la cantidad faltante y actualizar el diccionario piezas_faltantes
        cantidad_faltante = max(0, cantidad_deseada * cantidad_necesaria - cantidad_disponible)
        if cantidad_faltante > 0:
            piezas_faltantes[pieza] = cantidad_faltante

    # Verificar si la cantidad deseada es alcanzable
    if cantidad_minima >= cantidad_deseada:
        return True, piezas_faltantes
    else:
        return False, piezas_faltantes


def consultar_maquinas_final(entry_cantidad, tabla_consultas, lista_acciones, tipo_pre_combox):
    # Esta función realiza la consulta y actualiza la interfaz gráfica
    for item in tabla_consultas.get_children():
        tabla_consultas.delete(item)

    cantidad_deseada = int(entry_cantidad.get())
    modelo_seleccionado = tipo_pre_combox.get()

    se_puede_armar, piezas_faltantes = verificar_posibilidad_maquina_teminada(cantidad_deseada, modelo_seleccionado)

    if se_puede_armar:
        mensaje = f"Se pueden armar {cantidad_deseada} Motores {modelo_seleccionado}."
        lista_acciones.insert(0, mensaje)
    else:
        mensaje = f"No se pueden armar {cantidad_deseada} Motores {modelo_seleccionado}. Piezas faltantes en la tabla:"
        lista_acciones.insert(0, mensaje)
        for pieza, cantidad_faltante in piezas_faltantes.items():
            # Agregar las filas al treeview
            tabla_consultas.insert("", tk.END, values=(pieza, cantidad_faltante), tags=("blue",))



 
#-==============================funciones de los motores ==============================================

motor_330 = {
    "caja_torneado_330": 1,
    "eje": 1,
    "manchon": 1,
    "ruleman_6005": 1,
    "ruleman_6205": 2,
    "corona_330": 1,
    "seguer": 1,
    "sinfin": 1,
    "motores_220w": 1,
    "oring":1,
    "ruleman6000": 1
}
motor_300 =  {
    "caja_torneado_300": 1,
    "eje": 1,
    "manchon": 1,
    "ruleman_6005": 1,
    "ruleman_6205": 2,
    "corona_300": 1,
    "seguer": 1,
    "sinfin": 1,
    "motores_220w": 1,
    "oring":1,            
    "ruleman6000": 1
}
motor_250 = {
    "caja_torneado_250": 1,
    "eje_250": 1,
    "manchon_250": 1,
    "ruleman_6004": 1,
    "ruleman_6204": 2,
    "corona_250": 1,
    "seguer": 1,
    "sinfin": 1,
    "motores250_220w": 1,
    "oring":1,
    "ruleman6000": 1

}


   
def contar_motores_disponibles(modelo_motor):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'armado_de_caja'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        # Manejo de errores, puedes adaptarlo según tus necesidades
        print(f"Error al obtener datos de la base de datos: {e}")
        return -1  # Indicador de error
    finally:
        conn.close()


    if modelo_motor == "330":
        piezas_necesarias = motor_330
    elif modelo_motor == "300":
        piezas_necesarias = motor_300
    elif modelo_motor == "250":
        piezas_necesarias = motor_250

    
    # Verificar la cantidad mínima de piezas necesarias para un afilador

    # Calcular la cantidad máxima de afiladores que se pueden armar
    cantidad_minima = float('inf')
    for pieza, cantidad_necesaria in piezas_necesarias.items():
        for dato in datos:
            if dato[0] == pieza:
                cantidad_disponible = dato[1]
                cantidad_posible = cantidad_disponible // cantidad_necesaria
                cantidad_minima = min(cantidad_minima, cantidad_posible)

    return cantidad_minima

def actualizar_muestra_motores(modelo_motor, label_muestra):
    total_motores = contar_motores_disponibles(modelo_motor)
    label_muestra.config(text=f"{total_motores}")



def obtener_cantidad_piezas_motor():
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'armado_de_caja'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return {}
    finally:
        conn.close()

    cantidades_disponibles = {}
    for pieza, cantidad in datos:
        cantidades_disponibles[pieza] = cantidad

    return cantidades_disponibles


def verificar_posibilidad_construccion_motor(cantidad_deseada, modelo_seleccionado):
    # Obtener la base según el modelo
    bases_prearmadas = {
        "330": motor_330,
        "300": motor_300,
        "250": motor_250
    }

    tipo_de_modelo = bases_prearmadas.get(modelo_seleccionado)

    if tipo_de_modelo is None:
        print(f"Modelo '{modelo_seleccionado}' no reconocido.")
        return False, {}

    # Obtener las cantidades de piezas disponibles desde la base de datos
    cantidades_disponibles = obtener_cantidad_piezas_motor()

    # Verificar si es posible armar la cantidad deseada
    cantidad_minima = float('inf')
    piezas_faltantes = {}

    for pieza, cantidad_necesaria in tipo_de_modelo.items():
        cantidad_disponible = cantidades_disponibles.get(pieza, 0)

        # Calcular la cantidad máxima que se puede armar sin exceder las cantidades disponibles
        cantidad_maxima_posible = cantidad_disponible // cantidad_necesaria

        cantidad_minima = min(cantidad_minima, cantidad_maxima_posible)

        # Calcular la cantidad faltante y actualizar el diccionario piezas_faltantes
        cantidad_faltante = max(0, cantidad_deseada * cantidad_necesaria - cantidad_disponible)
        if cantidad_faltante > 0:
            piezas_faltantes[pieza] = cantidad_faltante

    # Verificar si la cantidad deseada es alcanzable
    if cantidad_minima >= cantidad_deseada:
        return True, piezas_faltantes
    else:
        return False, piezas_faltantes

  
def consultar_piezas_sector_motor(entry_cantidad, tabla_consultas, lista_acciones, tipo_pre_combox):
    # Esta función realiza la consulta y actualiza la interfaz gráfica
    for item in tabla_consultas.get_children():
        tabla_consultas.delete(item)

    cantidad_deseada = int(entry_cantidad.get())
    modelo_seleccionado = tipo_pre_combox.get()

    se_puede_armar, piezas_faltantes = verificar_posibilidad_construccion_motor(cantidad_deseada, modelo_seleccionado)

    if se_puede_armar:
        mensaje = f"Se pueden armar {cantidad_deseada} Motores {modelo_seleccionado}."
        lista_acciones.insert(0, mensaje)
    else:
        mensaje = f"No se pueden armar {cantidad_deseada} Motores {modelo_seleccionado}. Piezas faltantes en la tabla:"
        lista_acciones.insert(0, mensaje)
        for pieza, cantidad_faltante in piezas_faltantes.items():
            # Agregar las filas al treeview
            tabla_consultas.insert("", tk.END, values=(pieza, cantidad_faltante), tags=("blue",))




#-------------------------------Funciones pre armado------------------------------------------------


def stock_de_prearmado(modelo):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'pre_armado'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return -1
    finally:
        conn.close()

    # Obtener la base según el modelo
    if modelo == "inoxidable 330":
        tipo_de_modelo = base_pre_inox_armada330
    elif modelo == "inoxidable 300":
        tipo_de_modelo = base_pre_inox_armada300
    elif modelo == "inoxidable 250":
        tipo_de_modelo = base_pre_inox_armada250
    elif modelo == "pintada 330":
        tipo_de_modelo = base_pre_pintada_armada330
    elif modelo == "pintada 300":
        tipo_de_modelo = base_pre_pintada_armada300

    cantidad_minima = float('inf')
    for pieza, cantidad_necesaria in tipo_de_modelo.items():
        for dato in datos:
            if dato[0] == pieza:
                cantidad_disponible = dato[1]
                cantidad_posible = cantidad_disponible // cantidad_necesaria
                cantidad_minima = min(cantidad_minima, cantidad_posible)

    return cantidad_minima

def actualizar_muestra_prearmado(modelo, label_muestra):
    total_piezas = stock_de_prearmado(modelo)
    label_muestra.config(text=f"{total_piezas}")

def obtener_cantidad_piezas_prearmado():
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'pre_armado'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return {}
    finally:
        conn.close()

    cantidades_disponibles = {}
    for pieza, cantidad in datos:
        cantidades_disponibles[pieza] = cantidad

    return cantidades_disponibles

def verificar_posibilidad_construccion(cantidad_deseada, modelo_seleccionado):
    # Obtener la base según el modelo
    bases_prearmadas = {
        "inoxidable 330": base_pre_inox_armada330,
        "inoxidable 300": base_pre_inox_armada300,
        "inoxidable 250": base_pre_inox_armada250,
        "pintada 330": base_pre_pintada_armada330,
        "pintada 300": base_pre_pintada_armada300,
    }

    tipo_de_modelo = bases_prearmadas.get(modelo_seleccionado)

    if tipo_de_modelo is None:
        print(f"Modelo '{modelo_seleccionado}' no reconocido.")
        return False, {}

    # Obtener las cantidades de piezas disponibles desde la base de datos
    cantidades_disponibles = obtener_cantidad_piezas_prearmado()

    # Verificar si es posible armar la cantidad deseada
    cantidad_minima = float('inf')
    piezas_faltantes = {}

    for pieza, cantidad_necesaria in tipo_de_modelo.items():
        cantidad_disponible = cantidades_disponibles.get(pieza, 0)

        # Calcular la cantidad máxima que se puede armar sin exceder las cantidades disponibles
        cantidad_maxima_posible = cantidad_disponible // cantidad_necesaria

        cantidad_minima = min(cantidad_minima, cantidad_maxima_posible)

        # Calcular la cantidad faltante y actualizar el diccionario piezas_faltantes
        cantidad_faltante = max(0, cantidad_deseada * cantidad_necesaria - cantidad_disponible)
        if cantidad_faltante > 0:
            piezas_faltantes[pieza] = cantidad_faltante

    # Verificar si la cantidad deseada es alcanzable
    if cantidad_minima >= cantidad_deseada:
        return True, piezas_faltantes
    else:
        return False, piezas_faltantes

def consultar_piezas_sector(entry_cantidad, tabla_consultas, lista_acciones, tipo_pre_combox):
    # Esta función realiza la consulta y actualiza la interfaz gráfica
    for item in tabla_consultas.get_children():
        tabla_consultas.delete(item)

    cantidad_deseada = int(entry_cantidad.get())
    modelo_seleccionado = tipo_pre_combox.get()

    se_puede_armar, piezas_faltantes = verificar_posibilidad_construccion(cantidad_deseada, modelo_seleccionado)

    if se_puede_armar:
        mensaje = f"Se pueden armar {cantidad_deseada} {modelo_seleccionado}."
        lista_acciones.insert(0, mensaje)
    else:
        mensaje = f"No se pueden armar {cantidad_deseada} {modelo_seleccionado}. Piezas faltantes en la tabla:"
        lista_acciones.insert(0, mensaje)
        for pieza, cantidad_faltante in piezas_faltantes.items():
            # Agregar las filas al treeview
            tabla_consultas.insert("", tk.END, values=(pieza, cantidad_faltante), tags=("blue",))



#=============================Funciiones de afiladores==============================

def contar_afiladores_disponibles():
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'afilador'"
        )
        datos = cursor.fetchall()
    except sqlite3.Error as e:
        # Manejo de errores, puedes adaptarlo según tus necesidades
        print(f"Error al obtener datos de la base de datos: {e}")
        return -1  # Indicador de error
    finally:
        conn.close()

    # Verificar la cantidad mínima de piezas necesarias para un afilador
    piezas_necesarias = {
        "capuchon_afilador": 2,
        "carcaza_afilador": 1,
        "eje_corto": 1,
        "eje_largo": 1,
        "ruleman608": 2,
        "palanca_afilador": 1,
        "resorte_palanca": 1,
        "resorte_empuje": 2
    }

    # Calcular la cantidad máxima de afiladores que se pueden armar
    cantidad_minima = float('inf')
    for pieza, cantidad_necesaria in piezas_necesarias.items():
        for dato in datos:
            if dato[0] == pieza:
                cantidad_disponible = dato[1]
                cantidad_posible = cantidad_disponible // cantidad_necesaria
                cantidad_minima = min(cantidad_minima, cantidad_posible)

    return cantidad_minima

def actualizar_muestra(label_muestra):
    total_afialdores = contar_afiladores_disponibles()
    label_muestra.config(text=f"En fabrica se pueden armar {total_afialdores} Afiladores")


def preguntar_por_afiladores(cantidad_deseada, piezas_disponibles):
    piezas_necesarias = {
        "capuchon_afilador": 2,
        "carcaza_afilador": 1,
        "eje_corto": 1,
        "eje_largo": 1,
        "ruleman608": 2,
        "palanca_afilador": 1,
        "resorte_palanca": 1,
        "resorte_empuje": 2
    }

    piezas_faltantes = {}

    for pieza, cantidad_necesaria in piezas_necesarias.items():
        cantidad_disponible = piezas_disponibles.get(pieza, 0)
        if cantidad_disponible < cantidad_deseada * cantidad_necesaria:
            cantidad_faltante = cantidad_deseada * cantidad_necesaria - cantidad_disponible
            piezas_faltantes[pieza] = cantidad_faltante

    cantidad_posible = min(piezas_disponibles.get(pieza, 0) // cantidad_necesaria for pieza, cantidad_necesaria in piezas_necesarias.items())

    return cantidad_posible, piezas_faltantes


def consultar_afiladores(entry_cantidad, tabla_consultas, lista_acciones):
    for item in tabla_consultas.get_children():
        tabla_consultas.delete(item)

    cantidad_deseada = int(entry_cantidad.get())

    # Conectar a la base de datos
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    # Obtener la cantidad de piezas disponibles desde la base de datos
    cursor.execute("SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'afilador'")  # Actualiza el nombre de la tabla aquí
    piezas_disponibles = dict(cursor.fetchall())

    # Cerrar la conexión a la base de datos
    conn.close()

    cantidad_posible, piezas_faltantes = preguntar_por_afiladores(cantidad_deseada, piezas_disponibles)

    if cantidad_posible >= cantidad_deseada:
        mensaje = f"Se pueden armar {cantidad_deseada} afiladores."
        lista_acciones.insert(0, mensaje)
    else:
        mensaje = f"No se pueden armar {cantidad_deseada} afiladores. Piezas faltantes en la tabla "
        lista_acciones.insert(0, mensaje)
        for pieza, cantidad_faltante in piezas_faltantes.items():
            tabla_consultas.insert("", tk.END, values=(pieza, cantidad_faltante, "Modelo", "Tipo"), tags=("blue",))


#def preguntar_por_afiladores(cantidad_deseada):
#    try:
#        conn = sqlite3.connect("basedatospiezas.db")
#        cursor = conn.cursor()
#        cursor.execute(
#            "SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'afilador'"
#        )
#        datos = cursor.fetchall()
#    except sqlite3.Error as e:
#        # Manejo de errores, puedes adaptarlo según tus necesidades
#        print(f"Error al obtener datos de la base de datos: {e}")
#        return -1  # Indicador de error
#    finally:
#        conn.close()
#
#    # Verificar la cantidad mínima de piezas necesarias para un afilador
#    piezas_necesarias = {
#        "capuchon_afilador": 2,
#        "carcaza_afilador": 1,
#        "eje_corto": 1,
#        "eje_largo": 1,
#        "ruleman608": 2,
#       "palanca_afilador": 1,
#      "resorte_palanca": 1,
#      "resorte_empuje": 2
#    }
#
#    # Calcular la cantidad máxima de afiladores que se pueden armar
#    cantidad_minima = float('inf')
#    piezas_faltantes = {}
#
#    for pieza, cantidad_necesaria in piezas_necesarias.items():
#        for dato in datos:
#            if dato[0] == pieza:
#                cantidad_disponible = dato[1]
#                cantidad_posible = cantidad_disponible // cantidad_necesaria
#                cantidad_minima = min(cantidad_minima, cantidad_posible)
#
#                # Verificar si la cantidad deseada es alcanzable
#                if cantidad_minima < cantidad_deseada:
#                    cantidad_faltante = cantidad_deseada - cantidad_minima
#                    piezas_faltantes[pieza] = cantidad_faltante
#
#    return cantidad_minima, piezas_faltantes
#
# Ejemplo de uso
#cantidad_deseada = int(input("Ingrese la cantidad deseada de afiladores: "))
#cantidad_posible, piezas_faltantes = preguntar_por_afiladores(cantidad_deseada)
#
#if cantidad_posible >= cantidad_deseada:
#    print(f"Se pueden armar {cantidad_deseada} afiladores.")
#else:
#    print(f"No se pueden armar {cantidad_deseada} afiladores.")
#    print("Piezas faltantes:")
#    for pieza, cantidad_faltante in piezas_faltantes.items():
#        print(f"{pieza}: {cantidad_faltante}")
        


#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ suma total de mquinas @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###@#@#@##
#lo que me va a dar de comer 
def verificar_disponibilidad_pedido(pedido):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        # Consulta SQL para obtener las cantidades disponibles de las piezas
        cursor.execute("""
            SELECT piezas, cantidad
            FROM piezas_finales_defenitivas
            WHERE sector = 'armado_final'
        """)

        datos_piezas = dict(cursor.fetchall())

    except sqlite3.Error as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return False, {}

    finally:
        conn.close()

    piezas_faltantes = {}
    for modelo, cantidad in pedido.items():
        # Obtener la base de piezas según el modelo
        base_piezas_modelo = obtener_base_piezas_modelo(modelo)

        if base_piezas_modelo is None:
            print(f"Modelo '{modelo}' no reconocido.")
            return False, {}

        # Verificar si hay suficientes piezas disponibles para el pedido
        for pieza, cantidad_necesaria in base_piezas_modelo.items():
            cantidad_disponible = int(datos_piezas.get(pieza, 0))
            cantidad_necesaria = int(cantidad_necesaria) if cantidad_necesaria else 0
            cantidad = int(cantidad) if cantidad else 0
            cantidad_requerida = cantidad_necesaria * cantidad
            if cantidad_disponible < cantidad_requerida:
                cantidad_faltante = cantidad_requerida - cantidad_disponible
                piezas_faltantes[(modelo, pieza)] = cantidad_faltante

    if not piezas_faltantes:
        return True, {}
    else:
        return False, piezas_faltantes

def obtener_base_piezas_modelo(modelo):
    # Define la relación entre modelos y sus piezas correspondientes
    bases_prearmadas = {
        "inoxidable 330": i330,
        "inoxidable 300": i300,
        "inoxidable 250": i250,
        "pintada 330": p330,
        "pintada 300": p300,
    }

    return bases_prearmadas.get(modelo)


def on_averiguar_click(entry_i330, entry_i300, entry_i250, entry_p330, entry_p300, tree, listbox):
    for item in tree.get_children():
        tree.delete(item)
        
    # Función que se ejecuta al hacer clic en el botón "Averiguar"
    pedido_maquinas = {
        "inoxidable 330": entry_i330.get(),
        "inoxidable 300": entry_i300.get(),
        "inoxidable 250": entry_i250.get(),
        "pintada 330": entry_p330.get(),
        "pintada 300": entry_p300.get(),
    }

    se_puede_armar, piezas_faltantes = verificar_disponibilidad_pedido(pedido_maquinas)
    
    if se_puede_armar:
        listbox.insert(0, "El pedido se puede armar.")
    else:
        listbox.insert(0,"No hay suficientes piezas para armar el pedido. Piezas faltantes:")
        for (modelo, pieza), cantidad_faltante in piezas_faltantes.items():
            tree.insert('', 'end', values=(pieza, cantidad_faltante, modelo))


#)))))))))))))))))))))))))))))))))))) fin de mes )))))))))))))))))))))))))))))))))))))))))))))))))))))))


def actualizar_cantidad_a_cero(label, meses_opcional, listbox):
    try:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        # Obtener el total de la cantidad antes de la actualización
        cursor.execute("SELECT SUM(cantidad) FROM producto_final")
        total_anterior = cursor.fetchone()[0]

        # Actualizar el texto del label
        nuevo_texto = f"En {meses_opcional.get()} Se armo: {total_anterior} maquinas"
        label.config(text=nuevo_texto)
        listbox.insert(0, "Base de Datos Actualiza... ")

        # Guardar el texto en un archivo de texto
        with open("registro_maquinas.txt", "a") as archivo:
            archivo.write(nuevo_texto + "\n")

        # Actualizar todas las filas de la tabla producto_final estableciendo la cantidad a cero
        cursor.execute("UPDATE producto_final SET cantidad = 0")

        # Confirmar los cambios
        conn.commit()
        print("Cantidad actualizada a cero correctamente.")

    except sqlite3.Error as e:
        print(f"Error al actualizar la cantidad a cero: {e}")

    finally:
        conn.close()
        
def abrir_archivo_registro():
    try:
        # Abrir el archivo de registro con el programa predeterminado
        subprocess.run(["notepad.exe", "registro_maquinas.txt"])
    except Exception as e:
        print(f"Error al abrir el archivo de registro: {e}")
        
       
        
#-------------------------------------------------------------------------


def agujeriado(pieza, cantidad_entry, tabla, info_listbox):   
    cantidad = cantidad_entry.get()  # Obtener el valor del Entry como una cadena de texto

    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        # Validar que 'cantidad' sea un número entero positivo
        if not cantidad.isdigit() or int(cantidad) <= 0:
            info_listbox.insert(0, "Ingrese una cantidad válida (número entero positivo).")
            return

        cantidad = int(cantidad)

        # Mostrar un cuadro de diálogo de confirmación
        confirmar = messagebox.askyesno("Confirmar acción", f"¿Estás seguro de agujerear {cantidad} {pieza}?")

        if confirmar:
            if pieza == "cuadrado_regulador_final":
                # Obtener la cantidad actual en la tabla 'carros'
                cursor.execute("SELECT cantidad FROM piezas_del_fundicion WHERE piezas = 'cuadrado_regulador'")
                cantidad_actual = cursor.fetchone()[0]
            
                # Verificar si la cantidad actual es mayor que 0
                if cantidad_actual > 0:
                    # Verificar si la cantidad actual es mayor o igual a la cantidad a restar
                    if cantidad_actual >= cantidad:
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_del_fundicion SET cantidad = cantidad - ? WHERE piezas = 'cuadrado_regulador'", (cantidad,))
                        
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'cuadrado_regulador_final'", (cantidad,))
                        info_listbox.insert(0, f"Se agujerearon {cantidad} {pieza} ")
                    else:
                        info_listbox.insert(0, f"No suficientes {pieza} en stock")
                else:
                    info_listbox.insert(0, f"No hay {pieza} en stock")       
                    
            elif pieza == "carros_final":
                # Obtener la cantidad actual en la tabla 'carros'
                cursor.execute("SELECT cantidad FROM piezas_finales_defenitivas WHERE piezas = 'carros'")
                cantidad_actual = cursor.fetchone()[0]

                # Verificar si la cantidad actual es mayor que 0
                if cantidad_actual > 0:
                    # Verificar si la cantidad actual es mayor o igual a la cantidad a restar
                    if cantidad_actual >= cantidad:
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad - ? WHERE piezas = 'carros'", (cantidad,))

                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'carros_final'", (cantidad,))
                        info_listbox.insert(0, f"Se agujerearon {cantidad} {pieza} ")
                    else:
                        info_listbox.insert(0, f"No suficientes {pieza} en stock")
                else:
                    info_listbox.insert(0, f"No hay {pieza} en stock")

            elif pieza == "tornillo_teletubi_eco_fin":
                # Obtener la cantidad actual en la tabla 'carros'
                cursor.execute("SELECT cantidad FROM piezas_del_fundicion WHERE piezas = 'tornillo_teletubi_eco'")
                cantidad_actual = cursor.fetchone()[0]

                # Verificar si la cantidad actual es mayor que 0
                if cantidad_actual > 0:
                    # Verificar si la cantidad actual es mayor o igual a la cantidad a restar
                    if cantidad_actual >= cantidad:
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_del_fundicion SET cantidad = cantidad - ? WHERE piezas = 'tornillo_teletubi_eco'", (cantidad,))

                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'tornillo_teletubi_eco_fin'", (cantidad,))
                        info_listbox.insert(0, f"Se agujerearon {cantidad} {pieza} ")
                    else:
                        info_listbox.insert(0, f"No suficientes {pieza} en stock")
                else:
                    info_listbox.insert(0, f"No hay {pieza} en stock")

                    

            elif pieza == "carros_250_final":
                # Obtener la cantidad actual en la tabla 'carros'
                cursor.execute("SELECT cantidad FROM piezas_finales_defenitivas WHERE piezas = 'carros_250'")
                cantidad_actual = cursor.fetchone()[0]
            
                # Verificar si la cantidad actual es mayor que 0
                if cantidad_actual > 0:
                    # Verificar si la cantidad actual es mayor o igual a la cantidad a restar
                    if cantidad_actual >= cantidad:
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad - ? WHERE piezas = 'carros_250'", (cantidad,))
                        
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'carros_250_final'", (cantidad,))
                        info_listbox.insert(0, f"Se agujerearon {cantidad} {pieza} ")
                    else:
                        info_listbox.insert(0, f"No suficientes {pieza} en stock")
                else:
                    info_listbox.insert(0, f"No hay {pieza} en stock")    

  
            elif pieza == "movimientos_final":
                # Obtener la cantidad actual en la tabla 'carros'
                cursor.execute("SELECT cantidad FROM piezas_finales_defenitivas WHERE piezas = 'movimientos'")
                cantidad_actual = cursor.fetchone()[0]
            
                # Verificar si la cantidad actual es mayor que 0
                if cantidad_actual > 0:
                    # Verificar si la cantidad actual es mayor o igual a la cantidad a restar
                    if cantidad_actual >= cantidad:
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad - ? WHERE piezas = 'movimientos'", (cantidad,))
                        
                        # Actualizar la cantidad en la tabla 'Piezas_final_defenitivas'
                        cursor.execute("UPDATE piezas_finales_defenitivas SET cantidad = cantidad + ? WHERE piezas = 'movimientos_final'", (cantidad,))
                        info_listbox.insert(0, f"Se agujerearon {cantidad} {pieza} ")
                    else:
                        info_listbox.insert(0, f"No suficientes {pieza} en stock")
                else:
                    info_listbox.insert(0, f"No hay {pieza} en stock")
            conn.commit()
            cantidad_entry.delete(0, "end")


    except sqlite3.Error as e:
        # Manejo de errores y rollback en caso de error
        info_listbox.insert(0, f"Error en la base de datos: {e}")
        conn.rollback()

    finally:
        conn.close()
        
def mostrar_pieza_sin_augeriar(tree1, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE piezas IN ('carros', 'movimientos', 'carros_250') UNION  SELECT piezas, cantidad FROM piezas_del_fundicion WHERE piezas IN ( 'cuadrado_regulador', 'tornillo_teletubi_eco') ")
 
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)

    subtitulo_text = "Stock Sin Augeriar"
    info.config(text=subtitulo_text)
    
def mostrar_pieza_augeriada(tree1, info):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE piezas IN ('carros_final', 'movimientos_final', 'carros_250_final', 'cuadrado_regulador_final', 'tornillo_teletubi_eco_fin')")
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)

    subtitulo_text = "Stock Augeriado"
    info.config(text=subtitulo_text)


#-------------------------------------------------


def enviar_piezas_a_roman(
    pieza, cantidad, tabla_carmelo, tabla_stock_pulidas, arbol, lista_acciones, info
):
    pieza_seleccionada = pieza.get()
    cantidad_ingresada = cantidad.get()

    if not cantidad_ingresada.isdigit() or int(cantidad_ingresada) < 0:
        lista_acciones.insert(0, "Ingrese una Cantidad Válida")
        return

    # Mostrar una ventana de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea enviar {cantidad_ingresada} piezas de {pieza_seleccionada} a Roman?")

    if confirmacion:
        conn = None
        cursor = None

        try:
            conn = sqlite3.connect("basedatospiezas.db")
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT cantidad FROM {tabla_carmelo} WHERE piezas = ?",
                (pieza_seleccionada,),
            )
            resultado = cursor.fetchone()
            cantidad_existente = resultado[0] if resultado else 0

            if int(cantidad_ingresada) > cantidad_existente:
                lista_acciones.insert(
                    0, "No hay suficientes piezas en la fábrica"
                )
                return

            # Iniciar una transacción
            conn.execute("BEGIN")

            # Actualizar la tabla de Carmelo reduciendo la cantidad
            nueva_cantidad_carmelo = cantidad_existente - int(cantidad_ingresada)
            cursor.execute(
                f"UPDATE {tabla_carmelo} SET cantidad = ? WHERE piezas = ?",
                (nueva_cantidad_carmelo, pieza_seleccionada),
            )

            # Actualizar la tabla de Stock Pulidas aumentando la cantidad
            cursor.execute(
                f"SELECT cantidad FROM {tabla_stock_pulidas} WHERE piezas = ?",
                (pieza_seleccionada,),
            )
            resultado_stock_pulidas = cursor.fetchone()
            cantidad_stock_pulidas = (
                resultado_stock_pulidas[0] if resultado_stock_pulidas else 0
            )

            nueva_cantidad_stock_pulidas = cantidad_stock_pulidas + \
                int(cantidad_ingresada)
            cursor.execute(
                f"UPDATE {tabla_stock_pulidas} SET cantidad = ? WHERE piezas = ?",
                (nueva_cantidad_stock_pulidas, pieza_seleccionada),
            )

            # Confirmar la transacción
            conn.commit()

        except sqlite3.Error as e:
            # Revertir la transacción en caso de error
            if conn:
                conn.rollback()
            lista_acciones.insert(0, f"Error en la base de datos: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        lista_acciones.insert(
            0,
            f"{cantidad_ingresada} pieza de {pieza_seleccionada} se ha enviado a Roman.",
        )
    cantidad.delete(0, 'end')

def mecanizado_chapa(piezas, cantidad, lista_acciones):
    pieza = piezas.get()
    cantidad = cantidad.get()

    if not cantidad.isdigit():
        lista_acciones.insert(0, "Ingrese una cantidad válida (número entero positivo).")
        return

    cantidad = int(cantidad)

    if cantidad <= 0:
        lista_acciones.insert(0, "La cantidad debe ser un número entero positivo.")
        return

    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()

    try:
        # Definir un diccionario para mapear piezas a las correspondientes en bruto
        piezas_enbruto = {
            "vela_final_330": "vela_cortada_330",
            "vela_final_300": "vela_cortada_300",
            "vela_final_250": "vela_cortada_250",
            "planchada_final_330" : "planchada_cortada_330",
            "planchada_final_300" : "planchada_cortada_300",
            "planchada_final_250" : "planchada_cortada_250"
        }

        if pieza in piezas_enbruto:
            pieza_enbruto = piezas_enbruto[pieza]

            # Obtener la cantidad actual de piezas en bruto
            cursor.execute(
                f"SELECT cantidad FROM piezas_del_fundicion WHERE piezas = ?",
                (pieza_enbruto,),
            )
            cantidad_actual_enbruto = cursor.fetchone()

            if cantidad_actual_enbruto is not None:
                cantidad_actual_enbruto = cantidad_actual_enbruto[0]

                # Verificar si hay suficientes piezas en bruto disponibles
                if cantidad_actual_enbruto >= cantidad:
                    # Mostrar mensaje de confirmación
                    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea mecanizar {cantidad} {pieza_enbruto}?")
                    if not confirmacion:
                        lista_acciones.insert(0, "Se canceló la operación de mecanizado.")
                        return

                    # Actualizar la cantidad de cajas en bruto
                    nueva_cantidad_enbruto = max(
                        0, cantidad_actual_enbruto - cantidad)
                    cursor.execute(
                        f"UPDATE piezas_del_fundicion SET cantidad = ? WHERE piezas = ?",
                        (nueva_cantidad_enbruto, pieza_enbruto),
                    )

                    # Actualizar la cantidad de cajas tornadas
                    cursor.execute(
                        f"UPDATE piezas_del_fundicion SET cantidad = cantidad + ? WHERE piezas = ?",
                        (cantidad, pieza),
                    )

                    lista_acciones.insert(
                        0, f"Se han mecanizado {cantidad} {pieza_enbruto}.")
                    lista_acciones.insert(0, f"Se agregaron {cantidad} {pieza}")
                else:
                    lista_acciones.insert(
                        0, f"No hay suficientes piezas de {pieza_enbruto} en bruto disponibles.")
            else:
                lista_acciones.insert(
                    0, f"No se encontró la pieza en bruto correspondiente para {pieza}.")
        else:
            lista_acciones.insert(
                0, f"No se encontró la correspondencia en bruto para {pieza}.")

        conn.commit()
        

    except sqlite3.Error as e:
        # Manejo de errores y rollback en caso de error
        lista_acciones.insert(0, f"Error en la base de datos: {e}")
        conn.rollback()

    finally:
        cantidad.delete(0, 'end')
        conn.close()


def mostrar_calcomania(tree1, subtitulo):
    conn = sqlite3.connect("basedatospiezas.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT piezas, cantidad FROM piezas_finales_defenitivas WHERE sector = 'contro_calidad'")
    datos = cursor.fetchall()
    conn.close()
    for item in tree1.get_children():
        tree1.delete(item)
    for dato in datos:
        tree1.insert("", "end", values=dato)

    subtitulo_text = "Stock Calcomania"
    subtitulo.config(text=subtitulo_text)
    


            
#Acrualizar Piezas (agregar)
def actualizar_pieza_calco(lista_predefinida, entrada_cantidad, res, table, funcion, tree, info):
    actualizar_pieza = lista_predefinida.get()
    entrada_actualizar = entrada_cantidad.get()
    

    if entrada_actualizar.strip().isdigit():
        entrada_actualizar = int(entrada_actualizar)

        if entrada_actualizar < 0:
            res.config(text="La Cantidad NO puede ser Negativa")
        else:
            # Mostrar una ventana de confirmación
            confirmacion = messagebox.askyesno("Confirmar", f"¿Desea Agregar la cantidad de {entrada_actualizar} {actualizar_pieza} ?")

            if confirmacion:
                conn = sqlite3.connect("basedatospiezas.db")
                cursor = conn.cursor()
                cursor.execute(
                    f"SELECT cantidad FROM {table} WHERE piezas=?", (actualizar_pieza,)
                )
                cantidad_actual = cursor.fetchone()

                if cantidad_actual is not None:
                    cantidad_actual = cantidad_actual[0]
                    nueva_cantidad = cantidad_actual + entrada_actualizar
                    cursor.execute(
                        f"UPDATE {table} SET cantidad=? WHERE piezas=?", (nueva_cantidad, actualizar_pieza)
                    )
                    conn.commit()
                    conn.close()
                    mostrar_datos(tree, table, info)  # Llama a la función para mostrar los datos actualizados
                    res.insert(
                        0,
                        f"Carga exitosa: Usted cargó {entrada_actualizar} {actualizar_pieza}:",
                    )
                else:
                    res.insert(
                        0, f"La Pieza {actualizar_pieza} no se puede modificar"
                    )
    else:
        res.insert(0, "La cantidad ingresada no es un número válido")
        
    entrada_cantidad.delete(0, 'end')
        
        
#eliminar_piez(combox, cantida list tabla , funcion , arbol)
def eliminar_pieza(
    lista_predefinida_eliminar, entrada_cantidad_eliminar, res, table, funcion, tree, info
):
    pieza_eliminar = lista_predefinida_eliminar.get()
    cantidad_eliminar = entrada_cantidad_eliminar.get()

    try:
        cantidad_eliminar = int(cantidad_eliminar)
        if cantidad_eliminar < 0:
            raise ValueError("La cantidad no puede ser negativa.")
    except :
        res.insert(0, f"Error Ingrese un numero")
        return

    # Mostrar una ventana de confirmación
    confirmacion = messagebox.askyesno("Confirmar", f"¿Desea eliminar {cantidad_eliminar} unidades de {pieza_eliminar}?")

    if confirmacion:
        conn = sqlite3.connect("basedatospiezas.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                f"SELECT cantidad FROM {table} WHERE piezas=?", (pieza_eliminar,)
            )
            cantidad_actual = cursor.fetchone()

            if cantidad_actual is not None:
                cantidad_actual = cantidad_actual[0]
                if cantidad_eliminar <= cantidad_actual:
                    nueva_cantidad = cantidad_actual - cantidad_eliminar
                    if nueva_cantidad >= 0:
                        cursor.execute(
                            f"UPDATE {table} SET cantidad=? WHERE piezas=?",
                            (nueva_cantidad, pieza_eliminar),
                        )
                        res.insert(
                            0,
                            f" Descarga exitosa: se eliminaron {cantidad_eliminar} unidades de {pieza_eliminar}.",
                        )
                    else:
                        res.insert(0, f"No se puede eliminar la cantidad especificada de {pieza_eliminar}.")
                else:
                    res.insert(0, f"No hay suficientes unidades de {pieza_eliminar} en el stock.")
            else:
                res.insert(0, f"La pieza {pieza_eliminar} no se puede encontrar en la tabla {table}.")
        except sqlite3.Error as e:
            res.insert(0, f"Error en la base de datos: {e}")
        finally:
            conn.commit()
            conn.close()
            
        entrada_cantidad_eliminar.delete(0, 'end')
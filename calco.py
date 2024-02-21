import sqlite3


calco330Inox = {
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligo": 1,
    "fadeco_330_4estrella": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1
}

calco330Pintada = {
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligo": 1,
    "fadeco_330_3estrella": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1
}

calco300Inox = {
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligo": 1,
    "fadeco_300_4estrella": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1
}

calco300Pintada = {
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligo": 1,
    "fadeco_300_3estrella": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1
}

calco250Inox = {
    "garantia": 1,
    "manual_instruc": 1,
    "etiqueta_peligo": 1,
    "fadeco_250_2estrella": 1,
    "F_circulo": 1,
    "F_cuadrado": 1,
    "circulo_argentina": 1,
    "etiqueta_cable": 1
}



base_chapa_eco = {
    "chapa_principal_eco",
    "laterar_front_eco",
    "lateral_atras_330",
    "portaeje",
    "varilla "
}

bases_dict = {
    "Inox Eco": {
        "chapa_principal_eco": "chapa_principal_330_eco",
        "lateral_front_eco": "lateral_front_330",
        "lateral_atras": "lateral_atras_330",
        "planchuela": "planchuela_330",
        "varilla": "varilla_330",
        "portaeje": "portaeje",
    }
}
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


caja_eco = {
    "polea_grande": 1,
    "polea_chica": 1,
    "tornillo": 2,
    "tecla": 1,
    "capacitores": 1,
    "conector_hembra": 1,
    "cable_corto": 1,
    "motor_eco": 1,
    "carcaza_pintada": 1,
    "tapa_plastico": 1,
    "correa": 1,
    "capuchon_moror": 1
}

base_eco = {
    "base_eco": 1,
    "espiral": 1,
    "tornillo_guia": 1,
    "eje_rectificado": 1,
    "guia_U": 1,
    "resorte_movimiento": 1,
    "varilla_carro_330": 1,
    "carros_final": 1,
    "resorte_carro": 2,
    "patas": 4
}

maquina_final_eco = {
    "teletubi_eco": 1,#
    "cuchilla_330": 1,#
    "cubrecuchilla": 1,
    "vela_final_330": 1,#
    "cuadrado_reguladore_final": 1,#
    "velero": 1,#
    "cabezal_inox":1,#
    "brazo_330":1,#
    "perilla_brazo":1,#
    "planchada_final_330":1,#
    "resorte_brazo":1,#
    "perilla_cubrecuilla":2,#
    "varilla_brazo_330":1,#
    "base_afilador_250":1,#
    "afilador_final":1,
    "piedras":1,
    "cable_220w":1,
    "tubo_manija": 1,#
    "pipas":1,#
    "pinche_lateral": 1,
    "pinche_frontal":1,
    
    
    
    
    }
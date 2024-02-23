import tkinter as tk
from tkinter import ttk
from funciones import sort_column_alphanumeric, mostrar_piezas_armados, mostrar_pieza, mostrar_piezas_modelo, ensamblar_motor_terminado,mostrar_datos, eliminar_pieza, stock_prearmado, actualizar_inventario, mostrar_pieza_afilador, mostrar_afilador_final, motores_terminados,armado_final_afiladores_y_agregar_cantidad,  mostrar_por_pieza, bases_terminados, mostrar_piezas_finales, mostrar_piezas_i330, armado_de_maquinas, mostrar_maquinas_teminadas, agregar_a_lista_tarea,sort_column, sort_column_alpha, mostrar_motores

tipo = ["330", "300", "250"]

piezas_delete_armadocaja = [
    "caja_torneado_330",
    "caja_torneado_300",
    "caja_torneado_250",
    "manchon",
    "manchon_250",
    "eje",
    "eje_250",
    "ruleman_6005",
    "ruleman_6205",
    "corona_330",
    "corona_250",
    "corona_300",
    "motores_220w",
    "seguer",
    "sinfin",
    "motores250_220w",
    "oring",
    "ruleman6000",
    "ruleman_6004",
    "ruleman_6204",
    "caja_soldada_eco",
    "polea_grande",
    "polea_chica",
    "tornillo_teletubi_eco_fin",
    "capacitores_eco",
    "conector_hembra",
    "cable_corto_eco",
    "motores_eco",
    "tapa_plastico_eco",
    "correa_eco",
    "capuchon_motor_eco",
    "buje_eje_eco",
    "rectangulo_plastico_eco"
]

piezas_delete_armadocaja.sort()

piezas_delete_prearmado = [
    "aro_numerador",
    "base_pintada_300",
    "base_pintada_330",
    "cable_220w",
    "cajamotor_final_250",
    "cajamotor_final_300",
    "cajamotor_final_330",
    "capacitores",
    "capacitores_250",
    "carros",
    "carros_250",
    "carros_final",
    "carro_250_final",
    "movimiento_final"
    "eje_rectificado",
    "espiral",
    "guia_U",
    "inox_250",
    "inox_300",
    "inox_330",
    "movimientos",
    "patas",
    "perilla_numerador",
    "resorte_carro",
    "resorte_movimiento",
    "rueditas",
    "tapita_perilla",
    "teclas",
    "tornillo_guia",
    "varilla_carro_250",
    "varilla_carro_300",
    "varilla_carro_330",
    "bandeja_330",
    "bandeja_300"
    "inox_eco"
]
piezas_delete_prearmado.sort()

tipos_de_maquinas = ["inox_330", "inox_300", "inox_250", "pintada_330", "pintada_300", "eco"]

motores_250 = (
    "caja_torneado_250",
    "corona_250",
    "eje_250",
    "manchon_250",
    "motores250_220w",
    "oring",
    "ruleman_6004",
    "ruleman_6204",
    "ruleman6000",
    "seguer",
    "sinfin"
)

motores_300 = (
    "caja_torneado_300",
    "corona_300",
    "eje",
    "manchon",
    "motores_220w",
    "oring",
    "ruleman_6005",
    "ruleman_6205",
    "ruleman6000",
    "seguer",
    "sinfin"
)

motores_330 = (
    "caja_torneado_330",
    "corona_330",
    "eje",
    "manchon",
    "motores_220w",
    "oring",
    "ruleman_6005",
    "ruleman_6205",
    "ruleman6000",
    "seguer",
    "sinfin"
)

motores_eco = {
    "cable_corto_eco",
    "caja_soldada_eco",
    "capacitores_eco",
    "capuchon_motor_eco",
    "conector_hembra",
    "correa_eco",
    "buje_eje_eco",
    "motores_eco",
    "polea_chica",
    "polea_grande",
    "rectangulo_plastico_eco",
    "tapa_plastico_eco",
    "teclas",
    "tornillo_teletubi_eco_fin"
}


cantidad_piezas_afiladore = {
    "capuchon_afilador": 2,
    "carcaza_afilador": 1,
    "eje_corto": 1,
    "eje_largo": 1,
    "ruleman608": 2,
    "palanca_afilador": 1,
    "resorte_palanca": 1,
    "resorte_empuje": 2
}

i330pieza = {
    "brazo_330",
    "cubrecuchilla_330",
    "velero",
    "perilla_brazo",
    "cabezal_inox",
    "teletubi_330",
    "cuchilla_330",
    "cuadrado_regulador_final",
    "vela_final_330",
    "cubre_motor_rectangulo",
    "cubre_motor_cuadrado",
    "planchada_final_330",
    "varilla_brazo_330",
    "resorte_brazo",
    "tapa_afilador",
    "pipas",
    "tubo_manija",
    "afilador_final",
    "perilla_cubrecuchilla",
    "perilla_afilador",
    "base_afilador_330",
    "base_pre_armada330inox",
    "piedra_afilador",
    "pinche_frontal",
    "pinche_lateral" 
    }
i300pieza = {
    "brazo_300" ,
    "cubre_300" ,
    "velero" ,
    "perilla_brazo" ,
    "cabezal_inox" ,
    "teletu_300" ,
    "cuchilla_300" ,
    "cuadrado_regulador_final" ,
    "vela_final_300" ,
    "cubre_motor_rectangulo" ,
    "cubre_motor_cuadrado" ,
    "planchada_final_300" ,
    "varilla_brazo_300" ,
    "resorte_brazo" ,
    "tapa_afilador" ,
    "pipas" ,
    "tubo_manija" ,
    "afilador_final" ,
    "perilla_cubrecuchilla" ,
    "perilla_afilador" ,
    "base_afilador_300" ,
    "base_pre_armada300inox" ,
    "piedra_afilador",
    "pinche_frontal",
    "pinche_lateral" 
}
i250pieza = {
    "brazo_250" ,
    "cubrecuchilla_250" ,
    "velero" ,
    "perilla_brazo" ,
    "cabezal_250" ,
    "teletubi_250" ,
    "cuchilla_250" ,
    "cuadrado_regulador_final" ,
    "vela_final_250" ,
    "planchada_final_250" ,
    "varilla_brazo_250" ,
    "resorte_brazo" ,
    "tapa_afilador_250" ,
    "pipas" ,
    "tubo_manija_250" ,
    "afilador_final" ,
    "perilla_cubrecuchilla" ,
    "perilla_afilador" ,
    "base_afilador_250" ,
    "base_pre_armada250inox" ,
    "piedra_afilador" ,
    "capuchon_250",
    "pinche_frontal_250",
    "pinche_lateral_250" 
}
p330pieza = {
    "brazo_330" ,
    "cubrecuchilla_330" ,
    "velero" ,
    "perilla_brazo" ,
    "cabezal_pintada" ,
    "teletubi_330" ,
    "cuchilla_330" ,
    "cuadrado_regulador_final" ,
    "vela_final_330" ,
    "cubre_motor_rectangulo" ,
    "cubre_motor_cuadrado" ,
    "planchada_final_330" ,
    "varilla_brazo_330" ,
    "resorte_brazo" ,
    "tapa_afilador" ,
    "pipas" ,
    "tubo_manija" ,
    "afilador_final" ,
    "perilla_cubrecuchilla" ,
    "perilla_afilador" ,
    "base_afilador_330" ,
    "base_pre_armada330pint" ,
    "piedra_afilador",
    "pinche_frontal",
    "pinche_lateral" 
}
p300pieza = {
    "brazo_300" ,
    "cubre_300" ,
    "velero" ,
    "perilla_brazo" ,
    "cabezal_pintada" ,
    "teletu_300" ,
    "cuchilla_300" ,
    "cuadrado_regulador_final" ,
    "vela_final_300" ,
    "cubre_motor_rectangulo" ,
    "cubre_motor_cuadrado" ,
    "planchada_final_300" ,
    "varilla_brazo_300" ,
    "resorte_brazo" ,
    "tapa_afilador" ,
    "pipas" ,
    "tubo_manija" ,
    "afilador_final" ,
    "perilla_cubrecuchilla" ,
    "perilla_afilador",
    "base_afilador_300" ,
    "base_pre_armada300pint" ,
    "piedra_afilador",
    "pinche_frontal",
    "pinche_lateral" 
}

iEcopiezas = [
    "brazo_330",
    "cubrecuchilla_330",
    "velero",
    "perilla_brazo",
    "cabezal_inox",
    "teletubi_doblado_eco",
    "cuchilla_330",
    "vela_final_330",
    "cuadrado_reguladore_final",
    "planchada_final_330",
    "varilla_brazo_330",
    "resorte_brazo",
    "tapa_afilador_eco",
    "pipas",
    "tubo_manija",
    "afilador_final",
    "perilla_cubrecuilla",
    "perilla_afilador",
    "base_afilador_250",
    "base_pre_armadaECOinox",
    "piedra_afilador",
    "pinche_lateral",
    "pinche_frontal"
]

piezas_armado_final_delete = [
    "afilador_final",
    "base_afilador_250",
    "base_afilador_300",
    "base_afilador_330",
    "base_pre_armada250inox",
    "base_pre_armada300inox",
    "base_pre_armada300pint",
    "base_pre_armada330inox",
    "base_pre_armada330pint",
    "brazo_250",
    "brazo_300",
    "brazo_330",
    "cabezal_inox",
    "cabezal_pintura",
    "cuadrado_regulador",
    "cuadrado_regulador_final",
    "cubre_motor_cuadrado",
    "cubre_motor_rectangulo",
    "cubrecuchilla_250",
    "cubre_300",
    "cubrecuchilla_330",
    "cuchilla_250",
    "cuchilla_300",
    "cuchilla_330",
    "perilla_afilador",
    "perilla_brazo",
    "perilla_cubrecuchilla",
    "piedra_afilador",
    "pipas",
    "planchada_final_250",
    "planchada_final_300",
    "planchada_final_330",
    "resorte_brazo",
    "tapa_afilador",
    "tapa_afilador_250",
    "teletubi_250",
    "teletu_300",
    "teletubi_330",
    "tubo_manija",
    "tubo_manija_250",
    "varilla_brazo_250",
    "varilla_brazo_300",
    "varilla_brazo_330",
    "vela_final_250",
    "vela_final_300",
    "vela_final_330",
    "velero",
    "tapita_perilla"
    "capuchon_250", 
    "pinche_lateral", 
    "pinche_frontal",
    "pinche_frontal_250",
    "pinche_lateral_250", 
    "teletubi_eco_final"
]




def seccion_armado(notebook):
    pestania = ttk.Frame(notebook, style='Color.TFrame')
    pestania.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
    )

    notebook.add(pestania, text="Zona De Armado")
    
    notebook.style = ttk.Style()
    notebook.style.configure('Color.TFrame', background='#192965', radius=20, borderwidth=10)  # Puedes ajustar el color
    notebook.style.configure('WhiteOnRed.TLabel', background='#192965', foreground='white')  # Puedes ajustar el color
    notebook.style.configure('WhiteOnRed.TEntry', fieldbackground='black', foreground='black')  # Puedes ajustar el color
    notebook.style.configure('WhiteOnRed.TCombobox', fieldbackground='#192965', foreground='white')  # Puedes ajustar el color
    notebook.style.configure("Estilo9.TButton", font=("Verdana", 8, "bold"), padding=(2, 2))
    notebook.style.configure("Separador1.TSeparator", background="yellow")
    notebook.style.configure("Separador2.TSeparator", background="blue")
    notebook.style.configure("Estilo2.TButton", background="green", padding=2)
    notebook.style.configure("Estilo5.TButton", font=("Courier", 8, "italic"))
    notebook.style.configure("Estilo4.TButton", background="yellow", padding=7)    
    notebook.style.configure("Gradient.TButton", padding=1, relief="flat", font=("Arial", 8, "bold"))


    
    ttk.Label(pestania, text="Zona De Armado", style="WhiteOnRed.TLabel", font=("Arial", 20, "bold")).grid(
        row=1, column=0, columnspan=5)
    caja1 = ttk.Frame(pestania, style='Color.TFrame')
    caja1.grid(row=2, column=0, sticky="n")

    res = ttk.Label(caja1, text="Mostrar Datos", style="WhiteOnRed.TLabel")
    res.grid(row=1, column=0)

    arbol = ttk.Treeview(caja1, columns=("Pieza", "Cantidad", "Modelo"))
    arbol.heading("Pieza", text="Pieza" , command=lambda: sort_column_alpha(arbol, "Pieza", False))
    arbol.heading("Cantidad", text="Cant", command=lambda: sort_column(arbol, "Cantidad", False))
    arbol.heading("Modelo", text="Modelo", command=lambda: sort_column_alphanumeric(arbol, "Modelo", False))
    arbol.column("#0", width=0, stretch=tk.NO)
    arbol.column("Pieza", anchor=tk.W, width=190)
    arbol.column("Cantidad", anchor=tk.W, width=40)
    arbol.column("Modelo", anchor=tk.W, width=50)
    arbol.config(height=15)
    arbol.grid(row=2, column=0, pady=1, padx=1)

    ttk.Label(caja1, text="Acciones",style="Color.TLabel").grid(row=3, column=0)

    result = tk.Listbox(caja1, width=30)
    result.grid(row=4, column=0, padx=3, pady=3)
    
    scrollbar = ttk.Scrollbar(caja1, orient="horizontal", command=result.xview)
    scrollbar.grid(row=5, column=0, sticky="ew")

    result.configure(xscrollcommand=scrollbar.set)

 #-------------------------------------------------------------------------
 
    caja2 = ttk.Frame(pestania, style='Color.TFrame')
    caja2.grid(row=2, column=1, padx=5, sticky="n")

    ttk.Label(caja2, text="Armado de Cajas", style="WhiteOnRed.TLabel", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=3)

    motores = ttk.Frame(caja2, style='Color.TFrame')
    motores.grid(row=1, column=0, columnspan=3)

    ttk.Label(motores, text="Cantidad De Motores", style="WhiteOnRed.TLabel").grid(row=1, column=0)
    tk.Button( 
        motores,
        text="Motores all",
        font=('Arial', 10, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda: mostrar_motores(arbol, res)).grid(row=1, column=1, padx=1)

    ttk.Separator(caja2, orient="horizontal", style="Separador2.TSeparator").grid(
        row=2, column=0, sticky="ew", columnspan=2, padx=3, pady=3
    )

    ttk.Label(caja2, text="Mostrar Piezas", style="WhiteOnRed.TLabel").grid(row=3, column=0)
    tk.Button(
        caja2, 
        text="Ver", 
        font=('Arial', 10, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda:mostrar_piezas_armados(arbol, "armado_de_caja", res)).grid(row=3, column=1)

    ttk.Separator(caja2, orient="horizontal", style="Separador2.TSeparator").grid(
        row=4, column=0, sticky="ew", columnspan=2, pady=3, padx=3)
    

    botonera_cajas = ttk.Frame(caja2, style='Color.TFrame')
    botonera_cajas.grid(row=5, column=0, columnspan=2)

    ttk.Label(botonera_cajas, text="Piezas por modelo", style="WhiteOnRed.TLabel").grid(row=0, column=0, columnspan=3)
    ttk.Button(botonera_cajas ,text="330", command=lambda: mostrar_piezas_modelo(arbol, motores_330, res, "330")).grid(row=1, column=0, pady=5, padx=5)
    ttk.Button(botonera_cajas, text="300", command=lambda: mostrar_piezas_modelo(arbol, motores_300, res, "300")).grid(row=1, column=1, pady=5, padx=5)
    ttk.Button(botonera_cajas, text="250", command=lambda: mostrar_piezas_modelo(arbol, motores_250, res, "250")).grid(row=2, column=0, pady=5, padx=5)
    ttk.Button(botonera_cajas, text="eco", command=lambda: mostrar_piezas_modelo(arbol, motores_eco, res, "eco")).grid(row=2, column=1, pady=5, padx=5)

    ttk.Separator(botonera_cajas, orient="horizontal", style="Separador2.TSeparator").grid(
        row=3, column=0, sticky="ew", columnspan=3, pady=5, padx=5)

    ttk.Label(caja2, text="Motores Armados", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=7, column=0, columnspan=2)

    checkbox = ttk.Frame(caja2, style='Color.TFrame')
    checkbox.grid(row=8, column=0, columnspan=2)

    modelo = tk.IntVar()
    modelo.set(1)
    ttk.Label(checkbox, text="Modelo", style="WhiteOnRed.TLabel").grid(row=0, column=0, columnspan=3)
    tk.Radiobutton(checkbox, text="330", variable=modelo,selectcolor='#2f3542',
                   value=1, background='#192965', foreground='#fff',borderwidth=3, relief="raised").grid(row=1, column=0, padx=2, pady=2)
    tk.Radiobutton(checkbox, text="300", variable=modelo,selectcolor='#2f3542',
                   value=2, background='#192965', foreground='#fff',borderwidth=3, relief="raised").grid(row=1, column=1, padx=2, pady=2)
    tk.Radiobutton(checkbox, text="250", variable=modelo,selectcolor='#2f3542',
                   value=3, background='#192965', foreground='#fff',borderwidth=3, relief="raised").grid(row=1, column=2, padx=2, pady=2)
    tk.Radiobutton(checkbox, text="Eco", variable=modelo, selectcolor='#2f3542',
                   value=4, background='#192965', foreground='#fff',borderwidth=3, relief="raised").grid(row=1, column=3, padx=2, pady=2)


    ttk.Label(caja2, text="Cantidad", style="WhiteOnRed.TLabel").grid(row=9, column=0,columnspan=2)
    cantidad_motores = tk.Entry(caja2, width=10)
    cantidad_motores.grid(row=10, column=0, columnspan=2, pady=3, padx=3)
    
    def enviar():
        # Obtener el valor actual del objeto IntVar (modelo)
        modelo_seleccionado = modelo.get()
        # Luego, usar el valor para acceder al diccionario y llamar a la función
        ensamblar_motor_terminado(modelo_seleccionado, cantidad_motores, result)

    # Crear el botón y asociarlo a la función 'enviar'
    tk.Button(
        caja2,
        text="Motores Terminado",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=enviar).grid(row=11, column=0, columnspan=2, padx=5, pady=5)

    ttk.Separator(caja2, orient="horizontal", style="Separador2.TSeparator").grid(
        row=12, column=0, sticky="ew", columnspan=2, pady=3, padx=3)


    ttk.Label(caja2, text="Consulta", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=13, column=0, columnspan=2)
    ttk.Label(caja2, text="Motores Terminados ", style="WhiteOnRed.TLabel").grid(row=14, column=0, columnspan=2)
    tk.Button(
        caja2,
        text="Terminados", 
        font=('Arial', 10, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda: motores_terminados(arbol, res)).grid(row=15, column=0, columnspan=2 )
    
    ttk.Separator(caja2, orient="horizontal").grid(
        row=16, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja2, text="Piezas Rotas o Defectuosa", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=17, column=0, columnspan=2)

    ttk.Label(caja2, text="Seleccionar Piezas", style="WhiteOnRed.TLabel").grid(row=18, column=0)
    pieza_del = ttk.Combobox(caja2, values=piezas_delete_armadocaja, state="readonly", width=16)
    pieza_del.grid(row=18, column=1)

    ttk.Label(caja2, text="Cantidad", style="WhiteOnRed.TLabel").grid(row=19, column=0)
    cantidad_delete = ttk.Entry(caja2, width=10)
    cantidad_delete.grid(row=19, column=1, padx=4, pady=4)

    #eliminar_piez(combox, cantida list tabla , funcion , arbol)

    tk.Button(
        caja2,
        text="Delete",
        background="red",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: eliminar_pieza(pieza_del, cantidad_delete, result, "piezas_finales_defenitivas", mostrar_datos, arbol ,info="")).grid(row=20, column=1, padx=2, pady=2)


    ttk.Separator(caja2, orient="horizontal", style="Separador2.TSeparator").grid(
        row=21, column=0, sticky="ew", columnspan=2, pady=3, padx=3)
    

    caja3 = ttk.Frame(pestania, style='Color.TFrame')
    caja3.grid(row=2, column=2, sticky="n")

     #=================================PRe Armado ==================+++++=====
    
    caja4 = ttk.Frame(caja3, style='Color.TFrame')
    caja4.grid(row=9, column=0,padx=15, columnspan=2)

    ttk.Label(caja4, text="Pre Armado", style="WhiteOnRed.TLabel", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(caja4, text="Total De Piezas", style="WhiteOnRed.TLabel").grid(row=1, column=0)
    tk.Button(
        caja4, 
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        text="Mostrar",
        command=lambda: stock_prearmado(arbol, res)).grid(row=1, column=1)

    ttk.Separator(caja4, orient="horizontal", style="Separador2.TSeparator").grid(
        row=2, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja4, text="Piezas De Modelos", style="WhiteOnRed.TLabel").grid(row=3, column=0, columnspan=2)

    botonera_prearmado = ttk.Frame(caja4, style='Color.TFrame')
    botonera_prearmado.grid(row=4, column=0, columnspan=2)
    ttk.Button(botonera_prearmado, text="330", command=lambda: mostrar_por_pieza(arbol,"330",res)).grid(row=0, column=0, pady=5,padx=5)
    ttk.Button(botonera_prearmado, text="300", command=lambda: mostrar_por_pieza(arbol,"300", res)).grid(row=0, column=1, pady=5,padx=5)
    ttk.Button(botonera_prearmado, text="250", command=lambda: mostrar_por_pieza(arbol,"250", res)).grid(row=1, column=0, pady=5,padx=5)
    ttk.Button(botonera_prearmado, text="Eco", command=lambda: mostrar_por_pieza(arbol,"eco", res)).grid(row=1, column=1, pady=5,padx=5)

    ttk.Separator(caja4, orient="horizontal", style="Separador2.TSeparator").grid(
        row=5, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja4, text="Maquinas pre-armadas", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=6, column=0, columnspan=2)

    ttk.Label(caja4, text="Modelo de Maquina", style="WhiteOnRed.TLabel").grid(row=7, column=0)
    tipo_prearmada = ttk.Combobox(caja4, values=tipos_de_maquinas, state="readonly", width=16)
    tipo_prearmada.grid(row=7, column=1)

    ttk.Label(caja4, text="Cantidad", style="WhiteOnRed.TLabel").grid(row=8, column=0)
    cantidad_prearmada = tk.Entry(caja4, width=10)
    cantidad_prearmada.grid(row=8, column=1, pady=4, padx=4)

    tk.Button(
        caja4, 
        text="Pre Armado", 
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: actualizar_inventario(result, cantidad_prearmada.get(), tipo_prearmada.get()),
    ).grid(row=9, column=1)

    ttk.Separator(caja4, orient="horizontal", style="Separador2.TSeparator").grid(
        row=10, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja4, text="Consulta", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=11, column=0, columnspan=2)
    ttk.Label(caja4, text="Motores Terminados ", style="WhiteOnRed.TLabel").grid(row=12, column=0, columnspan=2)
    tk.Button(
        caja4,
        text="Terminados", 
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda: bases_terminados(arbol, res)).grid(row=13, column=0, columnspan=2)
    
    ttk.Separator(caja4, orient="horizontal", style="Separador2.TSeparator").grid(
        row=14, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja4, text="Piezas Rotas o Defectuosa", style="WhiteOnRed.TLabel").grid(row=15, column=0)

    ttk.Label(caja4, text="Seleccionar Piezas", style="WhiteOnRed.TLabel").grid(row=16, column=0)
    prearmadolo_delete = ttk.Combobox(caja4, values=piezas_delete_prearmado, state="readonly", width=16)
    prearmadolo_delete.grid(row=16, column=1)

    ttk.Label(caja4, text="Cantidad", style="WhiteOnRed.TLabel").grid(row=17, column=0)
    cantidad_prearmado_delete = tk.Entry(caja4, width=10)
    cantidad_prearmado_delete.grid(row=17, column=1, pady=5, padx=5)

    tk.Button(
        caja4,
        text="Delete",
        background="red",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: eliminar_pieza(prearmadolo_delete, cantidad_prearmado_delete, result, "piezas_finales_defenitivas", mostrar_datos, arbol,info="")).grid(row=18, column=1)

    ttk.Separator(caja4, orient="horizontal", style="Separador2.TSeparator").grid(
        row=19, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

 #----------====armado======---------
    caja5 = ttk.Frame(pestania, style='Color.TFrame')
    caja5.grid(row=2, column=4, sticky="n")

    ttk.Label(caja5, text="Armado Final", style="WhiteOnRed.TLabel", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(caja5, text="Piezas Totales", style="WhiteOnRed.TLabel").grid(row=1, column=0)
    tk.Button(
        caja5,
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        text="Mostrar", command=lambda: mostrar_piezas_finales(arbol, res)).grid(row=1, column=1)

    ttk.Separator(caja5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=2, column=0, sticky="ew", columnspan=2, padx=3, pady=3
    )

    ttk.Label(caja5, text="Mostrar Base Pre_armadas", style="WhiteOnRed.TLabel").grid(row=3, column=0)
    tk.Button(
        caja5,
        text="Ver", 
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda: bases_terminados(arbol, res)).grid(row=3, column=1)

    ttk.Separator(caja5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=4, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    botonera_armadofinal = ttk.Frame(caja5, style='Color.TFrame')
    botonera_armadofinal.grid(row=5, column=0 , columnspan=2)

    ttk.Label(botonera_armadofinal, style="WhiteOnRed.TLabel",font=("Arial",12,"bold"), text="Piezas por modelo").grid(row=0, column=0, columnspan=3)
    
    ttk.Button(botonera_armadofinal, text="Inox 330", command=lambda: mostrar_piezas_i330(arbol, res, i330pieza, "Inox 330")).grid(row=1, column=0, pady=5, padx=5)
    ttk.Button(botonera_armadofinal, text="Inox 300", command=lambda: mostrar_piezas_i330(arbol, res, i300pieza, "Inox 300")).grid(row=1, column=1, pady=5, padx=5)
    ttk.Button(botonera_armadofinal, text="Inox 250", command=lambda: mostrar_piezas_i330(arbol, res, i250pieza, "Inox 250")).grid(row=1, column=2, pady=5, padx=5)

    ttk.Button(botonera_armadofinal, text="Pintada 330", command=lambda: mostrar_piezas_i330(arbol, res, p330pieza, "Pint 330")).grid(row=2, column=0, pady=5, padx=5)
    ttk.Button(botonera_armadofinal, text="Pintada 300", command=lambda: mostrar_piezas_i330(arbol, res, p300pieza, "Pint 300")).grid(row=2, column=1, pady=5, padx=5)
    ttk.Button(botonera_armadofinal, text="ECO", command=lambda: mostrar_piezas_i330(arbol, res, iEcopiezas, "Eco ")).grid(row=2, column=2, pady=5, padx=5)

    ttk.Separator(botonera_armadofinal, orient="horizontal", style="Separador2.TSeparator").grid(
        row=3, column=0, sticky="ew", columnspan=4, pady=1, padx=1)

    ttk.Label(caja5, style="WhiteOnRed.TLabel", text="Maquinas Teminadas", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2)

    ttk.Label(caja5, text="Modelo", style="WhiteOnRed.TLabel").grid(row=7, column=0)
    modele_final = ttk.Combobox(caja5, values=tipos_de_maquinas, state="readonly", width=16)
    modele_final.grid(row=7, column=1)

    ttk.Label(caja5, style="WhiteOnRed.TLabel", text="Cantidad").grid(row=8, column=0)
    cantidad_final = tk.Entry(caja5, width=10)
    cantidad_final.grid(row=8, column=1, pady=5, padx=5)

    tk.Button(
        caja5, 
        text="Confirmar",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: armado_de_maquinas(cantidad_final.get() ,modele_final.get(), result)).grid(row=9, column=1)

    ttk.Separator(caja5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=10, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja5, style="WhiteOnRed.TLabel", font=("Arial", 12, "bold"), text="Piezas Rotas o Defectuosa").grid(row=11, column=0, columnspan=2)

    ttk.Label(caja5, style="WhiteOnRed.TLabel", text="Seleccionar Piezas").grid(row=12, column=0)
    armadolo_delete = ttk.Combobox(caja5, values=piezas_armado_final_delete, state="readonly", width=18)
    armadolo_delete.grid(row=12, column=1)

    ttk.Label(caja5, style="WhiteOnRed.TLabel", text="Cantidad").grid(row=13, column=0)
    cantidad_delete_final = tk.Entry(caja5, width=10)
    cantidad_delete_final.grid(row=13, column=1, pady=5, padx=5)

    tk.Button(
        caja5, 
        text="Delete",
        background="red",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: eliminar_pieza(armadolo_delete, cantidad_delete_final, result, "piezas_finales_defenitivas", mostrar_datos, arbol,info="")).grid(row=14, column=1)

    ttk.Separator(caja5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=15, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(caja5, style="WhiteOnRed.TLabel", text="Listado De Maquinas Terminadas", font=("Arial", 12, "bold") ).grid(
        row=16, column=0, columnspan=2)
    tk.Button(
        caja5, 
        text="Mostrar Maquinas",
        bg= "#00d0ff",  # Color de fondo
        fg="white",    # Color del texto
        padx=10,
        pady=5,
        font=('Helvetica', 10, 'bold'),
        command=lambda: mostrar_maquinas_teminadas(arbol, res)).grid(row=17, column=0, columnspan=2)

    ttk.Separator(caja5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=18, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

#-------------------------------------------------------------------------------


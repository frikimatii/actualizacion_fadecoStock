
import tkinter as tk
from tkinter import ttk
from funciones import sort_column, contar_afiladores_disponibles, consultar_afiladores, actualizar_muestra, actualizar_muestra_prearmado, consultar_piezas_sector, actualizar_muestra_motores, consultar_piezas_sector_motor, mostrar_maquinas_disponibles, consultar_maquinas_final, on_averiguar_click,  actualizar_cantidad_a_cero,  abrir_archivo_registro ,sort_column_alpha, guardar_datos_csv

cantidad_piezas_afiladore = {
    "capuchon_afilador": 2,
    "carcaza_afilador": 1,
    "eje_corto": 1,
    "eje_largo": 1,
    "ruleman608": 2,
    "palanca_afilador": 1,
    "resorte_palanca" : 1,
    "resorte_empuje": 2
}

total_afialdores = contar_afiladores_disponibles()

i330 = {
    "brazo_330": 1,
    "cubrecuchilla_330": 1,
    "velero": 1,
    "perilla_brazo": 1,
    "cabezal_inox": 1,
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
    "base_pre_armada330inox": 1,
    "piedra_afilador": 1,
    "tapita_afilador": 1,
    "tapita_perilla" : 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1 
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
    "tapita_afilador": 1,
    "tapita_perilla" : 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1 

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
    "capuchon_250": 1,
    "tapita_perilla" : 1,
    "pinche_frontal_250" : 1,
    "pinche_lateral_250" : 1 

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
    "tapita_afilador": 1,
    "tapita_perilla" : 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1 

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
    "tapita_afilador": 1,
    "tapita_perilla" : 1,
    "pinche_frontal" : 1,
    "pinche_lateral" : 1 

}

texto_con_salto = "Preguntar cuántas máquinas se pueden armar. Seleccione un \n                   tipo de máquinas y la cantidad que desea."
texto_con_salto_motores = "Preguntar cuantos motores se pueden armar \n                         ingrese el tipo y cantidad"
texto_prearmado = "preguntar cuantas bases pre Armadas se pueden armar\n                    ingrese tipo y cantidad"
texto_afiladores = "preguntar cuantos afiladores se pueden armar EN FABRICA\n                           ingrese la cantidad"

tipo_motor = ("330", "300", "250", "eco")
tipo_maquina = ("inoxidable 330", "inoxidable 300", "inoxidable 250", "pintada 330", "pintada 300", "inoxidable eco")

base_pre_inox_armada330 = {
    "inox_330": 1,
    "aro_numerador": 1,
    "espiral": 1,
    "perilla_numerador": 1,
    "tapita_perilla": 1,
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
    "tapita_afilador": 1

}

meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def consultorio(notebook):
    pestana_consultas = ttk.Frame(notebook , style='Pestania.TFrame')
    pestana_consultas.grid(
        row=3,
        column=0)

    notebook.add(pestana_consultas, text="Consultorio")
    
    notebook.style = ttk.Style()
    notebook.style.configure('Color.TFrame', background='#192965', radius=20, borderwidth=10)  # Puedes ajustar el color
    notebook.style.configure('WhiteOnRed.TLabel', background='#192965', foreground='white')  # Puedes ajustar el color
    notebook.style.configure('WhiteOnRed.TEntry', fieldbackground='black', foreground='black')  # Puedes ajustar el color
    notebook.style.configure('WhiteOn.TLabel', background='#192965', foreground='white')  # Puedes ajustar el color


    estilo = ttk.Style()
    estilo.configure('Pestania.TFrame', background='#192965')
    
    style = ttk.Style()
    style.configure("Custom.TLabel", foreground="white", background="#192965", font=("Arial", 10, "bold"))
    #estilo.configure('Color.TFrame', borderwidth=10 ,background='#434ed1', radius=20)

    notebook.configure(style='Pestania.TNotebook')

    box1 = ttk.Frame(pestana_consultas, style='Pestania.TFrame')
    box1.grid(row=0, column=0, sticky="ne")

    titulo = ttk.Label(box1, text="Consultorio ", background="#192965",foreground='white' ,font=("Arial", 20, "bold"))
    titulo.grid(row=0, column=0, columnspan=2)
    
    subtitulo = ttk.Label(box1, text="", background="#192965", foreground="white", font=("Arial", 8, "bold"))
    subtitulo.grid(row=1, column=0, padx=1, pady=1)

    tabla_consultas = ttk.Treeview(box1, columns=("Pieza", "Cantidad", "Modelo"))
    tabla_consultas.heading("Pieza", text="Pieza", command=lambda: sort_column_alpha(tabla_consultas, "Pieza", False) )
    tabla_consultas.heading("Cantidad", text="Cant Faltante",command=lambda: sort_column(tabla_consultas, "Cantidad", False))
    tabla_consultas.heading("Modelo", text="Modelo", command=lambda: sort_column_alpha(tabla_consultas, "Modelo", False))
    tabla_consultas.column("#0", width=0, stretch=tk.NO)
    tabla_consultas.column("Pieza", anchor=tk.W, width=150)
    tabla_consultas.column("Cantidad", anchor=tk.W, width=80)
    tabla_consultas.column("Modelo", anchor=tk.W, width=100)
    tabla_consultas.config(height=14)
    tabla_consultas.grid(row=3, column=0, pady=1, padx=1)
    
    tabla_consultas.tag_configure("red", background="red")
    tabla_consultas.tag_configure("green", background="green")
    
    ttk.Label(box1, text="Acciones",style="Color.TLabel").grid(row=4, column=0)

    lista_acciones = tk.Listbox(box1, width=35)
    lista_acciones.grid(
        row=5,
        column=0,
    )
    scrollbar = ttk.Scrollbar(box1, orient="horizontal", command=lista_acciones.xview)
    scrollbar.grid(row=6, column=0, sticky="ew")

    lista_acciones.configure(xscrollcommand=scrollbar.set)


#________________________________________________________________________________


    box2 = ttk.Frame(pestana_consultas, style='Pestania.TFrame')
    box2.grid(row=0, column=1)
    

    maquinas_terminadas = ttk.Frame(box2, style='Pestania.TFrame')
    maquinas_terminadas.grid(row=0, column=0, sticky="n")
    
    ttk.Label(maquinas_terminadas, text="Consultorio De Maquinas", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(maquinas_terminadas, text=texto_con_salto, style="WhiteOnRed.TLabel", font=("Arial", 8)).grid(row=1, column=0,columnspan=2, padx=2, pady=2)    

    ttk.Label(maquinas_terminadas, text="Tipo De Maquina", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0 ,sticky="se")

    tipo_maquina_combox = ttk.Combobox(maquinas_terminadas, values=tipo_maquina,  state="readonly", width=14)
    tipo_maquina_combox.grid(row=2, column=1, sticky="nw")
    
    ttk.Label(maquinas_terminadas, text="Cantidad", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="se")    
    
    entry_cantidad = ttk.Entry(maquinas_terminadas, width=10)
    entry_cantidad.grid(row=3, column=1, sticky="nw")
    
    tk.Button(
        maquinas_terminadas,
        text="Consultar",
        background="#253a93",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command= lambda : consultar_maquinas_final(entry_cantidad, tabla_consultas, lista_acciones, tipo_maquina_combox)).grid(row=4, column=0 , columnspan=2,padx=1, pady=1)

    ttk.Separator(maquinas_terminadas, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

    ttk.Label(maquinas_terminadas, text="Posibilidad de maquinas terminadas", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=6, column=0 ,columnspan=2)    

    buttons = ttk.Frame(maquinas_terminadas, style='Pestania.TFrame')
    buttons.grid(row=7, column=0, columnspan=3)
    
    tk.Button(
        buttons, 
        text="Inox 330", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: mostrar_maquinas_disponibles("inox 330", inox_330)
        ).grid(row=0, column=0, padx=1, pady=1)
    
    inox_330 = ttk.Label(buttons, text="I330", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    inox_330.grid(row=1, column=0,pady=1 )
    
    tk.Button(
        buttons, 
        text="Inox 300", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: mostrar_maquinas_disponibles("inox 300", inox_300)
        ).grid(row=0, column=1, padx=1, pady=1)

    inox_300 = ttk.Label(buttons, text="I300", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    inox_300.grid(row=1, column=1,pady=1 )
    
    
    tk.Button(
        buttons, 
        text="Inox 250", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: mostrar_maquinas_disponibles("inox 250", inox_250)
        ).grid(row=0, column=2, padx=1, pady=1)
    
    inox_250 = ttk.Label(buttons, text="I250", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    inox_250.grid(row=1, column=2,pady=1)
    
    
    tk.Button(
        buttons, 
        text="Pint 330", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: mostrar_maquinas_disponibles("pint 330", pint_330)
        ).grid(row=2, column=0, padx=1, pady=1)
    
    pint_330 = ttk.Label(buttons, text="P330", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    pint_330.grid(row=3, column=0,pady=1 )
    
    tk.Button(
        buttons, 
        text="Pint 300", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: mostrar_maquinas_disponibles("pint 300", pint_300)
        ).grid(row=2, column=1, padx=1, pady=1)

    pint_300 = ttk.Label(buttons, text="P300", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    pint_300.grid(row=3, column=1,pady=1 )

    tk.Button(
        buttons, 
        text="Inox Eco", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: mostrar_maquinas_disponibles("inox eco", inox_eco)
        ).grid(row=2, column=2, padx=1, pady=1)
    
    inox_eco = ttk.Label(buttons, text="IEco", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    inox_eco.grid(row=3, column=2,pady=1 )
    
    
#__________________________________________________________________________________________________________    

    ttk.Separator(maquinas_terminadas, orient="horizontal").grid(row=8, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
#__________________________________________________________________________________________________________    

    consulta_motores = ttk.Frame(box2, style='Pestania.TFrame')
    consulta_motores.grid(row=1, column=0,sticky="n")
    
    ttk.Label(consulta_motores, text="Consultorio De Motores", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(consulta_motores, text=texto_con_salto_motores, style="WhiteOnRed.TLabel", font=("Arial", 8)).grid(row=1, column=0,columnspan=2)    
    
    ttk.Label(consulta_motores, text="Tipo Motores", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="se")

    tipo_maquina_combox_motor = ttk.Combobox(consulta_motores, values=tipo_motor,  state="readonly", width=10)
    tipo_maquina_combox_motor.grid(row=2, column=1, sticky="nw")
    
    ttk.Label(consulta_motores, text="Cantidad", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=3, column=0,padx=3, pady=3, sticky="se")    
    
    entry_motores_cantidad = ttk.Entry(consulta_motores, width=10)
    entry_motores_cantidad.grid(row=3, column=1, sticky="nw")
    
    tk.Button(
        consulta_motores,
        text="Consultar",
        background="#253a93",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda : consultar_piezas_sector_motor(entry_motores_cantidad, tabla_consultas, lista_acciones, tipo_maquina_combox_motor)).grid(row=4, column=0 , columnspan=2)
    
    ttk.Separator(consulta_motores, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

    ttk.Label(consulta_motores, text="Total De Motores", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2)

    botones = ttk.Frame(consulta_motores, style='Pestania.TFrame')
    botones.grid(row=7, column=0, columnspan=2)
    
    tk.Button(
        botones, 
        text="330", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command=lambda: actualizar_muestra_motores("330", motor330),  # Cambia "330" por el modelo deseado
        ).grid(row=0, column=0, padx=1, pady=1)
    tk.Button(
        botones, 
        text="300", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command=lambda: actualizar_muestra_motores("300", motor300)        
    ).grid(row=0, column=1, padx=1, pady=1)
    tk.Button(
        botones, 
        text="250", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: actualizar_muestra_motores("250", motor250)
        ).grid(row=0, column=2, padx=1, pady=1)

    tk.Button(
        botones, 
        text="250", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command= lambda: actualizar_muestra_motores("eco", motoreco)
        ).grid(row=0, column=3, padx=1, pady=1)
    
    motor330 = ttk.Label(botones, text="330", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    motor330.grid(row=1, column=0,pady=1 )
    motor300 = ttk.Label(botones, text="300", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    motor300.grid(row=1, column=1,pady=1 )
    motor250 = ttk.Label(botones, text="250", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    motor250.grid(row=1, column=2,pady=1 )
    motoreco = ttk.Label(botones, text="Eco", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    motoreco.grid(row=1, column=3,pady=1 )

#__________________________________________________________________________________________________________    

    ttk.Separator(consulta_motores, orient="horizontal").grid(row=8, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
#__________________________________________________________________________________________________________    



    box3 = ttk.Frame(pestana_consultas, style='Pestania.TFrame')
    box3.grid(row=0, column=2)
    
    
    bases_prearmadas = ttk.Frame(box3, style='Pestania.TFrame')
    bases_prearmadas.grid(row=0, column=0, sticky="n")
    
    ttk.Label(bases_prearmadas, text="Consultorio Prearamado", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(bases_prearmadas, text=texto_prearmado, style="WhiteOnRed.TLabel", font=("Arial", 8)).grid(row=1, column=0,columnspan=2)    
    
    ttk.Label(bases_prearmadas, text="Tipo De Base", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="se")

    tipo_pre_combox = ttk.Combobox(bases_prearmadas, values=tipo_maquina,  state="readonly", width=14)
    tipo_pre_combox.grid(row=2, column=1, sticky="nw")
    
    ttk.Label(bases_prearmadas, text="Cantidad", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=3, column=0,sticky="se")    
    
    entry_pre_cantidad = ttk.Entry(bases_prearmadas, width=10)
    entry_pre_cantidad.grid(row=3, column=1, sticky="nw")
    
    tk.Button(
        bases_prearmadas,
        text="Consultar",
        background="#253a93",
        foreground="white",
        padx=4,
        pady=1,
        command=lambda: consultar_piezas_sector(entry_pre_cantidad, tabla_consultas, lista_acciones, tipo_pre_combox),
        font=('Helvetica', 8, "bold")).grid(row=4, column=0 , columnspan=2)

    ttk.Separator(bases_prearmadas, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
        
    ttk.Label(bases_prearmadas, text="Cantidad maquinas armadas ", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=6, column=0,columnspan=2)

    botonera = ttk.Frame(bases_prearmadas, style='Pestania.TFrame')
    botonera.grid(row=7, column=0, columnspan=2)
    
    tk.Button(
        botonera, 
        text="Inox 330", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        relief=tk.GROOVE,  # Tipo de relieve del botón
        command=lambda: actualizar_muestra_prearmado("inoxidable 330", maquina_i330),
        ).grid(row=0, column=0, padx=1, pady=1)
    
    maquina_i330 = ttk.Label(botonera, text="inox 330", style="WhiteOnRed.TLabel", font=("Arial", 9, "bold"))
    maquina_i330.grid(row=1, column=0,padx=1, pady=1)   
    
    tk.Button(
        botonera, 
        text="Inox 300", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        command=lambda: actualizar_muestra_prearmado("inoxidable 300", maquina_i300),
        relief=tk.GROOVE,).grid(row=0, column=1, padx=1, pady=1)
    
    maquina_i300 = ttk.Label(botonera, text="inox 300", style="WhiteOnRed.TLabel", font=("Arial", 9, "bold"))
    maquina_i300.grid(row=1, column=1,padx=1, pady=1) 
    
    tk.Button(
        botonera, 
        text="Inox 250", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        command=lambda: actualizar_muestra_prearmado("inoxidable 250", maquina_i250),
        relief=tk.GROOVE,).grid(row=0, column=2, padx=1, pady=1)
    
    maquina_i250 = ttk.Label(botonera, text="inox 250", style="WhiteOnRed.TLabel", font=("Arial", 9, "bold"))
    maquina_i250.grid(row=1, column=2,padx=1, pady=1)   
    
    tk.Button(
        botonera, 
        text="Pintada 330", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        command=lambda: actualizar_muestra_prearmado("pintada 330", maquina_p330),
        relief=tk.GROOVE,).grid(row=2, column=0, padx=1, pady=1)
    
    maquina_p330 = ttk.Label(botonera, text="Pint 330", style="WhiteOnRed.TLabel", font=("Arial", 9, "bold"))
    maquina_p330.grid(row=3, column=0,padx=1, pady=1)    
    
    tk.Button(
        botonera, 
        text="Pintada 300", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        command=lambda: actualizar_muestra_prearmado("pintada 300", maquina_p300),
        relief=tk.GROOVE,).grid(row=2, column=1, padx=1, pady=1)
    
    maquina_p300 = ttk.Label(botonera, text="Pint 300", style="WhiteOnRed.TLabel", font=("Arial", 9, "bold"))
    maquina_p300.grid(row=3, column=1,padx=1, pady=1)    

    tk.Button(
        botonera, 
        text="Inox Eco", 
        bg="#ff6c00",  # Color de fondo
        fg="white",    # Color del texto
        padx=4,
        pady=1,
        font=('Helvetica', 8, 'bold'),
        command=lambda: actualizar_muestra_prearmado("inoxidable eco", maquina_Ieco),
        relief=tk.GROOVE,).grid(row=2, column=2, padx=1, pady=1)
    
    maquina_Ieco = ttk.Label(botonera, text="Inox eco", style="WhiteOnRed.TLabel", font=("Arial", 9, "bold"))
    maquina_Ieco.grid(row=3, column=2,padx=1, pady=1)   
    
    

#__________________________________________________________________________________________________________    

    ttk.Separator(bases_prearmadas, orient="horizontal").grid(row=8, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
#__________________________________________________________________________________________________________    

    afiladores = ttk.Frame(box3, style='Pestania.TFrame')
    afiladores.grid(row=1, column=0, sticky="n")

    ttk.Label(afiladores, text="Consultorio Afiladores", style="WhiteOnRed.TLabel", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(afiladores, text=texto_afiladores, style="WhiteOnRed.TLabel", font=("Arial", 8)).grid(row=1, column=0,columnspan=2, padx=3, pady=3)

    ttk.Label(afiladores, text="Cantidad", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0,padx=1, pady=1, columnspan=2)

    entry_afilador_cantidad = ttk.Entry(afiladores, width=10 )
    entry_afilador_cantidad.grid(row=3, column=0, columnspan=2, pady=3)

    consultar_button = tk.Button(
        afiladores,
        text="Consultar",
        background="#253a93",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command= lambda : consultar_afiladores(entry_afilador_cantidad, tabla_consultas,  lista_acciones)
    )
    consultar_button.grid(row=4, column=0 , columnspan=2,padx=1, pady=1)
    
    text = ttk.Label(afiladores, text=f"En fabrica se pueden armar {total_afialdores} Afiladores", style="WhiteOnRed.TLabel", font=("Arial", 8, "bold"))
    text.grid(row=5, column=0, columnspan=2)

    consultar_button2 = tk.Button(
        afiladores,
        text="Consultar",
        background="#ff6c00",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command= lambda: actualizar_muestra(text)
    )
    consultar_button2.grid(row=6, column=0 , columnspan=2,padx=1, pady=1)
    
#__________________________________________________________________________________________________________    
    
    ttk.Separator(afiladores, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
#__________________________________________________________________________________________________________    


    box4 = ttk.Frame(pestana_consultas, style='Pestania.TFrame')
    box4.grid(row=0, column=3)
    
    consulta_pedidos = ttk.Frame(box4, style='Pestania.TFrame')
    consulta_pedidos.grid(row=0, column=0)
    
    ttk.Label(consulta_pedidos, text=f"Consulta de pedido", style="WhiteOnRed.TLabel", font=("Arial", 20, "bold")).grid(row=1, column=0, columnspan=2)
    
    ttk.Label(consulta_pedidos, text="Inoxidable 330", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0,padx=1, pady=1, sticky="se")    
    ttk.Label(consulta_pedidos, text="Inoxidable 300", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=3, column=0,padx=1, pady=1, sticky="se")
    ttk.Label(consulta_pedidos, text="Inoxidable 250", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=4, column=0,padx=1, pady=1, sticky="se")
    ttk.Label(consulta_pedidos, text="Pintada 330", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=5, column=0,padx=1, pady=1, sticky="se")
    ttk.Label(consulta_pedidos, text="Pintada 300", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=6, column=0,padx=1, pady=1, sticky="se")
    ttk.Label(consulta_pedidos, text="Inoxidable Eco", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=7, column=0,padx=1, pady=1, sticky="se")

    
    entry_i330 = ttk.Entry(consulta_pedidos, width=7)
    entry_i330.grid(row=2, column=1, sticky="nw")
    
    entry_i300 = ttk.Entry(consulta_pedidos, width=7)
    entry_i300.grid(row=3, column=1, sticky="nw")
    
    entry_i250 = ttk.Entry(consulta_pedidos, width=7)
    entry_i250.grid(row=4, column=1, sticky="nw")
    
    entry_p330 = ttk.Entry(consulta_pedidos, width=7)
    entry_p330.grid(row=5, column=1, sticky="nw")
    
    entry_p300 = ttk.Entry(consulta_pedidos, width=7)
    entry_p300.grid(row=6, column=1, sticky="nw")

    entry_ieco = ttk.Entry(consulta_pedidos, width=7)
    entry_ieco.grid(row=7, column=1, sticky="nw")
    
    resultado_final= tk.Button(
        consulta_pedidos,
        text="Averiguar",
        background="#530075",
        foreground="white",
        padx=7,
        pady=2,
        font=('Helvetica', 9, "bold"),
        command=lambda: on_averiguar_click(entry_i330, entry_i300, entry_i250, entry_p330, entry_p300, entry_ieco, tabla_consultas, lista_acciones) 

    )
    resultado_final.grid(row=8, column=0 , columnspan=2,padx=2, pady=2)

    ttk.Button(consulta_pedidos, text="Abrir Tabla", command= lambda: guardar_datos_csv(tabla_consultas, "datos_treeview.csv")).grid(row=9, column=0, columnspan=2, padx=4, pady=4)

    
    ttk.Separator(consulta_pedidos, orient="horizontal").grid(row=10, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

    finde_mes = ttk.Frame(box4, style='Pestania.TFrame')
    finde_mes.grid(row=1, column=0)
    
    ttk.Label(finde_mes, text="Cierre Del Mes", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=0, column=0,padx=2, pady=2, columnspan=2)

    meses_opcional = ttk.Combobox(finde_mes, values=meses, state="readonly", width=12)
    meses_opcional.grid(row=2, column=0, sticky="se")
        
    
    cierre_mes = tk.Button(
        finde_mes,
        text="Terminar El Mes",
        background="#530075",
        foreground="white",
        padx=5,
        pady=2,
        font=('Helvetica', 8, "bold"),
        command=lambda : actualizar_cantidad_a_cero(total, meses_opcional, lista_acciones)
    )
    cierre_mes.grid(row=2, column=1 , columnspan=2,padx=3, pady=3, sticky="nw")

    total = ttk.Label(finde_mes, text="", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold"))
    total.grid(row=3, column=0,padx=3, pady=3, columnspan=2)

    
    mostrar_registro = tk.Button(
        finde_mes,
        text="Mostrar Registro",
        background="#530075",
        foreground="white",
        padx=20,
        pady=7,
        font=('Helvetica', 8, "bold"),
        command=lambda: abrir_archivo_registro()
    )
    mostrar_registro.grid(row=4, column=0, columnspan=2)


#TESTEO1
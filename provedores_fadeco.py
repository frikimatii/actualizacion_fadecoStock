import tkinter as tk
from tkinter import ttk
from funciones import (
    enviar_piezas_a_pulido,
    mostrar_datos,
    mover_piezas_a_stock_pulidas,
    mostrar_datos_especifico,
    agregar_a_lista_tarea,
    mostrar,
    envios_de_bruto_a_pulido,
    sort_column_numeric,
    envios_de_bruto_a_niquelar,
    envios_de_niquelado_a_fabrica,
    envios_pulido_a_fabrica,
    envios_pulido_a_fabrica_cabezal,
    envios_de_bruto_cabezal,
    mostrar_pieza_afilador,
    mostrar_afilador_final,
    armado_final_afiladores_y_agregar_cantidad,
    mostrar_pieza_afilador_roman,
    enviar_piezas_a_roman,
    sort_column_alpha
)

modelo_piezas = ["base_pintada_330", "base_pintada_300"]  
modelo_piezas.sort()
niquelado = [
    "eje_rectificado",
    "varilla_brazo_330",
    "varilla_brazo_300",
    "varilla_brazo_250",
    "tubo_manija",
    "tubo_manija_250",
    "palanca_afilador"
]
niquelado.sort()

piezas_carmelo = [
    "brazo_330",
    "brazo_300",
    "brazo_250",
    "cubrecuchilla_330",
    "cubre_300",
    "cubrecuchilla_250",
    "teletubi_330",
    "teletu_300",
    "teletubi_250",
    "vela_final_330",
    "vela_final_300",
    "vela_final_250",
    "planchada_final_330",
    "planchada_final_300",
    "planchada_final_250",
    "tapa_afilador",
    "velero",
    "aro_numerador",
    "tapa_afilador_250",
    "caja_torneado_330",
    "caja_torneado_300",
    "caja_torneado_250",
    "inox_330",
    "inox_300",
    "inox_250"
]
piezas_carmelo.sort()
piezas_maxi = [
    "brazo_330",
    "brazo_300",
    "brazo_250",
    "cubrecuchilla_330",
    "cubre_300",
    "cubrecuchilla_250",
    "teletubi_330",
    "teletu_300",
    "teletubi_250",
    "vela_final_330",
    "vela_final_300",
    "vela_final_250",
    "planchada_final_330",
    "planchada_final_300",
    "planchada_final_250",
    "tapa_afilador",
    "velero",
    "aro_numerador",
    "tapa_afilador_250",
    "caja_torneado_330",
    "caja_torneado_300",
    "caja_torneado_250",
    "inox_330",
    "inox_300",
    "inox_250"
]
piezas_maxi.sort()
pieza_buen_hombre =  [
    "brazo_330",
    "brazo_300",
    "brazo_250",
    "cubrecuchilla_330",
    "cubre_300",
    "cubrecuchilla_250",
    "teletubi_330",
    "teletu_300",
    "teletubi_250",
    "vela_final_330",
    "vela_final_300",
    "vela_final_250",
    "planchada_final_330",
    "planchada_final_300",
    "planchada_final_250",
    "tapa_afilador",
    "velero",
    "aro_numerador",
    "tapa_afilador_250",
    "caja_torneado_330",
    "caja_torneado_300",
    "caja_torneado_250",
    "inox_330",
    "inox_300",
    "inox_250"
]
pieza_buen_hombre.sort()

cabezal = ["cabezal_pintura"]

piezas_afilador = ["capuchon_afilador","carcaza_afilador","eje_corto","eje_largo","ruleman608","palanca_afilador","resorte_palanca","resorte_empuje"]
piezas_afilador.sort()


def ventana_provedores(notebook):
    pestania = ttk.Frame(notebook, style='Color.TFrame')
    pestania.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
    )

    notebook.add(pestania, text="Provedores")

    notebook.style = ttk.Style()
    notebook.style.configure('Color.TFrame', background='#192965', radius=20, borderwidth=10) 
    notebook.style.configure('WhiteOnRed.TLabel', background='#192965', foreground='#c1c1c1')  
    notebook.style.configure('WhiteOnRed.TEntry', fieldbackground='black', foreground='black')  
    notebook.style.configure('WhiteOnRed.TCombobox', fieldbackground='#192965', foreground='white')  
    notebook.style.configure("Estilo9.TButton", font=("Verdana", 7, "bold"), padding=(2, 2))
    notebook.style.configure("Separador1.TSeparator", background="yellow")
    notebook.style.configure("Separador2.TSeparator", background="blue")
    notebook.style.configure("Estilo2.TButton", background="black")
    notebook.style.configure("Estilo9.TButton", font=("Arial", 12, "bold"), backgrund='white')
    notebook.style.configure("Estilo4.TButton", background="yellow", padding=7)

 


    caja1 = ttk.Frame(pestania, style='Color.TFrame')
    caja1.grid(row=0, column=0, sticky="ne", padx=2)
    
    ttk.Label(caja1, text="Provedores", style="WhiteOnRed.TLabel", font=("Verdana", 22, "bold")).grid(row=0, column=0)
    info = ttk.Label(caja1, text=" Tabla de datos", style="WhiteOnRed.TLabel")
    info.grid(row=1, column=0)
    arbol = ttk.Treeview(caja1, columns=("Pieza", "Cantidad"))
    arbol.heading(
        "Pieza", text="Pieza", command=lambda: sort_column_alpha(arbol, "Pieza", False))
    arbol.heading(
        "Cantidad",
        text="Cant",
        command=lambda: sort_column_numeric(arbol, "Cantidad", False),
    )
    arbol.column("#0", width=0, stretch=tk.NO)
    arbol.column("Pieza", anchor=tk.W, width=190)
    arbol.column("Cantidad", anchor=tk.W, width=40)
    arbol.config(height=14)
    arbol.grid(row=2, column=0, pady=1, padx=1)

    ttk.Label(caja1, text="Acciones",style="Color.TLabel").grid(row=3, column=0)

    result = tk.Listbox(caja1, width=35)
    result.grid(row=4, column=0, padx=3, pady=3)
    
    scrollbar = ttk.Scrollbar(caja1, orient="horizontal", command=result.xview)
    scrollbar.grid(row=5, column=0, sticky="ew")

    result.configure(xscrollcommand=scrollbar.set)

#----------------------Carmelo-------------------------------------
    
    box2 = ttk.Frame(pestania, style='Color.TFrame')
    box2.grid(row=0, column=1, sticky="n",pady=3, padx=4)
    
    ttk.Label(box2, text="Carmelo", style="WhiteOnRed.TLabel",font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2)
    
    ttk.Label(box2, text="Envios A Carmelo", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w")
    ttk.Label(box2, text="Pieza", style="WhiteOnRed.TLabel",).grid(row=2, column=0, sticky="ew")
    ttk.Label(box2, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=2, column=1, sticky="ew")

    pieza_predeterminadas = ttk.Combobox(box2, values=piezas_carmelo, state="readonly", width=17)
    pieza_predeterminadas.grid(row=3, column=0, sticky="w")

    cantidad_agregar_carmelo = ttk.Entry(box2, width=10 ,style='WhiteOnRed.TEntry')
    cantidad_agregar_carmelo.grid(row=3, column=1, sticky="w")

    tk.Button(
        box2,
        text="Enviar Piezas",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: enviar_piezas_a_pulido(
            pieza_predeterminadas,
            cantidad_agregar_carmelo,
            "carmelo_pulido",
            arbol,
            result,info
        ),
    ).grid(row=4, column=1,pady=2, sticky="w")
    
    ttk.Separator(box2, orient="horizontal", style="Separador2.TSeparator").grid(
    row=5, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

    
    ttk.Label(box2, text="Piezas Resibidas", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=6, column=0, sticky="w")
    ttk.Label(box2, text="Pieza", style="WhiteOnRed.TLabel",).grid(row=7, column=0, sticky="w")
    ttk.Label(box2, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=7, column=1, sticky="ew")

    pieza_predeterminadas1 = ttk.Combobox(box2, values=piezas_carmelo, state="readonly" , width=17)
    pieza_predeterminadas1.grid(row=8, column=0, sticky="w")

    cantidad_piezas_terminadas_carmelo = ttk.Entry(box2, width=10,style='WhiteOnRed.TEntry')
    cantidad_piezas_terminadas_carmelo.grid(row=8, column=1, sticky="w")

    tk.Button(
        box2,
        text="Piezas Terminadas",
        background="blue",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: mover_piezas_a_stock_pulidas(
            pieza_predeterminadas1,
            cantidad_piezas_terminadas_carmelo,
            "carmelo_pulido",
            "piezas_finales_defenitivas",
            arbol,
            result,info
        ),
    ).grid(row=9, column=1, pady=2, sticky="w")
    
    ttk.Separator(box2, orient="horizontal", style="Separador2.TSeparator").grid(
    row=10, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
    
    ttk.Label(box2, text="Consultas De Stock Carmelo", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=11, column=0, columnspan=2)

    ttk.Button(
        box2,
        text="Stock Total",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos(arbol, "carmelo_pulido", info),
    ).grid(row=12, column=0, columnspan=3)

    botonera1 = ttk.Frame(box2, style='Color.TFrame')
    botonera1.grid(row=13, column=0, columnspan=2)

    ttk.Button(
        botonera1,
        text="Stock 330",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos_especifico("carmelo_pulido", "330", arbol, info),
    ).grid(row=0, column=0, padx=2, pady=2)
    ttk.Button(
        botonera1,
        text="Stock 300",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos_especifico("carmelo_pulido", "300", arbol, info),
    ).grid(row=0, column=1, padx=2, pady=2)
    ttk.Button(
        botonera1,
        text="Stock 250",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos_especifico("carmelo_pulido", "250", arbol, info),
    ).grid(row=0, column=2, padx=2, pady=2)

    ttk.Separator(box2, orient="horizontal", style="Separador1.TSeparator").grid(
    row=14, column=0, columnspan=2, sticky="ew", padx=3, pady=3)
    
#-----------------------Maxi-------------------------------------------

    box3 = ttk.Frame(pestania, style='Color.TFrame')
    box3.grid(row=0, column=2, sticky="n",padx=4, pady=3)

    ttk.Label(box3, text="Maxi", style="WhiteOnRed.TLabel",font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(box3, text="Envios A Maxi", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=1, column=0,sticky="w")
    ttk.Label(box3, text="Pieza", style="WhiteOnRed.TLabel",).grid(row=2, column=0, sticky="ew")
    ttk.Label(box3, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=2, column=1, sticky="ew")

    pieza_predeterminadas2 = ttk.Combobox(box3, values=piezas_maxi, state="readonly", width=17)
    pieza_predeterminadas2.grid(row=3, column=0,sticky="w")

    cantidad_agregar_maxi = ttk.Entry(box3, width=10,style='WhiteOnRed.TEntry')
    cantidad_agregar_maxi.grid(row=3, column=1, sticky="w")

    tk.Button(
        box3,
        text="Enviar Piezas",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: enviar_piezas_a_pulido(
            pieza_predeterminadas2, cantidad_agregar_maxi, "maxi_pulido", arbol, result,info
        ),
    ).grid(row=4, column=1,pady=2, sticky="w")

    ttk.Separator(box3, orient="horizontal", style="Separador2.TSeparator").grid(
        row=5, column=0, columnspan=2, sticky="ew", padx=3, pady=3
    )
    
    ttk.Label(box3, text="Piezas Resibidas", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=6, column=0, sticky="w")
    ttk.Label(box3, text="Pieza", style="WhiteOnRed.TLabel",).grid(row=7, column=0, sticky="w")
    ttk.Label(box3, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=7, column=1, sticky="ew")

    pieza_predeterminadas4 = ttk.Combobox(box3, values=piezas_maxi,state="readonly")
    pieza_predeterminadas4.grid(row=8, column=0, sticky="w")

    cantidad_piezas_terminadas_maxi = ttk.Entry(box3, width=10,style='WhiteOnRed.TEntry')
    cantidad_piezas_terminadas_maxi.grid(row=8, column=1, sticky="w")

    tk.Button(
        box3,
        text="Piezas Terminadas",
        background="blue",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: mover_piezas_a_stock_pulidas(
            pieza_predeterminadas4,
            cantidad_piezas_terminadas_maxi,
            "maxi_pulido",
            "piezas_finales_defenitivas",
            arbol,
            result,info
        ),
    ).grid(row=9, column=1,pady=2,sticky="w")
    ttk.Separator(box3, orient="horizontal", style="Separador2.TSeparator").grid(
    row=10, column=0, columnspan=2, sticky="ew", padx=3, pady=3)


    ttk.Label(box3, text="Consultas De Stock Maxi", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=11, column=0, columnspan=2)

    ttk.Button(
        box3, text="Stock Total", style = "Estilo9.TButton", command=lambda: mostrar_datos(arbol, "maxi_pulido", info)
    ).grid(row=12, column=0, columnspan=2)

    botonera2 = ttk.Frame(box3, style='Color.TFrame')
    botonera2.grid(row=13, column=0, columnspan=3)

    ttk.Button(
        botonera2,
        text="Stock 330",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos_especifico("maxi_pulido", "330", arbol, info),
    ).grid(row=0, column=0, padx=2, pady=2)
    ttk.Button(
        botonera2,
        text="Stock 300",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos_especifico("maxi_pulido", "300", arbol, info),
    ).grid(row=0, column=1, padx=2, pady=2)
    ttk.Button(
        botonera2,
        text="Stock 250",
        style = "Estilo9.TButton",
        command=lambda: mostrar_datos_especifico("maxi_pulido", "250", arbol, info),
    ).grid(row=0, column=2, padx=2, pady=2)
    
    ttk.Separator(box3, orient="horizontal", style="Separador1.TSeparator").grid(row=14, column=0, columnspan=2, sticky="ew", padx=3, pady=3)

    
    box1 = ttk.Frame(pestania, style='Color.TFrame')
    box1.grid(row=0, column=3, sticky="n",pady=3, padx=4, columnspan=2)
    
    # 0000----------------------------Afiladores ROMAN ------------------------------------#
    
    
    ttk.Label(box1, text="Armado De Afilador", style="WhiteOnRed.TLabel", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2)

    ttk.Label(box1, text="Mostrar Piezas", style="WhiteOnRed.TLabel").grid(row=1, column=0, columnspan=2)
    tk.Button(
        box1, 
        text="en Fabrica", 
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda: mostrar_pieza_afilador(arbol, info)).grid(row=2, column=1)
    tk.Button(
        box1, 
        text="en Roman", 
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1,
        command=lambda: mostrar_pieza_afilador_roman(arbol, info)).grid(row=2, column=0)
    

    ttk.Separator(box1, orient="horizontal", style="Separador2.TSeparator").grid(
        row=3, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    ttk.Label(box1, text="Afiladores Terminadas", style="WhiteOnRed.TLabel").grid(row=4, column=0)
    tk.Button(
        box1, 
        text="Mostrar", 
        font=('Arial', 8, "italic"),
        background= "gray", 
        foreground= "white",
        padx=4,
        pady=1, 
        command=lambda: mostrar_afilador_final(arbol, info)).grid(row=4, column=1)

    ttk.Separator(box1, orient="horizontal", style="Separador2.TSeparator").grid(
        row=5, column=0, sticky="ew", columnspan=2, pady=3, padx=3)

    envios_afilador = ttk.Frame(box1, style='Color.TFrame')
    envios_afilador.grid(row=6, column=0, columnspan=2)
    
    ttk.Label(envios_afilador, text="Enviar piezas a Roman", font=("Arial", 12, "bold"), style="WhiteOnRed.TLabel").grid(row=0, column=0, columnspan=2)
    
    ttk.Label(envios_afilador, text="Piezas", style="WhiteOnRed.TLabel").grid(row=1, column=0)
    ttk.Label(envios_afilador, text="Cantidad", style="WhiteOnRed.TLabel").grid(row=1, column=1)
    
    comboxboxafiladores = ttk.Combobox(envios_afilador, values=piezas_afilador ,state="readonly", width=15)
    comboxboxafiladores.grid(row=2, column=0)
    
    entrycantidad1 = ttk.Entry(envios_afilador, width=7)
    entrycantidad1.grid(row=2, column=1)
    
    tk.Button(envios_afilador, 
            text="Envios a Roman",
            background="green",
            foreground="white",
            padx=4,
            pady=1, 
            command= lambda:enviar_piezas_a_roman(comboxboxafiladores, entrycantidad1, "piezas_finales_defenitivas", "piezas_afiladores_roman", arbol, result ,info
        )).grid(row=3, column=1)
    
    
    ttk.Separator(envios_afilador, orient="horizontal", style="Separador2.TSeparator").grid(
        row=4, column=0, sticky="ew", columnspan=2, pady=3, padx=3)
    
    
    ttk.Label(envios_afilador, text="ENTREGA DE AFILADORES TERMINADOS" ,font=("Arial", 10, "bold"), style="WhiteOnRed.TLabel").grid(row=5, column=0, columnspan=2)
    cantidad_terminada = ttk.Entry(envios_afilador, width=10)
    cantidad_terminada.grid(row=6, column=0,columnspan=2, pady=2)
    tk.Button(envios_afilador,
            text="Afiladores Terminados",
            background="blue",
            foreground="white",
            padx=4,
            pady=1,
            command=lambda:  armado_final_afiladores_y_agregar_cantidad(cantidad_terminada, result)
            ).grid(row=7, column=0, columnspan=2)

    ttk.Separator(envios_afilador, orient="horizontal", style="Separador2.TSeparator").grid(
        row=8, column=0, sticky="ew", columnspan=2, pady=3, padx=3)
    
    
#0000000000000000000000000niquelado0000000000000000000000000000000000000

    box5 = ttk.Frame(box2, style='Color.TFrame')
    box5.grid(row=16, column=0 ,columnspan=2)
    
    ttk.Label(box5, text="Niquelado", style="WhiteOnRed.TLabel",font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3)
    grupbtn = tk.Frame(box5)
    grupbtn.grid(row=1, column=0, columnspan=3)
    ttk.Button(
        grupbtn,
        text="Stock en bruto",
        style="Estilo2.TButton",
        command=lambda: mostrar(arbol, "piezas_del_fundicion", "niquelado", info),
    ).grid(row=1, column=0)
    
    ttk.Button(
        grupbtn,
        text="Stock en fabrica",
        style="Estilo2.TButton",
        command=lambda: mostrar(arbol, "piezas_finales_defenitivas", "niquelado", info),
    ).grid(row=1, column=1)
    
    ttk.Button(
        grupbtn,
        text="Stock en niquelado",
        style="Estilo2.TButton",
        command= lambda: mostrar(arbol, "pieza_retocadas", "niquelado", info)
    ).grid(row=1, column=2)
    
    ttk.Label(box5, text="Piezas A Niquelar", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=2)
    ttk.Label(box5, text="Piezas", style="WhiteOnRed.TLabel").grid(row=3, column=0, sticky="w")
    
    lista_piezas = ttk.Combobox(box5, values=niquelado, state="readonly", width=17)
    lista_piezas.grid(row=3, column=1, sticky="w")
    
    ttk.Label(box5, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=4, column=0, sticky="w")
    
    cantidad_a_niquelar = ttk.Entry(box5,style='WhiteOnRed.TEntry', width=10)
    cantidad_a_niquelar.grid(row=4, column=1, sticky="w",pady=1)

    tk.Button(
        box5,
        text="Enviar",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: envios_de_bruto_a_niquelar(
            lista_piezas.get(), cantidad_a_niquelar, result, arbol, "niquelado"
        ),
    ).grid(row=5, column=1, columnspan=2, padx=2, pady=2,sticky="w")

    ttk.Separator(box5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=6, column=0, columnspan=2, sticky="ew", padx=3, pady=3
    )

    ttk.Label(box5, text="Piezas Terminadas", style="WhiteOnRed.TLabel", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=2)
    ttk.Label(box5, text="Piezas", style="WhiteOnRed.TLabel").grid(row=8, column=0, sticky="w")
    
    lista_piezas_nique = ttk.Combobox(box5, values=niquelado, state="readonly", width=17)
    lista_piezas_nique.grid(row=8, column=1, sticky="w")
    
    ttk.Label(box5, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=9, column=0, sticky="w")
    
    cantidad_a_niquelado = ttk.Entry(box5,style='WhiteOnRed.TEntry', width=10)
    cantidad_a_niquelado.grid(row=9, column=1, sticky="w" ,pady=1)

    tk.Button(
        box5,
        text="Resivido",
        background="blue",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: envios_de_niquelado_a_fabrica(lista_piezas_nique.get(),cantidad_a_niquelado ,result, arbol, "niquelado")
        ).grid(row=10, column=1, columnspan=2, padx=2, pady=2, sticky="w")

    ttk.Separator(box5, orient="horizontal", style="Separador2.TSeparator").grid(
        row=11, column=0, columnspan=2, sticky="ew", padx=3, pady=3
    )    
    
    
#30000000000000000000000000000000Pintura000000000000000000000000000000000000000000000
    
    box6 = ttk.Frame(box3, style='Color.TFrame')
    box6.grid(row=17, column=0, columnspan=2)
    
    ttk.Label(box6, text="Pintura", style="WhiteOnRed.TLabel",font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3 )

    btn_group = tk.Frame(box6)
    btn_group.grid(row=1, column=0, columnspan=3)

    ttk.Button(
        btn_group,
        text="Stock en fabrica",
        style="Estilo2.TButton",
        command=lambda: mostrar(arbol, "piezas_del_fundicion", "pintor", info),
    ).grid(row=1, column=0)
    ttk.Button(
        btn_group,
        text="Stock Terminado",
        style="Estilo2.TButton",
        command=lambda: mostrar(arbol, "piezas_finales_defenitivas", "pintor", info),
    ).grid(row=1, column=1)
    ttk.Button(
        btn_group,
        text="Stock en Pintura",
        style="Estilo2.TButton",
        command=lambda: mostrar(arbol, "pieza_retocadas", "pintor", info),
    ).grid(row=1, column=2)

    ttk.Separator(box6, orient="horizontal", style="Separador2.TSeparator").grid(
        row=2, column=0, columnspan=3, padx=5, pady=5
    )
    
    cajapintura1 = ttk.Frame(box6, style='Color.TFrame')
    cajapintura1.grid(row=3, column=0)
    
    ttk.Label(cajapintura1 , text="Envios A Pintura",font=("Arial", 11, "bold"), style="WhiteOnRed.TLabel").grid(row=3, column=0, columnspan=2)

    ttk.Label(cajapintura1 , text="Tipo", style="WhiteOnRed.TLabel",).grid(row=4, column=0, sticky="ew")
    modelo = ttk.Combobox(cajapintura1 , values=modelo_piezas,state="readonly", width=17)
    modelo.grid(row=4, column=1, sticky="w")

    ttk.Label(cajapintura1 , text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=5, column=0, sticky="ew")
    enviar_a_pintura = ttk.Entry(cajapintura1 , width=10, style='WhiteOnRed.TEntry' )
    enviar_a_pintura.grid(row=5, column=1, pady=2)

    tk.Button(
        cajapintura1 ,
        text="Enviar Bases",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        font=('Helvetica', 8, "bold"),
        command=lambda: envios_de_bruto_a_pulido(
            modelo.get(), enviar_a_pintura, result, arbol, "pintor"
        ),
    ).grid(row=6, column=1)
    
    cajapintura2 = ttk.Frame(box6, style='Color.TFrame')
    cajapintura2.grid(row=3, column=1)
    
    ttk.Label(cajapintura2, text="Envios de cabezales",font=("Arial", 11, "bold"), style="WhiteOnRed.TLabel",).grid(row=0, column=0)

    cantidad_cabezales = ttk.Entry(cajapintura2, width=10,style='WhiteOnRed.TEntry')
    cantidad_cabezales.grid(row=1, column=0, pady=2, sticky="s")

    tk.Button(
        cajapintura2,
        text="Enviar Cabezales",
        background="green",
        foreground="white",
        padx=4,
        pady=1,
        command=lambda: envios_de_bruto_cabezal("cabezal_pintura", cantidad_cabezales, result, arbol, "pintor"),
        font=('Helvetica', 8, "bold")).grid(row=2, column=0, columnspan=1)

    ttk.Separator(box6, orient="horizontal", style="Separador2.TSeparator").grid(
        row=4, column=0, columnspan=2, sticky="ew", padx=3, pady=3
    )

    cajapintura4 = ttk.Frame(box6, style='Color.TFrame')
    cajapintura4.grid(row=5, column=0)


    ttk.Label(cajapintura4, text="Bases Resibidas",font=("Arial", 12, "bold"), style="WhiteOnRed.TLabel",).grid(row=11, column=0, columnspan=2)

    ttk.Label(cajapintura4, text="Tipo", style="WhiteOnRed.TLabel",).grid(row=12, column=0)
    modelo_pintur = ttk.Combobox(cajapintura4, values=modelo_piezas, state="readonly")
    modelo_pintur.grid(row=12, column=1)

    ttk.Label(cajapintura4, text="Cantidad", style="WhiteOnRed.TLabel",).grid(row=13, column=0)
    resibe_a_pintura = ttk.Entry(cajapintura4, width=10, style='WhiteOnRed.TEntry')
    resibe_a_pintura.grid(row=13, column=1, pady=3)

    tk.Button(
        cajapintura4,
        text="Cantida Resibida",
        background="blue",
        foreground="white",
        padx=10,
        pady=4,
        font=('Helvetica', 8, "bold"),
        command=lambda: envios_pulido_a_fabrica(modelo_pintur.get(),resibe_a_pintura, result, arbol, "pintor" )
    ).grid(row=14, column=1, pady=2)

    cajapintura3 = ttk.Frame(box6, style='Color.TFrame')
    cajapintura3.grid(row=5, column=1)


    ttk.Label(cajapintura3, text="Cabezales Terminados", style="WhiteOnRed.TLabel",font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="s")

    cantidad_resibida_cabezales = ttk.Entry(cajapintura3, width=10,style='WhiteOnRed.TEntry')
    cantidad_resibida_cabezales.grid(row=1, column=0, pady=5)

    tk.Button(
        cajapintura3,
        text="Resivir Cabzales",
        background="blue",
        foreground="white",
        padx=10,
        pady=4,
        font=('Helvetica', 8, "bold"),
        command=lambda: envios_pulido_a_fabrica_cabezal("cabezal_pintura", cantidad_resibida_cabezales, result, arbol, "pintor")
    ).grid(row=2, column=0)

    ttk.Separator(box6, orient="horizontal", style="Separador2.TSeparator").grid(
        row=17, column=0, columnspan=2, sticky="ew", padx=3, pady=3
    )


#(((((((((((((((((((((((((((((((((((((Stock )))))))))))))))))))))))))))))))))))))
    box4 = ttk.Frame(box1, style='Color.TFrame')
    box4.grid(row=16, column=0, sticky="n", columnspan=2)
    

    botonera2 = ttk.Frame(box4, style='Color.TFrame')
    botonera2.grid(row=0, column=0, columnspan=2)

    ttk.Label(botonera2, text="Stock en Fabrica",font=("Arial", 15, "bold"), style="WhiteOnRed.TLabel").grid(row=0, column=0,columnspan=2)
    ttk.Button(
        botonera2,
        style="Estilo9.TButton",
        text="Stock Total Bruto",
        command=lambda: mostrar_datos(arbol, "piezas_del_fundicion", info),
    ).grid(row=1, column=0, padx=3, pady=2)
    ttk.Button(
        botonera2,
        style="Estilo9.TButton",
        text="Stock Total Pulido",
        command=lambda: mostrar(arbol, "piezas_finales_defenitivas", "pulido", info),
    ).grid(row=1, column=1, padx=3, pady=2)

    ttk.Separator(botonera2, orient="horizontal", style="Separador2.TSeparator").grid(
        row=3, column=0, columnspan=2, sticky="ew", padx=3, pady=3
    )

#99999999999999999999999999999999999Observaciones ###############################################

    box7 = ttk.Frame(box1, style='Color.TFrame')
    box7.grid(row=17, column=0, columnspan=2)
    
    ttk.Label(box7, text="Observaciones", style="WhiteOnRed.TLabel",font=("Arial", 14, "bold")).grid(row=0, column=1, sticky="w")
    caja_texto = tk.Text(box7, height=6, width=30,)
    caja_texto.grid(row=1, column=1, columnspan=1)
    ttk.Button(
        box7, text="Enviar", style="Estilo4.TButton", command=lambda: agregar_a_lista_tarea(caja_texto, result)
    ).grid(row=2, column=1, sticky="e", pady=2, padx=2)

import tkinter as tk
from tkinter import ttk

from stock_chapa import crear_pestana_chapa
from provedores_fadeco import ventana_provedores
from mecanizado import mecanizado
from session_stock import stock
from index import inicio
from parte_armado import seccion_armado
from consultas import consultorio


root = tk.Tk()
root.title("Control De Stock Fadeco 2024-25")
root.iconbitmap("C:/Fadeco/img/FLogo.ico")
root.geometry("1250x650")
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0)


inicio(notebook)
stock(notebook)
ventana_provedores(notebook)
crear_pestana_chapa(notebook)
mecanizado(notebook)
seccion_armado(notebook)
consultorio(notebook)


root.mainloop() 

#TESTEO1
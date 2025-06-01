import sqlite3
import os
import tkinter as tk
from tkinter import messagebox, ttk
import re  

# Ruta a la base de datos
db_path = r"C:\Users\arqis\OneDrive\Escritorio\basededatos\alumnos.db"

# Conexión a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    correo TEXT
)
""")
conn.commit()

# Funciones de operación
def agregar_estudiante():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    correo = entry_correo.get()

    if not nombre or not edad or not correo:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
        return

    # Validar que edad sea un número
    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Edad inválida", "La edad debe ser un número.")
        return

    # Validar formato de correo
    patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron_correo, correo):
        messagebox.showerror("Correo inválido", "Por favor, introduce un correo válido (ej: usuario@dominio.com).")
        return

    # Insertar estudiante
    cursor.execute("INSERT INTO estudiantes (nombre, edad, correo) VALUES (?, ?, ?)", (nombre, edad, correo))
    conn.commit()
    mostrar_estudiantes()

    # Limpiar campos
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_correo.delete(0, tk.END)

def mostrar_estudiantes():
    for fila in tree.get_children():
        tree.delete(fila)
    cursor.execute("SELECT * FROM estudiantes")
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)

# Interfaz
root = tk.Tk()
root.title("Gestión de Estudiantes")
root.geometry("650x400")

# Frame de entrada
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5)
entry_nombre = tk.Entry(frame_form)
entry_nombre.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Edad:").grid(row=1, column=0, padx=5)
entry_edad = tk.Entry(frame_form)
entry_edad.grid(row=1, column=1, padx=5)

tk.Label(frame_form, text="Correo:").grid(row=2, column=0, padx=5)
entry_correo = tk.Entry(frame_form)
entry_correo.grid(row=2, column=1, padx=5)

btn_agregar = tk.Button(frame_form, text="Agregar estudiante", command=agregar_estudiante)
btn_agregar.grid(row=3, columnspan=2, pady=5)

# Tabla de estudiantes con scrollbar
frame_tabla = tk.Frame(root)
frame_tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

scrollbar_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Edad", "Correo"), show="headings", yscrollcommand=scrollbar_y.set)
scrollbar_y.config(command=tree.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Edad", text="Edad")
tree.heading("Correo", text="Correo")

tree.column("ID", width=50, anchor="center")
tree.column("Nombre", width=150)
tree.column("Edad", width=50, anchor="center")
tree.column("Correo", width=200)

tree.pack(expand=True, fill=tk.BOTH)

mostrar_estudiantes()

root.mainloop()

# Cierre
conn.close()

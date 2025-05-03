import sqlite3

# Conexión y creación de tabla
conn = sqlite3.connect("alumnos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    correo TEXT
)
""")
conn.commit()

# Funciones principales

def agregar_estudiante(nombre, edad, correo):
    cursor.execute("INSERT INTO estudiantes (nombre, edad, correo) VALUES (?, ?, ?)", (nombre, edad, correo))
    conn.commit()
    print("Estudiante agregado correctamente.")

def mostrar_estudiantes():
    cursor.execute("SELECT * FROM estudiantes")
    filas = cursor.fetchall()
    if filas:
        for fila in filas:
            print(fila)
    else:
        print("No hay estudiantes registrados.")

def buscar_por_nombre(nombre):
    cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ?", ('%' + nombre + '%',))
    resultados = cursor.fetchall()
    if resultados:
        for estudiante in resultados:
            print(estudiante)
    else:
        print("No se encontraron estudiantes con ese nombre.")

def editar_estudiante(id_estudiante, nuevo_nombre, nueva_edad, nuevo_correo):
    cursor.execute("UPDATE estudiantes SET nombre = ?, edad = ?, correo = ? WHERE id = ?", 
                   (nuevo_nombre, nueva_edad, nuevo_correo, id_estudiante))
    conn.commit()
    if cursor.rowcount:
        print("Estudiante actualizado correctamente.")
    else:
        print("No se encontró un estudiante con ese ID.")

def eliminar_estudiante(id_estudiante):
    cursor.execute("DELETE FROM estudiantes WHERE id = ?", (id_estudiante,))
    conn.commit()
    if cursor.rowcount:
        print("Estudiante eliminado correctamente.")
    else:
        print("No se encontró un estudiante con ese ID.")

# Menú principal
while True:
    print("\n1. Agregar estudiante\n2. Mostrar todos\n3. Buscar por nombre\n4. Editar estudiante\n5. Eliminar estudiante\n6. Salir")
    op = input("Elige una opción: ")

    if op == '1':
        nombre = input("Nombre: ")
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida.")
            continue
        correo = input("Correo: ")
        agregar_estudiante(nombre, edad, correo)

    elif op == '2':
        mostrar_estudiantes()

    elif op == '3':
        nombre = input("Nombre a buscar: ")
        buscar_por_nombre(nombre)

    elif op == '4':
        try:
            id_edit = int(input("ID del estudiante a editar: "))
            nuevo_nombre = input("Nuevo nombre: ")
            nueva_edad = int(input("Nueva edad: "))
            nuevo_correo = input("Nuevo correo: ")
            editar_estudiante(id_edit, nuevo_nombre, nueva_edad, nuevo_correo)
        except ValueError:
            print("Entrada inválida.")
    
    elif op == '5':
        try:
            id_eliminar = int(input("ID del estudiante a eliminar: "))
            eliminar_estudiante(id_eliminar)
        except ValueError:
            print("ID inválido.")

    elif op == '6':
        break

    else:
        print("Opción no válida.")

# Cierre de conexión
conn.close()

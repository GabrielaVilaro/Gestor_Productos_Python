from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3

"""----------------------------------Funciones-----------------------------------------"""

def conexionBBDD(): #creando la base de datos
    miConexion = sqlite3.connect("Productos")

    miCursor = miConexion.cursor()

    miCursor.execute('''
        CREATE TABLE DATOSPRODUCTOS
        (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE_PRODUCTO VARCHAR(50),
        PRECIO FLOAT(20),
        DESCRIPCION VARCHAR (100))
        ''')

    messagebox.showinfo("BBDD", "Base creada")

def salirDelPrograma(): #funcion para salir del programa

	valor = messagebox.askquestion("Salir", "¿Realmente quiere salir del programa?")

	if valor =="yes":
		root.destroy() #cierra el programa

def limpiarCuadros():

	miProducto.set("")
	miIdProd.set("")
	miPrecio.set("")
	textoComentario.delete(1.0, END) #borra desde el primer carcter hasta el final 

def crear():
	miConexion=sqlite3.connect("Productos")

	miCursor = miConexion.cursor()

	miCursor.execute("INSERT INTO DATOSPRODUCTOS VALUES(NULL, '" + miProducto.get() + 
		"','" + miPrecio.get() +  
		"','" + textoComentario.get("1.0", END) + "')")

	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro insertado con éxito.")

def leer():
	miConexion=sqlite3.connect("Productos")

	miCursor = miConexion.cursor()

	miCursor.execute("SELECT * FROM DATOSPRODUCTOS WHERE ID=" + miIdProd.get())

	elProducto = miCursor.fetchall()

	for producto in elProducto:

		miIdProd.set(producto[0])
		miProducto.set(producto[1])
		miPrecio.set(producto[2])
		textoComentario.insert(1.0, producto[3])

	miConexion.commit()

def actualizar():
	miConexion=sqlite3.connect("Productos")

	miCursor = miConexion.cursor()

	miCursor.execute("UPDATE DATOSPRODUCTOS SET NOMBRE_PRODUCTO= '" + miProducto.get() + 
		"', PRECIO='" + miPrecio.get() + 
		"', DESCRIPCION='" + textoComentario.get("1.0", END) +
		"' WHERE ID=" + miIdProd.get())


	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro actualizado con éxito.")

def borrar():
	miConexion=sqlite3.connect("Productos")

	miCursor = miConexion.cursor()

	miCursor.execute("DELETE FROM DATOSPRODUCTOS WHERE ID=" + miIdProd.get())

	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro eliminado con éxito")

def tabla():
        from tkinter import ttk
        miConexion=sqlite3.connect("Productos")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM DATOSPRODUCTOS")
        rows = miCursor.fetchall()

        """------------------------------Tabla---------------------------------"""
        
        tree= ttk.Treeview(root, column=("one", "two", "three", "four"), show='headings')
        tree.column("one", width=70)
        tree.column("two", width=70)
        tree.column("three", width=70)
        tree.column("four", width=70)
        tree.heading("one", text='ID')
        tree.heading("two", text="Producto")
        tree.heading("three", text="Precio")
        tree.heading("four", text="Descripción")
        tree.pack()
        for row in rows:
            print(row)
            tree.insert("",END, values=row)


        miConexion.close()


def aCercaDe():

	messagebox.showinfo("A cerca de", "Versión de práctica Gestor de productos By Gabriela Vilaró")

"""-------------------------Creación del menú del CRUD-------------------------"""
root = Tk()

root.title("Gestor de productos")

barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)

bbddMenu = Menu(barraMenu, tearoff=0) #armando el menú
                            #saca las lineas
bbddMenu.add_command(label="Conectar", command = conexionBBDD) #acá conecto con la base de datos
bbddMenu.add_command(label="Salir", command = salirDelPrograma)

borrarMenu = Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Borrar campos", command = limpiarCuadros)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Crear", command = crear)
crudMenu.add_command(label="Leer", command = leer)
crudMenu.add_command(label="Actualizar", command = actualizar)
crudMenu.add_command(label="Borrar", command = borrar)

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="A cerca de", command = aCercaDe)

barraMenu.add_cascade(label="Base de datos", menu=bbddMenu)#acomodo los elementos en el menú
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

"""----------------------------------Creación de los cuadros del crud-------------------------------"""

miFrame =Frame(root)
miFrame.pack()

miIdProd = StringVar()
miProducto = StringVar()#tipo entry
miPrecio = StringVar()

cuadroId=Entry(miFrame, textvariable = miIdProd)
cuadroId.grid(row=1, column = 1, padx=10, pady=10)

cuadroProducto=Entry(miFrame, textvariable = miProducto)
cuadroProducto.grid(row=2, column = 1, padx=10, pady=10) 

cuadroPrecio=Entry(miFrame, textvariable = miPrecio)
cuadroPrecio.grid(row=3, column = 1, padx=10, pady=10) 

textoComentario = Text(miFrame, width=16, height=5)
textoComentario.grid(row=4, column = 1, padx=10, pady=10) 

scrollVert=Scrollbar(miFrame, command=textoComentario.yview) #deslizador
scrollVert.grid(row=5, column=2, sticky="nsew") #fila 5

textoComentario.config(yscrollcommand=scrollVert.set)

"""-----------------------------Creación de las etiquetas de los cuadros---------------------------- """
idLabel = Label(miFrame, text="ID:")
idLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

nombreLabel = Label(miFrame, text="Producto:")
nombreLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

precioLabel = Label(miFrame, text="Precio: ")
precioLabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

comentariosLabel = Label(miFrame, text="Descripción")
comentariosLabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

"""---------------------------------Creación de los botones del crud----------------------------------------"""

miFrame2=Frame(root)

miFrame2.pack()

botonCrear=Button(miFrame2, text="Crear", command = crear)
botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

botonLeer=Button(miFrame2, text="Leer", command = leer)
botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

botonActualizar=Button(miFrame2, text="Actualizar", command = actualizar)
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text="Borrar", command=borrar)
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text="Ver datos", command=tabla)
botonBorrar.grid(row=1, column=4, sticky="e", padx=10, pady=10)

root.mainloop()

from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
from datetime import datetime, date, time, timedelta
import time
import datetime

root = Tk()
#==================RELOJ DIGITAL=============================================================
root.focus()
root.config(cursor='watch')

root.title("SISTEMA LAVANDERIA")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.attributes("-fullscreen", False)
ahora = time.strftime("%c")

#==================FechaACTUAL===============#
x = datetime.datetime.now()
fecha =  ("%s/%s/%s" % (x.day, x.month, x.year))
#==================FechaACTUAL===============#

#==================================LISTBOX============================================

def on_keyrelease(event):
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from test_list
    if value == '':
        data = test_list
    else:
        data = []
        for item in test_list:
            if value in item.lower():
                data.append(item)

    # update data in listbox
    listbox_update(data)

def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    # display element selected on list
    print('(event) previous:', event.widget.get('active'))
    print('(event)  current:', event.widget.get(event.widget.curselection()))
    print('---')

test_list = ('saco', 'terno', 'blusa', 'vestido', 'mochila', 'sinnombre', 'nose', 'algo' )

#=====================================================================================
def Database():
    global conn, cursor
    conn = sqlite3.connect('lavanderia.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `cliente` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nombre TEXT, apellido TEXT, estado TEXT, descripcion TEXT, precio TEXT, fecha TEXT)")

def Create():
    if  NOMBRE.get() == "" or APELLIDO.get() == "" or ESTADO.get() == "" or DESCRIPCION.get() == "" or PRECIO.get() == "" or FECHA.get() == "":
        txt_result.config(text="Por favor complete el campo requerido!", fg="red")
    else:
        Database()
        cursor.execute("INSERT INTO `cliente` (nombre, apellido, estado, descripcion, precio, fecha) VALUES(?, ?, ?, ?, ?, ?)", (str(NOMBRE.get()), str(APELLIDO.get()), str(ESTADO.get()), str(DESCRIPCION.get()), str(PRECIO.get()), str(FECHA.get())))
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM `cliente` ORDER BY `apellido` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        conn.commit()
        NOMBRE.set("")
        APELLIDO.set("")
        ESTADO.set("")
        DESCRIPCION.set("")
        PRECIO.set("")
        FECHA.set("")
        cursor.close()
        conn.close()
        txt_result.config(text="Instancia creada", fg="green")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `cliente` ORDER BY `apellido` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    txt_result.config(text="Datos mostrados correctamente", fg="black")

def Search():
    tree.delete(*tree.get_children())
    Database()
    nose = (str(NOMBRE.get()), str(APELLIDO.get()),)
    cursor.execute("SELECT * FROM `cliente` WHERE nombre = ? AND apellido = ?", nose)
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    txt_result.config(text="Datos mostrados correctamente", fg="black")

def Update():
    Database()
    if ESTADO.get() == "":
        txt_result.config(text="Por favor seleccione un genero", fg="red")
    else:
        tree.delete(*tree.get_children())
        cursor.execute("UPDATE `cliente` SET `nombre` = ?, `apellido` = ?, `estado` =?,  `descripcion` = ?,  `precio` = ?, `fecha` = ? WHERE `mem_id` = ?", (str(NOMBRE.get()), str(APELLIDO.get()), str(ESTADO.get()), str(DESCRIPCION.get()), str(PRECIO.get()), str(FECHA.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `cliente` ORDER BY `apellido` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        cursor.close()
        conn.close()
        NOMBRE.set("")
        APELLIDO.set("")
        ESTADO.set("")
        DESCRIPCION.set("")
        PRECIO.set("")
        FECHA.set("")
        btn_create.config(state=NORMAL)
        btn_read.config(state=NORMAL)
        btn_update.config(state=DISABLED)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Datos actualizados con exito", fg="black")

def OnSelected(event):
    global mem_id;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    NOMBRE.set("")
    APELLIDO.set("")
    ESTADO.set("")
    DESCRIPCION.set("")
    PRECIO.set("")
    FECHA.set("")
    NOMBRE.set(selecteditem[1])
    APELLIDO.set(selecteditem[2])
    DESCRIPCION.set(selecteditem[4])
    PRECIO.set(selecteditem[5])
    FECHA.set(selecteditem[6])
    btn_create.config(state=DISABLED)
    btn_read.config(state=DISABLED)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=DISABLED)

def Delete():
    if not tree.selection():
       txt_result.config(text="Por favor, seleccione un artículo primero", fg="red")
    else:
        result = tkMessageBox.askquestion('SISTEMA LAVANDERIA', '¿Seguro que quieres borrar este registro?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `cliente` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            txt_result.config(text="Se borraron los datos", fg="black")

def Exit():
    result = tkMessageBox.askquestion('SISTEMA LAVANDERIA', '¿Seguro que quieres salir?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()




#==================================VARIABLES==========================================
NOMBRE = StringVar()
APELLIDO = StringVar()
ESTADO = StringVar()
DESCRIPCION = StringVar()
PRECIO = StringVar()
FECHA = StringVar()

#==================================FRAME==============================================
Top = Frame(root, width=900, height=50, bd=8, relief="raise")
Top.pack(side=TOP)
Left = Frame(root, width=600, height=500, bd=8, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500, bd=8, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=100, bd=8, relief="raise")
Buttons.pack(side=BOTTOM)
RadioGroup = Frame(Forms)
AlAgua = Radiobutton(RadioGroup, text="En inventario", variable=ESTADO, value="En inventario", font=('arial', 16)).pack(side=LEFT)
AlSeco = Radiobutton(RadioGroup, text="Entregado", variable=ESTADO, value="Entregado", font=('arial', 16)).pack(side=LEFT)



#====================EmpaquetandoENTRY===================#
entry = Entry(Left)
entry.pack()
#====================EmpaquetandoENTRY===================#

#====================EmpaquetandoLISTBOX===================#
listbox = Listbox(Left)
listbox.pack()
#====================EmpaquetandoLISTBOX===================#

#====================EmpaquetandoFECHA===================#
fecha = Label(Top, font=('ubuntu', 30, 'bold'), bg='#3C3B37', fg='white', bd=0, text = fecha)
fecha.pack(side = LEFT)
#====================EmpaquetandoRELOJ===================#

#====================EmpaquetandoFECHA===================#
time1 = ''
clock = Label(Top, font=('ubuntu', 30, 'bold'), bg='#3C3B37', fg='white', bd=0)
clock.pack(side = RIGHT)



def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    clock.after(200, tick)
tick()
#====================EmpaquetandoRELOJ===================#


#==================================LABEL WIDGET=======================================
txt_title = Label(Top, width=900, font=('arial', 24), text = "Sistema Lavanderia")
txt_title.pack()
txt_nombre = Label(Forms, text="Nombre:", font=('arial', 16), bd=15)
txt_nombre.grid(row=0, sticky="e")
txt_apellido = Label(Forms, text="Apellido:", font=('arial', 16), bd=15)
txt_apellido.grid(row=1, sticky="e")
txt_estado = Label(Forms, text="Estado:", font=('arial', 16), bd=15)
txt_estado.grid(row=2, sticky="e")
txt_descripcion = Label(Forms, text="Descripcion:", font=('arial', 16), bd=15)
txt_descripcion.grid(row=3, sticky="e")
txt_precio = Label(Forms, text="Precio:", font=('arial', 16), bd=15)
txt_precio.grid(row=4, sticky="e")
txt_fecha = Label(Forms, text="Fecha:", font=('arial', 16), bd=15)
txt_fecha.grid(row=5, sticky="e")
txt_result = Label(Buttons)
txt_result.pack(side=TOP)

#==================================ENTRY WIDGET=======================================
nombre = Entry(Forms, textvariable=NOMBRE, width=30)
nombre.grid(row=0, column=1)
apellido = Entry(Forms, textvariable=APELLIDO, width=30)
apellido.grid(row=1, column=1)
RadioGroup.grid(row=2, column=1)
descripcion = Entry(Forms, textvariable=DESCRIPCION, width=30)
descripcion.grid(row=3, column=1)
precio = Entry(Forms, textvariable=PRECIO, width=30)
precio.grid(row=4, column=1)
fecha = Entry(Forms, textvariable=FECHA, width=30)
fecha.grid(row=5, column=1)

Entry = entry.bind('<KeyRelease>', on_keyrelease)
Listbox = listbox.bind('<<ListboxSelect>>', on_select)
listbox_update(test_list)

#==================================BUTTONS WIDGET=====================================
btn_create = Button(Buttons, width=10, text="Crear", command=Create)
btn_create.pack(side=LEFT)
btn_read = Button(Buttons, width=10, text="Leer", command=Read )
btn_read.pack(side=LEFT)
btn_update = Button(Buttons, width=10, text="Actualizar", command=Update, state=DISABLED)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Borrar", command=Delete)
btn_delete.pack(side=LEFT)
btn_exit = Button(Buttons, width=10, text="Salir", command=Exit)
btn_exit.pack(side=LEFT)
btn_buscar = Button(Buttons, width=10, text="Buscar", command=Search)
btn_buscar.pack(side=LEFT)

#==================================LIST WIDGET========================================
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("ClienteID", "Nombre", "Apellido", "Estado", "Descripcion", "Precio", "Fecha"), selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('ClienteID', text="ClienteID", anchor=W)
tree.heading('Nombre', text="Nombre", anchor=W)
tree.heading('Apellido', text="Apellido", anchor=W)
tree.heading('Estado', text="Estado", anchor=W)
tree.heading('Descripcion', text="Descripcion", anchor=W)
tree.heading('Precio', text="Precio", anchor=W)
tree.heading('Fecha', text="Fecha", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=150)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#==================================INITIALIZATION=====================================
if __name__ == '__main__':
    root.mainloop()

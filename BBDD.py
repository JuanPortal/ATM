from tkinter import *
import sqlite3

root = Tk()
root.title("Cajero")
root.iconbitmap("logo.ico")
root.geometry("450x350")
root.resizable(0, 0)

frLogin = Frame(root)
frHome = Frame(root)
frSaldo = Frame(root)
frMovimientos = Frame(root)
frRetiro = Frame(root)
frDeposito = Frame(root)
frTransferencia = Frame(root)
frPagoServicios = Frame(root)
frCambioClave = Frame(root)
frLogout = Frame(root)

for fr in (frLogin, frHome, frSaldo, frMovimientos, frRetiro, frDeposito, frTransferencia, frPagoServicios,
           frCambioClave, frLogout):
    fr.config(width=450, height=350)
    fr.grid(row=0, column=0, sticky="nsew")

retiro = IntVar()
retiro.set("")
deposito = IntVar()
deposito.set("")
transferencia = IntVar()
transferencia.set("")
pago = IntVar()
pago.set("")
numeroCuenta = StringVar()
numeroCuenta.set("")
codigoPago = StringVar()
codigoPago.set("")
contrasena = StringVar()
contrasena.set("")
contrasena2 = StringVar()
contrasena2.set("")
contrasena3 = StringVar()
contrasena3.set("")

label10 = Label(root)
label11 = Label(root)
label12 = Label(root)
label13 = Label(root)
label14 = Label(root)
label15 = Label(root)
label16 = Label(root)
label17 = Label(root)
label18 = Label(root)
label22 = Label(root)
label31 = Label(root)
label32 = Label(root)


def mostrar(frame):
    global label11
    global label12
    global label13
    global label14
    global label15
    global label16
    global label17
    global label18
    global label22
    global label31
    global label32
    global contrasena
    global contrasena2
    global contrasena3
    global pago
    label11.destroy()
    label12.destroy()
    label13.destroy()
    label14.destroy()
    label15.destroy()
    label16.destroy()
    label17.destroy()
    label18.destroy()
    label22.destroy()
    label31.destroy()
    label32.destroy()
    contrasena.set("")
    contrasena2.set("")
    contrasena3.set("")
    pago.set("")
    frame.tkraise()


mostrar(frLogin)  # MOSTRAR LOGIN!!!!


# ============= Clase Cliente ============= #

class Cliente:
    def __init__(self, saldo, codigo, password, movimiento):
        self.saldo = saldo
        self.codigo = codigo
        self.password = password
        self.movimiento = movimiento

    def setSaldo(self, nuevosaldo):
        self.saldo = nuevosaldo

    def agregar(self):
        conexion = sqlite3.connect("Cajero")
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO Usuarios VALUES('{self.codigo}', '{self.saldo}', '{self.password}')")
        conexion.commit()
        cursor.execute(f"INSERT INTO Movimientos VALUES('{self.codigo}', '')")
        conexion.commit()
        conexion.close()


miconexion = sqlite3.connect("Cajero")
micursor = miconexion.cursor()
micursor.execute("SELECT DISTINCT * FROM Usuarios")
bbdd = micursor.fetchall()
print(f"Usuarios: {bbdd}")

codigos = [codigo[0] for codigo in bbdd]
passwords = [password[2] for password in bbdd]
saldos = [saldo[1] for saldo in bbdd]

micursor.execute("SELECT * FROM Movimientos ")
bbdd2 = micursor.fetchall()
print(f"Movimientos: {bbdd2}")

miconexion.close()

indice = 0
print(f"Índice inicial: {indice}")
indice2 = 0
print(f"Índice 2 inicial: {indice2}")


# ============= Función Login ============= #

def ingresar(a, b):
    numeroCuenta.set("")
    contrasena.set("")
    global label10
    label10.destroy()
    global indice

    if a in codigos:
        indice = codigos.index(a)
        print(f"Nuevo índice: {indice}")
        if b == passwords[indice]:
            mostrar(frHome)

        else:
            label10 = Label(frLogin, text="Contraseña incorrecta", fg="red")
            label10.grid(row=1, column=0, padx=10, pady=10)
            label10.place(x=167, y=249)  # 116x9

    else:
        label10 = Label(frLogin, text="Usuario incorrecto", fg="red")
        label10.grid(row=1, column=0, padx=10, pady=10)
        label10.place(x=177, y=249)  # 97x9


# ============== Función Saldo ============== #

def verSaldo():
    mostrar(frSaldo)
    global label22
    label22.destroy()

    label22 = Label(frSaldo, text=f"Saldo actual: {saldos[indice]}", fg="green")
    label22.grid(row=1, column=0, padx=10, pady=10)
    label22.place(x=178, y=63.85)  # 94x9


# =========== Función Movimientos =========== #

def movements():
    mostrar(frMovimientos)

    miconexion0 = sqlite3.connect("Cajero")
    micursor0 = miconexion0.cursor()
    micursor0.execute(f"SELECT Movimientos FROM Movimientos WHERE Código = '{codigos[indice]}'")
    bbddmovements = micursor0.fetchall()
    miconexion0.close()
    movimientoslist = []
    for mm in bbddmovements:
        movimientoslist.insert(0, mm[0])
    cadena = "\n".join(movimientoslist)

    texto1 = Text(frMovimientos, width=35, height=10)
    texto1.grid(row=1, column=0, padx=10, pady=10)
    texto1.insert(END, cadena)
    texto1.place(x=83, y=86)  # 284x164


# ============= Función Retiro ============= #

def retirar(n):
    retiro.set("")
    global label11
    global label12
    label11.destroy()
    label12.destroy()
    miconexion1 = sqlite3.connect("Cajero")
    micursor1 = miconexion1.cursor()

    if n <= saldos[indice]:
        saldos[indice] -= n
        micursor1.execute(f"UPDATE Usuarios SET Saldo = {saldos[indice]} WHERE Código = '{codigos[indice]}'")
        miconexion1.commit()
        label11 = Label(frRetiro, text="Retiro realizado satisfactoriamente", fg="green")
        label11.grid(row=1, column=0, padx=10, pady=10)
        label11.place(x=135, y=133)  # 143x12

        label12 = Label(frRetiro, text=f"Saldo actual: {saldos[indice]}")  # Retirar tarjeta
        label12.grid(row=2, column=0, padx=10, pady=10)
        label12.place(x=184, y=176)  # 82x9

        micursor1.execute(f"INSERT INTO Movimientos VALUES('{codigos[indice]}', 'Retiro\t\t\t     -{n}')")
        miconexion1.commit()
        miconexion1.close()

    else:
        label11 = Label(frRetiro, text="No cuenta con saldo suficiente", fg="red")
        label11.grid(row=1, column=0, padx=10, pady=10)
        label11.place(x=144, y=133)  # 163x9


# ============ Función Depósito ============ #

def depositar(n):
    deposito.set("")
    global label13
    global label14
    label13.destroy()
    label14.destroy()
    miconexion2 = sqlite3.connect("Cajero")
    micursor2 = miconexion2.cursor()

    if n <= 5000:
        saldos[indice] += n
        micursor2.execute(f"UPDATE Usuarios SET Saldo = {saldos[indice]} WHERE Código = '{codigos[indice]}'")
        miconexion2.commit()
        label13 = Label(frDeposito, text="Depósito realizado satisfactoriamente", fg="green")
        label13.grid(row=1, column=0, padx=10, pady=10)
        label13.place(x=127, y=133)  # 197x12

        label14 = Label(frDeposito, text=f"Saldo actual: {saldos[indice]}")
        label14.grid(row=2, column=0, padx=10, pady=10)
        label14.place(x=181, y=176)  # 88x9

        micursor2.execute(f"INSERT INTO Movimientos VALUES('{codigos[indice]}', 'Depósito\t\t\t     -{n}')")
        miconexion2.commit()
        miconexion2.close()

    else:
        label13 = Label(frDeposito, text="La cantidad supera el límite de depósito", fg="red")
        label13.grid(row=1, column=0, padx=10, pady=10)
        label13.place(x=121, y=133)  # 209x12


# ========== Función Transferencia ========== #

def transferir(n, a):
    transferencia.set("")
    numeroCuenta.set("")
    global indice2
    global label15
    global label16
    label15.destroy()
    label16.destroy()
    miconexion3 = sqlite3.connect("Cajero")
    micursor3 = miconexion3.cursor()

    if a in codigos and n <= saldos[indice]:
        indice2 = codigos.index(a)
        saldos[indice] -= n
        micursor3.execute(f"UPDATE Usuarios SET Saldo = {saldos[indice]} WHERE Código = '{codigos[indice]}'")
        miconexion3.commit()
        saldos[indice2] += n
        micursor3.execute(f"UPDATE Usuarios SET Saldo = {saldos[indice2]} WHERE Código = '{codigos[indice2]}'")
        miconexion3.commit()
        label15 = Label(frTransferencia, text="Transferencia realizada satisfactoriamente", fg="green")
        label15.grid(row=1, column=0, padx=10, pady=10)
        label15.place(x=116, y=152)  # 219x9

        label16 = Label(frTransferencia, text=f"Saldo actual: {saldos[indice]}")
        label16.grid(row=2, column=0, padx=10, pady=10)
        label16.place(x=181, y=192)  # 88x9

        micursor3.execute(f"INSERT INTO Movimientos VALUES('{codigos[indice]}', 'Transferencia\t\t\t     -{n}')")
        micursor3.execute(f"INSERT INTO Movimientos VALUES('{codigos[indice2]}', 'Transferencia\t\t\t     +{n}')")
        miconexion3.commit()
        miconexion3.close()

        print(f"Saldo del otro {saldos[indice2]}")

    else:
        label15 = Label(frTransferencia, text="Intente nuevamente", fg="red")
        label15.grid(row=1, column=0, padx=10, pady=10)
        label15.place(x=172, y=162)  # 106x9


# ========= Función Pago Servicios ========= #

def pagar(n, a):
    pago.set("")
    codigoPago.set("")
    global label17
    global label18
    label17.destroy()
    label18.destroy()
    miconexion4 = sqlite3.connect("Cajero")
    micursor4 = miconexion4.cursor()

    if len(a) == 6 and n <= saldos[indice]:
        saldos[indice] -= n
        micursor4.execute(f"UPDATE Usuarios SET Saldo = {saldos[indice]} WHERE Código = '{codigos[indice]}'")
        miconexion4.commit()
        label17 = Label(frPagoServicios, text="Pago realizado satisfactoriamente", fg="green")
        label17.grid(row=1, column=0, padx=10, pady=10)
        label17.place(x=137, y=150)  # 177x12

        label18 = Label(frPagoServicios, text=f"Saldo actual: {saldos[indice]}")
        label18.grid(row=2, column=0, padx=10, pady=10)
        label18.place(x=181, y=195)  # 88x9

        micursor4.execute(f"INSERT INTO Movimientos VALUES('{codigos[indice]}', 'Pago servicios\t\t\t     -{n}')")
        miconexion4.commit()
        miconexion4.close()

    else:
        label17 = Label(frPagoServicios, text="Intente nuevamente", fg="red")
        label17.grid(row=1, column=0, padx=10, pady=10)
        label17.place(x=172, y=160)  # 106x9


# =========== Función Cambio Clave =========== #

def cambioClave(a, b, c):
    global label31
    global label32
    global contrasena
    global contrasena2
    global contrasena3
    label31.destroy()
    label32.destroy()
    contrasena.set("")
    contrasena2.set("")
    contrasena3.set("")

    if a == passwords[indice]:
        if len(b) > 0 and b == c:
            passwords.pop(indice)
            passwords.insert(indice, b)
            micursor.execute(f"UPDATE Usuarios SET Contraseña = '{passwords[indice]}' WHERE Código \
            = '{codigos[indice]}'")
            miconexion.commit()
            label31 = Label(frCambioClave, text="Contraseña actualizada correctamente", fg="green")
            label31.grid(row=1, column=0, padx=10, pady=10)
            label31.place(x=124, y=188)  # 202x9
        else:
            label32 = Label(frCambioClave, text="Las contraseñas no coinciden", fg="red")
            label32.grid(row=1, column=0, padx=10, pady=10)
            label32.place(x=148, y=188)  # 155x9

    else:
        label31 = Label(frCambioClave, text="Contraseña incorrecta", fg="red")
        label31.grid(row=1, column=0, padx=10, pady=10)
        label31.place(x=167, y=188)  # 116x9


# ================== Login ================== #

img2 = PhotoImage(file="GNB.png")
label19 = Label(frLogin, image=img2)
label19.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label19.place(x=125, y=35)  # 200x83

label8 = Label(frLogin, text="Usuario")
label8.grid(row=1, column=0, padx=10, pady=10)
label8.place(x=134, y=151)  # 40x9      espacio=28

input7 = Entry(frLogin, textvariable=numeroCuenta)
input7.grid(row=1, column=1, padx=10, pady=10)
input7.config(justify="center")
input7.place(x=205, y=153)  # 124x19

label9 = Label(frLogin, text="Contraseña")
label9.grid(row=2, column=0, padx=10, pady=10)
label9.place(x=124, y=191)  # 60x9      espacio=18

input6 = Entry(frLogin, textvariable=contrasena)
input6.grid(row=2, column=1, padx=10, pady=10)
input6.config(justify="center", show="*")
input6.place(x=205, y=193)  # 124x19

btnF5 = Button(frLogin, text="Ingresar", command=lambda: ingresar(numeroCuenta.get(), contrasena.get()))
btnF5.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
btnF5.place(x=198, y=291)  # 53x26

# ================== Home ================== #

label1 = Label(frHome, text="¿Qué deseas hacer?", fg="blue")
label1.grid(row=0, column=0, padx=10, pady=20, columnspan=4)
label1.place(x=174, y=39)  # 102x12

opc1 = Button(frHome, text="Saldo", command=lambda: verSaldo())
opc1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
opc1.place(x=10, y=90)  # 40x26

opc2 = Button(frHome, text="Movimientos", command=lambda: movements())
opc2.grid(row=1, column=1, padx=10, pady=10, sticky="e")
opc2.place(x=359, y=90)  # 81x26

opc3 = Button(frHome, text="Retiro", command=lambda: mostrar(frRetiro))
opc3.grid(row=2, column=0, padx=10, pady=10, sticky="w")
opc3.place(x=10, y=155)  # 42x26

opc4 = Button(frHome, text="Depósito", command=lambda: mostrar(frDeposito))
opc4.grid(row=2, column=1, padx=10, pady=10, sticky="e")
opc4.place(x=382, y=155)  # 58x26

opc5 = Button(frHome, text="Transferencia", command=lambda: mostrar(frTransferencia))
opc5.grid(row=3, column=0, padx=10, pady=10)
opc5.place(x=10, y=220)  # 81x26

opc6 = Button(frHome, text="Pago Servicio", command=lambda: mostrar(frPagoServicios))
opc6.grid(row=3, column=1, padx=10, pady=10)
opc6.place(x=358, y=220)  # 82x26

opc7 = Button(frHome, text="Cambio clave", command=lambda: mostrar(frCambioClave))
opc7.grid(row=3, column=1, padx=10, pady=10)
opc7.place(x=10, y=285)  # 83x26

opc8 = Button(frHome, text="Log out", command=lambda: mostrar(frLogin))
opc8.grid(row=3, column=1, padx=10, pady=10)
opc8.place(x=388, y=285)  # 52x26

# ================= Saldo ================= #

'''label20 = Label(frSaldo, text="Su saldo actual es de")
label20.grid(row=0, column=0, padx=10, pady=10)
label20.place(x=140, y=23.85)'''

img = PhotoImage(file="home_btn.png")
btn6 = Button(frSaldo, image=img, text="Home", command=lambda: mostrar(frHome))
btn6.config(height=25, width=25)
btn6.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn6.place(x=210, y=289)  # 31x31

# =============== Movimientos =============== #

label23 = Label(frMovimientos, text="Últimos movimientos", fg="blue")
label23.grid(row=0, column=0, padx=10, pady=10)
label23.place(x=168, y=37)  # 114x12

btn7 = Button(frMovimientos, image=img, text="Home", command=lambda: mostrar(frHome))
btn7.config(height=25, width=25)
btn7.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn7.place(x=210, y=289)  # 31x31

# ================= Retiro ================= #

label2 = Label(frRetiro, text="Ingrese la cantidad a retirar", fg="blue")
label2.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label2.place(x=154, y=34)  # 143x12

input1 = Entry(frRetiro, textvariable=retiro)
input1.grid(row=1, column=1, padx=10, pady=10)
input1.config(justify="center")
input1.place(x=163, y=80)  # 124x19

btnF1 = Button(frRetiro, text="Retirar", command=lambda: retirar(retiro.get()))
btnF1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
btnF1.place(x=203, y=219)  # 45x26

btn1 = Button(frRetiro, image=img, text="Home", command=lambda: mostrar(frHome))
btn1.config(height=25, width=25)
btn1.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn1.place(x=210, y=285)  # 31x31

# ================ Depósito ================ #

label3 = Label(frDeposito, text="Ingrese la cantidad a depositar", fg="blue")
label3.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label3.place(x=145, y=34)  # 161x12

input2 = Entry(frDeposito, textvariable=deposito)
input2.grid(row=1, column=1, padx=10, pady=10)
input2.config(justify="center")
input2.place(x=163, y=80)  # 124x19

btnF2 = Button(frDeposito, text="Depositar", command=lambda: depositar(deposito.get()))
btnF2.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
btnF2.place(x=195, y=219)  # 60x26

btn2 = Button(frDeposito, image=img, text="Home", command=lambda: mostrar(frHome))
btn2.config(height=25, width=25)
btn2.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn2.place(x=210, y=285)  # 31x31

# ============== Transferencia ============== #

label4 = Label(frTransferencia, text="Ingrese la cantidad a transferir y el número de cuenta receptora", fg="blue")
label4.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label4.place(x=59, y=25)  # 332x12

label5 = Label(frTransferencia, text="Cantidad")
label5.grid(row=1, column=0, padx=10, pady=10)
label5.place(x=130, y=67)  # 48x9      espacio=69

input3 = Entry(frTransferencia, textvariable=transferencia)
input3.grid(row=1, column=1, padx=10, pady=10)
input3.config(justify="center")
input3.place(x=222, y=72)  # 124x19

label6 = Label(frTransferencia, text="Número de cuenta")
label6.grid(row=2, column=0, padx=10, pady=10)
label6.place(x=105, y=107)  # 99x9      espacio=18

input4 = Entry(frTransferencia, textvariable=numeroCuenta)
input4.grid(row=2, column=1, padx=10, pady=10)
input4.config(justify="center")
input4.place(x=222, y=112)  # 124x19

btnF3 = Button(frTransferencia, text="Transferir", command=lambda: transferir(transferencia.get(), numeroCuenta.get()))
btnF3.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
btnF3.place(x=195, y=233)  # 60x26

btn4 = Button(frTransferencia, image=img, text="Home", command=lambda: mostrar(frHome))
btn4.config(height=25, width=25)
btn4.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn4.place(x=210, y=290)  # 31x31

# ============= Pago Servicios ============= #

label26 = Label(frPagoServicios, text="Ingrese el monto a pagar y el código de pago", fg="blue")
label26.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label26.place(x=106, y=28)  # 238x12

label27 = Label(frPagoServicios, text="Monto")
label27.grid(row=1, column=0, padx=10, pady=10)
label27.place(x=136, y=63)  # 36x9    espacio=42

input8 = Entry(frPagoServicios, textvariable=pago)
input8.grid(row=1, column=1, padx=10, pady=10)
input8.config(justify="center")
input8.place(x=215, y=68)  # 124x19

label7 = Label(frPagoServicios, text="Código de pago")
label7.grid(row=2, column=0, padx=10, pady=10)
label7.place(x=112, y=105)  # 85x12  espacio=18

input5 = Entry(frPagoServicios, textvariable=codigoPago)
input5.grid(row=2, column=1, padx=10, pady=10)
input5.config(justify="center")
input5.place(x=215, y=108)  # 124x19

btnF4 = Button(frPagoServicios, text="Pagar", command=lambda: pagar(pago.get(), codigoPago.get()))
btnF4.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
btnF4.place(x=205, y=237)  # 41x26

btn5 = Button(frPagoServicios, image=img, text="Home", command=lambda: mostrar(frHome))
btn5.config(height=25, width=25)
btn5.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn5.place(x=210, y=291)  # 31x31

# ============== Cambio Clave ============== #

label24 = Label(frCambioClave, text="Cambio de contraseña", fg="blue")
label24.grid(row=0, column=0, padx=10, pady=10)
label24.place(x=166, y=20)  # 119x9

label28 = Label(frCambioClave, text="Contraseña actual")
label28.grid(row=2, column=0, padx=10, pady=10)
label28.place(x=107, y=62)  # x  espacio=18

input9 = Entry(frCambioClave, textvariable=contrasena)
input9.grid(row=2, column=1, padx=10, pady=10)
input9.config(justify="center", show="*")
input9.place(x=222, y=67)  # 124x19

label29 = Label(frCambioClave, text="Constraseña nueva")
label29.grid(row=2, column=0, padx=10, pady=10)
label29.place(x=104, y=102)  # x  espacio=18

input10 = Entry(frCambioClave, textvariable=contrasena2)
input10.grid(row=2, column=1, padx=10, pady=10)
input10.config(justify="center", show="*")
input10.place(x=222, y=107)  # 124x19

label30 = Label(frCambioClave, text="Constraseña nueva")
label30.grid(row=2, column=0, padx=10, pady=10)
label30.place(x=104, y=142)  # x  espacio=18

input11 = Entry(frCambioClave, textvariable=contrasena3)
input11.grid(row=2, column=1, padx=10, pady=10)
input11.config(justify="center", show="*")
input11.place(x=222, y=147)  # 124x19

btnF6 = Button(frCambioClave, text="Actualizar", command=lambda: cambioClave(contrasena.get(), contrasena2.get(),
                                                                             contrasena3.get()))
btnF6.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
btnF6.place(x=194, y=229)  # 63x26

btn8 = Button(frCambioClave, image=img, text="Home", command=lambda: mostrar(frHome))
btn8.config(height=25, width=25)
btn8.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn8.place(x=210, y=289)  # 31x31

# ================= Logout ================= #

label25 = Label(frLogout, text="Logout")
label25.grid(row=0, column=0, padx=10, pady=10)
label25.place(x=140, y=23.85)

btn9 = Button(frLogout, image=img, text="Home", command=lambda: mostrar(frHome))
btn9.config(height=25, width=25)
btn9.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn9.place(x=210, y=289)

# ========================================== #

root.mainloop()

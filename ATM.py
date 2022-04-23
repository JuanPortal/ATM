from tkinter import *
import sqlite3

# Setting up the interface
root = Tk()
root.title("ATM")
root.iconbitmap("img/logo.ico")
root.geometry("450x350")
root.resizable(0, 0)

# Creating the frames
frLogin = Frame(root)
frHome = Frame(root)
frBalance = Frame(root)
frTransactions = Frame(root)
frWithdrawal = Frame(root)
frDeposit = Frame(root)
frTransfer = Frame(root)
frPayment = Frame(root)
frChangePassword = Frame(root)
frLogout = Frame(root)

for fr in (frLogin, frHome, frBalance, frTransactions, frWithdrawal, frDeposit, frTransfer, frPayment,
           frChangePassword, frLogout):
    fr.config(width=450, height=350)
    fr.grid(row=0, column=0, sticky="nsew")

# Initializing some variables and labels we'll use later
withdrawal_amount = IntVar()
withdrawal_amount.set("")
deposit_amount = IntVar()
deposit_amount.set("")
transfer_amount = IntVar()
transfer_amount.set("")
payment_amount = IntVar()
payment_amount.set("")
account_number = StringVar()
account_number.set("")
payment_code = StringVar()
payment_code.set("")
password = StringVar()
password.set("")
new_password = StringVar()
new_password.set("")
confirm_password = StringVar()
confirm_password.set("")

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


# This function will show us the selected frame
def show(frame):
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
    global password
    global new_password
    global confirm_password
    global payment_amount
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
    password.set("")
    new_password.set("")
    confirm_password.set("")
    payment_amount.set("")
    frame.tkraise()


show(frLogin)  # SHOW LOGIN!!!!

# Establishing the connection to the database
myconnection = sqlite3.connect("ATM")
mycursor = myconnection.cursor()
mycursor.execute("SELECT DISTINCT * FROM Users")
database = mycursor.fetchall()
print(f"Users: {database}")

codes = [code[0] for code in database]
balances = [balance[1] for balance in database]
passwords = [password[2] for password in database]

myconnection.close()

# Using indexes to select the users
index = 0
index2 = 0


# ================ Login Function ================ #

def login(input_code, input_password):
    account_number.set("")
    password.set("")
    global label10
    label10.destroy()
    global index

    if input_code in codes:
        index = codes.index(input_code)
        print(f"Current user: {database[index]}")
        if input_password == passwords[index]:
            show(frHome)

        else:
            label10 = Label(frLogin, text="Incorrect password", fg="red")
            label10.grid(row=1, column=0, padx=10, pady=10)
            label10.place(x=167, y=249)

    else:
        label10 = Label(frLogin, text="Incorrect user", fg="red")
        label10.grid(row=1, column=0, padx=10, pady=10)
        label10.place(x=177, y=249)


# ============== Balance Function ============== #

def show_balance():
    show(frBalance)
    global label22
    label22.destroy()

    label22 = Label(frBalance, text=f"Current balance: {balances[index]}", fg="green")
    label22.grid(row=1, column=0, padx=10, pady=10)
    label22.place(x=168, y=63.85)


# ============ Transactions Function =========== #

def show_transactions():
    show(frTransactions)

    connection = sqlite3.connect("ATM")
    cursor = connection.cursor()
    cursor.execute(f"SELECT Transactions FROM Transactions WHERE Code = '{codes[index]}'")
    transactions_database = cursor.fetchall()
    connection.close()
    transactions_list = []
    for transaction in transactions_database:
        transactions_list.insert(0, transaction[0])
    new_transaction = "\n".join(transactions_list)

    every_transaction = Text(frTransactions, width=35, height=10)
    every_transaction.grid(row=1, column=0, padx=10, pady=10)
    every_transaction.insert(END, new_transaction)
    every_transaction.place(x=83, y=86)


# ============= Withdrawal Function ============= #

def withdrawal(amount):
    withdrawal_amount.set("")
    global label11
    global label12
    label11.destroy()
    label12.destroy()
    connection = sqlite3.connect("ATM")
    cursor = connection.cursor()

    if amount <= balances[index]:
        balances[index] -= amount
        cursor.execute(f"UPDATE Users SET Balance = {balances[index]} WHERE Code = '{codes[index]}'")
        connection.commit()
        label11 = Label(frWithdrawal, text="Successfully withdrawn", fg="green")
        label11.grid(row=1, column=0, padx=10, pady=10)
        label11.place(x=165, y=133)

        label12 = Label(frWithdrawal, text=f"Current balance: {balances[index]}")
        label12.grid(row=2, column=0, padx=10, pady=10)
        label12.place(x=168, y=176)

        cursor.execute(f"INSERT INTO Transactions VALUES('{codes[index]}', 'Withdrawal\t\t\t     -{amount}')")
        connection.commit()
        connection.close()

    else:
        label11 = Label(frWithdrawal, text="Insufficient funds", fg="red")
        label11.grid(row=1, column=0, padx=10, pady=10)
        label11.place(x=179, y=133)


# ============ Depósito Function ============ #

def deposit(amount):
    deposit_amount.set("")
    global label13
    global label14
    label13.destroy()
    label14.destroy()
    connection = sqlite3.connect("ATM")
    cursor = connection.cursor()

    if amount <= 5000:
        balances[index] += amount
        cursor.execute(f"UPDATE Users SET Balance = {balances[index]} WHERE Code = '{codes[index]}'")
        connection.commit()
        label13 = Label(frDeposit, text="Deposit submitted", fg="green")
        label13.grid(row=1, column=0, padx=10, pady=10)
        label13.place(x=177, y=133)

        label14 = Label(frDeposit, text=f"Current balance: {balances[index]}")
        label14.grid(row=2, column=0, padx=10, pady=10)
        label14.place(x=168, y=176)

        cursor.execute(f"INSERT INTO Transactions VALUES('{codes[index]}', 'Deposit\t\t\t     -{amount}')")
        connection.commit()
        connection.close()

    else:
        label13 = Label(frDeposit, text="The amount exceeds the deposit limit", fg="red")
        label13.grid(row=1, column=0, padx=10, pady=10)
        label13.place(x=126, y=133)


# ========== Transfer Function ========== #

def transfer(amount, receiving_account):
    transfer_amount.set("")
    account_number.set("")
    global index2
    global label15
    global label16
    label15.destroy()
    label16.destroy()
    connection = sqlite3.connect("ATM")
    cursor = connection.cursor()

    if receiving_account in codes and amount <= balances[index]:
        index2 = codes.index(receiving_account)
        balances[index] -= amount
        cursor.execute(f"UPDATE Users SET Balance = {balances[index]} WHERE Code = '{codes[index]}'")
        connection.commit()
        balances[index2] += amount
        cursor.execute(f"UPDATE Users SET Balance = {balances[index2]} WHERE Code = '{codes[index2]}'")
        connection.commit()
        label15 = Label(frTransfer, text="Transfer successful", fg="green")
        label15.grid(row=1, column=0, padx=10, pady=10)
        label15.place(x=175, y=152)

        label16 = Label(frTransfer, text=f"Current balance: {balances[index]}")
        label16.grid(row=2, column=0, padx=10, pady=10)
        label16.place(x=168, y=192)

        cursor.execute(f"INSERT INTO Transactions VALUES('{codes[index]}', 'Transfer\t\t\t     -{amount}')")
        cursor.execute(f"INSERT INTO Transactions VALUES('{codes[index2]}', 'Transfer\t\t\t     +{amount}')")
        connection.commit()
        connection.close()

    else:
        label15 = Label(frTransfer, text="Try again", fg="red")
        label15.grid(row=1, column=0, padx=10, pady=10)
        label15.place(x=201, y=162)


# ============= Payment Function ============= #

def pay(amount, code_to_pay):
    payment_amount.set("")
    payment_code.set("")
    global label17
    global label18
    label17.destroy()
    label18.destroy()
    connection = sqlite3.connect("ATM")
    cursor = connection.cursor()

    if len(code_to_pay) == 6 and amount <= balances[index]:
        balances[index] -= amount
        cursor.execute(f"UPDATE Users SET Balance = {balances[index]} WHERE Code = '{codes[index]}'")
        connection.commit()
        label17 = Label(frPayment, text="Payment successful", fg="green")
        label17.grid(row=1, column=0, padx=10, pady=10)
        label17.place(x=172, y=150)

        label18 = Label(frPayment, text=f"Current balance: {balances[index]}")
        label18.grid(row=2, column=0, padx=10, pady=10)
        label18.place(x=168, y=195)

        cursor.execute(f"INSERT INTO Transactions VALUES('{codes[index]}', 'Payment\t\t\t     -{amount}')")
        connection.commit()
        connection.close()

    else:
        label17 = Label(frPayment, text="Try again", fg="red")
        label17.grid(row=1, column=0, padx=10, pady=10)
        label17.place(x=201, y=160)


# =========== Change Password Function =========== #

def change_password(current, new, confirm):
    global label31
    global label32
    global password
    global new_password
    global confirm_password
    label31.destroy()
    label32.destroy()
    password.set("")
    new_password.set("")
    confirm_password.set("")
    connection = sqlite3.connect("ATM")
    cursor = connection.cursor()

    if current == passwords[index]:
        if len(new) > 0 and new == confirm:
            passwords.pop(index)
            passwords.insert(index, new)
            cursor.execute(f"UPDATE Users SET Password = '{passwords[index]}' WHERE Code \
            = '{codes[index]}'")
            connection.commit()
            label31 = Label(frChangePassword, text="Password updated!", fg="green")
            label31.grid(row=1, column=0, padx=10, pady=10)
            label31.place(x=176, y=188)
        else:
            label32 = Label(frChangePassword, text="Passwords do not match", fg="red")
            label32.grid(row=1, column=0, padx=10, pady=10)
            label32.place(x=161, y=188)

    else:
        label31 = Label(frChangePassword, text="Incorrect password", fg="red")
        label31.grid(row=1, column=0, padx=10, pady=10)
        label31.place(x=175, y=188)


# ================== Login Frame ================== #

gnb_img = PhotoImage(file="img/GNB.png")
label19 = Label(frLogin, image=gnb_img)
label19.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label19.place(x=125, y=35)

label8 = Label(frLogin, text="User")
label8.grid(row=1, column=0, padx=10, pady=10)
label8.place(x=158, y=151)

input7 = Entry(frLogin, textvariable=account_number)
input7.grid(row=1, column=1, padx=10, pady=10)
input7.config(justify="center")
input7.place(x=205, y=153)

label9 = Label(frLogin, text="Password")
label9.grid(row=2, column=0, padx=10, pady=10)
label9.place(x=131, y=191)

input6 = Entry(frLogin, textvariable=password)
input6.grid(row=2, column=1, padx=10, pady=10)
input6.config(justify="center", show="*")
input6.place(x=205, y=193)

btnF5 = Button(frLogin, text="Log in", command=lambda: login(account_number.get(), password.get()))
# btnF5.bind("<Return>", lambda: login(account_number.get(), password.get()))
btnF5.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
btnF5.place(x=202, y=291)

# ================== Home Frame ================== #

label1 = Label(frHome, text="What would you like to do?", fg="blue")
label1.grid(row=0, column=0, padx=10, pady=20, columnspan=4)
label1.place(x=153, y=39)

opt1 = Button(frHome, text="Balance", command=lambda: show_balance())
opt1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
opt1.place(x=10, y=90)

opt2 = Button(frHome, text="Transactions", command=lambda: show_transactions())
opt2.grid(row=1, column=1, padx=10, pady=10, sticky="e")
opt2.place(x=363, y=90)

opt3 = Button(frHome, text="Withdraw", command=lambda: show(frWithdrawal))
opt3.grid(row=2, column=0, padx=10, pady=10, sticky="w")
opt3.place(x=10, y=155)

opt4 = Button(frHome, text="Deposit", command=lambda: show(frDeposit))
opt4.grid(row=2, column=1, padx=10, pady=10, sticky="e")
opt4.place(x=389, y=155)

opt5 = Button(frHome, text="Transfer", command=lambda: show(frTransfer))
opt5.grid(row=3, column=0, padx=10, pady=10)
opt5.place(x=10, y=220)

opt6 = Button(frHome, text="Payment", command=lambda: show(frPayment))
opt6.grid(row=3, column=1, padx=10, pady=10)
opt6.place(x=382, y=220)

opt7 = Button(frHome, text="Change password", command=lambda: show(frChangePassword))
opt7.grid(row=3, column=1, padx=10, pady=10)
opt7.place(x=10, y=285)

opt8 = Button(frHome, text="Log out", command=lambda: show(frLogin))
opt8.grid(row=3, column=1, padx=10, pady=10)
opt8.place(x=388, y=285)

# ================= Balance Frame ================= #

home_btn_img = PhotoImage(file="img/home_btn.png")
btn6 = Button(frBalance, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn6.config(height=25, width=25)
btn6.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn6.place(x=210, y=289)

# =============== Transactions Frame =============== #

label23 = Label(frTransactions, text="Latest transactions", fg="blue")
label23.grid(row=0, column=0, padx=10, pady=10)
label23.place(x=168, y=37)

btn7 = Button(frTransactions, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn7.config(height=25, width=25)
btn7.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn7.place(x=210, y=289)

# ================= Withdrawal Frame ================= #

label2 = Label(frWithdrawal, text="Enter the amount to withdraw", fg="blue")
label2.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label2.place(x=146, y=34)

input1 = Entry(frWithdrawal, textvariable=withdrawal_amount)
input1.grid(row=1, column=1, padx=10, pady=10)
input1.config(justify="center")
input1.place(x=163, y=80)

btnF1 = Button(frWithdrawal, text="Withdraw", command=lambda: withdrawal(withdrawal_amount.get()))
btnF1.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
btnF1.place(x=194, y=219)

btn1 = Button(frWithdrawal, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn1.config(height=25, width=25)
btn1.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn1.place(x=210, y=285)

# ================ Deposit Frame ================ #

label3 = Label(frDeposit, text="Enter the amount to deposit", fg="blue")
label3.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label3.place(x=151, y=34)

input2 = Entry(frDeposit, textvariable=deposit_amount)
input2.grid(row=1, column=1, padx=10, pady=10)
input2.config(justify="center")
input2.place(x=163, y=80)

btnF2 = Button(frDeposit, text="Deposit", command=lambda: deposit(deposit_amount.get()))
btnF2.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
btnF2.place(x=199, y=219)

btn2 = Button(frDeposit, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn2.config(height=25, width=25)
btn2.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn2.place(x=210, y=285)

# ============== Transfer Frame ============== #

label4 = Label(frTransfer, text="Enter the amount to transfer and the receiving account number", fg="blue")
label4.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label4.place(x=58, y=25)

label5 = Label(frTransfer, text="Amount")
label5.grid(row=1, column=0, padx=10, pady=10)
label5.place(x=152, y=69)

input3 = Entry(frTransfer, textvariable=transfer_amount)
input3.grid(row=1, column=1, padx=10, pady=10)
input3.config(justify="center")
input3.place(x=222, y=72)

label6 = Label(frTransfer, text="Account number")
label6.grid(row=2, column=0, padx=10, pady=10)
label6.place(x=105, y=109)

input4 = Entry(frTransfer, textvariable=account_number)
input4.grid(row=2, column=1, padx=10, pady=10)
input4.config(justify="center")
input4.place(x=222, y=112)

btnF3 = Button(frTransfer, text="Transfer", command=lambda: transfer(transfer_amount.get(), account_number.get()))
btnF3.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
btnF3.place(x=198, y=233)

btn4 = Button(frTransfer, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn4.config(height=25, width=25)
btn4.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn4.place(x=210, y=290)

# ============= Payment Frame ============= #

label26 = Label(frPayment, text="Enter the amount to pay and the payment code", fg="blue")
label26.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
label26.place(x=100, y=28)

label27 = Label(frPayment, text="Amount")
label27.grid(row=1, column=0, padx=10, pady=10)
label27.place(x=144, y=66)

input8 = Entry(frPayment, textvariable=payment_amount)
input8.grid(row=1, column=1, padx=10, pady=10)
input8.config(justify="center")
input8.place(x=215, y=68)

label7 = Label(frPayment, text="Payment code")
label7.grid(row=2, column=0, padx=10, pady=10)
label7.place(x=112, y=106)

input5 = Entry(frPayment, textvariable=payment_code)
input5.grid(row=2, column=1, padx=10, pady=10)
input5.config(justify="center")
input5.place(x=215, y=108)

btnF4 = Button(frPayment, text="Pay", command=lambda: pay(payment_amount.get(), payment_code.get()))
btnF4.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
btnF4.place(x=211, y=237)

btn5 = Button(frPayment, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn5.config(height=25, width=25)
btn5.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn5.place(x=210, y=291)

# ============== Change Password Frame ============== #

label24 = Label(frChangePassword, text="Change password", fg="blue")
label24.grid(row=0, column=0, padx=10, pady=10)
label24.place(x=178, y=20)

label28 = Label(frChangePassword, text="Current password")
label28.grid(row=2, column=0, padx=10, pady=10)
label28.place(x=101, y=65)

input9 = Entry(frChangePassword, textvariable=password)
input9.grid(row=2, column=1, padx=10, pady=10)
input9.config(justify="center", show="*")
input9.place(x=222, y=67)

label29 = Label(frChangePassword, text="New password")
label29.grid(row=2, column=0, padx=10, pady=10)
label29.place(x=117, y=105)

input10 = Entry(frChangePassword, textvariable=new_password)
input10.grid(row=2, column=1, padx=10, pady=10)
input10.config(justify="center", show="*")
input10.place(x=222, y=107)

label30 = Label(frChangePassword, text="New password")
label30.grid(row=2, column=0, padx=10, pady=10)
label30.place(x=117, y=145)

input11 = Entry(frChangePassword, textvariable=confirm_password)
input11.grid(row=2, column=1, padx=10, pady=10)
input11.config(justify="center", show="*")
input11.place(x=222, y=147)

btnF6 = Button(frChangePassword, text="Update", command=lambda: change_password(password.get(), new_password.get(),
                                                                                confirm_password.get()))
btnF6.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
btnF6.place(x=202, y=229)

btn8 = Button(frChangePassword, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn8.config(height=25, width=25)
btn8.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn8.place(x=210, y=289)

# ================= Logout Frame ================= #

label25 = Label(frLogout, text="Logout")
label25.grid(row=0, column=0, padx=10, pady=10)
label25.place(x=140, y=23.85)

btn9 = Button(frLogout, image=home_btn_img, text="Home", command=lambda: show(frHome))
btn9.config(height=25, width=25)
btn9.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
btn9.place(x=210, y=289)

# =============================================== #

root.mainloop()

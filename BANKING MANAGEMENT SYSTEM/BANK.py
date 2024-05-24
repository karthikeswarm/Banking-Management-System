import sqlite3
from time import sleep
import datetime as dt

class Bank:
    def __init__(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect("banking_system.db")
        self.cur = self.conn.cursor()
        self.create_tables()
        self.show_menu()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                Account_No INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Gender TEXT,
                DOB DATE,
                Age INTEGER,
                Mobile_No INTEGER,
                Balance INTEGER,
                Pin INTEGER
            )
        ''')



        self.conn.commit()

    def show_menu(self):
        print("Main Menu")
        print("1. Withdrawal")
        print("2. Deposit")
        print("3. Balance Status")
        print("4. Open New Account")
        print("5. See Details")
        print("6. Update Details")
        print("7. Exit")

        while True:
            ch = int(input("Enter your choice = "))

            if ch == 1:
                self.withdrawal()
            elif ch == 2:
                self.deposit()
            elif ch == 3:
                self.bal_status()
            elif ch == 4:
                self.new_account()
            elif ch == 5:
                self.see_details()
            elif ch == 6:
                self.update_details()
            elif ch == 7:
                print("Thanks for using our service. Do come again.")
                self.cur.close()
                self.conn.close()
                sleep(1)
                exit()
            else:
                print("Please check your input...")

    def withdrawal(self):
        accNo = int(input("Enter your Account no = "))
        pin = int(input("Enter your pin no = "))

        query = f"SELECT Balance, Pin FROM Accounts WHERE Account_No = {accNo}"
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data:
            accBal, accPin = data
            if accPin == pin:
                amount = int(input("Enter amount to withdraw = "))
                if amount <= accBal:
                    accBal -= amount
                    query = f"UPDATE Accounts SET Balance = {accBal} WHERE Account_No = {accNo}"
                    self.cur.execute(query)
                    self.conn.commit()
                    print(f"Withdrawal successful. Remaining balance = {accBal}")
                else:
                    print("Insufficient balance.")
            else:
                print("Incorrect PIN.")
        else:
            print("Account not found.")

    def deposit(self):
        accNo = int(input("Enter your Account no = "))
        pin = int(input("Enter your pin no = "))

        query = f"SELECT Balance, Pin FROM Accounts WHERE Account_No = {accNo}"
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data:
            accBal, accPin = data
            if accPin == pin:
                amount = int(input("Enter amount to deposit = "))
                accBal += amount
                query = f"UPDATE Accounts SET Balance = {accBal} WHERE Account_No = {accNo}"
                self.cur.execute(query)
                self.conn.commit()
                print(f"Deposit successful. Updated balance = {accBal}")
            else:
                print("Incorrect PIN.")
        else:
            print("Account not found.")

    def bal_status(self):
        accNo = int(input("Enter your Account no = "))

        query = f"SELECT Balance FROM Accounts WHERE Account_No = {accNo}"
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data:
            accBal = data[0]
            print(f"Balance in your account = {accBal}")
        else:
            print("Account not found.")

    def new_account(self):
        name = input("Enter your name = ")
        gender = input("Enter your gender = ")
        y, m, d = input("Enter your dob (yyyy-mm-dd) = ").split("-")
        dob = dt.date(int(y), int(m), int(d))
        age = int(input("Enter your age = "))
        mob = int(input("Enter your mobile no = "))
        bal = int(input("Deposit your initial amount = "))
        pin = int(input("Please select any 4 digit numeric pin for your account = "))

        query = f'''
            INSERT INTO Accounts (Name, Gender, DOB, Age, Mobile_No, Balance, Pin)
            VALUES ('{name}', '{gender}', '{dob}', {age}, {mob}, {bal}, {pin})
        '''
        self.cur.execute(query)
        self.conn.commit()
        print("Congratulations! Your account is successfully created.")

    def see_details(self):
        accNo = int(input("Enter your Account no = "))

        query = f"SELECT * FROM Accounts WHERE Account_No = {accNo}"
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data:
            print("Your Details are as Follows\n")
            print("Account_No =", data[0])
            print("Name =", data[1])
            print("Gender =", data[2])
            print("DOB =", data[3])
            print("Age =", data[4])
            print("Mobile_No =", data[5])
            print("Balance =", data[6])
            print("Pin =", data[7])
        else:
            print("Account not found.")

    def update_details(self):
        accNo = int(input("Enter your Account no = "))
        pin = int(input("Enter your pin no = "))

        query = f"SELECT * FROM Accounts WHERE Account_No = {accNo}"
        self.cur.execute(query)
        data = self.cur.fetchone()

        if data:
            accBal, accPin = data[6], data[7]
            if accPin == pin:
                print("Your Details are as Follows\n")
                print("Account_No =", data[0])
                print("Name =", data[1])
                print("Gender =", data[2])
                print("DOB =", data[3])
                print("Age =", data[4])
                print("Mobile_No =", data[5])
                print("Balance =", data[6])
                print("Pin =", data[7])

                field = input("\nEnter name of the field you would like to update = ")
                if field in ['Name', 'Gender', 'DOB', 'Age', 'Mobile_No']:
                    value = input(f"Enter new value for {field} = ")
                elif field == 'Balance':
                    value = int(input("Enter new value for Balance = "))
                else:
                    print("Invalid field name.")
                    return

                query = f"UPDATE Accounts SET {field} = {value} WHERE Account_No = {accNo}"
                self.cur.execute(query)
                self.conn.commit()
                print("Record Successfully Updated.")
            else:
                print("Incorrect PIN.")
        else:
            print("Account not found.")

if __name__ == "__main__":
    a = Bank()

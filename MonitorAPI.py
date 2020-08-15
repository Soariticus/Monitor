import time
import sqlite3 as sql
import os
from inspect import currentframe, getframeinfo
import xlwt
import xlrd
from datetime import datetime
import asyncio
from xlutils.copy import copy as xl_copy
from datetime import date

path = os.path.dirname(os.path.realpath(__file__))

conn = sql.connect(path + '/databases/data.db')
c = conn.cursor()

conn2 = sql.connect(path + '/databases/store.db')
c2 = conn2.cursor()

timeReq = 900

try:  # In the case the database ever needs to be fully wiped, this will set it up again.
    c.execute("CREATE TABLE users (userID int, name text, oldTime int, hour integer, messages integer)")
    print("Database (HOURLY) was wiped, setting up database.")
    #c.execute(f"INSERT INTO users VALUES (1, 5, 'soar', 0)")
except sql.OperationalError as e:
    print("Database (HOURLY) is set, no errors.")

try:
    c2.execute("CREATE TABLE users (userID int, name text, time int, messages int)")
    print("Database (LONG TERM) was wiped, setting up database.")
except sql.OperationalError as e:
    print("Database (LONG TERM) is set, no errors.")


class monitor:
    global conn, c, self
    # Format: id (INT), oldTime (INT), name (TEXT), messages (INT)

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    def read(self, uid, choice):
        output = None
        if choice == 1:
            c.execute(f"SELECT * FROM users WHERE userID = ?", (uid,))
            output = c.fetchone()
        elif choice == 2:
            c2.execute = c.execute(f"SELECT * FROM users WHERE userID = ?", (uid,))
            output = c2.fetchone()
        return output

    def getHour(self):
        curHour = round(time.time()) % 3600
        secLeft = 3600 - curHour
        minLeft = secLeft / 60
        output = [f"Minutes left until next hour = {round(minLeft)}", secLeft]
        return output

    async def timer(self, sec):
        print("!!!!!!!!!!!!!!!!")
        print(f"waiting {sec}s once")
        print("!!!!!!!!!!!!!!!!")
        await asyncio.sleep(sec)
        self.excWrite(self)
        c.execute(f"UPDATE users SET messages = 0")

    async def timerInf(self):
        while True:
            print("!!!!!!!!!!!!!!!!")
            print("Calling addStoreDb() and waiting 3600s")
            print("!!!!!!!!!!!!!!!!")
            await asyncio.sleep(3600)
            c.execute(f"UPDATE users SET messages = 0")
            self.excWrite(self)

    def checkUser(self, uid, name):
        try:
            testID = self.read(self, uid, 1)
            if testID:
                self.checkCooldown(self, uid)
            else:
                print(f"Couldn't find user {name}, creating new profile.")
                self.newUser(self, uid, name)
        except sql.OperationalError as e:
            frameinfo = getframeinfo(currentframe())
            exit(f"Error: {e} | {frameinfo.filename} | line: {frameinfo.lineno} ")

    def checkCooldown(self, uid):
        curTime = round(int(time.time()))
        userS = self.read(id, uid, 1)
        if (curTime - timeReq) > userS[2]:
            messages = int(userS[4]) + 1
            c.execute(f"UPDATE users SET oldTime = {curTime}, messages = {messages} WHERE userID = {uid}")
            conn.commit()
            timePassed = curTime - userS[2]
            db = self.read(id, uid, 1)
            print(f"Enough time has passed: {timePassed}s/{timeReq}s")
            print(f"messages = {db[4]}")
            print("____________________________________________")
        else:
            timePassed = curTime - userS[2]
            print(f"Not enough time has passed: {timePassed}s/{timeReq}s")
            print("____________________________________________")

    def newUser(self, uid, name):
        curTime = int(round(time.time()))
        values = (uid, name, curTime, date.today(), 1)
        c.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", values)
        conn.commit()
        print(f"New user created with credentials: {uid} : {curTime}")
        print("____________________________________________")

    def getChoice(self):
        choice = input("Would you like to [c]heck a user, create a [n]ew user or [r]ead a user? ").lower()

        if choice == "c":
            test = int(input("What is the ID of the person you'd like to check? "))
            monitor.checkUser(self, test)
            print(f'called checkuser on user: {test}')

        elif choice == "n":
            userID = int(input("What is the ID of the person you'd like to create? "))
            monitor.newUser(self, userID)

        elif choice == "r":
            test = int(input("What is the ID of the person you'd like to read? "))
            thing = monitor.read(self, test, 1)
            print("user |{test}| returned: {thing}")

    def getAllUsers(self, choice):
        output = None
        if choice == 1:
            c.execute(f"SELECT * FROM users")
            output = c.fetchall()
        elif choice == 2:
            c2.execute(f"SELECT * FROM users")
            output = c2.fetchall()
        return output

    def parseTime(self):
        now = datetime.utcnow()
        if len(str(now.hour)) < 2:
            hour = "0" + str(now.hour)
        else:
            hour = now.hour
        if len(str(now.minute)) < 2:
            minute = "0" + str(now.minute)
        else:
            minute = now.minute
        if len(str(now.second)) < 2:
            second = "0" + str(now.second)
        else:
            second = now.second
        return f"{hour}:{minute}:{second} [UTC]"

    def excWrite(self):
        items = self.getAllUsers(self, 1)

        hour = round(round(time.time()) / (60 * 60))
        hour = hour % 24

        oldSheet = xlrd.open_workbook('output.xls', formatting_info=True)
        book = xl_copy(oldSheet)

        sheet = book.add_sheet(f"Hour {hour}")
        num = 1

        while(num < 96):
            if num % 4 == 0:
                sheet.write(0, num, "Time (IN UTC)")
                sheet.write(0, (num + 1), "Name")
                sheet.write(0, (num + 2), "Messages")
                num += 1
            else:
                num += 1

        for x in items:
            if num == 1:
                sheet.write(num, 0, self.parseTime(self))
            sheet.write(num, hour, x[1])
            sheet.write(num, (hour + 1), x[4])
            num += 1
        book.save("output.xls")
        if hour % 24 == 0:
            asyncio.sleep(5)
            oldSheet = xlrd.open_workbook('output.xls', formatting_info=True)
            book = xl_copy(oldSheet)
            thing = datetime.utcnow()
            day = (f"{thing.day}-{thing.month}-{thing.year}")

            sheet = book.add_sheet(f"Day {day}")
            sheet.write(0, 0, f"{day}")
            book.save("output.xls")

    async def startTimer(self):
        time = [0, 2]  # self.getHour(self)
        await self.timer(self, time[1])
        print("Starting infinite timer")
        await self.timerInf(self)

    def addStoreDb(self):
        items = self.getAllUsers(self, 1)
        num = 0
        for x in items:
            values = (x[0], x[1], round(time.time()), x[4])
            c2.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", values)
            num += 1
        conn2.commit()

monitor.parseTime(self=monitor)
# monitor.getChoice(self=monitor)
# monitor.excWrite(self=monitor)

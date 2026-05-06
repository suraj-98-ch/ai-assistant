import csv
import sqlite3

con = sqlite3.connect("jarvis.db")

cursor = con.cursor()

query = """CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, path TEXT)"""
cursor.execute(query)

#query = "INSERT INTO sys_command (name,path) VALUES ('microsoft office','C:\\Program Files\\Microsoft Office\\root\\Office16\\MICROSOFT OFFICE.exe')"
#cursor.execute(query)
#con.commit()

#query = """CREATE TABLE IF NOT EXISTS web_command( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, url TEXT)"""
#cursor.execute(query)

#query = "INSERT INTO web_command (name,url) VALUES ('youtube','https://www.youtube.com/')"
#cursor.execute(query)
#con.commit()

#create a table with the desired columns 
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, mobile_no TEXT, email TEXT )''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns

#desired_columns_indices = [0, 18]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    #csvreader = csv.reader(csvfile)
    #for row in csvreader:
        #selected_data = [row[i] for i in desired_columns_indices]
        #cursor.execute(''' INSERT INTO contacts (id, name, mobile_no) VALUES(null,?,?)''', tuple(selected_data))

# Commit changes and close connection
#con.commit()
#con.close()
#query = 'chetan'
#query = query.strip().lower()

#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])

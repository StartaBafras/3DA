import sqlite3
def create():
    con=sqlite3.connect("printer.db")
    cur=con.cursor()
    cur.execute("create table if not exists orders('name','file','owner','amount')")
    cur.execute("insert into orders values(?,?,?,?)",('İsim','Dosya','Alıcı','Miktar'))
    con.commit()
    con.close()
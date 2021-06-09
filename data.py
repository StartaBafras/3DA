import sqlite3
def create():
    con=sqlite3.connect("printer.db")
    cur=con.cursor()

    cur.execute("create table if not exists orders('name','file','owner','amount','date','cost','time')")
    cur.execute("insert into orders values(?,?,?,?,?,?,?)",('İsim','Dosya','Alıcı','Miktar','Tarih','Maliyet','Basım Süresi'))

    cur.execute("create table if not exists stock('name','file','owner','amount','date','cost','time')")
    cur.execute("insert into stock values(?,?,?,?,?,?,?)",('İsim','Dosya','Alıcı','Miktar','Tarih','Maliyet','Basım Süresi'))

    cur.execute("create table if not exists costs('name','file','filament','f_amount','electirc','time','cost','date')")
    cur.execute("insert into costs values(?,?,?,?,?,?,?,?)",('İsim','Dosya','Filament Fiyatı (₺)','Filament Miktarı (gr)','Elektirik Sarfiyatı (₺)','Basım Süresi (dk)','Toplam Maliyet(₺)','Tarih'))
    con.commit()
    con.close()
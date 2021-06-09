from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem
import sqlite3
from PyQt5.QtCore import QDate,QDateTime
import sys
import data

#Hizmetler:
#    Sipariş Listesi +
#    Satış Listesi -
#    Stok: 
#    + Sipariş listesinden doğrudan aktarma
#    + Maliyeti veritabanından çekmek
#    Maliyet hesaplayıcı ve kayıtlı maliyetler
#    Kasa -
#    import edilen paketler ayıklanmalı
#    veritabanı kodları sadeleştirilmeli
#    lambda kullanımı kayıt butonlarında sadeleştirme yapabilir mi denenmeli
#    ön tanımlı filament parası ve elektirik fiyatı eklenmeli


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_menu()
        self.setMinimumSize(900,500)
        self.open=Window()
        self.setCentralWidget(self.open)
        self.show()

    def create_menu(self):
        menubar = self.menuBar()
        #Sipariş kısmı
        order = menubar.addMenu("Siparişler")#Üst menü 

        add_order = QAction("Sipariş Ekle",self)#alt menüler oluşturuldu
        see_order = QAction("Siparişleri Gör",self)

        order.addAction(add_order)#Atamalar yapıldı
        order.addAction(see_order)

        #Stok kısmı
        stock_and_cost = menubar.addMenu("Stok")

        add_stock = QAction("Stok Gir",self)
        see_stock = QAction("Stok Görüntüle",self)

        stock_and_cost.addAction(add_stock)
        stock_and_cost.addAction(see_stock)

        #Maliyet kısmı
        costs = menubar.addMenu("Maliyet")

        calculate_cost = QAction("Maliyet Hesapla",self)
        see_cost = QAction("Kayıtlı Maliyetleri Görüntüle",self)

        costs.addAction(calculate_cost)
        costs.addAction(see_cost)

        #veritabanı kısmı
        database = menubar.addMenu("Veritabanı")

        create_db = QAction("Veritabanı Oluştur",self)

        database.addAction(create_db)



        order.triggered.connect(self.response)
        stock_and_cost.triggered.connect(self.response)
        costs.triggered.connect(self.response)
        database.triggered.connect(self.response)

    def response(self,action):
        if action.text() == "Sipariş Ekle":
            yazi = action.text()
            self.open.new_tab(add_order(),yazi)
        elif action.text() == "Siparişleri Gör":
            yazi = action.text() 
            self.open.new_tab(see_order(),yazi)
        elif action.text() == "Stok Gir":
            yazi = action.text()
            self.open.new_tab(add_stock(),yazi)
        elif action.text() == "Stok Görüntüle":
            yazi = action.text()
            self.open.new_tab(see_stock(),yazi)
        elif action.text() == "Maliyet Hesapla":
            yazi = action.text()
            self.open.new_tab(calculate_cost(),yazi)
        elif action.text() == "Kayıtlı Maliyetleri Görüntüle":
            yazi = action.text()
            self.open.new_tab(see_cost(),yazi)
        elif action.text() == "Veritabanı Oluştur":
            data.create()
            QMessageBox.about(self,"Veritabanı Oluşturuldu","Yeni veritabanı oluşturuldu. Eğer veritabanını yeniden kurmak için bu seçeneği kullandıyasnız lütfen eski veritabanını silip tekrar deneyin.")

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tabwidget=QTabWidget()
        self.tabwidget.addTab(add_order(),"Sipariş Ekle")
        self.tabwidget.setTabsClosable(True)
        h_box=QHBoxLayout()
        h_box.addWidget(self.tabwidget)
        self.setLayout(h_box)
        self.tabwidget.tabCloseRequested.connect(self.close_function)
        self.show()

    def close_function(self,index):
        self.tabwidget.removeTab(index)
    def new_tab(self,w_name,yazi):
        self.tabwidget.addTab(w_name,yazi)

class add_order(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()

        self.order_name = QLabel("Sipariş İsmi")
        self.order_name_i = QLineEdit()

        self.order_file = QLabel("Dosya Linki")
        self.order_file_i = QLineEdit()

        self.order_owner = QLabel("Alıcının İsmi")
        self.order_owner_i = QLineEdit()

        self.order_amount = QLabel("Miktar")
        self.order_amount_i = QSpinBox()

        self.order_date=QLabel("Sipariş Tarihi")
        self.order_date_i=QDateTimeEdit(QDateTime.currentDateTime())

        self.save_button = QPushButton("Kayıt Et")
        self.save_button.clicked.connect(self.save)


        f_box.addWidget(self.order_name)
        f_box.addWidget(self.order_name_i)
        f_box.addWidget(self.order_file)
        f_box.addWidget(self.order_file_i)
        f_box.addWidget(self.order_owner)
        f_box.addWidget(self.order_owner_i)
        f_box.addWidget(self.order_amount)
        f_box.addWidget(self.order_amount_i)
        f_box.addWidget(self.order_date)
        f_box.addWidget(self.order_date_i)
        f_box.addWidget(self.save_button)
        

        self.setLayout(f_box)

    def save(self):
        try:

            name = self.order_name_i.text()
            o_file = self.order_file_i.text()
            owner = self.order_owner_i.text()
            amount = self.order_amount_i.text()
            date = self.order_date_i.text()
            #print(name,o_file,owner,amount)


            con=sqlite3.connect("printer.db")
            cursor=con.cursor()
            cursor.execute("SELECT * from costs WHERE file = ?",[o_file])
            data = cursor.fetchall()
            print(data[0][5])#index dışına düşüp düşmeyeceğini kontrol etmek için yazdırıyoruz

            cursor.execute("insert into orders values(?,?,?,?,?,?,?)",(name,o_file,owner,amount,date,data[0][6],data[0][5])) #Hatalı mı ?
            
            con.commit()
            con.close()
            QMessageBox.about(self,"Veritabanı","Kayıt Edildi")
        except IndexError:
            print("h")
            cursor.execute("insert into orders values(?,?,?,?,?,'0','0')",(name,o_file,owner,amount,date))
            con.commit()
            con.close()
            QMessageBox.about(self,"Index Error","Girilen dosya maliyet veritabanındaki herhangi bir dosya ile eşleşmedi bu sebepten maliyet girdileri 0 olarak belirlendi. Lütfen dosyayı maliyet veritabanına kayıt ediniz.")
            
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")

class see_order(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box = QHBoxLayout()

        self.table = QTableWidget()
        #self.table.setRowCount(4)
        self.table.setColumnCount(7)

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_button = QPushButton("Veritabanından Yükle")
        self.load_button.clicked.connect(self.load)

        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete)

        self.transfer_button = QPushButton("Stoklara Aktar")
        self.transfer_button.clicked.connect(self.transfer)

        h_box.addWidget(self.load_button)
        h_box.addWidget(self.transfer_button)
        h_box.addWidget(self.delete_button)


        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)

    def load(self):
        try:
            con = sqlite3.connect("printer.db")
            raw_data = con.execute("SELECT * FROM orders")
            self.table.setRowCount(0)
            for row_number, row_data in enumerate(raw_data):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            con.close()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")

    def delete(self):
        try:
            #a = self.table.currentRow()#factmany ile kullanılabilir veritabanında benzersiz ıd olmalı sanırım
            c = self.table.item(self.table.currentRow(),4).text()
            con = sqlite3.connect("printer.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM orders WHERE date = ?",[c])
            con.commit()
            con.close()
            self.load()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")

    def transfer(self):
        try:
            date = self.table.item(self.table.currentRow(),4).text()
            con = sqlite3.connect("printer.db")
            cursor = con.cursor()
            cursor.execute("SELECT * from orders WHERE date = ?",[date])
            data = cursor.fetchall()
            cursor.execute("insert into stock values(?,?,?,?,?,?,?)",(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5],data[0][6]))
            cursor.execute("DELETE FROM orders WHERE date = ?",[date])
            con.commit()
            con.close()
            self.load()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")


class add_stock(QWidget):
    def __init__(self):
        super().__init__()

        f_box = QFormLayout()
        h_box = QHBoxLayout()

        self.stock_name = QLabel("Sipariş İsmi")
        self.stock_name_i = QLineEdit()

        self.stock_file = QLabel("Dosya Linki")
        self.stock_file_i = QLineEdit()

        self.stock_owner = QLabel("Alıcının İsmi")
        self.stock_owner_i = QLineEdit()

        self.stock_amount = QLabel("Miktar")
        self.stock_amount_i = QSpinBox()

        self.save_button = QPushButton("Kayıt Et")
        self.save_button.clicked.connect(self.save)
        

        f_box.addWidget(self.stock_name)
        f_box.addWidget(self.stock_name_i)
        f_box.addWidget(self.stock_file)
        f_box.addWidget(self.stock_file_i)
        f_box.addWidget(self.stock_owner)
        f_box.addWidget(self.stock_owner_i)
        f_box.addWidget(self.stock_amount)
        f_box.addWidget(self.stock_amount_i)
        
        h_box.addWidget(self.save_button)


        f_box.addItem(h_box)
        self.setLayout(f_box)

    def save(self):
        try:
            name = self.stock_name_i.text()
            o_file = self.stock_file_i.text()
            owner = self.stock_owner_i.text()
            amount = self.stock_amount_i.text()
            self.stock_date_i = QDateTimeEdit(QDateTime.currentDateTime())
            date = self.stock_date_i.text()
            #print(name,o_file,owner,amount)


            con=sqlite3.connect("printer.db")
            cursor=con.cursor()
            cursor.execute("SELECT * from costs WHERE file = ?",[o_file])
            data = cursor.fetchall()
            print(data[0][5])#index dışına düşüp düşmeyeceğini kontrol etmek için yazdırıyoruz

            cursor.execute("insert into stock values(?,?,?,?,?,?,?)",(name,o_file,owner,amount,date,data[0][5],data[0][6]))
                
            con.commit()
            con.close()
            QMessageBox.about(self,"Veritabanı","Kayıt Edildi")
        except IndexError:
            cursor.execute("insert into orders values(?,?,?,?,?,'0','0')",(name,o_file,owner,amount,date))
            con.commit()
            con.close()
            QMessageBox.about(self,"Index Error","Girilen dosya maliyet veritabanındaki herhangi bir dosya ile eşleşmedi bu sebepten maliyet girdileri 0 olarak belirlendi. Lütfen dosyayı maliyet veritabanına kayıt ediniz.")
            
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")

class see_stock(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_button = QPushButton("Veritabanından Yükle")
        self.load_button.clicked.connect(self.load)

        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete)



        h_box.addWidget(self.load_button)
        h_box.addWidget(self.delete_button)


        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)

    def load(self):
        try:
            con = sqlite3.connect("printer.db")
            raw_data = con.execute("SELECT * FROM stock")
            self.table.setRowCount(0)
            for row_number, row_data in enumerate(raw_data):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            con.close()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")

    def delete(self):
        try:
            date = self.table.item(self.table.currentRow(),4).text()
            con = sqlite3.connect("printer.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM orders WHERE date = ?",[date])
            con.commit()
            con.close()
            self.load()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")




class calculate_cost(QWidget):
    def __init__(self):
        super().__init__()

        f_box = QFormLayout()
        h_box = QHBoxLayout()

        self.name = QLabel("İsim")
        self.name_i = QLineEdit()

        self.file = QLabel("Dosya Linki")
        self.file_i = QLineEdit()

        self.stock_filament_cost = QLabel("Filament Maliyeti (gr)")
        self.stock_filament_cost_i = QLineEdit()

        self.stock_electirc_cost = QLabel("Basım Süresi (Dakika)")
        self.stock_electirc_cost_i = QLineEdit()

        self.total_cost = QLabel("Toplam Maliyet (₺)")
        self.total_cost_i = QLineEdit()

        self.calculate_cost = QPushButton("Maliyet Hesapla")
        self.calculate_cost.clicked.connect(self.calculate)

        self.save_cost = QPushButton("Kayıt Et")
        self.save_cost.clicked.connect(self.save)

        f_box.addWidget(self.file)
        f_box.addWidget(self.file_i)
        f_box.addWidget(self.stock_filament_cost)
        f_box.addWidget(self.stock_filament_cost_i)
        f_box.addWidget(self.stock_electirc_cost)
        f_box.addWidget(self.stock_electirc_cost_i)
        f_box.addWidget(self.total_cost)
        f_box.addWidget(self.total_cost_i)

        h_box.addWidget(self.calculate_cost)
        h_box.addWidget(self.save_cost)

        f_box.addItem(h_box)

        self.setLayout(f_box)



    def calculate(self):
        try:
            el_co = self.stock_electirc_cost_i.text()
            fi_co = self.stock_filament_cost_i.text()
            #1 saatlik elektirik 270w'a göre = 0.2125
            #1 kg filament 110₺

            cost = str(((int(el_co)/60)*0.2125) + ((110/1000) * int(fi_co)))

            self.total_cost_i.setText(cost)
        except ValueError:
            QMessageBox.about(self,"Value Error","Filament Maliyeti ve Basım Süresi Boş Bırakılamaz")
    def save(self):
        try:
            self.calculate()
            name = self.name_i.text()
            file_adress = self.file_i.text()
            fi_co = self.stock_filament_cost_i.text()
            el_co = self.stock_electirc_cost_i.text()
            to_co = self.total_cost_i.text()
            el = ((int(el_co)/60)*0.2125)
            fi = ((110/1000) * int(fi_co))
            date = QDateTimeEdit(QDateTime.currentDateTime())
            date = date.text()

            con=sqlite3.connect("printer.db")
            cursor=con.cursor()
            cursor.execute("insert into costs values(?,?,?,?,?,?,?,?)",(name,file_adress,fi,fi_co,el,el_co,to_co,date))  
            con.commit()
            con.close()
            QMessageBox.about(self,"Veritabanı","Kayıt Edildi")
        except ValueError:
            QMessageBox.about(self,"Value Error","Filament Maliyeti ve Basım Süresi Boş Bırakılamaz")
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")



class see_cost(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box = QHBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(8)

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_button = QPushButton("Veritabanından Yükle")
        self.load_button.clicked.connect(self.load)

        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete)



        h_box.addWidget(self.load_button)
        h_box.addWidget(self.delete_button)


        f_box.addWidget(self.table)
        f_box.addItem(h_box)
        self.setLayout(f_box)

    def load(self):
        try:
            con = sqlite3.connect("printer.db")
            raw_data = con.execute("SELECT * FROM costs")
            self.table.setRowCount(0)
            for row_number, row_data in enumerate(raw_data):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
            con.close()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")

    def delete(self):
        try:
            date = self.table.item(self.table.currentRow(),7).text()
            con = sqlite3.connect("printer.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM costs WHERE date = ?",[date])
            con.commit()
            con.close()
            self.load()
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")
        except AttributeError:
            QMessageBox.about(self,"AttributeError","Listeden herhangi bir seçim yapılmadı")



app = QApplication(sys.argv)
pencere = MainWindow()
sys.exit(app.exec_())

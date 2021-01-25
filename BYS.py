from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem
import sqlite3
import sys
import data
#Hizmetler:
#    Sipariş Listesi
#    Satış Listesi
#    Stok
#    Maliyet hesaplayıcı ve kayıtlı maliyetler
#    Kasa

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

        order = menubar.addMenu("Siparişler")#Üst menü 

        add_order = QAction("Sipariş Ekle",self)#alt menüler oluşturuldu
        see_order = QAction("Siparişleri Gör",self)

        order.addAction(add_order)#Atamalar yapıldı
        order.addAction(see_order)


        database = menubar.addMenu("Veritabanı")

        create_db = QAction("Veritabanı Oluştur",self)

        database.addAction(create_db)






        order.triggered.connect(self.response)
        database.triggered.connect(self.response)

    def response(self,action):
        if action.text() == "Sipariş Ekle":
            yazi = action.text()
            self.open.new_tab(add_order(),yazi)
        elif action.text() == "Siparişleri Gör":
            yazi = action.text() 
            self.open.new_tab(see_order(),yazi)
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
        f_box.addWidget(self.save_button)
        

        self.setLayout(f_box)

    def save(self):
        try:

            name = self.order_name_i.text()
            o_file = self.order_file_i.text()
            owner = self.order_owner_i.text()
            amount = self.order_amount_i.text()
            print(name,o_file,owner,amount)
            con=sqlite3.connect("printer.db")
            cursor=con.cursor()
            cursor.execute("insert into orders values(?,?,?,?)",(name,o_file,owner,amount))
            con.commit()
            con.close()
            QMessageBox.about(self,"Veritabanı","Kayıt Edildi")
        except sqlite3.OperationalError:
            QMessageBox.about(self,"sqlite3.OperationalError","Veritabanına bağlanılamadı lütfen yeniden oluşturmayı deneyin veya geliştirici ile iletişime geçin")

class see_order(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()

        self.table = QTableWidget()
        #self.table.setRowCount(4)
        self.table.setColumnCount(4)

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_button = QPushButton("Veritabanından Yükle")
        self.load_button.clicked.connect(self.load)





        f_box.addWidget(self.load_button)
        f_box.addWidget(self.table)

        self.setLayout(f_box)

    def load(self):
        con = sqlite3.connect("printer.db")
        raw_data = con.execute("SELECT * FROM orders")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(raw_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))






app = QApplication(sys.argv)
pencere = MainWindow()
sys.exit(app.exec_())

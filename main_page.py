import sys
import sqlite3
from PyQt5 import QtTest
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from PyQt5.QtWidgets import QApplication,QWidget,QTableWidget,QTableWidgetItem


baglanti = sqlite3.connect('cafe-database.db')
kalem = baglanti.cursor()

baslikFont = QFont('Calibri',34)
baslikFont2 = QFont('Calibri',20)
butonFont = QFont('Calibri',30)
butonFont2 = QFont('Calibri',20)

def ustBolum(mevcutPencere):
    geriButon = QPushButton("<",mevcutPencere)
    geriButon.setFont(baslikFont)
    geriButon.setGeometry(20,20,50,50)
    geriButon.clicked.connect(mevcutPencere.geriDon)

    kapatButon = QPushButton("X",mevcutPencere)
    kapatButon.setFont(baslikFont)
    kapatButon.setGeometry(1300,20,50,50)
    kapatButon.clicked.connect(Pencere.kapat)

class odemeYap(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()

        aciklama = QLabel('Sevgi Kahvesi Ödeme Ekranı: ')
        aciklama2 = QLabel('Ödemenizi öğrenmek için masa numaranızı girin :')
        self.aciklama3 = QLabel("Tutar: ")

        aciklama.setFont(baslikFont)
        aciklama2.setFont(baslikFont2)
        self.aciklama3.setFont(baslikFont2)

        sorgulaButton = QPushButton("Sorgula")
        sorgulaButton.setFont(butonFont2)



        self.masa_numara  = QLineEdit()
        self.masa_numara.setPlaceholderText("Masa numarasını girin:")

        sorgulaButton.clicked.connect(self.tutarSorgula)



        dikey.addStretch()
        dikey.addWidget(aciklama)
        dikey.addWidget(aciklama2)
        dikey.addWidget(self.masa_numara)
        dikey.addWidget(sorgulaButton)
        dikey.addWidget(self.aciklama3)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def geriDon(self):
        self.close()
    def tutarSorgula(self):

        self.aciklama3.setText("Hesaplanıyor...")
        QTest.qWait(1000)


        masa_nu = self.masa_numara.text()

        ucret_bul = kalem.execute("SELECT yiyecek_ucret FROM adisyon  WHERE masa_numarasi = ? ",(masa_nu,))
        tutar  = 0
        for i in ucret_bul.fetchall():
            tutar = tutar + i[0]

        tutar_gosterim = str(tutar) + " TL"
        self.aciklama3.setText(tutar_gosterim)
        self.aciklama3.setFont(baslikFont2)
class adisyonEkle(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Müşteri Adisyonu")
        self.setWindowIcon(QIcon('cafe-tasarim/cafe-logo.jpg'))

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        self.setGeometry(800,100,350,600)

        baslik = QLabel("Sipariş vermek istediğiniz ürünleri seçiniz.")
        baslik.setFont(baslikFont2)
        baslik.setAlignment(Qt.AlignHCenter)

        aciklama = QLabel('Sipariş vermek için çift tıklayınız.')
        aciklama2 = QLabel("LÜTFEN MASA NUMARANIZI GİRİNİZ : ")
        aciklama2.setFont(baslikFont2)

        self.masa_nu = QLineEdit()
        self.masa_nu.setPlaceholderText("Masa numarası")

        self.masa_nu.returnPressed.connect(self.masaNu)

        self.tablo = QTableWidget(self)
        row = kalem.execute("SELECT * FROM menu")
        row_count = len(row.fetchall())

        col = kalem.description
        col_count = len(col)

        self.tablo.setRowCount(row_count)
        self.tablo.setColumnCount(col_count)

        # self.tablo.setItem(0,0,QTableWidgetItem( col[0][0]))
        # self.tablo.setItem(0,1, QTableWidgetItem(col[1][0]))
        # self.tablo.setItem(0,2, QTableWidgetItem(col[2][0]))
        # self.tablo.setItem(0,3, QTableWidgetItem(col[3][0]))

        load_data = kalem.execute("SELECT * FROM menu")

        self.tablo.setRowCount(0)
        for row, form in enumerate(load_data):
            self.tablo.insertRow(row)
            for column, item in enumerate(form):
                self.tablo.setItem(row, column,QTableWidgetItem(str(item)))

        self.tablo.setColumnHidden(0,True)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tablo.doubleClicked.connect(self.on_click)
        self.tablo.cellDoubleClicked.connect(self.on_click)



        dikey.addWidget(baslik)
        dikey.addWidget(aciklama)
        dikey.addWidget(aciklama2)
        dikey.addWidget(self.masa_nu)
        dikey.addWidget(self.tablo)


        yatay.addLayout(dikey)
        self.setLayout(yatay)

    def on_click(self,row,col):

        self.numara = self.masa_nu.text()
        print(self.numara)

        item = self.tablo.item(row,col)
        urun = item.text()
        print(item.text())

        yemek_id = kalem.execute("SELECT yemek_id FROM menu WHERE yemek_ad = ?", (urun,))
        self.id = yemek_id.fetchall()[0][0]

        yemek_fiyat = kalem.execute("SELECT yemek_fiyat FROM menu WHERE yemek_ad = ?", (urun,))
        self.fiyat = yemek_fiyat.fetchall()[0][0]

        kalem.execute("INSERT INTO adisyon (masa_numarasi,yiyecek_id,yiyecek_ucret) VALUES (?,?,?)",
                      (int(self.numara), int(self.id), int(self.fiyat),))
        baglanti.commit()

    def masaNu(self):

        self.numara = self.masa_nu.text()

        if (self.numara == ""):
            QMessageBox.question(self,"Uyarı","Sipariş vermek için masa numarasını girin!!",QMessageBox.Ok)
        else :
            QMessageBox.question(self,"Bilgi","Masa numarası başarıyla girildi.",QMessageBox.Ok)
        return self.numara
class menuClass(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Sevgi Kahvesi Menü")
        aciklama = QLabel("Fiyatını görmek istediğiniz yiyeceğin üzerine tıklayın")
        baslik.setFont(baslikFont)
        baslik.setAlignment(Qt.AlignHCenter)

        liste = QListWidget()

        kafe_menu = kalem.execute("SELECT * FROM menu")

        for i in kafe_menu:
            liste.addItem(i[2])

        liste.sortItems()
        # **

        liste.setAlternatingRowColors(True)

        liste.itemClicked.connect(self.yiyecekBilgi)

        # listedeki elemanın üzerine okla gelince türünü ve fiyatini göstersin labelde

        # adisyonButon = QPushButton("Adisyona Ekle")
        # adisyonButon.setFont(butonFont)

        #adisyonButon.clicked.connect(self.ekle)

        dikey.addWidget(baslik)
        dikey.addWidget(aciklama)
        dikey.addWidget(liste)
        #dikey.addWidget(adisyonButon)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)

    def yiyecekBilgi(self,item):
        item_ismi = item.text()
        item_fiyat = kalem.execute("SELECT yemek_fiyat FROM menu WHERE yemek_ad = ? ",(item_ismi,))
        fiyat = item_fiyat.fetchall()[0][0]
        QMessageBox.question(self,'Uyarı',str("Seçilen ürünün fiyatı : " + str(fiyat) +" TL."),QMessageBox.Ok)
    def geriDon(self):
        self.close()
class araPencere(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        menuButon = QPushButton("Menü görüntüle")
        adisyonButon = QPushButton("Sipariş ver")
        odemeButton = QPushButton("Ödeme yap")

        menuButon.setFont(butonFont)
        adisyonButon.setFont(butonFont)
        odemeButton.setFont(butonFont)

        menuButon.clicked.connect(self.menuGoruntule)
        adisyonButon.clicked.connect(self.ekle)
        odemeButton.clicked.connect(self.odemeYap)

        dikey.addStretch()
        dikey.addWidget(menuButon)
        dikey.addStretch()
        dikey.addWidget(adisyonButon)
        dikey.addStretch()
        dikey.addWidget(odemeButton)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.showFullScreen()

    def geriDon(self):
        self.close()
    def menuGoruntule(self):
        self.menu = menuClass()
        self.menu.showFullScreen()
    def ekle(self):
        self.adisyon = adisyonEkle()
        self.adisyon.show()
    def odemeYap(self):
        self.odeme = odemeYap()
        self.odeme.showFullScreen()
class uyeOturumAcma(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Üye Girişi")
        baslik.setFont(baslikFont)
        baslik.setAlignment(Qt.AlignHCenter)

        uye_ismi_mesaj = QLabel("Lütfen kullanıcı adınız giriniz:")
        uye_ismi_mesaj.setFont(baslikFont2)
        self.kullanici_ad = QLineEdit()
        self.kullanici_ad.setPlaceholderText("İsim")

        uye_sifre_mesaj = QLabel("Lütfen parolanızı giriniz:")
        uye_sifre_mesaj.setFont(baslikFont2)
        self.kullanici_sifre = QLineEdit()
        self.kullanici_sifre.setEchoMode(QLineEdit.Password)
        self.kullanici_sifre.setPlaceholderText("Şifre")

        uyeGiris = QPushButton("Giriş Yap")
        uyeGiris.setFont(butonFont2)
        uyeGiris.clicked.connect(self.girisYap)

        self.flag = QLabel(" ")

        dikey.addStretch()
        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(uye_ismi_mesaj)
        dikey.addWidget(self.kullanici_ad)
        dikey.addWidget(uye_sifre_mesaj)
        dikey.addWidget(self.kullanici_sifre)
        dikey.addStretch()
        dikey.addWidget(uyeGiris)
        dikey.addStretch()
        dikey.addWidget(self.flag)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
    def girisYap(self):
        #bu kısımda düzenlemeler yapılmalı
        self.isim = self.kullanici_ad.text()
        self.sifre = self.kullanici_sifre.text()

        kullanici_ad = kalem.execute("SELECT kullanici_ad FROM uye_giris_bilgileri WHERE kullanici_ad = ?",(self.isim,))
        isim = kullanici_ad.fetchall()[0][0]

        if(self.isim != "" and self.sifre != ""):
            if (self.isim == isim):
                kullanici_sifre = kalem.execute(
                    "SELECT kullanici_sifre FROM uye_giris_bilgileri WHERE kullanici_ad = ?", (self.isim,))
                sifre = str((kullanici_sifre.fetchall()[0][0]))
                if (self.sifre == sifre):
                    self.flag.setText("Giriş işlemi yapılıyor.")
                    QtTest.QTest.qWait(1000)
                    self.flag.close()
                    QMessageBox.question(self, "Bilgi", "Kullanıcı girişi yapıldı!", QMessageBox.Ok)
                    
                    self.araPencereAc()
                    # ***

                else:
                    QMessageBox.question(self, "Uyarı", "Kullanıcı parolanızı yanlış girdiniz!", QMessageBox.Ok)
            else:
                QMessageBox.question(self, "Uyarı", "Kullanıcı adınızı yanlış girdiniz!", QMessageBox.Ok)
            #  !! kullanıcı adı yanlış girildiğinde program sonlanıyor

        else :
            if(self.isim == ""):
                QMessageBox.question(self,"Uyarı","Kullanıcı adınızı girmediniz!!!",QMessageBox.Ok)
            if(self.sifre == ""):
                QMessageBox.question(self,"Uyarı","Kullanıcı şifrenizi girmediniz!!!",QMessageBox.Ok)

        self.close()

    def geriDon(self):
        self.close()
    def araPencereAc(self):
        self.arapencere = araPencere()
        self.showFullScreen()
class uyeKayitYapma(QWidget):
    def __init__(self):
        super().__init__()

        ustBolum(self)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Üye Kayıt Penceresi")
        baslik.setFont(baslikFont)
        baslik.setAlignment(Qt.AlignHCenter)

        uye_ismi_mesaj = QLabel("Lütfen kullanıcı adınız giriniz:")
        uye_ismi_mesaj.setFont(baslikFont2)
        self.kullanici_ad = QLineEdit()
        self.kullanici_ad.setPlaceholderText("İsim")

        uye_sifre_mesaj = QLabel("Lütfen parolanızı giriniz:")
        uye_sifre_mesaj.setFont(baslikFont2)
        self.kullanici_sifre = QLineEdit()
        self.kullanici_sifre.setEchoMode(QLineEdit.Password)
        self.kullanici_sifre.setPlaceholderText("Şifre")

        uyeGiris = QPushButton("Kaydet")
        uyeGiris.setFont(butonFont2)
        uyeGiris.clicked.connect(self.kaydet)

        self.flag = QLabel(" ")

        dikey.addStretch()
        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(uye_ismi_mesaj)
        dikey.addWidget(self.kullanici_ad)
        dikey.addWidget(uye_sifre_mesaj)
        dikey.addWidget(self.kullanici_sifre)
        dikey.addStretch()
        dikey.addWidget(uyeGiris)
        dikey.addStretch()
        dikey.addWidget(self.flag)

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
    def kaydet(self):
        isim = self.kullanici_ad.text()
        sifre = self.kullanici_sifre.text()

        if (isim == "" or sifre == ""):
            if(isim == ""):
                QMessageBox.question(self,"Uyarı","Kullanıcı adınızı girmediniz!!!",QMessageBox.Ok)
            if(sifre == ""):
                QMessageBox.question(self,"Uyarı","Kullanıcı şifrenizi girmediniz!!!",QMessageBox.Ok)

        if (isim != "" and sifre != ""):
            self.flag.setText("Kaydediliyor. Lütfen bekleyin.")
            QTest.qWait(750)
            self.flag.setText("Kaydedildi.")
            QTest.qWait(500)
            kalem.execute("INSERT INTO uye_giris_bilgileri (kullanici_ad,kullanici_sifre) VALUES (?,?)",(isim,sifre,))
            baglanti.commit()
            QMessageBox.question(self,"Uyarı","Kayıt işleminiz tamamlanmıştır",QMessageBox.Ok)
            self.close()

        self.flag.close()
    def geriDon(self):
        self.close()
class intro(QWidget):
    def __init__(self):
        super().__init__()

        dikey = QVBoxLayout()
        yatay = QHBoxLayout()

        self.baslik = "Sevgi Kafe "

        self.setWindowTitle(self.baslik)

        self.setWindowIcon(QIcon('cafe-tasarim/cafe-logo.jpg'))

        yazi = QLabel()
        resim = QLabel()
        pixmap = QPixmap('C:\\Users\\asus\\PycharmProjects\\cafe-system\\cafe-tasarim\\kahve.jpg')
        resim.setPixmap(pixmap)
        resim.setAlignment(Qt.AlignHCenter)

        yazi.setText("Sevda Kafe Siparis Sistemi")
        yazi.setAlignment(Qt.AlignHCenter)
        yazi.setFont(baslikFont)

        dikey.addStretch()
        dikey.addWidget(yazi)
        dikey.addStretch()
        dikey.addWidget(resim)
        dikey.addStretch()

        yatay.addLayout(dikey)
        self.setLayout(yatay)
class Pencere(QWidget):
    def __init__(self):
        super().__init__()

        self.giris = intro()
        self.giris.showFullScreen()
        QTest.qWait(2000)

        kapatButon = QPushButton("X",self)
        kapatButon.setFont(baslikFont)
        kapatButon.setGeometry(1300, 20, 50, 50)
        kapatButon.clicked.connect(self.kapat)

        yatay = QHBoxLayout()
        dikey = QVBoxLayout()

        baslik = QLabel("Sevgi Kahvesi Sipariş Sistemi")
        baslik.setFont(baslikFont)

        uyeButon = QPushButton("Üye Girişi Yap")
        uyeKaydi = QPushButton("Üye Kaydı Yap")

        uyeButon.clicked.connect(self.uyeGiris)
        uyeKaydi.clicked.connect(self.uyeKayit)

        uyeButon.setFont(butonFont)
        uyeKaydi.setFont(butonFont)

        dikey.addStretch()
        dikey.addWidget(baslik)
        dikey.addStretch()
        dikey.addWidget(uyeButon)
        dikey.addStretch()
        dikey.addWidget(uyeKaydi)
        dikey.addStretch()

        yatay.addStretch()
        yatay.addLayout(dikey)
        yatay.addStretch()

        self.setLayout(yatay)
        self.showFullScreen()

    def uyeGiris(self):
        self.uyeGirisIslemi = uyeOturumAcma()
        self.uyeGirisIslemi.showFullScreen()
    def uyeKayit(self):
        self.uyeKayitIslemi = uyeKayitYapma()
        self.uyeKayitIslemi.showFullScreen()
    def kapat(self):
        qApp.quit()


uygulama  = QApplication(sys.argv)
pencere = Pencere()
uygulama.exit(uygulama.exec_())
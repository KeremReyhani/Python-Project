import re
import time


class Kayit:
    def __init__(self, programad):
        self.programad = programad
        self.dongu = True

    def program(self):
        secim = self.menu()

        if secim == "1":
            print("Kayıt Ekleme Menüsüne Yönlendiriliyorsunuz...")
            time.sleep(3)
            self.kayitekle()

        if secim == "2":
            print("Kayıt Silme Menüsüne Yönlendiriliyorsunuz...")
            time.sleep(3)
            (self.kayitcikar())

        if secim == "3":
            print("Verilere Erişiliyor...")
            time.sleep(3)
            self.kayitoku()

        if secim == "4":
            self.cikis()

    def menu(self):
        def kontrol(secim):
            if re.search("[^1-4]", secim):
                raise Exception("Lütfen 1 ve 4 Arasında Geçerli Bir Seçim Yapınız...")
            elif len(secim) != 1:
                raise Exception("Lütfen 1 ve 4 Arasında Geçerli Bir Seçim Yapınız...")

        while True:
            try:
                secim = input(
                    "Merhabalar, {} Otomasyon Sistemine Hoşgeldiniz.\n\nLütfen Yapmak İstediğiniz İşlemi Seçiniz...\n\n[1]-Kayıt Ekle\n[2]-Kayıt Sil\n[3]-Kayıt Oku\n[4]-Çıkış\n\n".format(
                        self.programad))
                kontrol(secim)
            except Exception as hata:
                print(hata)
                time.sleep(3)
            else:
                break

        return secim

    def kayitekle(self):
        def kontrolad(Ad):
            if Ad.isalpha() == False:
                raise Exception("Geçerli Bir Ad Giriniz...")

        while True:
            try:
                Ad = input("Adınız: ")
                kontrolad(Ad)
            except Exception as hataad:
                print(hataad)
                time.sleep(3)
            else:
                break

        def kontrolsoyad(Soyad):
            if Soyad.isalpha() == False:
                raise Exception("Geçerli Bir Soyad Giriniz...")

        while True:
            try:
                Soyad = input("Soyadınız: ")
                kontrolsoyad(Soyad)
            except Exception as hatasoyad:
                print(hatasoyad)
                time.sleep(3)
            else:
                break

        def kontrolyas(Yas):
            if Yas.isdigit() == False:
                raise Exception("Geçerli Bir Yaş Giriniz...")

        while True:
            try:
                Yas = input("Yaşınız: ")
                kontrolyas(Yas)
            except Exception as Yas:
                print(Yas)
                time.sleep(3)
            else:
                break

        def kontroltc(Tc):
            if Tc.isdigit() == False:
                raise Exception("Geçerli Bir Kimlik Numarası Giriniz...")
            elif len(Tc) != 11:
                raise Exception("Kimlik Numaranız 11 Karakterden Oluşmalıdır...")

        while True:
            try:
                Tc = input("Kimlik Numaranız: ")
                kontroltc(Tc)
            except Exception as hatatc:
                print(hatatc)
                time.sleep(3)
            else:
                break

        def kontrolmail(Mail):
            if not re.search("@" and ".com", Mail):
                raise Exception("Geçerli Bir E-posta Adresi Giriniz...")

        while True:
            try:
                Mail = input("E-posta Adresiniz: ")
                kontrolmail(Mail)
            except Exception as hatamail:
                print(hatamail)
                time.sleep(3)
            else:
                break

        with open("C:/Users/kerem/Desktop/Bilgiler.txt", "r", encoding="utf-8") as Dosya:
            satirsayisi = Dosya.readlines()
        if len(satirsayisi) == 0:
            Id = 1
        else:
            with open("C:/Users/kerem/Desktop/Bilgiler.txt", "r", encoding="utf-8") as Dosya:
                Id = int(Dosya.readlines()[-1].split("-")[0]) + 1

        with open("C:/Users/kerem/Desktop/Bilgiler.txt", "a+", encoding="utf-8") as Dosya:
            Dosya.write("{}-{} {} {} {} {}\n".format(Id, Ad, Soyad, Yas, Tc, Mail))
            print("Veriler İşlenmiştir...")
        self.menudon()

    def kayitcikar(self):
        y = input("Lütfen Silmek İstediğiniz Kişinin Id Numarasını Giriniz...")
        with open("C:/Users/kerem/Desktop/Bilgiler.txt", "r", encoding="utf-8") as Dosya:
            liste = []
            liste2 = Dosya.readlines()
            for i in range(0, len(liste2)):
                liste.append(liste2[i].split("-")[0])

        del liste2[liste.index(y)]

        with open("C:/Users/kerem/Desktop/Bilgiler.txt", "w+", encoding="utf-8") as YeniDosya:
            for i in liste2:
                YeniDosya.write(i)
            print("Kayıt Siliniyor...")
            time.sleep(3)
            print("Kayıt Başarıyla Silinmiştir...")
        self.menudon()

    def kayitoku(self):
        with open("C:/Users/kerem/Desktop/Bilgiler.txt", "r", encoding="utf-8") as Dosya:
            for i in Dosya:
                print(i)
            self.menudon()

    def cikis(self):
        print("Otomasyondan Çıkılıyor...")
        time.sleep(3)
        self.dongu = False
        exit()

    def menudon(self):
        while True:
            x = input("Ana Menüye Dönmek İçin 6'ya, Çıkmak İçin Lütfen 5'e Basınız...")
            if x == "6":
                print("Ana Menüye Dönülüyor...")
                time.sleep(3)
                self.program()
                break
            elif x == "5":
                self.cikis()
                break
            else:
                print("Lütfen Geçerli Bir Seçim Yapınız...")


Sistem = Kayit("Anlaşılır Ekonomi")
while Sistem.dongu:
    Sistem.program()
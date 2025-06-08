import json
import re
import time
import random

class Site:
    def __init__(self):
        self.dongu=True
        self.veriler=self.verial()

    def program(self):
        secim=self.menu()

        if secim=="1":
            self.giris()
        if secim=="2":
            self.kayitol()
        if secim=="3":
            self.cikis()

    def menu(self):
        def kontrol(secim):
            if re.search("[^1-3]",secim):
                raise Exception("Lütfen 1 ve 3 Arasında Gerçerli Bir Seçim Yapnınız...")
            elif len(secim)!=1:
                raise Exception("Lütfen 1 ve 3 Arasında Gerçerli Bir Seçim Yapnınız...")
        while True:
            try:
                secim=input("Merhabalar, Anlaşılır Ekonomi Sitesine Hoşgeldiniz.\n\nLütfen Yapmak İstediğiniz İşlemi Seçiniz...\n\n[1]-Giriş\n[2]-Kayıt Ol\n[3]-Çıkış\n\n")
                kontrol(secim)
            except Exception as hata:
                print(hata)
                time.sleep(3)
            else:
                break
        return secim
    def giris(self):
        print("Giriş Menüsüne Yönlendiriliyorsunuz...")
        time.sleep(2)
        KullaniciAdi=input("Lütfen Adınızı Giriniz: ")
        Sifre=input("Lütfen Şifrenizi Giriniz: ")

        sonuc=self.giriskontrol(KullaniciAdi,Sifre)

        if sonuc==True:
            self.girisbasarili()
        else:
            self.girisbasarisiz()

    def giriskontrol(self,KullaniciAdi,Sifre):
        self.veriler=self.verial()
        try:
            for kullanici in self.veriler["Kullanıcılar"]:
                if kullanici["KullaniciAdi"]==KullaniciAdi and kullanici["Sifre"]==Sifre:
                    return True
        except KeyError:
            return False
        return False

    def girisbasarili(self):
        print("Kontrol Ediliyor...")
        time.sleep(2)
        print("Giriş Başarılı. Anlaşılır Ekonomi Sitesine Hoşgeldiniz...")
        self.sonuc=False
        self.dongu=False

    def girisbasarisiz(self):
        print("Kontrol Ediliyor...")
        time.sleep(2)
        print("Giriş Başarısız. Kullanıcı Adı veya Şifre Hatalı!!!")
        self.menudon()

    def kayitol(self):
        def kontrolka(KullaniciAdi):
            if len(KullaniciAdi)<8:
                raise Exception("Kullanıcı Adınız En Az 8 Karakterden Oluşmalıdır...")
        while True:
            try:
                KullaniciAdi=input("Kullanıcı Adınız: ")
                kontrolka(KullaniciAdi)
            except Exception as hataad:
                print(hataad)
                time.sleep(2)
            else:
                break

        def kontrolsifre(Sifre):
            if len(Sifre)<8:
                raise Exception("Şifreniz En Az 8 Karakterden Oluşmalıdır...")
            elif not re.search("[0-9]",Sifre):
                raise Exception("Şifrenizde En Az Bir Tane Rakam Olmalıdır...")
            elif not re.search("[A-Z]",Sifre):
                raise Exception("Şifrenizde En Az Bir Tane Büyük Harf Olmalıdır...")
            elif not re.search("[a-z]",Sifre):
                raise Exception("Şifrenizde En Az Bir Tane Küçük Harf Olmalıdır...")
        while True:
            try:
                Sifre=input("Şifreniz: ")
                kontrolsifre(Sifre)
            except Exception as hataad:
                   print(hataad)
                   time.sleep(2)
            else:
                 break

        def kontrolmail(Mail):
            if not re.search("@" and ".com",Mail):
                raise Exception("Geçerli Bir Mail Adresi Giriniz...")
        while True:
             try:
                Mail=input("E-posta Adresiniz: ")
                kontrolmail(Mail)
             except Exception as hataad:
                print(hataad)
                time.sleep(2)
             else:
                break

        sonuc=self.kayitvarmi(KullaniciAdi,Mail)
        if sonuc==True:
            print("Bu Kullanıcı Adı ve Mail Sistemde Kayıtlı...")
        else:
            aktivasyonkodu=self.aktivasyongonder()
            durum=self.aktivasyonkontrol(aktivasyonkodu)
        while True:
            if durum==True:
                self.verikaydet(KullaniciAdi,Sifre,Mail)
                break
            else:
                input("Geçersiz Aktivasyon Kodu... Lütfen Tekrar Giriniz!...\n...")

    def kayitvarmi(self,KullaniciAdi,Mail):
        self.veriler=self.verial()
        try:
            for kullanici in self.veriler["Kullanicilar"]:
                if kullanici["KullaniciAdi"]==KullaniciAdi and kullanici["Mail"]==Mail:
                    return True
        except KeyError:
            return False
        return False

    def aktivasyongonder(self):
        with open("C:/Users/kerem/Desktop/Aktivasyon.txt","w",encoding="utf-8") as Dosya:
            aktivasyon=str(random.randint(10000,99999))
            Dosya.write("Aktivasyon Kodunuz:"+aktivasyon)
        return aktivasyon

    def aktivasyonkontrol(self,aktivasyon):
        aktivasyonkodual=input("Lütfen E-postanıza Gelen Aktivasyon Kodunu Giriniz: ")
        if aktivasyon==aktivasyonkodual:
            return True
        else:
            return False

    def verial(self):
        try:
            with open("C:/Users/kerem/Desktop/Kullanıcılar.txt","r",encoding="utf-8") as Dosya:
                veriler=json.load(Dosya)
        except FileNotFoundError:
            with open("C:/Users/kerem/Desktop/Kullanıcılar.txt","w",encoding="utf-8") as Dosya:
                Dosya.write("{}")
            with open("C:/Users/kerem/Desktop/Kullanıcılar.txt","r",encoding="utf-8") as Dosya:
                veriler=json.load(Dosya)
        return veriler
    def verikaydet(self,KullaniciAdi,Sifre,Mail):
        self.veriler=self.verial()

        try:
            self.veriler["Kullanıcılar"].append({"KullaniciAdi":KullaniciAdi,"Sifre":Sifre,"Mail":Mail})
        except KeyError:
            self.veriler["Kullanıcılar"]=list()
            self.veriler["Kullanıcılar"].append({"KullaniciAdi":KullaniciAdi,"Sifre":Sifre,"Mail":Mail})

        with open("C:/Users/kerem/Desktop/Kullanıcılar.txt", "w", encoding="utf-8") as Dosya:
            json.dump(self.veriler,Dosya,ensure_ascii=False,indent=4)
            print("Kayıt Başarıyla Oluşturulmuştur...")
        self.menudon()

    def cikis(self):
        print("Siteden Çıkılıyor...")
        time.sleep(2)
        self.dongu=False
        exit()

    def menudon(self):
        while True:
            x=input("Ana Menüye Dönmek İçin 5'e, Çıkmak İçin Lütfen 4'e Basınız...:")
            if x=="5":
                print("Ana Menüye Dönülüyor...")
                time.sleep(2)
                self.program()
                break
            elif x=="4":
                self.cikis()
                break
            else:
                print("Lütfen Geçerli Bir Seçim Yapınız...")

Sistem=Site()
while Sistem.dongu:
    Sistem.program()
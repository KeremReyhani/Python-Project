import tkinter as tk
import random

renkler = ['black-siyah', 'white-beyaz', 'red-kırmızı', 'green-yeşil', 'blue-mavi', 'yellow-sarı',
           'brown-kahverengi', 'orange-turuncu', 'grey-gri', 'maroon-bordo', 'purple-mor', 'pink-pembe']

score = 0

kalan_zaman = 30

def başla(event): #bind ile fonksiyon yazarken event olmak zorunda
    if kalan_zaman == 30:
        geri_sayım()
    sonraki_renk()

def sonraki_renk():
    if kalan_zaman > 0:
        giriş.focus()
        if giriş.get().lower() == renkler[1][renkler[1].find("-")+1:].lower():
            global score
            score += 1
        giriş.delete(0, tk.END)
        random.shuffle(renkler) #elemanların yerlerini karıştırır
        yazı.config(fg=str(renkler[1][:renkler[1].find("-")]), text=str(renkler[0][renkler[0].find("-")+1:]))
        puan.config(text="Puan: "+ str(score))

def geri_sayım():
    global kalan_zaman
    if kalan_zaman > 0:
        kalan_zaman -= 1
        zaman.config(text="Kalan Zaman: " + str(kalan_zaman))
        zaman.after(1000, geri_sayım) #yazdığın kadar milisaniye geçtikten sonra işlemi yapar

pencere = tk.Tk()
pencere.title("Renk Oyunu")
pencere.geometry("500x400")

bilgi = tk.Label(pencere, fg="red", text="Yazının Rengi Nedir?", font=("Courier", 12))
bilgi.pack()
puan = tk.Label(pencere, fg="green", text="Başlamak İçin Enter'e Bas", font=("Courier", 12))
puan.pack()
zaman = tk.Label(pencere, fg="blue", text="Kalan Zaman: " + str(kalan_zaman), font=("Courier", 12))
zaman.pack()
yazı = tk.Label(pencere, font=("Helvetica", 60))
yazı.pack()

giriş = tk.Entry(pencere)
pencere.bind("<Return>", başla) #tuşu çalıştırmak için
giriş.pack()
giriş.focus()

pencere.mainloop()
import tkinter as tk
import random

def KontrolEt():
    global sayaç
    if sayı1.get().isdigit():
        s1 = int(sayı1.get())
        sayaç += 1
        if s1 > sayı2:
            yazı2.configure(text = "Daha küçük bir sayı giriniz")
        elif s1 < sayı2:
            yazı2.configure(text = "Daha büyük bir sayı giriniz")
        else:
            yazı2.configure(text = f"Sayıyı {sayaç} defada tahmin ettiniz.")
    sayı1.selection_range(0, tk.END) #önce girdiğimizi silmemek için

pencere = tk.Tk()
pencere.title("Sayı Tahmini")
pencere.geometry("350x200")

yazı1 = tk.Label(pencere, text="1-10 arasında sayı giriniz", font="Courier 12 bold", width=25, justify="center")
yazı1.place(x = 15, y =20)

sayı1 = tk.Entry(pencere, font="Courier 12 bold", width=15, justify="center")
sayı1.place(x = 70, y = 50)
sayı1.focus()

kontrol = tk.Button(pencere, text="Kontrol", font="Courier 12", width=10, command=KontrolEt)
kontrol.place(x = 90, y = 80)

yazı2 = tk.Label(pencere, text="", font="Courier 14 bold", width=25, justify="center")
yazı2.place(x = 0, y =120)

sayı2 = random.randint(1, 10)
sayaç = 0

pencere.mainloop()
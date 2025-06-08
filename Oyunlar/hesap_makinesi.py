import tkinter as tk

def topla():
    if sayı1.get().isdigit() and sayı2.get().isdigit(): #girilen değer sayı mı değil mi
        s1 = float(sayı1.get())
        s2 = float(sayı2.get())
        sonuç.configure(text=str(s1+s2)) #sonuca ulaşmak için
def çıkar():
    if sayı1.get().isdigit() and sayı2.get().isdigit(): #girilen değer sayı mı değil mi
        s1 = float(sayı1.get())
        s2 = float(sayı2.get())
        sonuç.configure(text=str(s1-s2)) #sonuca ulaşmak için
def çarp():
    if sayı1.get().isdigit() and sayı2.get().isdigit(): #girilen değer sayı mı değil mi
        s1 = float(sayı1.get())
        s2 = float(sayı2.get())
        sonuç.configure(text=str(s1*s2)) #sonuca ulaşmak için
def böl():
    if sayı1.get().isdigit() and sayı2.get().isdigit(): #girilen değer sayı mı değil mi
        s1 = float(sayı1.get())
        s2 = float(sayı2.get())
        sonuç.configure(text=str(s1/s2)) #sonuca ulaşmak için

pencere = tk.Tk()
pencere.title("Hesap Makinesi")
pencere.geometry("320x300")

sonuç = tk.Label(pencere, text="Sonuç", font="Courier 16 bold", width=30, justify= "center")
sonuç.place(x = -50, y = 20) #sonuç etiketi nerde
sayı1 = tk.Entry(pencere, font="Courier 14 bold", width=15, justify= "right")
sayı1.place(x = 70, y = 50)
sayı2 = tk.Entry(pencere, font="Courier 14 bold", width=15, justify= "right")
sayı2.place(x = 70, y = 80)

tuş1 = tk.Button(pencere, text="+", font="Courier 14 bold", width=10, command=topla) #fonksiyonu çağırmak için
tuş1.place(x = 90, y = 110)
tuş2 = tk.Button(pencere, text="-", font="Courier 14 bold", width=10, command=çıkar) #fonksiyonu çağırmak için
tuş2.place(x = 90, y = 150)
tuş3 = tk.Button(pencere, text="*", font="Courier 14 bold", width=10, command=çarp) #fonksiyonu çağırmak için
tuş3.place(x = 90, y = 190)
tuş4 = tk.Button(pencere, text="/", font="Courier 14 bold", width=10, command=böl) #fonksiyonu çağırmak için
tuş4.place(x = 90, y = 230)

sayı1.focus() #imleç sayı1'de başlayacak
pencere.mainloop()

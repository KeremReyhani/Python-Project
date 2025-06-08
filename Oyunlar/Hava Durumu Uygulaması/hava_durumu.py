import requests
import json
import pprint   #çıktının okunabilirliğini artırır

while True:
    sehir=input("Bilgilerini öğrenmek istediğiniz şehri giriniz: ")

    apikey="ebc94b015fe669197da30dd9d1fbedc5"

    adres="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=tr&units=metric".format(sehir,apikey)

    baglan=requests.get(adres)

    sorgu=baglan.json()
    pprint.pprint(sorgu)

    print()
    print()

    havadurumu=sorgu["weather"][0]["description"]
    sıcaklık=sorgu["main"]["temp"]
    hissedilen=sorgu["main"]["feels_like"]

    print("{} için hava durumu bilgileri aşağıdaki gibidir...\n\nSıcaklık: {}°\nDurum: {}\nHissedilen Sıcaklık: {}°".format(sehir,sıcaklık,havadurumu,hissedilen))
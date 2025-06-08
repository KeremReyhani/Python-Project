import random
def sahte_isim():
    ad=["Albert", "Charles", "Nicolas", "Michael", "Anders", "Isaac", "Stephen", "Marie", "Richard"]
    soyad=["Einstein", "Darwin", "Copernicus", "Faraday", "Celsius", "Newton", "Hawking", "Curie","Dawkins"]
    return (f"{random.choice(ad)} {random.choice(soyad)}")
for i in range(5):
    print(sahte_isim())

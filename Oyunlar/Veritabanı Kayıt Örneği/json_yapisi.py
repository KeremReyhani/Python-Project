import json

Bilgiler="""{"Ad":"Kerem","Soyad":"Reyhani","Yas":20}"""
print(type(Bilgiler))

BilgiOku=json.loads(Bilgiler)
print(BilgiOku["Ad"])
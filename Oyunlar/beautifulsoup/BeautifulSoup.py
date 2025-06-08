from bs4 import BeautifulSoup

kod = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
    <title>Liste Örnekleri-1</title>
</head>
    <body>
    <ol>
        <li>
            SICAK İÇECEKLER
            <ol type="I">
                <li>ÇAY</li>
                <li>KAHVE</li>
                    <ol type="a">
                        <li>TÜRK KAHVESİ</li>
                        <li>NESCAFE</li>
                    </ol>
                <li>SICAK ÇİKOLATA</li>
            </ol>
        </li>
        
        <li>
            SOĞUK İÇECEKLER
            <ol>
                <li>MEYVE SULARI
                    <ul>
                        <li>Vişne</li>
                        <li>Şeftali</li>
                        <li>Kayısı</li>
                        <li>Elma</li>
                    </ul>
                </li>
                
                <li>
                    LİMONATA
                </li>
            </ol>
        </li>
    </ol>
    
    </body>
</html>"""

parset=BeautifulSoup(kod,"html.parser")

"""yaz=parset.prettify()
print(yaz)"""

"""yaz = parset.title
print(yaz)"""

"""yaz=parset.title.string
print(yaz)"""

"""yaz=parset.find_all("li")
print(yaz)"""

"""yaz=parset.li.findChildren()
print(yaz)"""

yaz=parset.li.find_next_sibling()
print(yaz)
import turtle
import random

pencere = turtle.Screen()
pencere.screensize(600,600)
pencere.title("Kaplumbağaları Yakala")
pencere.bgcolor("blue")
pencere.bgpic("underwater.gif")

oyuncu = turtle.Turtle()
oyuncu.color("white")
oyuncu.shape("triangle")
oyuncu.shapesize(3)
oyuncu.penup() #çizim yapmasını engeller (kalemi kaldır)

Score = 0
puan = turtle.Turtle()
puan.speed(0)
puan.shape("square")
puan.color("white")
puan.penup()
puan.hideturtle() #şekli gizler
puan.goto(-200, 200) #konum
puan.write(f"Puan {Score}", align="center", font=("Courier", 24, "normal"))

speed = 1
hız_puan = turtle.Turtle()
hız_puan.speed(0)
hız_puan.shape("square")
hız_puan.color("white")
hız_puan.penup()
hız_puan.hideturtle() #şekli gizler
hız_puan.goto(200, 200) #konum
hız_puan.write(f"Hız {speed}", align="center", font=("Courier", 24, "normal"))

# pencerede olan olayları kontrol edeceğiz
def SolaDon(): #sol oka bastığında dönecek
    oyuncu.left(30)
def SagaDon():
    oyuncu.right(30)

def HızArttır():
    global speed #speed ana kodda diye global
    speed += 1
    hız_puan.clear()
    hız_puan.write(f"Puan {speed}", align="center", font=("Courier", 24, "normal"))

def HızAzalt():
    global speed
    speed -= 1
    hız_puan.clear()
    hız_puan.write(f"Puan {speed}", align="center", font=("Courier", 24, "normal"))

pencere.listen()
pencere.onkey(SolaDon, "Left")
pencere.onkey(SagaDon, "Right")
pencere.onkey(HızArttır, "Up")
pencere.onkey(HızAzalt, "Down")
pencere.tracer(2) #hızı arttırır

max_hedef = 5
hedefler = []
for i in range(max_hedef):
    hedefler.append(turtle.Turtle())
    hedefler[i].penup()
    hedefler[i].color("yellow")
    hedefler[i].shape("turtle")
    hedefler[i].speed(0)
    hedefler[i].setposition(random.randint(-300, 300), random.randint(-300, 300))

"""
hedef = turtle.Turtle()
hedef.penup()
hedef.color("yellow")
hedef.shape("turtle")
hedef.speed(0)
hedef.setposition(random.randint(-300, 300), random.randint(-300, 300)) #herhangi bir yere tam sayı (konum) ekleyecek
"""

while True:
    oyuncu.forward(speed) #oyunucunun hızı

    if oyuncu.xcor() > 300 or oyuncu.xcor() < -300: #ekrandan çıktıktan sonra geri dönmesini sağlar
        oyuncu.right(180)
    if oyuncu.ycor() > 300 or oyuncu.ycor() < -300:
        oyuncu.left(180)

    for i in range(max_hedef): #oyuncuyla çarpışma durumu
        hedefler[i].forward(1)

        if hedefler[i].xcor() > 500 or hedefler[i].xcor() < - 500: #ekran dışına çıktığında geri dönsün
            hedefler[i].right(random.randint(150, 250))
        if hedefler[i].ycor() > 500 or hedefler[i].ycor() < - 500:
            hedefler[i].left(random.randint(150, 250))

        if oyuncu.distance(hedefler[i]) < 40: #hedefin yeniden doğmasını sağlar
            hedefler[i].setposition(random.randint(-300, 300), random.randint(-300, 300))
            hedefler[i].right(random.randint(0, 360)) #çarptıktan sonra
            Score += 10
            puan.clear()
            puan.write(f"Puan {Score}", align="center", font=("Courier", 24, "normal"))

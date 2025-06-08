import turtle, time, random

pencere = turtle.Screen()
pencere.title("Araba Yarışı")
pencere.bgcolor("Grey")
pencere.setup(width=700, height=500)
pencere.tracer(0)

pencere.register_shape("racingback.gif")
pencere.register_shape("racingcar.gif")

araba = turtle.Turtle()
araba.speed(0)
araba.shape("racingcar.gif")
araba.shapesize(2)
araba.color("red")
araba.setheading(90)
araba.penup()
araba.goto(0, -200)

arka = turtle.Turtle()
arka.speed(0)
arka.pensize(3)
arka.shape("square")
arka.color("white")
arka.penup()
arka.hideturtle()
arka.goto(0, 0)

kamera_dy = 0
kamera_y = 0

def sol():
    x = araba.xcor()
    x = x - 10
    if x < -170:
        x = -170
    araba.setx(x)

def sağ():
    x = araba.xcor()
    x = x + 10
    if x > 170:
        x = 170
    araba.setx(x)

engeller = []
for i in range(10):
    engel = turtle.Turtle()
    engel.speed(0)
    engel.shape("square")
    engel.shapesize(3, 6)
    engel.color("red")
    engel.setheading(90)
    engel.penup()
    engel.dx = random.randint(-170, 170)
    engel.dy = 500 #ilk konumu
    engel.goto(engel.dx, engel.dy)
    engeller.append(engel)

pencere.listen()
pencere.onkeypress(sol, "Left")
pencere.onkeypress(sağ, "Right")

başlangıç_zamanı = time.time() #engellerin geleceği zaman
i = -1 #engelleri hareket ettirmek için

while True:
    kamera_dy = -2 #aşağı inecek
    kamera_y += kamera_dy
    kamera_y = kamera_y % 700

    arka.goto(0, kamera_y - 700)
    arka.shape("racingback.gif")
    arka.stamp() #arka alan sürekli hareket etsin diye

    araba.shape("racingcar.gif")
    araba.stamp()


    arka.goto(0, kamera_y)
    arka.shape("racingback.gif")
    arka.stamp() #arka alan diye görünsün diye

    araba.shape("racingcar.gif")
    araba.stamp()

    if time.time() - başlangıç_zamanı > random.randint(3, 6):
        başlangıç_zamanı = time.time()
        i = i + 1
        if i == 9:  # son engel
            i = -1
            for engel in engeller:
                engel.dx = random.randint(-170, 170)
                engel.dy = 500
                engel.goto(engel.dx, engel.dy)

    y = engeller[i].ycor()
    y = y - 2
    engeller[i].sety(y)

    if engeller[i].distance(araba) < 30: #çarptığınfa
        print("Çarptı")


    pencere.update()
    arka.clear() #arka plan düzenlensin diye
    araba.clear()
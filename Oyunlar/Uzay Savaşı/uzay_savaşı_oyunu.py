import turtle, random
import winsound

pencere = turtle.Screen()
pencere.bgcolor("black")
pencere.title("Uzay Savaşı")
pencere.bgpic("uzay.gif")
pencere.setup(width=600, height=600)

turtle.register_shape("oyuncu.gif") #resimleri tanıtmak
turtle.register_shape("dusman.gif")
turtle.register_shape("ates.gif")

oyuncu = turtle.Turtle()
oyuncu.color("blue")
oyuncu.speed(0)
oyuncu.shape("oyuncu.gif")
oyuncu.setheading(90)
oyuncu.penup()
oyuncu.goto(0, -250)
oyuncuhızı = 20

ateş = turtle.Turtle()
ateş.color("yellow")
ateş.speed(0)
ateş.shape("ates.gif")
ateş.setheading(90)
ateş.penup()
ateş.goto(0, -240)
ateşhızı = 40
ateş.hideturtle()
ateş.turtlesize(1, 1)
ateşkontrol = False

yaz = turtle.Turtle()
yaz.color("white")
yaz.speed(0)
yaz.penup()
yaz.goto(0, 200)
yaz.hideturtle()

def ateşgit():
    y = ateş.ycor()
    y += ateşhızı
    ateş.sety(y)

def sola_git():
    x = oyuncu.xcor()
    x -= oyuncuhızı
    if x < -300:
        x = -300
    oyuncu.setx(x)

def sağa_git():
    x = oyuncu.xcor()
    x += oyuncuhızı
    if x > 300:
        x = 300
    oyuncu.setx(x)

def ateş_et():
    global ateşkontrol
    winsound.PlaySound("lazer.wav", winsound.SND_ASYNC)
    x = oyuncu.xcor()
    y = oyuncu.ycor()
    ateş.goto(x, y)
    ateş.showturtle()
    ateşkontrol = True

hedefler = []
for i in range(7):
    hedefler.append(turtle.Turtle())
for hedef in hedefler:
    hedef.color("red")
    hedef.speed(0)
    hedef.turtlesize(1, 1)
    hedef.penup()
    hedef.setheading(90)
    hedef.shape("dusman.gif")
    x = random.randint(-280, 280)
    y = random.randint(180, 260)
    hedef.goto(x, y)

pencere.listen()
pencere.onkey(sola_git, "Left")
pencere.onkey(sağa_git, "Right")
pencere.onkey(ateş_et, "space")

while True:
    if ateşkontrol:
        ateşgit()
    for hedef in hedefler:
        y = hedef.ycor()
        y -= 2
        hedef.sety(y)
        if hedef.distance(ateş) < 30:
            ateş.hideturtle()
            hedef.hideturtle()
            hedefler.pop(hedefler.index(hedef)) #silinmesi için
            winsound.PlaySound("patlama.wav", winsound.SND_ASYNC)

            if hedef.ycor() < -270 or hedef.distance(oyuncu) < 30:
                yaz.write("KAYBETTİNİZ", align="center", font=("Courier", 24, "bold"))

        if len(hedefler) == 0:
            yaz.write("KAZANDINIZ", align="center", font=("Courier", 24, "bold"))
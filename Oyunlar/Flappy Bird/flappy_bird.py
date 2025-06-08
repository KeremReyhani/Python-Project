import turtle, time, random

pencere = turtle.Screen()
pencere.title("Flappy Bird")
pencere.bgcolor("blue")
pencere.bgpic("background.gif")
pencere.setup(width=500, height=700)
pencere.tracer(0)
pencere.register_shape("bird.gif")

kuş = turtle.Turtle()
kuş.speed(0)
kuş.color("yellow")
kuş.shape("bird.gif")
kuş.penup()
kuş.goto(-180, 0)
kuş.dx = 0
kuş.dy = 1

score = 100
puan = turtle.Turtle()
puan.speed(0)
puan.color("white")
puan.penup()
puan.goto(0, 290)
puan.write(f"Puan: {score}", align="center", font=("Courier", 24, "bold"))

yer_çekimi = -0.3

def yukarı(x, y):
    kuş.dy += 8

    if kuş.dy > 8:
        kuş.dy = 8


pencere.listen()
pencere.onscreenclick(yukarı)

borular = []

starting_time = time.time()

while True:
    time.sleep(0.02)
    pencere.update()

    kuş.dy += yer_çekimi

    if (time.time() - starting_time > random.randint(2, 10)):
        starting_time = time.time()

        boru_üst = turtle.Turtle()
        boru_üst.speed(0)
        boru_üst.color("red")
        boru_üst.shape("square")
        boru_üst.h = random.randint(10, 20)
        boru_üst.shapesize(boru_üst.h, 2, outline=None)
        boru_üst.penup()
        boru_üst.goto(300, 250)
        boru_üst.dx = -3
        boru_üst.dy = 0

        boru_alt = turtle.Turtle()
        boru_alt.speed(0)
        boru_alt.color("red")
        boru_alt.shape("square")
        boru_alt.h = 40 - boru_üst.h - random.randint(1, 10)
        boru_alt.shapesize(boru_alt.h, 2, outline=None)
        boru_alt.penup()
        boru_alt.goto(300, -250)
        boru_alt.dx = -3
        boru_alt.dy = 0

        borular.append((boru_üst, boru_alt))

    y = kuş.ycor()
    y += kuş.dy
    kuş.sety(y)

    if len(borular) >0:
        for boru in borular:
            x = boru[0].xcor()
            x += boru[0].dx
            boru[0].setx(x)

            x = boru[1].xcor()
            x += boru[1].dx
            boru[1].setx(x)

            if boru[0].xcor() < -300:
                boru[0].hideturtle()
                boru[1].hideturtle()
                borular.pop(borular.index(boru))

            if (kuş.xcor() + 10 > boru[0].xcor() - 20) and (kuş.xcor() - 10 < boru[0].xcor() + 20):
                if (kuş.ycor() + 10 > boru[0].ycor() - boru[0].h*10) or (kuş.ycor() - 10 < boru[1].ycor() + boru[1].h*10): #piksele çevirmek için 10'la çarp
                    print("Kuş Yaralandı")
                    score -= 1
                    puan.clear()
                    puan.write(f"Puan: {score}", align="center", font=("Courier", 24, "bold"))

    if score < 0:
        puan.clear()
        puan.write("Kuş Öldü", align="center", font=("Courier", 24, "bold"))
        print("Kuş Öldü")

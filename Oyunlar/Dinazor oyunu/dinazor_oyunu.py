import turtle, random, time

pencere = turtle.Screen()
pencere.title("Dinazor Oyunu")
pencere.bgcolor("black")
pencere.setup(height=500, width=800)
pencere.bgpic("back.gif")
pencere.tracer(0)

pencere.register_shape("dino.gif")
pencere.register_shape("cactus.gif")

dino = turtle.Turtle()
dino.speed(0)
dino.shape("dino.gif")
dino.color("green")
dino.penup()
dino.dy = 0
dino.durum = "hazır"
dino.goto(-200, -50)

kaktüs = turtle.Turtle()
kaktüs.speed(0)
kaktüs.shape("cactus.gif")
kaktüs.color("grey")
kaktüs.penup()
kaktüs.dx = -5
kaktüs.goto(200, -70)

yerçekimi = -0.5

puan = 100

def atla():
    if dino.durum == "hazır":
        dino.dy = 12
    dino.durum = "zıplıyor"

pencere.listen()
pencere.onkeypress(atla, "space")

while True:
    time.sleep(0.003)

    if dino.ycor() < -50:
        dino.sety(-50)
        dino.dy = 0
        dino.durum = "hazır"

    if dino.ycor() != -50 and dino.durum == "zıplıyor":
        dino.dy += yerçekimi

    y = dino.ycor()
    y += dino.dy
    dino.sety(y)

    x = kaktüs.xcor()
    x += kaktüs.dx
    kaktüs.setx(x)

    if kaktüs.xcor() < -400:
        x = random.randint(400, 600)
        kaktüs.setx(x)
        kaktüs.dx *= 1.005

    if kaktüs.distance(dino) < 30:
        puan -= 1
        print(f"Puan: {puan}")
        if puan < 0:
            print("Dinazor Öldü")

    pencere.update()
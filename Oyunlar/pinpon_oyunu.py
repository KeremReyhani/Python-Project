import turtle

pencere = turtle.Screen()
pencere.title("PingPong")
pencere.bgcolor("black")
pencere.setup(width=800, height=600)
pencere.tracer(0) #güncelleme olmayacak

raket_a = turtle.Turtle()
raket_a.speed(0)
raket_a.shape("square")
raket_a.color("white")
raket_a.penup()
raket_a.goto(-350, 0)
raket_a.shapesize(5, 1)

raket_b = turtle.Turtle()
raket_b.speed(0)
raket_b.shape("square")
raket_b.color("white")
raket_b.penup()
raket_b.goto(350, 0)
raket_b.shapesize(5, 1)

ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.dx = 0.15 #hareket etmesi için
ball.dy = 0.15

yazı = turtle.Turtle()
yazı.speed(0)
yazı.color("white")
yazı.penup()
yazı.goto(0, 260)
yazı.write("Oyuncu A: 0  Oyuncu B: 0", align="center", font=("Courier", 24, "bold"))
yazı.hideturtle()

puan_a = 0
puan_b = 0

def raket_a_up():
    y = raket_a.ycor()
    y = y + 30
    raket_a.sety(y) #yeni değeri belirle

def raket_a_down():
    y = raket_a.ycor()
    y = y - 30
    raket_a.sety(y) #yeni değeri belirle

def raket_b_up():
    y = raket_b.ycor()
    y = y + 30
    raket_b.sety(y) #yeni değeri belirle

def raket_b_down():
    y = raket_b.ycor()
    y = y - 30
    raket_b.sety(y) #yeni değeri belirle

pencere.listen()
pencere.onkeypress(raket_a_up, "w")
pencere.onkeypress(raket_a_down, "s")
pencere.onkeypress(raket_b_up, "Up")
pencere.onkeypress(raket_b_down, "Down")

while True:
    pencere.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy),

    if ball.ycor() > 290 or ball.ycor() < -290: #yukarda ve aşağıda yön değiştirecek
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        puan_a += 1
        yazı.clear()
        yazı.write(f"Oyuncu A: {puan_a}  Oyuncu B: {puan_b}", align="center", font=("Courier", 24, "bold"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        puan_b += 1
        yazı.clear()
        yazı.write(f"Oyuncu A: {puan_a}  Oyuncu B: {puan_b}", align="center", font=("Courier", 24, "bold"))

    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < raket_b.ycor() + 60 and ball.ycor() > raket_b.ycor() - 60): #top rakete çarpınca
        ball.setx(340)
        ball.dx *= -1

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < raket_a.ycor() + 60 and ball.ycor() > raket_a.ycor() - 60):
        ball.setx(-340)
        ball.dx *= -1
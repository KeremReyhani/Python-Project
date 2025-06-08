import turtle, random, time

def puan(x, y): #click yapılan konum
    global p
    p += 1
    ok.goto(random.randint(-300, 300), random.randint(-300, 300)) #bastığında yeri deiğişyor

pencere = turtle.Screen()
pencere.title("Fare Oyunu")
pencere.bgcolor("lightgreen")
pencere.setup(width=600, height=600)

ok = turtle.Turtle()
ok.speed(0)
ok.shape("circle")
ok.color("red")
ok.shapesize(3)
ok.penup()
ok.goto(random.randint(-300, 300), random.randint(-300, 300))

p = 0
score = turtle.Turtle()
score.speed(0)
score.shape("square")
score.color("white")
score.penup()
score.goto(0, 260)
score.hideturtle()
score.write("Başla", align="center", font=("Courier", 24, "normal"))

süre = 5
while True:
    baş_süre =time.time()
    while time.time() - baş_süre < süre:
        ok.onclick(puan)
    else:
        score.clear()
        score.write(f"Puan {p}", align="center", font=("Courier", 24, "normal"))
        time.sleep(2)
        p = 0
        score.write("Başla", align="center", font=("Courier", 24, "normal"))
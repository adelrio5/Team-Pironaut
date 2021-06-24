# Importing necessary libraries
import turtle
import csv

# Setup of screen
screen= turtle.Screen()
screen.setup(720, 360)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic('map.gif')


# Setup of turtle navigation and appearance
dot = turtle.Turtle()
dot.color('yellow')
dot.hideturtle()
dot.penup()


with open('data.csv', mode='r') as data:
    reader = csv.reader(data)
    # Ignore header row
    next(reader)
    for row in reader:
        y, x = (round(float(row[1]), 0), round(float(row[2]), 0))
        
        # Navigate to x and y position and draw dot
        dot.goto(x, y)
        dot.dot(5)
                       
            
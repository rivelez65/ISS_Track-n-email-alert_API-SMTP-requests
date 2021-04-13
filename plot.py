from turtle import Turtle, Screen

ALIGNMENT = 'center'
FONT = ('Courier', 8, 'normal')


class IssPlotter:
    def __init__(self):

        self.t = Turtle()
        self.screen = Screen()
        self.screen.title("ISS PLOTTER")

        self.image = "worldmap_grid.gif"

        self.screen.addshape(self.image)
        self.t.shape(self.image)
        self.t.goto(-16, 11)
        self.iss = Turtle()
        self.iss.shape('circle')
        self.iss.shapesize(0.25, 0.25)
        self.iss.penup()


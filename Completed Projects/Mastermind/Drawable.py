"""
    Daniel Gonzalez
    Mastermind: Drawable
"""

import turtle
from Settings import Settings

class Drawable:

    """Drawable is an object that must have a draw method.
    Reduces code repetition by handling the creation of turtle objects
    used to draw."""

    def __init__(self, pen=None):
        """Constructor method
        pen - turtle object used to draw. If none, creates one"""

        if( (pen == None) or (not isinstance(pen, turtle.Turtle))):
            self.pen = self.new_pen()
        else:
            self.pen = pen

    def new_pen(self):
        """new_pen() reates a new turtle object with the default settings needed for this program.
            Returns the turtle"""

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.width(3)
        pen.pencolor(Settings().get_setting('linecolor'))
        pen.fillcolor(Settings().get_setting('fillcolor'))
        return pen

    def move_pen_to(self, x, y):
        """Moves the pen object to the specified coordinates without drawing.
            Heading is set to 90.
            x, y - (x,y) coordinates to move the turtle to"""

        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.seth(90)

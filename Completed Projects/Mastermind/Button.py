"""
    Daniel Gonzalez
    Mastermind: Button
"""

from Circle import *


class Button(Circle):
    """ A Menu button has a shape to specify what actions should be taken if it is clicked.
        It is given a different symbol and color depending on the type of button. The buttons
        provide no actions, only defining its shape and size. When clicked, the controller
        will have to decide what to do next."""

    def __init__(self, x, y, shape,
                 radius=10,
                 pen=None):
        """Constructor
            x, y - (x,y) coordinates of the button
            shape - string representing type of button
            radius - size of button's radius
            pen - turtle object used to draw the button"""

        Circle.__init__(self, x, y, radius, pen)
        self.shape = shape

    def draw(self):
        # Simple circle, but color/symbol changes depending on shape
        self.pen.width(10)
        if (self.shape == "QUIT"):
            Circle.fill(self, "medium violet red", True)
            self.pen.pencolor("white")
            self.pen.width(8)
            # Power button shape
            Drawable.move_pen_to(self, self.x + self.radius / 2, self.y)
            self.pen.circle(self.radius / 2)
            Drawable.move_pen_to(self, self.x, self.y)
            self.pen.forward(self.radius / 1.5)

        elif (self.shape == "ENTER"):
            Circle.fill(self, "blue", True)
            self.pen.pencolor("white")
            # Draws a check shape
            Drawable.move_pen_to(self, self.x + self.radius / 2, self.y + self.radius / 2)
            self.pen.goto(self.x, self.y - self.radius / 2)
            self.pen.goto(self.x - self.radius / 2, self.y - self.radius / 10)

        elif (self.shape == "CLEAR"):
            Circle.fill(self, "red", True)
            self.pen.pencolor("white")
            # Line top right to bottom left
            Drawable.move_pen_to(self, self.x + self.radius / 2, self.y + self.radius / 2)
            self.pen.goto(self.x - self.radius / 2, self.y - self.radius / 2)
            # Line top left to bottom right
            Circle.move_pen_to(self, self.x - self.radius / 2, self.y + self.radius / 2)
            self.pen.goto(self.x + self.radius / 2, self.y - self.radius / 2)
        elif (self.shape == "HELP"):
            Circle.fill(self, "orange", True)
            self.pen.pencolor("white")
            # Draw a '?'
            Circle.move_pen_to(self, self.x, self.y - self.radius / 4)
            self.pen.seth(0)
            self.pen.circle(self.radius / 2.3, 240)
            Circle.move_pen_to(self, self.x, self.y - self.radius / 4)
            self.pen.goto(self.x, self.y - self.radius / 3.2)
            Circle.move_pen_to(self, self.x, self.y - self.radius / 1.5)
            self.pen.dot(size=10)

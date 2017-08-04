# models.py
# Thomas Noone tgn8 and Theodore Comora thc34
# 12/10/2014
"""Models module for Breakout

This module contains the model classes for the Breakout game. Anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, both paddle
and individual bricks can just be instances of GRectangle.  There is no need for a
new class in the case of these objects.

We only need a new class when we have to add extra features to our objects.  That
is why we have classes for Ball and BrickWall.  Ball is usually a subclass of GEllipse,
but it needs extra methods for movement and bouncing.  Similarly, BrickWall needs
methods for accessing and removing individual bricks.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


class BrickWall(object):
    """An instance represents the layer of bricks in the game.  When the wall is
    empty, the game is over and the player has won. This model class keeps track of
    all of the bricks in the game, allowing them to be added or removed.
    
    INSTANCE ATTRIBUTES:
        _bricks [list of GRectangle, can be empty]:
            This is the list of currently active bricks in the game.  When a brick
            is destroyed, it is removed from the list.
    
    As you can see, this attribute is hidden.  You may find that you want to access 
    a brick from class Gameplay. It is okay if you do that,  but you MAY NOT 
    ACCESS THE ATTRIBUTE DIRECTLY. You must use a getter and/or setter for any 
    attribute that you need to access in GameController.  Only add the getters and 
    setters that you need.
    
    We highly recommend a getter called getBrickAt(x,y).  This method returns the first
    brick it finds for which the point (x,y) is INSIDE the brick.  This is useful for
    collision detection (e.g. it is a helper for _getCollidingObject).
    
    You will probably want a draw method too.  Otherwise, you need getters in Gameplay
    to draw the individual bricks.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    def getBricks(self):
        '''Returns the list of bricks in the initial state of the game'''
        return self._bricks
    
    def __init__(self):
        '''Sets the initial state of the bricks in the game.
        Changes the bricks x value based on its column
        Changes the bricks y value based on its row
        changes the bricks color based on its row'''
        self._bricks = []
        for x in range(0,BRICKS_IN_ROW):
            for y in range(0,BRICK_ROWS):
                self._bricks.append(GRectangle(x=BRICK_SEP_H/2 + x*BRICK_WIDTH
                                    + x*BRICK_SEP_H,y=620-BRICK_Y_OFFSET - BRICK_HEIGHT*y - y*BRICK_SEP_V,width=
                                    BRICK_WIDTH,height=BRICK_HEIGHT,linecolor = ROW_COLORS[y], fillcolor= ROW_COLORS[y]))
    
    def draw(self,view):
        '''Draws the bricks'''
        for x in self._bricks:
            x.draw(view)
    

class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Gameplay will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    In addition you must add the following methods in this class: an __init__
    method to set the starting velocity and a method to "move" the ball.  The
    __init__ method will need to use the __init__ from GEllipse as a helper.
    The move method should adjust the ball position according to  the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    def __init__(self):
        '''Creates the ball and its initial location
        Creates the ball's initial velocity in the x and y direction
        Velocity x direction is randomized so it does not fall the same
        way each time.'''
        
        GEllipse.__init__(self,x = GAME_WIDTH/2 - BALL_DIAMETER/2,y = GAME_HEIGHT/2,width = BALL_DIAMETER,height = BALL_DIAMETER,fillcolor = colormodel.RED)
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1.0, 1.0])
        
    def getVy(self):
        '''Returns: the velocity in the y direction'''
        return self._vy
    
    def getVx(self):
        '''Returns: the velocity in the x direction'''
        return self._vx
    
    def setVy(self, v):
        '''Sets the velocity in the y direction equal to v
        
        Precondition: v is a float.
        '''
        self._vy = v
        
    def setVx(self, v):
        '''Sets the velocity in the x direction equal to v
        
        Precondition: v is a float.
        '''
        self._vx = v
    
    def moveBall(self):
        '''Changes the y position of the ball with respect to the y-velocity
        Changes the x position of the ball with respect to the x-velocity'''
        
        self.x = self.x + self._vx
        self.y = self.y + self._vy
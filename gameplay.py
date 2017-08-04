# gameplay.py
# Thomas Noone tgn8 and Theodore Comora thc34
# 12/10/2014
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Gameplay represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Gameplay.

The subcontroller Gameplay manages the paddle, ball, and bricks.  These are model
objects.  The ball and the bricks are represented by classes stored in models.py.
The paddle does not need a new class (unless you want one), as it is an instance
of GRectangle provided by game2d.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *

class Gameplay(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is
    won, it stops animating.  You should create a NEW instance of 
    Gameplay (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    
    INSTANCE ATTRIBUTES:
        _wall   [BrickWall]:  the bricks still remaining 
        _paddle [GRectangle]: the paddle to play with 
        _ball [Ball, or None if waiting for a serve]: 
            the ball to animate
        _last [GPoint, or None if mouse button is not pressed]:  
            last mouse position (if Button pressed)
        _tries  [int >= 0]:   the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    might want to make a Paddle class for your paddle.  If you make changes,
    please change the invariants above.  Also, if you add more attributes,
    put them and their invariants below.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _win     [bool]:
            True indicates that the player has eliminated all of the bricks, so
            that breakout can enter STATE_WIN.
        _touchCount [int >= 0]:
            Amount of times the ball has made contact with the paddle.
            After 7 times, the speed of the ball will increase
    """
    def getBall(self):
        '''Returns: the ball as a Ball object.
        
        This method returns the attribute _ball directly. Any changes
        made to this will modify the ball.'''
        return self._ball
    
    def setBall(self, ball):
        "Sets the the ball to animate equal to ball"
        self._ball = ball
    
    def getTries(self):
        '''Returns: the number of tries left as an int'''
        return self._tries
    
    def getWin(self):
        '''Returns: the win attribute (bool) of the current game state
        
        This will return True when the bricks have been eliminated.'''
        return self._win
    
    def __init__(self):
        '''This initializes the game state.
        
        The wall and paddle are initialized right away because they are
        seen during STATE_COUNTDOWN. _ball begins as none and will be initialized
        in createBall(). _tries starts at the max value dictated by constants.py.
        _win begins as False and will only turn to true when the wall of bricks is empty.
        '''
        self._wall = BrickWall()
        self._paddle = GRectangle(x=GAME_WIDTH/2-PADDLE_WIDTH/2,y=PADDLE_OFFSET,width= PADDLE_WIDTH,height=PADDLE_HEIGHT, linecolor = colormodel.RGB(0,0,0), fillcolor = colormodel.RGB(0,0,0))
        self._last = None
        self._ball = None
        self._tries = NUMBER_TURNS
        self._win = False
        self._touchCount = 0
    
    def draw(self,view):
        '''Draw the paddle and wall'''
        self._wall.draw(view)
        self._paddle.draw(view)
    
    def createBall(self):
        '''Creates the ball. This is separate from the initializer
        because it should be created only in STATE_ACTIVE.'''
        self._ball = Ball()
        
    def drawBall(self, view):
        '''Draw the ball'''
        self._ball.draw(view)
    
    def updatePaddle(self, touch):
        '''This method allows the user to slide the paddle sideways, without
        making the paddle teleport to where the user clicked.
        When touch is equal to None, there has been no click.
        When the last mouse position is None and touch is not None, last becomes the first click
        When the last mouse position and touch are not None, the method will call _movePaddle
        because the cursor has changed positions.'''
        
        if touch == None:
            self._last = None
        elif self._last == None and touch != None: 
            self._last = touch    
        elif self._last != None and touch != None:
            self._movePaddle(touch)
                
    def _movePaddle(self, touch):
        '''This method is called upon by updatePaddle, and it ensures that the paddle will slide
        but will not transport'''
        
        distance = touch.x - self._last.x
        if self._paddle.x + distance < 0:
            self._paddle.x = 0
        elif self._paddle.x + PADDLE_WIDTH > GAME_WIDTH:
            self._paddle.x = GAME_WIDTH - PADDLE_WIDTH
        else:
            self._paddle.x = self._paddle.x + distance
        self._last = touch
    
    def updateBall(self):
        '''This method will update the ball's velocity after colliding with a wall.
        
           It calls _processCollision to detect collision with the paddle or bricks.
           When the ball reaches the bottom of the screen, the _tries attribute is
           decreased by 1.
           
           This method also checks if the touchCount reaches 7, in which the speed
           is increased.
        '''
        xvelocity = self._ball.getVx()
        yvelocity = self._ball.getVy()
        if self._ball.x + BALL_DIAMETER >= GAME_WIDTH or self._ball.x <= 0:
            self._ball.setVx(-xvelocity)
        elif self._ball.y + BALL_DIAMETER >= GAME_HEIGHT or self._ball.y + BALL_DIAMETER <= 0:
            if yvelocity > 0:
                self._ball.setVy(-yvelocity)
        elif self._ball.y <= 0:
            self._tries = self._tries - 1
            self._touchCount = 0
        self._processCollision()
        if self._touchCount == 10:
            self._ball.setVy(-yvelocity*1.3)
        
    def _processCollision(self):
        '''This method first checks to see if either of the bottom corners of the ball
           make contact with the paddle with the 'contain' method. If so, the y-velocity
           will reverse (we check to make sure that it goes from negative to positive
           to prevent 'bouncing'). Then it checks for all four corners making collisions
           with the bricks, in which case the brick is deleted from _wall.
           Finally, it checks to see if _wall is empty, when _win will change to True'''
        if self._paddle.contains(self._ball.x,self._ball.y):
            velocity = self._ball.getVy()
            if velocity < 0:
                self._ball.setVy(-velocity)
                self._touchCount = self._touchCount + 1
        elif self._paddle.contains(self._ball.x + BALL_DIAMETER, self._ball.y):
            velocity = self._ball.getVy()
            if velocity < 0:
                self._ball.setVy(-velocity)
                self._touchCount = self._touchCount + 1
        for brick in self._wall.getBricks():
            if brick.contains(self._ball.x,self._ball.y):
                velocity = self._ball.getVy()
                if velocity < 0:
                    self._ball.setVy(-velocity)
                self._wall.getBricks().remove(brick)
            elif brick.contains(self._ball.x + BALL_DIAMETER,self._ball.y):
                velocity = self._ball.getVy()
                if velocity < 0:
                    self._ball.setVy(-velocity)
                self._wall.getBricks().remove(brick)
            elif brick.contains(self._ball.x,self._ball.y + BALL_DIAMETER):
                velocity = self._ball.getVy()
                if velocity > 0:
                    self._ball.setVy(-velocity)
                self._wall.getBricks().remove(brick)
            elif brick.contains(self._ball.x + BALL_DIAMETER,self._ball.y + BALL_DIAMETER):
                velocity = self._ball.getVy()
                if velocity > 0:
                    self._ball.setVy(-velocity)
                self._wall.getBricks().remove(brick)
        if self._wall.getBricks() == []:
            self._win = True    

    def score(self):
        '''Generates the current score in the game, which is the amount of Bricks broken'''
        
        score = BRICKS_IN_ROW*BRICK_ROWS - len(self._wall.getBricks())
        return score
    
    def update(self,touch):
        '''Calls the three helper functions that move and update the ball and paddle.
           
           Precondition: touch is a GPoint object received from the game's view.
        '''
        self._ball.moveBall()
        self.updatePaddle(touch)
        self.updateBall()
        
    

# breakout.py
# Thomas Noone tgn8 and Theodore Comora thc34
# 12/10/2014
"""Primary module for Breakout application

This module contains the App controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the gameplay
module or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from gameplay import *
from game2d import *


# PRIMARY RULE: Breakout can only access attributes in gameplay.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is a Breakout App
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method init starts up the game.
        
        Method update either changes the state or updates the Gameplay object
        
        Method draw displays the Gameplay object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the init method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Gameplay.
    Gameplay should have a minimum of two methods: updatePaddle(touch) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView, it is inherited from GameApp]:
            the game view, used in drawing (see examples from class)
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
            the current state of the game represented a value from constants.py
            if the state is STATE_INACTIVE, then there is a welcome message
            if the sate is not STATE_INACTIVE, the welcome message is None
        _last   [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
        _game   [GModel, or None if there is no game currently active]: 
            the game controller, which manages the paddle, ball, and bricks
        _message 
            creates a welcome screen that tells the player to click in order to begin 
    ADDITIONAL INVARIANTS: Attribute _game is only None if _state is STATE_INACTIVE.
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _frames       [int, >=0]
            frames since game is initialized
    _lives        [int >=0]
            number of tries the player has left
    _score        [GLabel]
            a message that is always displayed at the top right corner
            that indiciates the eliminated blocks (makes use of the method
            score in gameplay)
    """
    
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message (in attribute _mssg) saying that the user should 
        press to play a game."""
        self._state = STATE_INACTIVE
        self._game = None
        self._last = None
        self._frames = 0
        self._lives = 3
        
    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, but most
        of the others belong in class Gameplay.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse (_last is None, but view.touch is not None). If so, it 
        (re)starts the game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        Paddle movement should be handled by class Gameplay (NOT in this class).
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Gameplay (NOT in this class).
        Gameplay should have methods named updatePaddle and updateBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_INACTIVE.  All of these checks
        should be in Gameplay, NOT in this class.
        
        While in STATE_GAMEOVER, if the player runs out of lives, the game is over, and
        a game over message is displayed.
        
        STATE_WIN occurs when the player has eliminated all of the bricks and the game is over;
        this is independent of the amount of lives left. A final message is displayed.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly. If dt > 0.5, you have a 
        framerate problem because you are trying to do something too complex."""
        if self._state == STATE_INACTIVE:
            self._message = GLabel(text='Press to Play!', x = GAME_WIDTH/2- 45, y = GAME_HEIGHT/2)
            self._game = Gameplay()
            if self._view.touch != None and self._last == None:
                self._state = STATE_COUNTDOWN
        if self._state == STATE_COUNTDOWN:
            self.countdownHelper()
        if self._state == STATE_ACTIVE:
            self.activeHelper()
        if self._state == STATE_PAUSED:
            self._message = GLabel(text= str(self._game.getTries()) + ' lives left.', x = GAME_WIDTH/2- 45, y = GAME_HEIGHT/2)
            if self._last == None and self._view.touch != None:
                self._frames = 0
                self._state = STATE_COUNTDOWN
        if self._state == STATE_COMPLETE:
            if self._game.getTries() == 0:
                self._message = GLabel(text= 'GAME OVER, YOUR SCORE WAS ' + str(self._game.score()), x = GAME_WIDTH/2- 100, y = GAME_HEIGHT/2)
                if self._last == None and self._view.touch != None:
                    self.init()
            elif self._game.getWin():
                self._message = GLabel(text= 'YOU WIN!', x = GAME_WIDTH/2- 45, y = GAME_HEIGHT/2)
                if self._last == None and self._view.touch != None:
                    self.init()
        self._last = self._view.touch
        
    def activeHelper(self):
        ''' Helper Function for STATE_ACTIVE.
        
            This checks the state of the ball: whenever it's y-position dips
            below 0, breakout will enter STATE_PAUSED. It will not decrease a life,
            because that is done in gameplay. This method will also check if the
            current game's tries have reached 0 or if the _win bool has become True.
            Then the state will change to STATE_COMPLETE.
        '''
        self._score = GLabel(text ='Score: ' + str(self._game.score()), x = 0, y = GAME_HEIGHT - 20)
        self._message = None
        self._game.update(self._view.touch)
        ball = self._game.getBall()
        if ball != None and ball.y <= 0:
            self._state = STATE_PAUSED
        if self._game.getTries() == 0 or self._game.getWin():
                self._state = STATE_COMPLETE
                
    def countdownHelper(self):
        ''' Helper Function for STATE_COUNTDOWN. This displays the seconds before entering STATE_ACTIVE
            
            When frames since the initialization of the state are between 0 and 60 (one second),
            the screen will display '3'. Breakout will then countdown from 3 before
            creating the ball and going into STATE_ACTIVE.
        '''
        self._game.updatePaddle(self._view.touch)
        self._frames = self._frames + 1
        self._score = GLabel(text = 'Score: ' + str(self._game.score()), x = 0, y = GAME_HEIGHT - 20)
        if 0 < self._frames <= 60:
            self._message = GLabel(text='3', x = GAME_WIDTH/2-3, y = GAME_HEIGHT/2+20) 
        if 60 < self._frames <= 120:
            self._message = GLabel(text='2', x = GAME_WIDTH/2-3, y = GAME_HEIGHT/2+20) 
        if 120 < self._frames <= 180:
            self._message = GLabel(text='1', x = GAME_WIDTH/2-3, y = GAME_HEIGHT/2+20)
        if self._frames > 180:
            self._game.createBall()
            self._state = STATE_ACTIVE
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Gameplay. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Gameplay.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if self._state == STATE_INACTIVE:
            self._message.draw(self.view)
        elif self._state == STATE_COUNTDOWN:
            self._game.draw(self.view)
            self._message.draw(self.view)
            self._score.draw(self.view)
        elif self._state == STATE_PAUSED:
            self._game.draw(self.view)
            self._message.draw(self.view)
            self._score.draw(self.view)
        elif self._state == STATE_COMPLETE:
            self._message.draw(self.view)
        else:
            self._game.draw(self.view)
            self._game.drawBall(self.view)
            self._score.draw(self.view)
'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 4: Bricka Game AI
'''
#########################################################################
# Reinforcement learning parameters
#########################################################################

class FV():
    def __init__(self):
        self.num_paddle_x = 15
        self.num_ball_x = 15
        self.num_ball_y = 4
        self.num_ball_dir = 2  # (top_left, top_right, bottom_left, bottom_right)
        self.num_brick_state = 256  # 2**8
        self.num_actions = 30
        
        self.action_stand_still = int(self.num_actions/2.0)
        
        self.total_num_states = self.num_paddle_x * self.num_ball_x * self.num_ball_y * self.num_ball_dir
        
        self.ALPHA = 0.5
        self.LAMBDA = 0.5
        self.EPSILON = 0.5
        
        #########################################################################
        # Game Play Parameters
        #########################################################################
        self.SCREEN_SIZE   = [640,480]
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.SCREEN_SIZE
        
#        self.HIDE_BRICKS = True
        self.HIDE_BRICKS = False
        
        self.BRICK_WIDTH   = 60
        self.BRICK_HEIGHT  = 15
        self.PADDLE_WIDTH  = 60
        self.PADDLE_HEIGHT = 12
        self.BALL_DIAMETER = 16
        self.BALL_RADIUS   = self.BALL_DIAMETER / 2
        
        self.MAX_PADDLE_X = self.SCREEN_SIZE[0] - self.PADDLE_WIDTH
        self.MAX_BALL_X   = self.SCREEN_SIZE[0] - self.BALL_DIAMETER
        self.MAX_BALL_Y   = self.SCREEN_SIZE[1] - self.BALL_DIAMETER
        
        # Paddle Y coordinate
        self.PADDLE_Y = self.SCREEN_SIZE[1] - self.PADDLE_HEIGHT - 10
        
        # Colour constants
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.BLUE  = (0,0,255)
        self.BRICK_COLOR = (200,200,0)
        
        # State constants
        self.STATE_BALL_IN_PADDLE = 0
        self.STATE_PLAYING = 1
        self.STATE_WON = 2
        self.STATE_GAME_OVER = 3
        
        # Added Variables:
        self.ball_speed = 5
        self.ball_increment = 0.00  ################# MAKE THIS 0 if you DONT want the speed to increase
        self.paddle_speed = 5





































"""
 bricka (a breakout clone)
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com

 Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

 Exercise 4: Bricka Game AI
"""
import sys
import pygame
import numpy as np
import reinforcement_learner as RL
import pickle
import time

import fixed_variables as FV
import matplotlib.pyplot as plt

class Bricka:

    def __init__(self, file_name=None):
        pygame.init()
        
        Q = None
        if file_name == None:
            self.FV = FV.FV()
        else:
            [self.FV, Q] = self.load_trained_system(file_name)         
            
        self.screen = pygame.display.set_mode(self.FV.SCREEN_SIZE)
        pygame.display.set_caption("bricka (a breakout clone by codeNtronix.com)")
        
        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()
        self.ai = RL.AI(self, Q)
    
        self.num_total_deaths = 0    
        self.num_total_hits = 0 #Number of times ball hits paddle
    
    
    def load_trained_system(self, file_name):
        obj = pickle.load(open(file_name, "r"))
        return obj

    def save_trained_system(self, file_name):
        obj = [self.FV, self.ai.Q]        
        pickle.dump(obj, open(file_name, "w+"))
        
    def init_game(self):
        self.lives = 1
        self.score = 0
        
        self.state = self.FV.STATE_BALL_IN_PADDLE
        self.episode_hits = 0

        random_paddle_pos = np.random.randint(0, self.FV.MAX_PADDLE_X)        
        
        self.paddle   = pygame.Rect(random_paddle_pos,self.FV.PADDLE_Y, self.FV.PADDLE_WIDTH, self.FV.PADDLE_HEIGHT)
        self.ball     = pygame.Rect(random_paddle_pos, self.FV.PADDLE_Y - self.FV.BALL_DIAMETER, self.FV.BALL_DIAMETER, self.FV.BALL_DIAMETER)
        self.ball_vel = [self.FV.ball_speed, -self.FV.ball_speed]
        
        created = self.create_bricks()
        
        self.num_bricks = 0
        if created != False:
            self.num_bricks = len(self.bricks)
        

    def reset_game(self):
        self.init_game()
        self.state = self.FV.STATE_PLAYING

    def create_bricks(self):
        if self.FV.HIDE_BRICKS == True:
            return False
        self.bricks = [] 
        y_ofs = 35
        for i in range(7):
            x_ofs = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs, self.FV.BRICK_WIDTH, self.FV.BRICK_HEIGHT))
                x_ofs += self.FV.BRICK_WIDTH + 10
            y_ofs += self.FV.BRICK_HEIGHT + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, self.FV.BRICK_COLOR, brick)
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
#        if keys[pygame.K_LEFT]:
#            self.paddle.left -= self.FV.paddle_speed
#            if self.paddle.left < 0:
#                self.paddle.left = 0
##            print "Paddle.left = ", self.paddle.left
#
#        if keys[pygame.K_RIGHT]:
#            self.paddle.left += self.FV.paddle_speed
#            if self.paddle.left > self.FV.MAX_PADDLE_X:
#                self.paddle.left = self.FV.MAX_PADDLE_X
##            print "Paddle.left = ", self.paddle.left

        if keys[pygame.K_SPACE] and self.state == self.FV.STATE_BALL_IN_PADDLE:
            up_right = [self.FV.ball_speed, -self.FV.ball_speed]
            self.ball_vel[0] = up_right[0] #Go up right
            self.ball_vel[1] = up_right[1]            
            self.state = self.FV.STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == self.FV.STATE_GAME_OVER or self.state == self.FV.STATE_WON):
            self.init_game()

    def move_ball(self):
        self.ball_vel[0] += self.FV.ball_increment * np.sign(self.ball_vel[0])
        self.ball_vel[1] += self.FV.ball_increment * np.sign(self.ball_vel[1])
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]
        

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= self.FV.MAX_BALL_X:
            self.ball.left = self.FV.MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= self.FV.MAX_BALL_Y:            
            self.ball.top = self.FV.MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break
        self.num_bricks = len(self.bricks)
        
        if len(self.bricks) == 0 and self.FV.HIDE_BRICKS == False:
            self.state = self.FV.STATE_WON
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = self.FV.PADDLE_Y - self.FV.BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
            self.episode_hits += 1
            self.num_total_hits += 1
            
        elif self.ball.top > self.paddle.top:
            #Lost round
            self.lives -= 1
            if self.lives > 0:
                self.state = self.FV.STATE_BALL_IN_PADDLE
            else:
                #Lost all lives
                self.state = self.FV.STATE_GAME_OVER

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("S: " + str(self.score) + " L: " \
            + str(self.lives) + " EpiHits = " + str(self.episode_hits) + "...Total Hits = " + str(self.num_total_hits)\
            + " Total Deaths = " + str(self.num_total_deaths), False, self.FV.WHITE)
            self.screen.blit(font_surface, (0,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, self.FV.WHITE)
            x = (self.FV.SCREEN_SIZE[0] - size[0]) / 2
            y = (self.FV.SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
        
    def check_state(self):
        ''' Depending on state move ball or display messages '''
        if self.state == self.FV.STATE_PLAYING:
            self.move_ball()
            self.handle_collisions()
        elif self.state == self.FV.STATE_BALL_IN_PADDLE:
            self.ball_vel = [self.FV.ball_speed, -self.FV.ball_speed]
            self.ball.left = self.paddle.left + self.paddle.width / 2
            self.ball.top  = self.paddle.top - self.ball.height
            self.show_message("PRESS SPACE TO LAUNCH THE BALL")
        elif self.state == self.FV.STATE_GAME_OVER:
            self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
        elif self.state == self.FV.STATE_WON:
            self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
    
    def draw_objects(self):
        ''' Draw bricks, paddle and ball '''
        self.show_stats()
        self.draw_bricks()
        
        pygame.draw.rect(self.screen, self.FV.BLUE, self.paddle) # Draw paddle
        pygame.draw.circle(self.screen, self.FV.WHITE, (self.ball.left + self.FV.BALL_RADIUS, self.ball.top + self.FV.BALL_RADIUS), self.FV.BALL_RADIUS) # Draw ball

        #Actually draw it on board
        pygame.display.flip()
    
    def run(self):
        '''
        This function is called when the training needs to be started or continued.
        It uses Reinforcement Learning to learn how to play the game.
        '''
        self.state = self.FV.STATE_PLAYING
        
        print "State = ", np.shape(self.ai.Q)
        print "num_paddle_x = ", self.FV.num_paddle_x
        print "num_ball_x = ", self.FV.num_ball_x
        print "num_ball_y = ", self.FV.num_ball_y
        print "num_ball_dir = ", self.FV.num_ball_dir # (top_left, top_right, bottom_left, bottom_right)
        print "num_brick_state = ", self.FV.num_brick_state #2**8
        print "num_actions = ", self.FV.num_actions
        print "HIDE_BRICKS = ", self.FV.HIDE_BRICKS
        
        try:
            self.run_training()
        except KeyboardInterrupt:
            print "Svaing And then Exiting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            file_name = "./trained/system_%d_%d.pickle"%(self.num_total_deaths, time.time())
            self.save_trained_system(file_name)
            
            print "State = ", np.shape(self.ai.Q)
            print "num_paddle_x = ", self.FV.num_paddle_x
            print "num_ball_x = ", self.FV.num_ball_x
            print "num_ball_y = ", self.FV.num_ball_y
            print "num_ball_dir = ", self.FV.num_ball_dir # (top_left, top_right, bottom_left, bottom_right)
            print "num_brick_state = ", self.FV.num_brick_state #2**8
            print "num_actions = ", self.FV.num_actions
            print "HIDE_BRICKS = ", self.FV.HIDE_BRICKS            
            
            exit(0)
            
    def run_training(self):  
        '''
        This function does the actual learning. It runs the learning episodes for ever
        until the program is cancelled. At this point it stores the Q table
        and saves it so that it can be tested later on.
        '''
        
        self.FV.ball_increment = 0.00   
        
        # Stats to check performance of system during learning
        previous = 0       
        longest_run = 0
        while 1:     
            self.clock.tick() # Program will never run more then 50 frames per second.
            self.screen.fill(self.FV.BLACK)
            self.ai.q_learn_move() # Makes random move or (so far) intelligent move.
            
            self.check_state()
            # Get new reward and state
            reward = self.ai.get_reward() 
            next_state = RL.State_Convertor().get_state(self)  # Get the current state of the system
            
            # Update Q  
            self.ai.update_Q(reward, next_state)
            
#            self.draw_objects()
                
            # Keep statistics for displaying to user while learning to measure performance.
            if self.episode_hits > longest_run: longest_run = self.episode_hits
            
            if self.state == self.FV.STATE_GAME_OVER:
                self.num_total_deaths += 1  # Increment Number of Deaths
                
                # Every 100 deaths log status of system to terminal for user
                if self.num_total_deaths%100 == 0:
                    self.ai.decrease_ALPHA(0.005)  # Decrement alpha parameter
                    self.ai.decrease_EPSILON(0.005)  # Decrement epsilon parameter so it will explore less
                    
                    print "--------------------------------------------------------------------------------------"
                    print "alpha = ", self.FV.ALPHA, ". epsilon = ", self.FV.EPSILON
                    
                    
                    print "S: " + str(self.score) + " L: " \
                        + str(self.lives) + " EpiHits = " + str(self.episode_hits) + "...Total Hits = " + str(self.num_total_hits)\
                        + " Total Deaths = " + str(self.num_total_deaths)   + "..... improved by: " + str(self.num_total_hits - previous)  \
                        + "..Longest Epi: " + str(longest_run)
            
                    longest_run = 0
                    previous = self.num_total_hits
                
                if len(self.bricks) == 0:
                    self.FV.HIDE_BRICKS = False                
                else:
                    self.FV.HIDE_BRICKS = True
                self.reset_game()
                
            elif self.state == self.FV.STATE_WON:
                self.FV.HIDE_BRICKS = False                
                self.reset_game()
            
            pygame.event.pump()

    def test_ai(self, increase_ball_speed):
        '''
        This function is very similar to the one before where it trains the system.
        Only that it does NOT update the Q matrix in any way. It will always choose
        the best move given the current state and play the game.
        '''
#        print "State = ", np.shape(self.ai.Q)
#        print "num_paddle_x = ", self.FV.num_paddle_x
#        print "num_ball_x = ", self.FV.num_ball_x
#        print "num_ball_y = ", self.FV.num_ball_y
#        print "num_ball_dir = ", self.FV.num_ball_dir # (top_left, top_right, bottom_left, bottom_right)
#        print "num_brick_state = ", self.FV.num_brick_state #2**8
#        print "num_actions = ", self.FV.num_actions
#        print "HIDE_BRICKS = ", self.FV.HIDE_BRICKS  
        
        self.FV.HIDE_BRICKS = False
        self.create_bricks()        
        
        if increase_ball_speed == 1:
            self.FV.ball_increment = 0.01
        else:
            self.FV.ball_increment = 0.00        
        
        self.state = self.FV.STATE_PLAYING
        self.FV.EPSILON = 0.0
        
        tic = time.time()        
        while 1:     
#            print "Ball velocity = ", self.ball_vel, increase_ball_speed
            self.clock.tick(50)  # Program will never run more then 50 frames per second.
            self.screen.fill(self.FV.BLACK)
            
            self.ai.q_learn_move()  # Makes random move or (so far) intelligent move.
#            self.ai.follow_ball()   # Simple AI that follows ball
            self.check_input()
            
            self.check_state()
            self.draw_objects()
            
            if self.state == self.FV.STATE_GAME_OVER:
                self.num_total_deaths += 1  # Increment Number of Deaths
                self.reset_game()
            elif self.state == self.FV.STATE_WON:
                self.reset_game() 
                tac = time.time()
                
#                print "Time stayed alive: ", (tac-tic)
                tic = tac
            
            pygame.event.pump()
if __name__ == "__main__":
    
#    file_name = None
#    if len(sys.argv) == 2:
#        file_name = sys.argv[1]
#    Bricka(file_name).run()
    
    pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

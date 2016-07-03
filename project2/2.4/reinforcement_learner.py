'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 4: Bricka Game AI
'''
import numpy as np

class AI():
    '''
    This class implements a Reinforcement Learning algorithm to learn to play 
    Break Out. It uses TD(0) algorithm to do this.
    
    The game canvas is broken up into grid cells (depending on the variables set)
    and the ball and paddle can be in any of those cells. The position of the ball
    and paddle are used to define the state of the system. Read more about it in the
    State_Converter class.
    
    Different Reward functions have been tested with and the current want is chosen 
    aupon. It can be read at the reward function.
    '''
    
    def __init__(self, model, Q=None):
        self.FV = model.FV
        if Q == None:
            self.Q = np.zeros((self.FV.total_num_states, self.FV.num_actions))
        else:
            self.Q = Q
        self.model = model
        self.curr_action = 5
        self.curr_state = State_Convertor().get_state(self.model)
     
     
    def follow_ball(self):
        '''
        This is the most basic AI approach where the paddle follows the ball.
        It works but fails soon after you start increasing the speed of the ball.
        '''
        paddle_x = self.model.paddle.left + self.FV.PADDLE_WIDTH/2
        ball_x = self.model.ball.left + self.FV.BALL_DIAMETER/2
        paddle_x_vel = ball_x - paddle_x
        paddle_x_vel = max(-10.0, min(paddle_x_vel, 10.0))
        new_left = self.model.paddle.left + paddle_x_vel
        new_left = max(0.0, min(new_left, self.model.FV.MAX_PADDLE_X))
        
        self.model.paddle.left = new_left
        
    def decrease_ALPHA(self, decrease_by):
        self.FV.ALPHA = max(0.1, self.FV.ALPHA - decrease_by)
    
    def decrease_EPSILON(self, decrease_by):
        self.FV.EPSILON = max(0.1, self.FV.EPSILON - decrease_by)
    
    def load_previously_trained(self, file_name):
        return np.load("%s.npy"%file_name)        
        
    def update_Q(self, reward, next_state):
        '''
        This function updates the Q-Table based on the reward and the value of
        the next state.
        '''
        Q = self.Q
        current_quality = Q[self.curr_state,self.curr_action]
        Q[self.curr_state,self.curr_action] += self.FV.ALPHA*(reward + self.FV.LAMBDA * self.max_reward(next_state) - current_quality)
                
    def max_reward(self, state):
        '''
        Returns the action number with the maximum value given the state.
        '''
        return np.max(self.Q[state, :])

    def q_learn_move(self):
        '''
        Makes random move or (so far) intelligent move. Changes the current 
        state by choosing some action.  The action is chosen either randomly to
        explore or by choosing the best to exploit.
        '''
        state = State_Convertor().get_state(self.model)

        action = None
        if np.random.random() < self.FV.EPSILON:  # Explore
            action = np.random.randint(0, self.FV.num_actions)
        else:  # Exploit
            action = self.get_best_action(state)

        self.curr_state = state
        self.curr_action = action
        
        self.take_action(action)  # Takes the action
        
    def get_best_action(self, state):
        '''
        Get the best action by looking at the Q-Table!
        '''
        best_quality = np.max(self.Q[state, :])
        best_list = np.where(self.Q[state, :] == best_quality)[0]
        best_action = np.random.choice(best_list)
        return best_action

    def take_action(self, action):
        '''
        This function applies the action to the system. It will move the ball
        according to the action.
        '''
        paddle_vel = action - self.FV.action_stand_still
        self.model.paddle.left += paddle_vel
#        paddle_vel = max(-2.0*self.FV.paddle_speed, min(paddle_vel, 2.0*self.FV.paddle_speed))
        self.model.paddle.left = max(0.0, min(self.model.paddle.left, self.model.FV.MAX_PADDLE_X))

    def get_reward(self):
        '''
        This function will get the reward of being in a certain state.
        
        If the game is over (death) then it returns a reward of -10000.
        Otherwise: +score (for not dying) - 1*distance_from_ball (This encourages it to 
            keep as close to the ball as possible)
        '''
        if self.model.state == self.FV.STATE_GAME_OVER:
            return -10000
        else:
            reward = 0
            paddle_x = self.model.paddle.left + self.FV.PADDLE_WIDTH/2.0
            ball_x = self.model.ball.left + self.FV.BALL_DIAMETER/2.0
            dist_to_ball = abs(ball_x - paddle_x)
            reward = -1*dist_to_ball  # Distance to ball. This will reduce it
            reward += self.model.score
#            reward += self.model.num_total_hits
#            reward += 1
            return reward
    

class State_Convertor:
    '''
    This converts the current system to a state value. It discretizes the canvas 
    into cells and the ball position, direction and paddle position in this discretized
    grid defines the state.
    
    '''
    def get_state(self, model):
        ''' 
        A by B (A - Ball state and B - Paddle state) 
        
        Returns the CURRENT STATE of the system. It separately calls two other
        functions in order to split up the calculations of the ball_state
        and the paddle_state.
        
        Once there two states are determined, it returns a combination of the two
        numbers and returns it as the state. (Basically converts from a 2D array to
        1D array in essence)
        '''
        ball_state = self.get_ball_state(model)
        paddle_state = self.get_paddle_state(model)
        state = ball_state * model.FV.num_paddle_x + paddle_state
        return state

    def get_paddle_state(self, model):
        '''
        This gets the state of the paddle. The paddle can NOT move up so we do 
        not need to worry about the y-position and only consider the x_position.
        This function returns the x_cell number in the discretized world and returns 
        it as the paddle state.
        
        Should be between 0 and num_paddle_x (e.g: 0 - 32)
        '''
        paddle_x = model.paddle.left + model.FV.PADDLE_WIDTH/2.0
        paddle_state = int(paddle_x/((1.0*model.FV.SCREEN_WIDTH)/model.FV.num_paddle_x))
        return paddle_state


    def get_ball_state(self, model):
        ''' 
        
        This combines the spacial position of the ball state and the direction state
        of the ball. Together these define the ball state.      
        
        Returns ball state integer. Will be between 0 and 
        (num_ball_directions * num_ball_x * num_ball_y) (e.g.: between 0 - 4*32*4)
            A by B (A - Ball Position and B - Ball Direction)        
        '''
        ball_x = model.ball.left + model.FV.BALL_DIAMETER/2.0
        ball_y = model.ball.top + model.FV.BALL_DIAMETER/2.0
        
        cell_x = int(ball_x/(model.FV.SCREEN_WIDTH/(1.0*model.FV.num_ball_x)))
        cell_y = int(ball_y/(model.FV.SCREEN_HEIGHT/(1.0*model.FV.num_ball_y)))
        
        ball_pos_state = model.FV.num_ball_x*cell_y + cell_x
        
        ball_direction = self.get_direction(model)
        ball_state = ball_direction * (model.FV.num_ball_x * model.FV.num_ball_y) + ball_pos_state
        return ball_state
        
    def get_direction(self, model):
        ''' 
        Depends on how many directions we will be working with. So it can also
        just be left or right.
        number with direction = [top_left, top_right, bottom_left, bottom_right] 
        '''
        ball_vel = model.ball_vel
        if ball_vel[0] < 0:  # Left 
            if model.FV.num_ball_dir == 2:  return 0
            if ball_vel[1] < 0: return 0  # Top Left
            else:   return 2  # Bottom Left
        else:  # Right
            if model.FV.num_ball_dir == 2:  return 1
            if ball_vel[1] < 0: return 1  # Top Right
            else:   return 3  # Bottom Right
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
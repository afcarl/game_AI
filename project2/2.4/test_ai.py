'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 4: Bricka Game AI
'''
import sys
import bricka as B

if __name__=="__main__":
    file_name = None
    if len(sys.argv) == 3:
        file_name = sys.argv[1]
        increase_ball_speed = int(sys.argv[2])
        game = B.Bricka(file_name)
        game.test_ai(increase_ball_speed)
        exit(0)
    print "Useage: python test_ai.py <pickle file name> <flag to increase ball speed>\n\t <pickle file name> = BEST_AI.pickle\n\t <flag to increase ball speed> = 0: no increase OR 1: increase ball speed"
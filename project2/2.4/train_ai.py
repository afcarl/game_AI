'''
Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Exercise 4: Bricka Game AI
'''
import sys
import bricka as B

if __name__=="__main__":
    file_name = None
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    B.Bricka(file_name).run()
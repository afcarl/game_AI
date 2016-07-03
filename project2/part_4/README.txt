Project 2. Task 4: Create a AI controller for Bricka.
=====================================================

To run the system you have to run the test_ai.py script. It takes in as argument a pickle data file name. This is contains the learned Q-table allowing it to make moves cleverly. You can use the BEST_AI.pickle file to test the system. To run:

	python test_ai.py BEST_AI.pickle

On the otherhand to train a system from scratch you would have to run the train_ai.py script. It will start the procedure of learning from scratch and will get the parameters of the system in the fixed_variables.py file. When you kill the process (cntrl-c) the system will have the current learned table in the trained directiory, from where it can be read and tested again.








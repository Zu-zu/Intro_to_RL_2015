import game_final as game;
import numpy as np;
import csv;
from mpl_toolkits import mplot3d

import matplotlib.pyplot as plt

#First explicitly define the state array
#for the state matrix, the columns will be expressed in [1,1], [1,2], .. etc and the index of a given
#column c, for a state [x,y] will be c = (x-1)*21 +(y-1)
#Additionally, row 0: hit, row 1: stick actions, row 2: how many times the hit action was performed, row 3: how many times the stick
#row 4: average return on hit, row 5: average return on stick

def MC(iterations):
    # for not hard-code the discount rate
    discount = 0.6

    value_array = np.zeros((210, 6))
    
    
    for x in range(iterations):
    
        init = game.init_state()

        #create an array of states that happened in a given episode
        previous_states = []
        previous_states.append(init)
        #print(previous_states);
        #print(len(previous_states));

        #collect all actions made in the process
        previous_actions = []
        #for now assume purely random policy

        i = 0
        t = False
        stop= False
        while stop == False:
            if t == False:
                i += 1
    
                #if the game needs to continue again
                a = np.random.choice([0,1])
                previous_actions.append(a)

                s, r, t = game.step(init,a)

                previous_states.append(s)
            else:
                #print("end")
                #print("these are the previous actions:")
                #print(previous_actions);
                #print("these are the previous states:")
                #print(previous_states);

                length = len(previous_states)
                for x in range(length-1):
                    chosen_action = previous_actions[x]
                    disc = len(previous_states)-(x+1)
                    value = r*(discount**(disc))
                    [dealer,player] = previous_states[x]
                    c = ((dealer-1)*21)+(player-1)
                    #add to the total value
                    value_array[c][chosen_action] += value
                    #add to the iteration
                    value_array[c][chosen_action+2] += 1
                    #recalculate average
                    value_array[c][chosen_action+4] = (value_array[c][chosen_action])/(value_array[c][chosen_action+2])
                stop = True

    xdata = []
    ydata = []
    zdata = []

    final_array = []
    for a in range(1,10):
        for b in range(1,21):
            final_array.append([a,b,0])
            xdata.append([a])
            ydata.append([b])

    counter = 0
    for x in final_array:
        hit = value_array[counter][4]
        stick = value_array[counter][5]
        if (hit) == (stick):
            final_array[counter][2]=0.5
            zdata.append([0.5])
        elif (hit) > (stick):
            final_array[counter][2] = 1
            zdata.append([1])   
        else:
            final_array[counter][2] = 0
            zdata.append([0])
        counter += 1
    #print(final_array);
    #with open("new_file.csv","w+") as my_csv:
        #csvWriter = csv.writer(my_csv,delimiter=',');
        #csvWriter.writerows(final_array);
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    ax.scatter3D(xdata, ydata, zdata, color = "green")
    plt.show()


                



#run that mothafucka
MC(1000000)


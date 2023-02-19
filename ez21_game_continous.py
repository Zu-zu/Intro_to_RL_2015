#this version of the script allowes a person to play until the end of the chain (until the reward can be determined)


import random
import numpy as np




def rules ():
    #The rules of the game
    # #The game is played with an infinite deck of cards (i.e. cards are sampled with replacement)
    # #Each draw from the deck results in a value between 1 and 10 (uniformly distributed)
    # #with a colour red (probability 1/3) or black (probability 2/3)
    # #There are no aces or picture/faces cards in the game
    # #At the start of the game both the player and the dealer draw one blck card (fully observed)
    # Each turn the player may either stick or hit
    # If the player hits then she draws another card from the deck
    # If the player sticks, she recieves no futher cards
    # The values of the player's cards are added (black cards) or substracted (red cards)
    # If the player's sum exceeds 21, or becomes less than 1, then she goes "bust" and loses the game (reward -1)
    # If the player sticks then the dealer starts taking turns. The dealer always sticks on any sum of 17 or greated,
    # and hits otherwise. If the dealer goes bust, then the player wins, otherwise the outome
    # win (reward +1), lose (reward -1), or draw (reward 0)- is the player with the largest sum
    return


# define the function that is essentially the environment 
def step (s, a):
    terminal_state = False;
    s_dealer, s_player = s;
    r=0;
    s_new = [0,0];
    #s is the state which includes the dealer's first card (1-10) and the player's sum (1-21)
    #a is an action (hit or stick)
    #the returns are the sample of the next state s'(which may be terminal) and reward r
    #case 1: the player sum is either above 21 or below 1, and the player looses
    if s_player >21 or s_player <1:
        print ("you lose");
        r = -1;
        s_new = [s_dealer,s_player]
        terminal_state = True;

    #case 2: the player decides to stick
    colours =[-1, 1];
    if a =="stick":
        #player recieves no further cards 
        #dealer start taking turns
        dealer_sum = s_dealer;
        while dealer_sum <17:
            card = random.randint(1,10);
            colour = np.random.choice(colours, replace=True,p=[1/3,2/3]);
            dealer_sum += (colour*card);
            print("dealer sum: " +str (dealer_sum));
            if dealer_sum >21 or dealer_sum <1:
                print ("Dealer has gone bust!");
                terminal_state= True;
                break
        #we now have both the player sum and the dealer sum.
        s_dealer = dealer_sum;
        s_new = [s_dealer,s_player]
        if dealer_sum >21 or dealer_sum <1:
            r = 1;
            terminal_state= True;
        elif dealer_sum == s_player:
            r =0;
            terminal_state= True;
        elif dealer_sum > s_player:
            r = -1;
            terminal_state= True;
        else:
            r = 1;
            terminal_state= True;
        return s_new, r, terminal_state

    #case 3: the player decided to hit - recieves another card
    elif a == "hit":
        card = random.randint(1,10);
        colour = np.random.choice(colours, replace=True,p=[1/3,2/3] );
        print("your new card is: "+str(card*colour));
        s_player += (colour*card);
        s_new = [s_dealer,s_player]
        print(s_player)
        if s_player >21 or s_player <1:
            print ("you've gone bust!")
            r = -1;
            terminal_state= True;
            
    return s_new, r, terminal_state;

#make a new function that runs the entire game and utilised the function above



def game(s_init):
    action = input("write stick to stop getting new cards and hit to get more cards  ")
    s,r,t = step(s_init,action);
    if t == False:
        game(s);
    else:
        print("final state is: "+ str(s));
        if r ==1:
            print("you've won");
        elif r ==0:
            print("it's a tie!")
        else:
            print("you've lost")
    

def run():
    s_init = [random.randint(1,10),random.randint(1,21)];
    print("your initial sum is: "+ str(s_init[1]))
    print("dealer's first card is: "+ str(s_init[0]));
    game(s_init);


run()
####################
# Project 10       #
# CSE 231 Sect 007 #
####################

#############################################################################
# Assignment Overview                                                       
#   Shamrock Solitare
#           Program creates and deals deck
#           Program moves kings to front of deck                                                      
#       Outputs option menu
#       User inputs card move
#           Program ensures move is viable
#           Program moves card based on user input
#       Prints foundation and tableau for each move                   
#       Prints win when foundation is full                                            
#                                                                                   
#############################################################################

#Starter Code


#DO NOT DELETE THESE LINES
import cards, random
from collections import deque
random.seed(100) #random number generator will always generate 
                 #the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau pile s to end of pile d.
    MTF s d: Move card from end of Tableau pile s to Foundation d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''


def fix_kings(tableau):
    '''
    Intakes Tableau
    Checks for each list item for king
    Moves king to front of list grouping
    '''
    copy = [] #copies and clears cards 
    for cards in tableau:
        copy.append(cards)
    tableau.clear()

    for cardlists in copy:
        if "K" in str(cardlists):
            templist = []
            if "K" in str(cardlists[0]): #if king is in first slot
                if "K" in str(cardlists[1]):
                    tableau.append(cardlists)
                    continue
                if "K" in str(cardlists[2]):
                    #recreates with king in front
                    templist.append(cardlists[0])
                    templist.append(cardlists[2])
                    templist.append(cardlists[1])
                    tableau.append(templist)
                    continue
                else:
                    tableau.append(cardlists)
                    continue
            if "K" in str(cardlists[1]): #if king is in second slot
                #checks backwards and moves to front
                if "K" in str(cardlists[2]):
                    templist.append(cardlists[1])
                    templist.append(cardlists[2])
                    templist.append(cardlists[0])
                    tableau.append(templist)
                    continue
                else:
                    templist.append(cardlists[1])
                    templist.append(cardlists[0])
                    templist.append(cardlists[2])
                    tableau.append(templist)
                    continue
            if "K" in str(cardlists[2]): #if king is in third slot
                #recreates cardlist with king in front
                    templist.append(cardlists[2])
                    templist.append(cardlists[0])
                    templist.append(cardlists[1])
                    tableau.append(templist)
                    continue
        #each options edits original tableau
        else:
            tableau.append(cardlists) 
            continue

                
def initialize():
    ''' 
    Creates empty foundation
    Creates, shuffles, and deals deck of cards
    Plugs into fix_kings function
    Returns tableau and empty foundation
    '''
    foundation = [[], [], [], []] #foundation starts empty
    tableau = []
    stock = cards.Deck() #creates deck stock
    stock.shuffle() #shuffles
    for x in range(0, 18):
        templist = []
        if x == 17: #last card set only gest 1 card
            templist.append(stock.deal())
        else: #every other card stack gets 3
            templist.append(stock.deal())
            templist.append(stock.deal())
            templist.append(stock.deal())
        tableau.append(templist)
    fix_kings(tableau) #moves kings to front
    #print(tableau)
    return (tableau, foundation) #returns tableau and emtpy foundation


def get_option():
    ''' 
    Obtains user input
    Ensures option is viable
    Returns option in list form
    '''
    option = input("\nInput an option (MTT,MTF,U,R,H,Q): " )

    oplist = option.split(" ")

    if oplist[0] == "mtt": #if user wants to move tableau to tableu decks
        if int(oplist[1]) > 17: #ensures its an available source
            print("Error in Source.")
            return None
        elif int(oplist[2]) > 17: #ensures destination is an available stack
            print("Error in Destination.")
            return None
        else:
            return oplist
    elif oplist[0] == "mtf": #tableau to foundation
        if int(oplist[1]) > 17: #ensures source is an available stack
            print("Error in Source.")
            return None
        elif int(oplist[2]) > 3: #ensures destination is a foundation
            print("Error in Destination.")
            return None
        else:
            return oplist
    #returns input list for all
    elif oplist[0] == "u":
        return oplist
    elif oplist[0] == "r":
        return oplist
    elif oplist[0] == "h":
        return oplist
    elif oplist[0] == "q":
        return oplist    
    else:
        print("Error in option:", option)
        return None #error returns None


def valid_tableau_to_tableau(tableau,s,d):
    '''
    Intakes tableau, source cards, and destination
    Ensures source card can be placed on new destination
        Any suit, increase or decrease by one
    '''
    try:
        denlength = len(tableau[d])

        if 1 <= denlength <= 2: #if card stack is 1 or 2 items
            source = tableau[s][-1] #source is last item
            destination = tableau[d][-1] #destination is last item

            sourcerank = source.rank() 
            destinationrank = destination.rank()
            
            destinationplus = destinationrank + 1
            destinationminus = destinationrank - 1
            #checks if source onto destination is moving up or down one rank
            if destinationplus == sourcerank: 
                return True
            elif destinationminus == sourcerank:
                return True
            else:
                return False
        else: #returns false if it is not 1 or 2 items
            return False
    except:
        return False

    
def valid_tableau_to_foundation(tableau,foundation,s,d):
    ''' 
    Intakes tableau, source cards, foundation, and destination
    Ensures source card can be placed on foundation destination
        Increasing by one and same suit
    '''
    try:
        found = len(foundation[d])

        source = tableau[s][-1]
        sourcesuit = source.suit()
        sourcerank = source.rank()
        #if foundation already has a card in it
        if found > 0:
            destination = foundation[d][-1]
            destinationrank = destination.rank()
            destinationsuit = destination.suit()
            #ensures foundation goes up one rank(and same suit)
            destinationplus = destinationrank + 1

            if destinationplus == sourcerank: #if rank is increased by one
                if destinationsuit == sourcesuit: #if suits are the same
                    return True
                else:
                    return False #returns if not same suit
            else:
                return False #returns false if not same rank

        else: #if foundation is empty
            if sourcerank == 1:
                return True
            else:
                return False
            
    except:
        return False #returns false if any failures


    
def move_tableau_to_tableau(tableau,s,d):
    '''
    Intakes tableau, source, and destination
    Uses validate function to make sure move is possible
    Takes source and moves to destination
    Returns true/false if move has been made
    '''

    s = int(s)
    d = int(d)
    valid = valid_tableau_to_tableau(tableau,s,d) #validation check
    s = int(s)
    d = int(d)

    if valid == False:
        return False #if not valid, fails
    if valid == True: 
        #moves from back of stack to destination
        destination = tableau[d]
        popped = tableau[s].pop()
        destination.append(popped)

        return True


def move_tableau_to_foundation(tableau, foundation, s,d):
    '''
    Intakes tableau, source, foundation, and destination
    Uses validate function to make sure move is possible
    Takes source and moves to foundation destination
    Returns true/false if move has been made
    '''
    s = int(s)
    d = int(d)
    valid = valid_tableau_to_foundation(tableau,foundation,s,d) #validation check
    s = int(s)
    d = int(d)

    if valid == False:
        return False #if not valid, fails
    if valid == True:
        #moves from back of stack to foundation
        destination = foundation[d]
        popped = tableau[s].pop()
        destination.append(popped)

        return True


def check_for_win(foundation):
    ''' 
    Intakes foundation
    Checks to see if each foundation has 13 cards
    Returns true/false accordingly
    '''
    if len(foundation[0]) == 13:
        if len(foundation[1]) == 13:
            if len(foundation[2]) == 13:
                if len(foundation[3]) == 13:
                    return True #returns true if every foundation is 13 cards
    else:
        return False #if not done, not winning
    
def undo(moves,tableau,foundation):
    '''
    Undo the last move;
       Parameters:
           moves: the history of all valid moves. It is a list of tuples 
                  (option,source,dest) for each valid move performed since the 
                  start of the game. 
           tableau: the data structure representing the tableau.  
       Returns: Bool (True if there are moves to undo. False if not)
    '''
       
    if moves: # there exist moves to undo
        last_move = moves.pop()
        option = last_move[0]
        option = option.upper()
        source = last_move[1]
        dest = last_move[2]
        dest = int(dest)
        source = int(source)

        print("Undo:",option,source,dest)
        if option == 'MTT':
            tableau[source].append(tableau[dest].pop())
        else: # option == 'MTF'
            tableau[source].append(foundation[dest].pop())
        return True
    else:
        return False

def display(tableau, foundation):
    '''Display the foundation in one row;
       Display the tableau in 3 rows of 5 followed by one row of 3.
       Each tableau item is a 3-card pile separated with a vertical bar.'''
    print("\nFoundation:")
    print(" "*15,end='') # shift foundation toward center
    # display foundation with labels
    for i,L in enumerate(foundation):
        if len(L)==0:
            print("{:d}:    ".format(i),end="  ") # padding for empty foundation slot
        else:
            print("{:d}: {} ".format(i,L[-1]),end="  ") # display only "top" card
    print()
    print("="*80)
    print("Tableau:")
    # First fifteen 3-card piles are printed; across 3 rows
    for i in range(15):
        print("{:2d}:".format(i),end='') # label each 3-card pile
        for c in tableau[i]:  # print 3-card pile (list)
            print(c,end=" ")
        print("    "*(3-len(tableau[i])),end='') # pad with spaces
        print("|",end="")
        if i%5 == 4: # start a new line after printing five lists
            print()
            print("-"*80)
    # Final row of only three 3-card piles is printed
    print(" "*15+"|",end='')  # shift first pile right
    for i in range(15,18):
        print("{:2d}:".format(i),end='') # label each 3-card pile
        for c in tableau[i]:
            print(c,end=" ")
        print("    "*(3-len(tableau[i])),end='') # pad with spaces
        print("|",end="")
    print()
    print("-"*80)
    

def main():
    '''
    Initializes deck
    Prints menu
    Intakes user inputs for menu options
    Plugs into functions to validate and move cards accordingly
    Loops until user quits
    ''' 
    tableau, foundation = initialize() #starting tableau and foundation
    print("\nWelcome to Shamrocks Solitaire.\n")

    display(tableau, foundation) #displays first solitare deck


    print(MENU)
    option = get_option()

    movelist = []
    looper = True

    while looper == True: #infinate loop

####################

        while option == None: #while option is available
            option = get_option()


####################

        if option[0] == "q": #user quits
            print("Thank you for playing.")
            break

####################

        elif option[0] == "mtt": #tableau to tableau
            s = option[1]
            d = option[2]
            tf = move_tableau_to_tableau(tableau,s,d) #true/false checker
            if tf == False:
                #optionprint = ", ".join(option)
                print("Error in move:", option[0].upper(),",", option[1], ",",option[2])
            if tf == True: 
                movelist.append(option) #adds to undo list
                display(tableau, foundation)

            option = get_option() #looper

####################

        elif option[0] == "mtf": #tableau to foundation
            s = option[1]
            d = option[2]
            tf = move_tableau_to_foundation(tableau, foundation, s,d) #true/false checker
            if tf == False:
                #optionprint = ", ".join(option)
                print("Error in move:", option[0].upper(),",", option[1], ",",option[2]) #fail print
            if tf == True:
                movelist.append(option) #adds to undo list
                check = check_for_win(foundation) #winner checker
                if check == True:
                    print("You won!")

                    display(tableau, foundation)
                    print("\n- - - - New Game. - - - -")
                    #creates new game
                    tableau, foundation = initialize()
                    display(tableau, foundation)
                    print(MENU)
                else:
                    display(tableau, foundation) #if wincheck fails

            option = get_option() #looper



####################

        elif option[0] == "u": #undo
            #given function
            if undo(movelist, tableau, foundation): #plugs in undo list
                display(tableau, foundation)
            else:
                print("No moves to undo")
            option = get_option() #looper

####################

        elif option[0] == "r":
            #new deck
            tableau, foundation = initialize()
            display(tableau, foundation)
            option = get_option() #looper

####################

        elif option[0] == "h":
            #displays menu again
            print(MENU)
            option = get_option() #looper

####################

        else:
            print("Error in option:", option) 
            option = get_option() #looper


if __name__ == '__main__':
     main()
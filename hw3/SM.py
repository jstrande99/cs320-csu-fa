# Programming of Gale-Shapley algorithm
#import time

def readSMFile(filename):
    """
    This function reads an instance of the stable matching problem
    from a file that is easy to create with a text editor.  While debugging,
    work with small examples, then test on larger examples.

    The men and women are each denoted with an integer from 1 to instanceSize.

    The format of the file is as follows:
    The first line has a single integer, giving the number n of men and women
    On each of the next n lines is the preference list of a man, separated by
       spaces.  The first of these lines gives the preference list of man 1,
       the second for man 2, etc.
    The next line is empty
    One each of the next n lines is the preference list of a woman, separated
       by spaces.  The first of these gives the preference list of woman 1, etc.

    Example for n = 4:
    4
    3 1 4 2
    3 2 1 4
    1 4 2 3
    1 4 3 2
 
    1 4 3 2
    2 4 3 1
    3 2 1 4
    1 4 3 2

    Make sure that each line ends with the newline ('\n') character.  Some
    text editors end lines with other characters.  Using 'vim' to create it
    is a safe bet.

    The procedure returns a triple, the first of which is n
    the second is an array MPrefLists, where MPrefLists[i][j] tells
    the jth woman from the top in man i's preference list, and the third
    is an array WPrefLists, where WPrefLists[i][j] tells the
    jth man from the top in i's preference list.  Since the men and
    women are indexed starting at 1, row 0 if each array is empty,
    and the first element of each remaining row is 0.

    For the above instance, the three returned elements are as follows.

    4,
    [[], [0, 3, 1, 4, 2], [0, 3, 2, 1, 4], [0, 1, 4, 2, 3], [0, 1, 4, 3, 2]],
    [[], [0, 1, 4, 3, 2], [0, 2, 4, 3, 1], [0, 3, 2, 1, 4], [0, 1, 4, 3, 2]]

    """

    MPrefLists = [[]]
    WPrefLists = [[]]
    with open(filename) as f:
        Lines = f.readlines()
        instanceSize = int(Lines[0][:-1])
        for i in range(instanceSize):
            New_list = [0] + [int(elem) for elem in str(Lines[i+1][:-1]).split(" ")]
            MPrefLists.append(New_list)
        for i in range(instanceSize+1,2*instanceSize+1,1):
            New_list = [0] + [int(elem) for elem in str(Lines[i+1][:-1]).split(" ")]
            WPrefLists.append(New_list)

    return instanceSize, MPrefLists, WPrefLists
             

def ComputeInvPrefLists(PrefLists):
    """
    The input is the preference lists for one gender.  Suppose it is
    the preference lists for the women. Then PrefLists[i][j] is the 
    jth highest man of woman i's preference list.

    The output is InvPrefLists, where InvPrefLists[i][j] tells the
    position of man j in woman i's preference list.

    Remember that the people in each gender are numbered starting at 
    1, not 0.

    If PrefLists is the preference list for the men, an analogous
    result is computed where the roles of men and women are swapped.

    For the women's preference list in the instance in the comments of
    the code for readSMFile, this method should return:
    [[], [0, 1, 4, 3, 2], [0, 4, 1, 3, 2], [0, 3, 2, 1, 4], [0, 1, 4, 3, 2]]
    """
    # FILL IN CODE HERE
    InvPrefLists = [[]]
    for i in range(1, len(PrefLists)):
        size = len(PrefLists[i])
        temp = [0]*(size)
        for j in range(1, size): 
            #j, PrefLists[i][j]
            # temp[man] = preference
            # PrefList[preference] = man
            temp[PrefLists[i][j]] = j
            #temp.append(PrefLists[i].index(j))
        InvPrefLists.append(temp)
    return InvPrefLists 

def propose(newMan, woman, InvWomenPrefLists, Fiance, MStartPositions):
    """
    This function simulates the proposal of a man to a woman.
    The newMan proposes to woman and if the woman is single
    or newMan ranks higher than her current match, he gets
    paired with her.  This function has to return the integer
    identifier of the man who got rejected (old fiancé or
    newMan) or None if no man was rejected (the woman started
    out single).

    Fiance is a Python list where Fiance[i] is the fiancé of
    woman i, or 0 if i is single.  The method must update this
    list if it changes as a result of the proposal.

    MStartPositions[i] tells the index in man i's preference list
    of the highest woman who hasn't rejected him.  The method
    must update this list if it changes as a result of the proposal.
    """
    # FILL IN CODE HERE

    if(Fiance[woman] == 0):
        Fiance[woman] = newMan
        return None
    elif(InvWomenPrefLists[woman][newMan] < InvWomenPrefLists[woman][Fiance[woman]]):
        rejectedMan = Fiance[woman]
        MStartPositions[Fiance[woman]] += 1
        Fiance[woman] = newMan
        return rejectedMan
    else:
        MStartPositions[newMan] += 1
        return newMan


def StackOfMen(instanceSize):
    """
    This function creates a stack that contains all
    the men. You can use a python list to implement a stack.
    For a tutorial on this, see the Python 3 tutorial at
    https://docs.python.org/3/tutorial/, Section 5.1.1.
    """
    return list(range(1, instanceSize+1))


def GaleShapley(instanceSize, MPrefLists, WPrefLists):
    """
    This is the main Gale-Shapley method.  The inputs are two python
    lists.  MPrefLists[i-1][j-1] gives the jth highest woman in man i's list.
    WPrefList[i-1][j-1] gives the jth highest man in woman i's list.

    What must be returned is a list of ordered pairs giving the stable
    set of marriages.  For consistency with the book's notation, list the man
    first in each pair.  A typical returned list for n = 4 is this:
    [(1, 1), (3, 2), (2, 3), (4, 4)], indicating that man 1 is married to woman
    1, man 3 is married to woman 2, etc.

    Store the single men in a stack created by make_stack_of_men().
    To find a single man to make a proposal, pop the stack.  When
    a man gets rejected, push him.

    Make a list MStartPositions[], where MStartPositions[i-1] gives
    the position of the first woman in man i's list that hasn't rejected
    him.  

    For the women's preference list in the instance in the comments of
    the code for readSMFile, this method should return:
    [(1, 1), (3, 2), (2, 3), (4, 4)]
    """
    # FILL IN CODE HERE ...
    #start_time = time.clock()
    #married = [(0,0) for i in range(instanceSize)]
    married = [[0,0] for i in range(instanceSize)]
    couple = [0 for i in range(instanceSize + 1)]
    men = [1 for i in range(instanceSize + 1)]
    stck = StackOfMen(instanceSize)
    womanL = ComputeInvPrefLists(WPrefLists)
    
    while(stck):
        popman = stck.pop()
        loser = propose(popman, MPrefLists[popman][men[popman]], womanL, couple, men)
        
        if(loser == None): 
            pass

        elif(loser == popman):
            stck.append(popman) 

        else: 
            stck.append(loser)
                   
        
    for j in range(len(couple)-1): 
        married[j][0] = couple[j + 1]
        married[j][1] = j + 1

    married = list(map(tuple, married))

    #print(time.clock() - start_time, "seconds")
    return married
    
def checkStability(instanceSize, MPrefLists, WPrefLists, Matching):
    '''
    This method checks the stability of a matching.  The first
    argument is a list where MPrefLists[i-1][j-1] gives the
    jth woman in man i's preference list.  The second argument
    is similar, but for women's preferences.  Matching is an
    array of two-tuples, giving the matching.  

    If the matching has an instability, the method returns
    a triple (False, (m1,w1),(m2,w2)), where m1 prefers w2 to w1
    and w2 prefers m1 to m1.  If the matching is stable, it
    returns a triple (True, (0,0), (0,0)).
    '''

    # Compute the inverses of the preference list mappings for men, women
    InvMenPrefLists = ComputeInvPrefLists(MPrefLists)
    InvWomenPrefLists = ComputeInvPrefLists(WPrefLists)

    # For each marriage, Marriage1...
    for i in range(instanceSize):
        Marriage1 = Matching[i]
        m1 = Marriage1[0]
        w1 = Marriage1[1]

        # m1's and m2's rankings of each other
        m1SpousePosition = InvMenPrefLists[m1][w1]
        w1SpousePosition = InvWomenPrefLists[w1][m1]

        # For each later marriage in the list, Marriage2 ...
        for j in range(i+1,instanceSize):
            Marriage2 = Matching[j]
            m2 = Marriage2[0]
            w2 = Marriage2[1]

            # m2, m2's rankings of each other
            m2SpousePosition = InvMenPrefLists[m2][w2]
            w2SpousePosition = InvWomenPrefLists[w2][m2]

            # If m1, w2 prefer each other to their spouses ...
            if m1SpousePosition > InvMenPrefLists[m1][w2] and w2SpousePosition > InvWomenPrefLists[w2][m1]:
                return False, Marriage1, Marriage2 

            # If m2, w1 prefer each other to their spouses ...
            if m2SpousePosition > InvMenPrefLists[m2][w1] and w1SpousePosition > InvWomenPrefLists[w1][m2]:
                return False, Marriage2, Marriage1

    #  If no instabilities have been discovered ...
    return True, (0,0), (0,0)

#myfile = readSMFile("test.txt")
#wpref = myfile[2]
#print(ComputeInvPrefLists(wpref))
#print(GaleShapley(4, myfile[1], myfile[2]))


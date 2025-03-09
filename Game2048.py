import random
from copy import deepcopy

class Game2048:
    
    def __init__(self):
        """ Initialize the game board """
        seed = input("Do you want to choose a random seed?\nType an integer to set, otherwise not to specified the seed.")
        try:
            random.seed(int(seed))
            print("Set seed: "+seed)
        except:
            print("No seed has set.")
            
        board = [[None]*4 for _ in range(4)]
        empty = [(i,j) for i in range(4) for j in range(4)]
        init_two = random.sample(empty,2)
        board[init_two[0][0]][init_two[0][1]] = board[init_two[1][0]][init_two[1][1]]=2
        self.board = board
        self.infinite_mode = None
        self.max_val = 0
        
        
    def __str__(self):
        """ Print the game board """
        
        result = "-"*29+"\n"
        for i in range(4):
            cur_row = "|"
            for j in range(4):
                entry = self.board[i][j]
                if entry is None:
                    cur_row+="      |"
                else:
                    cur_row+=" "+" "*(4-len(str(entry))) + str(entry) + " |"
            result+=cur_row
            result+="\n" +"-"*29+"\n"
        return result
    
    
    def empty_board(self):
        """ return the list of empty entries's cooridinates"""
        empty = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] is None:
                    empty.append((i,j))
        return empty
    
    
    def generate_2(self):
        """ 
        If there are some None at the board, generate a 2 at random position;
        Otherwise leave the board as is.
        """
        empty = self.empty_board()
        if empty:
            i, j = random.choice(empty)
            
            self.board[i][j] = 2
    
    
    def is_2048(self):
        """ Return True if there is an 2048 at the board"""
        for i in range(4):
            for j in range(4):
                if self.board[i][j]==2048:
                    return True
        return False
        
        
    def is_movable(self, direction):
        """
        Determine if the board is movable in certain direction ('w', 'a', 's', 'd')
        return True if movable else False
        """
        
        if direction in ['w', 's']:            
            for j in range(4):
                col = [self.board[i][j] for i in range(4)]
                col_nonnull = [self.board[i][j] for i in range(4) if self.board[i][j] is not None]
                
                # If 'w'/'s' and exist None at above/below a non_null entry:
                for i in range(3):
                    if direction=='w' and col[i] is None and col[i+1] is not None:
                        return True
                    if direction=='s' and col[i+1] is None and col[i] is not None:
                        return True
                
                # If 'w'/'s' and exist consecutive same element at col_nonnull:
                for i in range(len(col_nonnull)-1):
                    if col_nonnull[i]==col_nonnull[i+1]:
                        return True
            return False
        
        else:
            for i in range(4):
                row = self.board[i]
                row_nonnull = [j for j in self.board[i] if j is not None]
                
                # If 'a'/'d' and exist None at to the left/right of a non_null entry:
                for j in range(3):
                    if direction=='a' and row[j] is None and row[j+1] is not None:
                        return True
                    if direction=='d' and row[j+1] is None and row[j] is not None:
                        return True
                
                # If 'a'/'d' and exist consecutive same element at row_nonnull:
                for i in range(len(row_nonnull)-1):
                    if row_nonnull[i]==row_nonnull[i+1]:
                        return True
            return False
                
    def move(self, direction):
        """
        Move the board at certain direction, given this direction is movable
        """
        if direction == 'w':
            for j in range(4):
                col_nonnull = [self.board[i][j] for i in range(4) if self.board[i][j] is not None]
                col_after = []
                i=0
                while i<len(col_nonnull):
                    if i+1<len(col_nonnull) and col_nonnull[i]==col_nonnull[i+1]:
                        col_after.append(col_nonnull[i]*2)
                        i+=2
                    else:
                        col_after.append(col_nonnull[i])
                        i+=1
                col_after+=[None]*(4-len(col_after))
                for i in range(4):
                    self.board[i][j] = col_after[i]
                    
        elif direction == 's':
            for j in range(4):
                col_nonnull = [self.board[i][j] for i in range(4) if self.board[i][j] is not None]
                col_after = []
                i=len(col_nonnull)-1
                while i>=0:
                    if i-1>=0 and col_nonnull[i]==col_nonnull[i-1]:
                        col_after = [col_nonnull[i]*2]+col_after
                        i-=2
                    else:
                        col_after = [col_nonnull[i]]+col_after
                        i-=1
                col_after = [None]*(4-len(col_after)) + col_after
                for i in range(4):
                    self.board[i][j] = col_after[i]
        
        elif direction == 'a':
            for i in range(4):
                row_nonnull = [j for j in self.board[i] if j is not None]
                row_after = []
                j=0
                while j<len(row_nonnull):
                    if j+1<len(row_nonnull) and row_nonnull[j]==row_nonnull[j+1]:
                        row_after.append(row_nonnull[j]*2)
                        j+=2
                    else:
                        row_after.append(row_nonnull[j])
                        j+=1
                row_after += [None]*(4-len(row_after))
                self.board[i]=row_after
        
        else: #direction == 'd'
            for i in range(4):
                row_nonnull = [j for j in self.board[i] if j is not None]
                row_after = []
                j=len(row_nonnull)-1
                while j>=0:
                    if j-1>=0 and row_nonnull[j]==row_nonnull[j-1]:
                        row_after = [row_nonnull[j]*2] + row_after
                        j-=2
                    else:
                        row_after = [row_nonnull[j]] + row_after
                        j-=1
                row_after = [None]*(4-len(row_after)) + row_after
                self.board[i]=row_after
    
    
    def is_validmove(self):
        """
        Determine if there is further valid move
        """

        return self.is_movable('w') or self.is_movable('a') or self.is_movable('s') or self.is_movable('d')
    
    def play(self):
        """ Play the game"""
        
        
        #REVERSE mode
        is_rev = input("Do you want to enable REVERSE mode, when you can get back anytime?\nEnter y to enable, otherwise enter NORMAL mode.")
        if is_rev=='y':
            prev_board=[]
            print("REVERSE mode enabled.")
        
        print("Game Started!\nEnter q if you want to quit the game anytime.")
        
        while True:
            print(self.__str__())
            
            message = "Choose a direction to move (w/a/s/d) "
            if is_rev=='y':
                message+="\nIf want to reverse to previous step, type r. "
            direction = input(message)
            
            if direction not in 'wasdrq' or direction=="":
                print("Invalid move.")
                continue
            
            # Quit the Game
            if direction == 'q':
                is_quit = input("Are you sure you want to quit the game? Enter q again to quit: ")
                if is_quit=='q':
                    break
                else:
                    continue
                
            # Implement REVERSE mode
            if direction == 'r':
                if is_rev=="n":
                    print("REVERSE mode disabled.")
                    continue
                if not prev_board:
                    print("There is no previous board")
                    continue
                self.board = prev_board.pop()
                continue
                
            # Check if the current move is valid
            if not self.is_movable(direction):
                print(f"The '{direction}' move is not valid for current step.")
                continue
            
            if is_rev=='y':
                prev_board.append(deepcopy(self.board))
                
            self.move(direction)
            
            # If there is 2048, game set. 
            # Potential INFINITE mode
            if self.is_2048():
                print(self.__str__())
                print("Congratulation! You get an 2048.")
                self.infinite_mode = input("Do you want to play INFINITE mode from now?\nEnter y to play or end the game otherwise.")
                if self.infinite_mode!='y':
                    break
            
            self.generate_2()
            
            if not self.is_validmove():
                print(self.__str__())
                print("There is no further valid move. Game ends.")
                break
        
        print("Thanks for playing 2048!")
        restart = input("Do you want to start another game? Enter y to start and quit otherwise")
        if restart == 'y':
            self.__init__()
            self.play() 
            
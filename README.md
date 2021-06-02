# PyArcade -- The Back End Test Suite 1

Readme update


# Software Requirements
All of the software requirements are written in detail in comments directly under the function signatures for two files
```proxy.py``` and ```mastermind.py```. You may, and probably will need to, create more functions for both of the 
classes defined in these files.

# Testing Requirements
Testing is a huge part of this assignment. The code implementations defined in the comments should not be 
terribly difficult. You must create a test suite that *efficiently* and *exhaustively* tests sensible inputs and 
outputs for the provided specifications. The concept of equivalence partitions is important here. When creating unit 
tests, you should not be creating an abundance of tests for which the input exercises the function in a similar way. 
Rather, you should choose tests that represent unique requirements for a function.

The rubric states:

1. Has higher than 90% code coverage using [pytest-cov](https://pypi.org/project/pytest-cov/)
2. Has test names which meaningfully describe the test.
3. Has tests which are atomic (definition of a unit test). 
4. Has tests which test *features* (integration tests) as well as simple functionality (unit tests). 

What you SHOULD consider testing:
1. Correctly typed inputs that have extra data. (behavior should be unaffected)
2. Correctly typed but erroneous inputs.
3. An entire sequence of inputs that results in winning the game in several ways. This is an integration test.

What is NOT required to be tested:
1. Input *types* being correct. We will consider type-hints as sufficient.

## Rubric
As always, mind the rubric. **You are not being graded solely on whether it works.** You must incorporate
good practices to keep code complexity to a minimum and also use git correctly.

## Patrick's Prev. Refactoring

### Smell 1
Bloating - Large Class. Before making extracting the SessionManager class, the MastermindGame would handle
all instances of sessions and would keep track of them. By creating a separate class to handle sessions,
it allows me to have sessions that are for different type of games (since each will have its own data).
This also helps keep MastermindGame only doing what it needs and keeps the others games from colliding
with session ids. The SessionManager class is responsible for creating and keeping track of the different
session classes for each game (MastermindGameSession and CheckerSession) which each contain the data
needed to play. An added benefit of this is that I can compare Session class types when looking up data
so that a request to MastermindGame doesn't return the results from a CheckersGame. 

Method Used: Extract Class

*Before*
```python
    def create_game(self, request: dict) -> dict:
        session_id = increment_session_id()
        game_sequence = generate_hidden_sequence()
        MastermindGame.sessions[session_id] = {"sequence": game_sequence, "guesses": [], "done": False}

        return {"session_id": session_id}
```
*After*
```python
    def create_game(self, request: dict) -> dict:
        return self.session_manager.init_mastermind_session(generate_hidden_sequence())
```

### Smell 2
Dispensables - Duplicated Code. Originally, I have a proxy for each game type, this lead to a lot of duplicate code 
especially with the read, create, and delete methods which were identical. There were only slight differences in the update section. To combine the update section,
I first checked the parts of code they had in common and then checked the individual
checks for each game type based on what type of game it was.

I used the Extract Method to do so

*Before*
```python
    ##mastermind update
    def update_game(self, request: dict) -> dict:
        if request is None \
                or len(request) != 2 \
                or "session_id" not in request \
                or "guess" not in request \
                or type(request["session_id"]) != int \
                or type(request["guess"]) != tuple \
                or not self.session_manager.session_exists(request["session_id"]) \
                or not self.session_manager.is_mastermind_session(request["session_id"]) \
                or self.session_manager.session_is_done(request["session_id"]) \
                or not tuple_contains_only_int_type(request["guess"]) \
                or len(set(request["guess"])) != 4 \
                or not input_has_valid_values(request["guess"]):
            return {"session_id": 0}

        return self.game_instance.update_game(request)

    
    ##checkers update
    def update_game(self, request: dict) -> dict:
        if request is None \
                or len(request) != 3 \
                or "session_id" not in request \
                or "piece_to_move" not in request \
                or "move_to" not in request \
                or type(request["session_id"]) != int \
                or type(request["piece_to_move"]) != tuple \
                or type(request["move_to"]) != tuple \
                or not self.session_manager.session_exists(request["session_id"]) \
                or not self.session_manager.is_checkers_session(request["session_id"]) \
                or self.session_manager.session_is_done(request["session_id"]) \
                or not tuple_contains_only_int_type(request["piece_to_move"]) \
                or not tuple_contains_only_int_type(request["piece_to_move"]) \
                or not self.is_valid_move(request) \
                or len(request["piece_to_move"]) != 2 \
                or len(request["move_to"]) != 2 \
                or not input_has_valid_values(request["piece_to_move"]) \
                or not input_has_valid_values(request["move_to"]):
            return {"session_id": 0}

        return self.game_instance.update_game(request)
```

*After*
```python
        if request is None \
                or not request_correct_size(request, 2) \
                or not key_present(request, "session_id") \
                or not correct_type(request, "session_id", int()) \
                or not self.session_exists(request) \
                or self.session_is_done(request):
            return {"session_id": 0}

        if is_mastermind_game(self.game_instance):
            if not self.valid_mastermind_update_request(request):
                return {"session_id": 0}
        elif is_checkers_game(self.game_instance):
            if not self.valid_checkers_update_request(request):
                return {"session_id": 0}

        return self.game_instance.update_game(request)
```

### Smell 3
Long Boolean Expressions. Across my proxy class, there were instances of duplicate
code in the if statements especially when both proxies were combined into a single
proxy. The create, read, and delete were the same but the update code got a lot more
complicated due to the added functionality for checkers. To combat this, I used the extract
method/decompose conditions to create easier to read methods that perform repeated tasks such as length and type
checks. By doing this, I was able to make the code a lot cleaner and easier to read.

*Before* 
```python
def update_game(self, request: dict) -> dict:
    if (self.game_instace == Mastermind):    
        if request is None \
                or len(request) != 2 \
                or "session_id" not in request \
                or "guess" not in request \
                or type(request["session_id"]) != int \
                or type(request["guess"]) != tuple \
                or not self.session_manager.session_exists(request["session_id"]) \
                or not self.session_manager.is_mastermind_session(request["session_id"]) \
                or self.session_manager.session_is_done(request["session_id"]) \
                or not tuple_contains_only_int_type(request["guess"]) \
                or len(set(request["guess"])) != 4 \
                or not input_has_valid_values(request["guess"]):
            return {"session_id": 0}
    elif (self.game_instace == Checkers):
            if request is None \
                or len(request) != 3 \
                or "session_id" not in request \
                or "piece_to_move" not in request \
                or "move_to" not in request \
                or type(request["session_id"]) != int \
                or type(request["piece_to_move"]) != tuple \
                or type(request["move_to"]) != tuple \
                or not self.session_manager.session_exists(request["session_id"]) \
                or not self.session_manager.is_checkers_session(request["session_id"]) \
                or self.session_manager.session_is_done(request["session_id"]) \
                or not tuple_contains_only_int_type(request["piece_to_move"]) \
                or not tuple_contains_only_int_type(request["piece_to_move"]) \
                or not self.is_valid_move(request) \
                or len(request["piece_to_move"]) != 2 \
                or len(request["move_to"]) != 2 \
                or not input_has_valid_values(request["piece_to_move"]) \
                or not input_has_valid_values(request["move_to"]):
            return {"session_id": 0}
```

*After*
```python
        if request is None \
                or not request_correct_size(request, 2) \
                or not key_present(request, "session_id") \
                or not correct_type(request, "session_id", int()) \
                or not self.session_exists(request) \
                or self.session_is_done(request):
            return {"session_id": 0}

        if is_mastermind_game(self.game_instance):
            if not self.valid_mastermind_update_request(request):
                return {"session_id": 0}
        elif is_checkers_game(self.game_instance):
            if not self.valid_checkers_update_request(request):
                return {"session_id": 0}
```

### Smell 4
Bloaters - Long Method. My main search algorithm for finding available moves needs to look at the right and left
pieces and backwards if it is a king piece. To make the code easier to read and to also isolate each direction for
testing, I created a few new methods from the long method. I used the extract method and consolidated the large chunks
into smaller methods that minimize what they are doing.


*Before*
```python
        right_row, right_col = piece.get_right_piece()
        right_piece = self.get_piece(right_row, right_col)
        moves.update(self.go_right(right_piece, piece, piece, [], visited))

        left_row, left_col = piece.get_left_piece()
        left_piece = self.get_piece(left_row, left_col)
        moves.update(self.go_left(left_piece, piece, piece, [], visited))

        if piece.is_king:
            back_right_row, back_back_right_col = piece.get_back_right_piece()
            back_right_piece = self.get_piece(back_right_row, right_col)
            moves.update(self.go_back_right(back_right_piece, piece, piece, [], visited))
    
            back_left_row, back_left_col = piece.get_back_left_piece()
            back_left_piece = self.get_piece(back_left_row, back_left_col)
            moves.update(self.go_left(back_left_piece, piece, piece, [], visited))
```

*After* 
```python
        self.traverse_forward(moves, origin, origin, jumped, visited)

        if origin.is_king:
            self.traverse_backward(moves, origin, origin, jumped, visited)
```
```python
    def traverse_forward(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        self.traverse_right(moves, piece, origin, jumped, visited)
        self.traverse_left(moves, piece, origin, jumped, visited)

    def traverse_backward(self, moves: dict, piece: GamePiece, origin: GamePiece, jumped: list, visited: set):
        self.traverse_back_left(moves, piece, origin, jumped, visited)
        self.traverse_back_right(moves, piece, origin, jumped, visited)
```

## Jason's Previous Refactoring

### Code Refactoring
1. Code smell Large Class: Minesweeper has a lot of methods that are used for initializing the board, but they are only
called once from the add_session function. These methods were spun off using the builder concept. 
   i.e. extracted the class. This too large of a change to show code snippets. Please note instead a new file was added
1.a Broke up the test_mastermind into multiple classes to test features and unit tests independently. extracted classes
2. Code smell Change Preventers: use of primitive int in creating minesweeper difficulty. I replaced it with 
constants that can easily be changed without needing to change every int. i.e. 
   organizing data by change value to reference
    ```python
   # old code
   # Randomly picks locations to assign mines
    mines = sample(mines, 10)
   
   # new code
    EASY_MINES = 10
    mines = sample(mines, MinesweeperBoardBuilder.EASY_MINES)
    ```
   
3. Code smell Dispensables: Had duplicate code in test_minesweeper so I just added it as a global variable so all the
classes could use it. Reduced line count by about 15 or so. i.e. organizing data by change value to reference
    ```python
   # old code
    def test_unhide_cell(self):
        four_corners_board_soln = {0: ['mine']+[1]+[0]*5+[1]+['mine'], 1: [1, 1]+[0]*5+[1, 1], 2: [0]*9, 3: [0]*9,
                                   4: [0]*9, 5: [0]*9, 6: [0]*9, 7: [1, 1]+[0]*5+[1, 1],
                                   8: ['mine']+[1]+[0]*5+[1]+['mine']}
        MinesweeperGame.add_session({})
        session_4 = MinesweeperGame.sessions[4]
        session_4["board"] = four_corners_board_soln
        MinesweeperTestBasicGame.instance.unhide_cell((8, 7), session_4)
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        board = ""
        for idx in range(8):
            board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 1 🬅 \n'
        board += line
        board_to_print = MinesweeperGame.print_player_board(session_4["player_board"], session_4["board"])
        self.assertEqual(board, board_to_print)

    def test_end_game(self):
        four_corners_board_soln = {0: ['mine']+[1]+[0]*5+[1]+['mine'], 1: [1, 1]+[0]*5+[1, 1], 2: [0]*9, 3: [0]*9,
                                   4: [0]*9, 5: [0]*9, 6: [0]*9, 7: [1, 1]+[0]*5+[1, 1],
                                   8: ['mine']+[1]+[0]*5+[1]+['mine']}
        MinesweeperGame.add_session({})
        session_4 = MinesweeperGame.sessions[4]
        session_4["board"] = four_corners_board_soln
        session_4 = MinesweeperGame.sessions[4]
        MinesweeperTestBasicGame.instance.unhide_cell((8, 8), session_4)
        self.assertEqual(session_4["done"], True)

   
   # new code
    FOUR_CORNERS_BOARD_SOLN = {0: ['mine']+[1]+[0]*5+[1]+['mine'], 1: [1, 1]+[0]*5+[1, 1], 2: [0]*9, 3: [0]*9,
                               4: [0]*9, 5: [0]*9, 6: [0]*9, 7: [1, 1]+[0]*5+[1, 1],
                               8: ['mine']+[1]+[0]*5+[1]+['mine']}
    def test_unhide_cell(self):
        MinesweeperGame.add_session({})
        session_4 = MinesweeperGame.sessions[4]
        session_4["board"] = FOUR_CORNERS_BOARD_SOLN
        MinesweeperTestBasicGame.instance.unhide_cell((8, 7), session_4)
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 🬅 \n'
        board = ""
        for idx in range(8):
            board += line
        line = '🬅 🬅 🬅 🬅 🬅 🬅 🬅 1 🬅 \n'
        board += line
        board_to_print = MinesweeperGame.print_player_board(session_4["player_board"], session_4["board"])
        self.assertEqual(board, board_to_print)

    def test_end_game(self):
        MinesweeperGame.add_session({})
        session_4 = MinesweeperGame.sessions[4]
        session_4["board"] = FOUR_CORNERS_BOARD_SOLN
        session_4 = MinesweeperGame.sessions[4]
        MinesweeperTestBasicGame.instance.unhide_cell((8, 8), session_4)
        self.assertEqual(session_4["done"], True)

    ```
4. Code smell Alternative Classes with Different Interfaces: Rather coding the proxy to increase complexity with two
   different classes doing the same thing I extracted a superclass simply named proxy and its validation methods. This code smell was
   identified before it was introduced, although I will provide an example to showcase this.
   ```python
   # old code
   class MastermindGameProxy(GameInterface):
        def create_game(self, request: dict) -> dict:
            #code goes here
   
        def read_game(self, request: dict) -> dict:
            #code goes here
        
        def delete_game(self, request: dict) -> dict:
            #code goes here

        def update_game(self, request: dict) -> dict:
            # mastermind specific game updates
   
        def valide_update_request(request: dict) -> dict:
            # validation code unqiue to mastermind
   
    class MinesweeperProxy(MinesweeperGameInterface):
        def start_game(self, request: dict) -> dict:
            #code goes here
   
        def display_game(self, request: dict) -> dict:
            #code goes here
        
        def delete_game(self, request: dict) -> dict:
            #code goes here
        
        def make_move(self, request: dict) -> dict:
            # minesweeper specific game updates
            
        def valide_move_request(request: dict) -> dict:
            # validation code unqiue to minesweeper

   # new code
   class GameProxy(GameInterface):
        def create_game(self, request: dict) -> dict:
            #code goes here
   
        def read_game(self, request: dict) -> dict:
            #code goes here
        
        def delete_game(self, request: dict) -> dict:
            #code goes here

        def update_game(self, request: dict) -> dict:
            # Call specific subclass for game specific updates
        
        class MastermindProxy:
           def update_game(self, request: dict) -> dict:
                # Mastermind game updates
   
           def valide_update_request(request: dict) -> dict:
                # validation code unqiue to mastermind
        
        class MinesweeperProxy:
           def update_game(self, request: dict) -> dict:
                # Minesweeper game updates
   
           def valide_update_request(request: dict) -> dict:
                # validation code unqiue to minesweeper
    ```

# Team Assigment

### Patrick's work: 59%
    1. Finished integration with Jason's code. Worked on test integration and testing in general.
    2. Developed Flask functionality and general menu algorithms and HMLT GUI.

### Jason's work: 41%
    1. Integrated MinesweeperGame with Patrick's code. Developed delete game GUI functionality. Assited in game design.
    2. Applied the design pattern to code. Helped develop game functinality with use of design pattern.
    3. Integrated Readme


## Code Design Pattern:
We chose to use the singleton design pattern. This made it easier for us to maintain our code in a way that prevented
adding extra functionality to our individual gameinterfaces. It was more maintainable to simply add 'sessions' which
contained the data of our game classes (with game interfaces) than adding functions to our game classes to be able to
preform necessary tasks. It also allowed us to be able to call a single class in our flask implementation. We were able
to make our code cleaner by eliminating the need for making too many changes to our game classes. If we had more time to
refactor our code we hope to be able to call functions exclusively from the sessions class that will manipulate 
the data of the individual game sessions. We chose to integrate the MinesweeperGame class with Patrick's code since he 
had already implemented a single responsibility design for his classes by adding a session manager and sessions classes
which served to isolate the manipulation of sessions and their data from the actual game interfaces. The implementation 
of the proxy code was made shorter with super class GameProxy which was able to take advantage of the new singleton 
sessions_manager so that all games data would be stored within a single object instance across all game proxies. This 
was extremely useful in decreasing the amount of code needed to write for implementing the flask GUI that we used in our 
project. Rather than having to call individual game objects, we could just game data managers and a single
session manager to access any data we wanted to display in our HTML5 GUI witin Flask. We implemented this by using the 
example provided in the lecture videos. 

You can see we used it in pyarcade/session_manager.py line 12, pyarcade/proxy.py line 14, mastermind.py line 15, 
checkers.py line 9 and minesweeper.py line 18. By implementing the singleton design were able to avoid the code smells
of dispensables and large classes.

   ```python
   class Singleton:
    _instance = None

    @classmethod
    def singleton(cls) -> 'Singleton':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    
    class SessionManager(Singleton):
        """
        Session Manager
        """
        active_sessions = {}

    # Proxy
    class GameProxy(GameInterface):
        game_id_map = {0: MastermindGame, 1: Checkers, 2: MinesweeperGame}
    
        def __init__(self, game_instance: GameInterface):
            self.game_instance = game_instance
            self.session_manager = SessionManager.singleton()
    
    # In the constructor for each game
    class Game(GameInterface):
        def __init__(self):
        self.session_manager = SessionManager.singleton()

   ```



 

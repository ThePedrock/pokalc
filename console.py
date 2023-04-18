from table.card import Card
from table.suit import Suit
from table.play import Play
from calculator.game import Game

class Console:
    privateCards: str = ""
    communiCards: str = ""
    players: str = ""

    privateCardsArray = []
    communiCardsArray = []

    exit: str = ""

    def __init__(self):
        Console.consoleLoop()

    def consoleLoop():

        while (Console.exit!="y"):
            Console.printGuide()
            Console.exit = input("Exit? (y/n)")
            if (Console.exit=="y"):
                break
            Console.privateCards = input("Private Cards: ")
            Console.communiCards = input("Community Cards: ")
            Console.players = input("Players: ")

            if (Console.validateConsoleData()):
                privateCardsArray = Console.codeToCards(Console.privateCards)
                communiCardsArray = Console.codeToCards(Console.communiCards)

                Console.runPokalcCommand(privateCardsArray, communiCardsArray, int(Console.players))

                Console.exit = input("Exit? (y/n)")

    def validateConsoleData():
        validationStr = ""
        validation = True
        if (not Console.privateCards.isnumeric()):
            Console.privateCards = 0
            validationStr += "Private Cards value is incorrect. \n"
            validation = False
        if (not Console.communiCards.isnumeric()):
            Console.communiCards = 0
            validationStr += "Community Cards value is incorrect. \n"
            validation = False
        if (not Console.players.isnumeric()):
            Console.players = 0
            validationStr += "Player value is incorrect. \n"
            validation = False

        if (not validation):
            print(validationStr)

        return validation
    
    def runPokalcCommand(pCardsArr, cCardsArr, players: int):
        probability_table = Game.build_probability_table(pCardsArr, cCardsArr)

        print("")
        print("Private Cards: " + Card.stringifyCardArray(pCardsArr))
        print("Community Cards: " + Card.stringifyCardArray(cCardsArr))
        print("Opponents: " + str(players-1))
        print("Calculating...")
        print("1Pair Win probs :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.ONE_PAIR)))
        print("2Pair Win probs :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.TWO_PAIR)))
        print("3Kind Win probs :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.THREE_OF_A_KIND)))
        print("Strght Win probs:" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.STRAIGHT)))
        print("Flush Win probs :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.FLUSH)))
        print("4Kind Win probs :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.FOUR_OF_A_KIND)))
        print("StrFsh Win probs:" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.STRAIGHT_FLUSH)))
        print("RylFls Win probs:" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, Play.ROYAL_FLUSH)))
        print("TOTAL Win probs :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, players, None)))

    def printGuide():
        print("SUITS: 1 (Hearts) | 2 (Diamonds) | 3 (Clubs) | 4 (Spades)")
        print("RANK: 01 (Ace) | 02...10 | 11 (Jack) | 12 (Queen) | 13 (King)")
        print("Example: 413 (King of Spades)")
        print("Private Cards Example: 113301")
        print("Communt Cards Example: 307110413")

    @staticmethod
    def codeToCard(code: str):
        if (len(code)!=3):
            return Card(0, Suit.UNKNOWN)
        
        suit = int(code[0])
        rank = int(code[-2:])

        return Card(rank,Suit(suit))
    
    @staticmethod
    def codeToCards(code: str):
        codedCards = []
        aCode = code

        while (len(aCode)>2):
            codedCards.append(aCode[:3])
            aCode = aCode[3:]

        cards = []

        for codedCard in codedCards:
            cards.append(Console.codeToCard(codedCard))
        
        return cards









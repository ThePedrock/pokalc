import tkinter
from tkinter import ttk, Label
from PIL import Image, ImageTk
import json
from threading import Thread
from threading import Event
from enum import Enum

from table.card import Card
from table.play import Play
from table.suit import Suit
from calculator.game import Game

class UI:
    APPVERSION = "1.0"
    WINDOWS_SIZE = [850, 605]

    ## IMAGE FROM: http://clipart-library.com/clipart/pT7K7d88c.htm ##
    POKER_DECK_IMAGE = "resources/pokerDeck.png"
    CARD_IMAGE_SIZE = [26,36]
    CARD_SIZE = [CARD_IMAGE_SIZE[0]*3,CARD_IMAGE_SIZE[1]*3]
    SELECTOR_CARD_SIZE = list(CARD_IMAGE_SIZE)

    ## UI VARIABLES ##
    CARD_LOCATION = [[100,450],[200,450],[170,270],[270,270],[370,270],[480,270],[590,270]]
    DEFAULT_HAND_CARD = [0,4]
    DEFAULT_TABLE_CARD = [1,4]
    REDRECTANGLE_WIDTH = 4
    LANGUAGES = ["English","Spanish"]

    _background = None

    _card_deck_frame = None
    _card_deck_frames_inside = []

    _card_frames = [None, None, None, None, None, None, None]
    _card_labels = [None, None, None, None, None, None, None]
    _result_frame = None

    _opponent_buttons = [None, None]
    _opponent_label = None
    _reset_button = None

    _language_dropdown = None

    ## BACKGROUND VARIABLES ##
    _card_deck_values = []

    _backgroundThread = None
    _backgroundStopEvent = None
    _card_slot = [None, None, None, None, None, None, None]

    _opponents = 1

    _language = 0

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("POKALC" + " " + UI.APPVERSION)
        self.root.geometry(str(UI.WINDOWS_SIZE[0])+"x"+str(UI.WINDOWS_SIZE[1]))
        self.root.configure(bg="green")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.loadSettings()
        self.tableBuilder()
        self.resetTableCards()
        self.initBackgroundLoopThread()

    def run(self):
        self.root.mainloop()

    def loadSettings(self):
        try:
            settings = None
            with open('settings.json', 'r') as file:
                settings = json.load(file)
            
            self._language = settings.get('language')
        except json.JSONDecodeError:
            pass

    def tableBuilder(self):
        UI._background = self.buildBackground()
        self.buildInterface(UI._background)

        # Card Selector Frame
        self._card_deck_frame = tkinter.Frame(UI._background)
        self._card_deck_frame.pack()
        self._card_deck_frame.config(bg="dark green",
                                    width=830,height=112)
        self._card_deck_frame.place(x=10, y=10)

        for i in range(4):
            for j in range(13):
                self._card_deck_frames_inside.append(tkinter.Frame(self._card_deck_frame))
                self._card_deck_frames_inside[len(self._card_deck_frames_inside)-1].pack()
                self._card_deck_frames_inside[len(self._card_deck_frames_inside)-1].config(bg="gray",
                                    width=UI.SELECTOR_CARD_SIZE[0],height=UI.SELECTOR_CARD_SIZE[1])
                self._card_deck_frames_inside[len(self._card_deck_frames_inside)-1].place(x=j*(UI.CARD_IMAGE_SIZE[0]+4)+(440*(i%2)), 
                                                                                        y=(((i-(i%2))/2)*(UI.CARD_IMAGE_SIZE[1]+30)))

                self._card_deck_values.append(self.createCardAndImage(j+1,i+1,UI.CARD_IMAGE_SIZE))

        self._card_deck_values.append(self.createCardAndImage(0,0,UI.CARD_IMAGE_SIZE))

        self.resetDeckCards()
                
                #self._card_selector_items.append(tkinter.Label(self._card_deck_frame, image=UI.cardImage(i,j,UI.CARD_IMAGE_SIZE)))
                #self._card_selector_items[len(self._card_selector_items)-1].place(x=(i*UI.CARD_IMAGE_SIZE[0])+4, y=(((i-(i%2))/2)*UI.CARD_IMAGE_SIZE[0])+4)

        for i in range(len(self._card_frames)):
            self._card_frames[i] = tkinter.Frame(UI._background)
            self._card_frames[i].pack()
            self._card_frames[i].config(bg="lightblue",
                        width=UI.CARD_SIZE[0],height=UI.CARD_SIZE[1])
            self._card_frames[i].place(x=UI.CARD_LOCATION[i][0], y=UI.CARD_LOCATION[i][1])

        self._result_frame = tkinter.Frame(UI._background)
        self._result_frame.pack()
        self._result_frame.config(bg="light slate gray", border=2, width=420, height=170)
        self._result_frame.place(x=390,y=430)

    def setDeckCard(self, slot: int, faceUp: bool):
        for widget in self._card_deck_frames_inside[slot].winfo_children():
                    widget.destroy()

        if (faceUp):
            aImage = tkinter.Label(self._card_deck_frames_inside[slot], image=self._card_deck_values[slot][1])
            aImage.pack()
            aImage.img = self._card_deck_values[slot][1]
            aImage.cardCode = UI.deckSlotToCardCode(slot)
            aImage.slot = slot

            aImage.bind("<Button-1>", lambda event: self.card_click(event, self._card_deck_frames_inside[slot], aImage.cardCode))
            aImage.bind("<B1-Motion>", lambda event: self.card_hold(event, self._card_deck_frames_inside[slot], aImage.cardCode))
            aImage.bind("<ButtonRelease-1>", lambda event: self.card_release(event, self._card_deck_frames_inside[slot], aImage.cardCode))
        else:
            aImage = tkinter.Label(self._card_deck_frames_inside[slot], image=self._card_deck_values[len(self._card_deck_values)-1][1])
            aImage.pack()
            aImage.img = self._card_deck_values[len(self._card_deck_values)-1][1]
            aImage.cardCode = [0,0]
            aImage.slot = slot

            aImage.bind("<Button-1>", lambda event: self.card_click(event, self._card_deck_frames_inside[slot], aImage.cardCode))
            aImage.bind("<B1-Motion>", lambda event: self.card_hold(event, self._card_deck_frames_inside[slot], aImage.cardCode))
            aImage.bind("<ButtonRelease-1>", lambda event: self.card_release(event, self._card_deck_frames_inside[slot], aImage.cardCode))

    def resetDeckCards(self):
        for i in range(len(self._card_deck_frames_inside)):
            self.setDeckCard(i, True)

    def resetTableCards(self):
        for i in range(len(UI._card_frames)):
            if (i<2):
                self.setCardToSlot(0,0,i)
            else:
                self.setCardToSlot(0,0,i)

    def initBackgroundLoopThread(self):
        self._backgroundStopEvent = Event()
        self._backgroundThread = UIBackgroundThread(self._backgroundStopEvent, self)
        self._backgroundThread.start()

    def createCardAndImage(self, rank: int, suit: int, imageSizeArray):
        newCard = Card(rank, Suit(suit))
        imageRank = 0
        imageSuit = 0

        ## Translate rank/suit card values to image ones ##
        if rank<1 or suit<1:
            imageRank = UI.DEFAULT_TABLE_CARD[0]
            imageSuit = UI.DEFAULT_TABLE_CARD[1]
        else:
            imageRank = rank-1
            match suit:
                case 1:
                    imageSuit = 3
                case 2:
                    imageSuit = 2
                case 3:
                    imageSuit = 0
                case 4:
                    imageSuit = 1
        
        newImage = UI.cardImage(imageRank, imageSuit, imageSizeArray)

        return [newCard, newImage]

    def setCardToSlot(self, rank: int, suit: int, slot: int):
        self._card_slot[slot] = Card(rank, Suit(suit))
        imageRank = 0
        imageSuit = 0
        
        ## Translate rank/suit card values to image ones ##
        if rank<1 or suit<1:
            if (slot<2):
                imageRank = UI.DEFAULT_HAND_CARD[0]
                imageSuit = UI.DEFAULT_HAND_CARD[1]
            else:
                imageRank = UI.DEFAULT_TABLE_CARD[0]
                imageSuit = UI.DEFAULT_TABLE_CARD[1]
        else:
            imageRank = rank-1
            match suit:
                case 1:
                    imageSuit = 3
                case 2:
                    imageSuit = 2
                case 3:
                    imageSuit = 0
                case 4:
                    imageSuit = 1

        self.setCardImageToSlot(imageRank, imageSuit, slot)

    def setCardImageToSlot(self, rank: int, suit: int, slot: int):
        if (UI._card_labels[slot]!=None):
                UI._card_labels[slot].destroy()
        
        imageCard = self.cardImage(rank,suit,UI.CARD_SIZE)
        UI._card_labels[slot] = tkinter.Label(UI._card_frames[slot], 
                                                        image=imageCard)
        
        UI._card_labels[slot].slot = slot
        UI._card_labels[slot].rank = rank
        UI._card_labels[slot].suit = suit
        
        UI._card_labels[slot].pack()
        UI._card_labels[slot].img = imageCard
        UI._card_labels[slot].cardCode = UI.imageCodeToCardCode(rank, suit)
        UI._card_labels[slot].slot = slot

        UI._card_labels[slot].bind("<Button-1>", lambda event: self.card_click(event, UI._card_labels[slot], UI._card_labels[slot].cardCode))
        UI._card_labels[slot].bind("<B1-Motion>", lambda event: self.card_hold(event, UI._card_labels[slot], UI._card_labels[slot].cardCode))
        UI._card_labels[slot].bind("<ButtonRelease-1>", lambda event: self.card_release(event, UI._card_labels[slot], UI._card_labels[slot].cardCode))

    def buildBackground(self):
        canvas = tkinter.Canvas(self.root, width=UI.WINDOWS_SIZE[0], height=UI.WINDOWS_SIZE[1])
        canvas.configure(bg="dark olive green")
        canvas.pack()

        canvas.create_oval(70, 215, 760, 440, outline="indianred4", width=2, fill="brown")
        canvas.create_oval(80, 225, 750, 425, outline="dark green", width=2, fill="dark green")
        canvas.create_rectangle(380, 425, 840, 595, outline="black", width=2, fill="light slate gray")

        return canvas
    
    def buildInterface(self, aBackground):
        # Arrow shaped buttons
        UI._opponent_buttons[0] = aBackground.create_polygon(50, 140, 25, 165, 75, 165, fill="gray", outline="black")
        UI._opponent_buttons[1] = aBackground.create_polygon(50, 250, 25, 225, 75, 225, fill="gray", outline="black")
        UI._reset_button = aBackground.create_oval(400, 145, 450, 195, fill="red", outline="black")
        
        
        UI._opponent_label = aBackground.create_text(50, 185, text=UI._opponents, fill="white", font=("Arial", 15))
        aBackground.create_text(50, 210, text="opponents", fill="white")

        aBackground.tag_bind(UI._opponent_buttons[0], "<Button-1>", self.up_button_click)
        aBackground.tag_bind(UI._opponent_buttons[1], "<Button-1>", self.down_button_click)
        aBackground.tag_bind(UI._reset_button, "<Button-1>", self.reset_button_click)
        aBackground.tag_bind(aBackground.create_text(425, 170, text="Reset", fill="white"), "<Button-1>", self.reset_button_click)

        # Configuration frame
        configFrame = tkinter.Frame(aBackground)
        configFrame.pack()
        configFrame.config(bg="dark green",
                        width=350,height=50)
        configFrame.place(x=690, y=135)

        # Language Dropdown
        varLangDropdown = tkinter.StringVar(configFrame)
        varLangDropdown.set("Language")
        UI._language_dropdown = ttk.Combobox(configFrame, textvariable=varLangDropdown)
        UI._language_dropdown["values"] = UI.LANGUAGES
        UI._language_dropdown.current(self._language)
        UI._language_dropdown.pack()

    def refreshOpponents(self):
        UI._background.delete(UI._opponent_label)
        UI._opponent_label = UI._background.create_text(50, 185, text=UI._opponents, fill="white", font=("Arial", 15))

    def on_closing(self):
        self._backgroundStopEvent.set()
        self.root.destroy()

    def up_button_click(self, event):
        if (UI._opponents<9):
            UI._opponents+=1
            self.refreshOpponents()

    def down_button_click(self, event):
        if (UI._opponents>1):
            UI._opponents-=1
            self.refreshOpponents()
    
    def reset_button_click(self, event):
        self.resetTableCards()
        self.resetDeckCards()
        self._backgroundThread.cleanMemory()

    def card_click(self, event, relatedFrame, cardCode):
        print("Card: [" + str(cardCode[0]) + "," + str(cardCode[1]) + "] on frame " + str(relatedFrame))
        
        self._backgroundThread.keepInMemory([relatedFrame, cardCode])

        return True

    def card_hold(self, event, relatedFrame, cardCode):
        print("Holding Card!")

    def card_release(self, event, relatedFrame, cardCode):
        print("Release Card!")

    @staticmethod
    def cardImage(rank: int, suit: int, size):
        _rank = rank
        _suit = suit
        if (_rank>12 or _suit>4):
            _rank=2
            _suit=4

        left = 3 + ((2+26)*_rank)
        upper = 3 + ((2+36)*_suit) 
        right = left+UI.CARD_IMAGE_SIZE[0]
        lower = upper+UI.CARD_IMAGE_SIZE[1]

        image = Image.open(UI.POKER_DECK_IMAGE)

        image_crop = image.crop((left, upper, right, lower))
        image_crop_resize = image_crop.resize((size[0], size[1]))

        return ImageTk.PhotoImage(image_crop_resize)
    
    @staticmethod
    def drawRectangle(background, slot: int):
        rectangle = background.create_rectangle(UI.CARD_LOCATION[slot][0]-UI.REDRECTANGLE_WIDTH, 
                                          UI.CARD_LOCATION[slot][1]-UI.REDRECTANGLE_WIDTH, 
                                          UI.CARD_LOCATION[slot][0]+UI.CARD_SIZE[0]+(UI.REDRECTANGLE_WIDTH*2), 
                                          UI.CARD_LOCATION[slot][1]+UI.CARD_SIZE[1]+(UI.REDRECTANGLE_WIDTH*2), 
                                          outline="orange", width=UI.REDRECTANGLE_WIDTH)
        
        return rectangle
    
    @staticmethod
    def drawRectangle(frame, colour):
        rectangle = frame.create_rectangle(0,0,frame.windo_width(),frame.windo_height(), 
                                           outline=colour, width=UI.REDRECTANGLE_WIDTH)
    
    @staticmethod
    def deleteRectangle(background, RECtangle):
        if (background!=None):
            background.delete(RECtangle)          

    @staticmethod
    def deckSlotToCardCode(deckSlot: int):
        _deckSlot = deckSlot+1
        _suit = int(((deckSlot-(deckSlot%13))/13)+1)
        _rank = int((deckSlot%13)+1)
        return [_rank, _suit]

    @staticmethod
    def deckCardCodeToSlot(cardCode):
        return (13*(cardCode[1]-1))+(cardCode[0]-1)

    @staticmethod
    def imageCodeToCardCode(_rank: int, _suit: int):
        if _suit>3:
            return[0,0]
        else:
            codeRank = _rank+1
            match _suit:
                case 0:
                    codeSuit = 3
                case 1:
                    #imageSuit = 3
                    codeSuit = 4
                case 2:
                    #imageSuit = 2
                    codeSuit = 2
                case 3:
                    #imageSuit = 0
                    codeSuit = 1
                #case 4:
                    #imageSuit = 1
                    #codeSuit = 0

        return [codeRank, codeSuit]     

    @staticmethod
    def getRGBFromScale(scale):
        value = scale*255
        if value<0:
            value=0
        if value>100:
            value=100
        red = 255
        green = 0
        if value > 50:
            red -= int((value-50) * 255/50)
            green += int((value-50) * 255/50)
        else:
            green += int(value * 255/50)
        blue = 0
        return f"#{red:02x}{green:02x}{blue:02x}"

class UIBackgroundThread(Thread):
    _UI = None
    _stopped = None

    _resultLabels = []
    _lastResults = []

    _swappingCardsMemory = []
    _memoryRectangles = [None,None]

    def __init__(self, event, ui):
        Thread.__init__(self)
        self._stopped = event
        self._UI = ui        

    def run(self):
        print("Background Thread Start...")
        while not self._stopped.wait(0.5):
            #print("Background Thread Loop...")
            print(str(self._swappingCardsMemory))

            self.swappingFromMemory()

            self.writeResultFrame()
        print("Background Thread Exit...")

    def drawRectangles(self):
        for i in range(len(self._swappingCardsMemory)):
            if (self._memoryRectangles[i]==None):
                UI.drawRectangle(self._swappingCardsMemory, "orange")
    
    def cleanMemory(self):
        self._swappingCardsMemory = []
        self._resultLabels = []
        self._lastResults = []

    def swappingFromMemory(self):
        if len(self._swappingCardsMemory)>1:
            print(self._swappingCardsMemory[0][0].master.winfo_id())
            print(self._UI._card_deck_frame.winfo_id())
            if (self._swappingCardsMemory[0][0].master.winfo_id()==self._UI._card_deck_frame.winfo_id() or
                self._swappingCardsMemory[1][0].master.winfo_id()==self._UI._card_deck_frame.winfo_id()):
                    if (self._swappingCardsMemory[0][0].winfo_parent()==self._swappingCardsMemory[1][0].winfo_id()):
                        pass
                    else:
                        deckCardArr = None
                        tableCardArr = None
                        if (self._swappingCardsMemory[0][0].master.winfo_id()!=self._UI._card_deck_frame.winfo_id()):
                            deckCardArr = self._swappingCardsMemory[1]
                            tableCardArr = self._swappingCardsMemory[0]
                        else:
                            deckCardArr = self._swappingCardsMemory[0]
                            tableCardArr = self._swappingCardsMemory[1]

                        if (tableCardArr[1] == [0,0]):
                            self._UI.setDeckCard(deckCardArr[0].winfo_children()[0].slot, False)
                            self._UI.setCardToSlot(deckCardArr[1][0],deckCardArr[1][1],tableCardArr[0].slot) 
                        else:
                            self._UI.setDeckCard(UI.deckCardCodeToSlot(tableCardArr[1]), True)
                            #self._UI.setDeckCard(deckCardArr[0].winfo_children()[0].slot, True)
                            self._UI.setCardToSlot(0,0,tableCardArr[0].slot)
            else:
                self._UI.setCardToSlot(self._swappingCardsMemory[1][1][0],
                                    self._swappingCardsMemory[1][1][1],
                                    self._swappingCardsMemory[0][0].slot)
                self._UI.setCardToSlot(self._swappingCardsMemory[0][1][0],
                                    self._swappingCardsMemory[0][1][1],
                                    self._swappingCardsMemory[1][0].slot)

            self._swappingCardsMemory = []        
        
    def keepInMemory(self, memoryArr):
        if len(self._swappingCardsMemory)<2:
            self._swappingCardsMemory.append(memoryArr)

    def writeResultFrame(self):
        _card_slot_temp = self._UI._card_slot
        _opponents_temp = self._UI._opponents
        _result_frame = self._UI._result_frame

        _pCardsArr = [_card_slot_temp[0], _card_slot_temp[1]]
        _cCardsArr = [_card_slot_temp[2],_card_slot_temp[3],_card_slot_temp[4],_card_slot_temp[5],_card_slot_temp[6]]

        _results = self.buildTextResult(_pCardsArr, _cCardsArr, _opponents_temp)


        if (not UIBackgroundThread.compareResults(self._lastResults, _results)):
            for widget in _result_frame.winfo_children():
                widget.destroy()

            for index, row in enumerate(_results):
                _startColumn = 0
                if ((index%2)>0):
                    _startColumn = 2
                Label(_result_frame, text=row[0], bg=_result_frame["bg"], foreground="white").grid(row=int((index-(index%2))/2), column=_startColumn, sticky="E")
                Label(_result_frame, text=row[1], bg=_result_frame["bg"], foreground=UI.getRGBFromScale(row[2])).grid(row=int((index-(index%2))/2), column=_startColumn+1, sticky="E")

            for widget in _result_frame.winfo_children():
                widget.config(font=("Arial", 12))

            self._lastResults = _results

    def buildTextResult(self, pCardsArr, cCardsArr, opponents: int):
        _pCardsArr = list(pCardsArr)
        _cCardsArr = list(cCardsArr)
        for i in range(len(_pCardsArr)):
            if (_pCardsArr[i].suit==0 or _pCardsArr[i].rank==0):
                _pCardsArr[i]=None

        for i in range(len(_cCardsArr)):
            if (_cCardsArr[i].suit==0 or _cCardsArr[i].rank==0):
                _cCardsArr[i]=None

        _result = self.validateTable(_pCardsArr, _cCardsArr, opponents)

        if not _result[0]:
            return [[_result[1],"",0]]
        
        #_arrText = None
        #_arrText = self.runEstimation(_pCardsArr, _cCardsArr, opponents)

        return self.runEstimation(_pCardsArr, _cCardsArr, opponents)

        #_result = ""
        #for sentence in _arrText:
        #    _result += sentence + "\n"

        #return _result

    def validateTable(self, pCardsArr, cCardsArr, opponents: int):
        _language = int(self._UI._language)
        if (len(pCardsArr)!=2):
            return [False, Messages._001._value_[_language]]
        if (len(cCardsArr)!=5):
            return [False, Messages._001._value_[_language]]
        if (opponents<1 or opponents>9):
            return [False, Messages._001._value_[_language]]
        
        for card in pCardsArr:
            if (card==None):
                return [False, Messages._002._value_[_language]]
            if (card.suit==0 or card.rank==0):
                return [False, Messages._002._value_[_language]]

        all_cards = list(pCardsArr)
        all_cards.extend(cCardsArr)

        cardList = []
        for card in all_cards:
            if card!=None:
                if card.getString() in cardList:
                    return [False, Messages._003._value_[_language]]
                else:
                    cardList.append(card.getString())
        
        return [True, Messages._000._value_[_language]]
    
    def runEstimation(self, pCardsArr, cCardsArr, opponents: int):
        _language = int(self._UI._language)
        _pCardsArr = []
        _cCardsArr = []
        for card in pCardsArr:
            if (card!=None):
                _pCardsArr.append(card)

        for card in cCardsArr:
            if (card!=None):
                _cCardsArr.append(card)

        probability_table = Game.build_probability_table(_pCardsArr, _cCardsArr)

        _winningProbArr = [Game.winning_probability_with_table(probability_table, opponents+1, Play.ONE_PAIR),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.TWO_PAIR),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.THREE_OF_A_KIND),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.STRAIGHT),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.FLUSH),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.FOUR_OF_A_KIND),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.STRAIGHT_FLUSH),
                           Game.winning_probability_with_table(probability_table, opponents+1, Play.ROYAL_FLUSH),
                           Game.winning_probability_with_table(probability_table, opponents+1, None)]

        _results = [[Messages._004._value_[_language] + " : ",Card.stringifyCardArray(_pCardsArr), len(_pCardsArr)],
                    [Messages._005._value_[_language] + " : ",Card.stringifyCardArray(_cCardsArr), len(_cCardsArr)],
                    [Messages._006._value_[_language] + " : ",str(opponents), opponents],
                    [Messages._008._value_[_language] + " : ","{:.2%}".format(_winningProbArr[0]), _winningProbArr[0]],
                    [Messages._009._value_[_language] + " : ","{:.2%}".format(_winningProbArr[1]), _winningProbArr[1]],
                    [Messages._010._value_[_language] + " : ","{:.2%}".format(_winningProbArr[2]), _winningProbArr[2]],
                    [Messages._011._value_[_language] + " : ","{:.2%}".format(_winningProbArr[3]), _winningProbArr[3]],
                    [Messages._012._value_[_language] + " : ","{:.2%}".format(_winningProbArr[4]), _winningProbArr[4]],
                    [Messages._013._value_[_language] + " : ","{:.2%}".format(_winningProbArr[5]), _winningProbArr[5]],
                    [Messages._014._value_[_language] + " : ","{:.2%}".format(_winningProbArr[6]), _winningProbArr[6]],
                    [Messages._015._value_[_language] + " : ","{:.2%}".format(_winningProbArr[7]), _winningProbArr[7]],
                    [Messages._016._value_[_language] + " : ","{:.2%}".format(_winningProbArr[8]), _winningProbArr[8]]]

        '''        
        _return = []
        _return.append("")
        _return.append(Messages._004._value_[_language] + " : " + Card.stringifyCardArray(_pCardsArr))
        _return.append(Messages._005._value_[_language] + " : " + Card.stringifyCardArray(_cCardsArr))
        _return.append(Messages._006._value_[_language] + " : " + str(opponents))
        _return.append(Messages._007._value_[_language])
        _return.append(Messages._008._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.ONE_PAIR)))
        _return.append(Messages._009._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.TWO_PAIR)))
        _return.append(Messages._010._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.THREE_OF_A_KIND)))
        _return.append(Messages._011._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.STRAIGHT)))
        _return.append(Messages._012._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.FLUSH)))
        _return.append(Messages._013._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.FOUR_OF_A_KIND)))
        _return.append(Messages._014._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.STRAIGHT_FLUSH)))
        _return.append(Messages._015._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, Play.ROYAL_FLUSH)))
        _return.append(Messages._016._value_[_language] + " :" + "{:.2%}".format(Game.winning_probability_with_table(probability_table, opponents+1, None)))
        '''
        
        return _results

    @staticmethod
    def compareResults(results1, results2):
        if (len(results1)!=len(results2)):
            return False
        
        for i in range(len(results1)):
            if (results1[i][2]!=results2[i][2]):
                return False
            
        return True

class Messages(Enum):
    _000 = ["Ok!","¡Vale!"]
    _001 = ["Error in structure", "Error en la estructura"]
    _002 = ["At least two private cards are needed", "Se requiere al menos dos cartas privadas"]
    _003 = ["Duplicated cards in hand", "Cartas en mano duplicadas"]

    _004 = ["Private Cards", "Cartas Privadas"]
    _005 = ["Community Cards", "Cartas Comunitarias"]
    _006 = ["Opponents", "Oponentes"]
    _007 = ["Calculating...", "Calculando..."]
    _008 = ["1Pair Win probs", "Prob.Vict. Pareja"]
    _009 = ["2Pair Win probs", "Prob.Vict. 2Parejas"]
    _010 = ["3Kind Win probs", "Prob.Vict. Trio"]
    _011 = ["Strght Win probs", "Prob.Vict. Esclera"]
    _012 = ["Flush Win probs", "Prob.Vict. Color"]
    _013 = ["4Kind Win probs", "Prob.Vict. Póker"]
    _014 = ["StrFsh Win probs", "Prob.Vict. Esc.Color"]
    _015 = ["RylFls Win probs", "Prob.Vict. Esc.Real"]
    _016 = ["TOTAL Win probs", "Prob.Vict. TOTAL"]

window = UI()
window.run()

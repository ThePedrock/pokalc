from table.card import Card
from table.suit import Suit
from table.deck import Deck
from table.play import Play

class Game:
    TOTAL_HAND_CARDS = 7
    TOTAL_DECK_CARDS = 52
    
    @staticmethod
    def one_pair_probability(hand):
        rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            rank_count[card.rank] += 1

        open_pair_indexes = []
        for i in range(len(rank_count)):
            if rank_count[i] > 1:
                return 1
            if rank_count[i] == 1:
                open_pair_indexes.append(rank_count[i])

        probability = 0

        if Game.TOTAL_HAND_CARDS-len(hand)>0:
            probability += (3/((Game.TOTAL_DECK_CARDS)-len(hand))) * len(open_pair_indexes)       
        
        if Game.TOTAL_HAND_CARDS-len(hand)>1:
            probability += (4/((Game.TOTAL_DECK_CARDS)-len(hand)) * 3/((Game.TOTAL_DECK_CARDS)-len(hand)-1)) * (13-len(open_pair_indexes))

        return probability
    
    @staticmethod
    def two_pair_probability(hand):
        rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            rank_count[card.rank] += 1

        probability = 0
        for i in range(len(rank_count)-1):
            for j in range(i+1, len(rank_count)):
                if (rank_count[i]>2 or rank_count[j]>2): 
                    return 0
                if (rank_count[i]>1 and rank_count[j]>1):
                    return 1
                elif ((Game.TOTAL_HAND_CARDS-len(hand))>(rank_count[i]+rank_count[j])):
                    nProbability=1
                    if rank_count[i]<2:
                        if rank_count[i]>0:
                            nProbability *= (3/((Game.TOTAL_DECK_CARDS)-len(hand)))
                        else:
                            nProbability *= (4/((Game.TOTAL_DECK_CARDS)-len(hand))) * (3/((Game.TOTAL_DECK_CARDS)-len(hand)-1))
                    if rank_count[j]<2:
                        if rank_count[i]>0:
                            nProbability *= (3/((Game.TOTAL_DECK_CARDS)-len(hand)))
                        else:
                            nProbability *= (4/((Game.TOTAL_DECK_CARDS)-len(hand))) * (3/((Game.TOTAL_DECK_CARDS)-len(hand)-1))

                    probability += nProbability
        
        return probability

    @staticmethod
    def three_of_a_kind_probability(hand):
        rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            rank_count[card.rank] += 1

        open_three_indexes = []
        for i in range(1, len(rank_count)):
            if rank_count[i] > 2:
                return 1
            if rank_count[i] == 0 and (((Game.TOTAL_HAND_CARDS)-len(hand))>2):
                open_three_indexes.append(i)            
            if rank_count[i] == 1 and (((Game.TOTAL_HAND_CARDS)-len(hand))>1):
                open_three_indexes.append(i)
            if rank_count[i] == 2 and (((Game.TOTAL_HAND_CARDS)-len(hand))>0):
                open_three_indexes.append(i)

        probability = 0
        for i in range(len(open_three_indexes)):
            match rank_count[open_three_indexes[i]]:
                case 0:
                    nProbability=1
                    for i in range(1,4):                        
                        nProbability*=((4-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability
                case 1:
                    nProbability=1
                    for i in range(1,3):                        
                        nProbability*=((3-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability                                         
                case 2:
                    nProbability=1
                    for i in range(1,2):                        
                        nProbability*=((2-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability      
                case _:
                    probability+=0

        return probability
    
    @staticmethod
    def straight_probability(hand):
        rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            rank_count[card.rank] += 1

        refined_rank_count = [rank_count[1],rank_count[2],rank_count[3],rank_count[4],rank_count[5],rank_count[6],rank_count[7],
                              rank_count[8],rank_count[9],rank_count[10],rank_count[11],rank_count[12],rank_count[13],
                              rank_count[1]]
        
        probability = 0
        for i in range(5, len(refined_rank_count)):
            zero_rank_count = 0
            for j in range(i-5, i):
                if refined_rank_count[j]==0:
                    zero_rank_count+=1
            
            nProbability = 1
            if (Game.TOTAL_HAND_CARDS)-len(hand)>=zero_rank_count:
                for k in range(zero_rank_count):
                    nProbability*=(4/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
                probability+=nProbability

        return probability 

    @staticmethod
    def flush_probability(hand):
        suit_count = [0,0,0,0,0]
        for card in hand:
            suit_count[card.suit.value] += 1
        
        open_flush_suits = [0,0,0,0,0]
        for i in range(1, len(suit_count)):
            if suit_count[i] > 4:
                return 1
            if suit_count[i] == 4 and (((Game.TOTAL_HAND_CARDS)-len(hand))>0):
                open_flush_suits[i] = 1
            if suit_count[i] == 3 and (((Game.TOTAL_HAND_CARDS)-len(hand))>1):
                open_flush_suits[i] = 1
            if suit_count[i] == 2 and (((Game.TOTAL_HAND_CARDS)-len(hand))>2):
                open_flush_suits[i] = 1
            if suit_count[i] == 1 and (((Game.TOTAL_HAND_CARDS)-len(hand))>3):
                open_flush_suits[i] = 1
            if suit_count[i] == 0 and (((Game.TOTAL_HAND_CARDS)-len(hand))>4):
                open_flush_suits[i] = 1
        
        probability = 0
        for i in range(1, len(open_flush_suits)):
            if open_flush_suits[i]==1:
                match suit_count[i]:
                    case 0:
                        nProbability=1
                        for i in range(1,6):                        
                            nProbability*=((13-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                        probability+=nProbability
                    case 1:
                        nProbability=1
                        for i in range(1,5):                        
                            nProbability*=((12-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                        probability+=nProbability
                    case 2:
                        nProbability=1
                        for i in range(1,4):                        
                            nProbability*=((11-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                        probability+=nProbability
                    case 3:
                        nProbability=1
                        for i in range(1,3):                        
                            nProbability*=((10-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                        probability+=nProbability
                    case 4:
                        nProbability=1
                        for i in range(1,2):                        
                            nProbability*=((9-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                        probability+=nProbability
                    case _:
                        probability+=0

        return probability

    @staticmethod
    def full_house_probability(hand):
        rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            rank_count[card.rank] += 1

        probability = 0
        for i in range(len(rank_count)-1):
            for j in range(i+1, len(rank_count)):
                #i as three, j as pair
                nProbability = 0
                cards_to_draw = (Game.TOTAL_HAND_CARDS-len(hand))
                if rank_count[i]==3 and rank_count[i]==2:
                    return 1
                
                if rank_count[i]==2:
                    cards_to_draw-=1
                    nProbability += (2/((Game.TOTAL_DECK_CARDS)-len(hand)))
                if rank_count[i]==1:
                    cards_to_draw-=2
                    nProbability += (3/((Game.TOTAL_DECK_CARDS)-len(hand))) * (2/((Game.TOTAL_DECK_CARDS)-len(hand)-1))
                if rank_count[i]==0:
                    cards_to_draw-=3
                    nProbability += (3/((Game.TOTAL_DECK_CARDS)-len(hand))) * (2/((Game.TOTAL_DECK_CARDS)-len(hand)-1)) * (1/((Game.TOTAL_DECK_CARDS)-len(hand)-2))

                if rank_count[j]==1:
                    nProbability *= (3/((Game.TOTAL_DECK_CARDS)-len(hand)-(3-rank_count[i])))
                    cards_to_draw-=1
                if rank_count[j]==0:
                    nProbability *= (4/((Game.TOTAL_DECK_CARDS)-len(hand)-(3-rank_count[i]))) * (3/((Game.TOTAL_DECK_CARDS)-len(hand)-(3-rank_count[i])-1))
                    cards_to_draw-=2

                if cards_to_draw>=0:
                    probability+=nProbability

                #i as pair, j as three
                nProbability = 0
                cards_to_draw = (Game.TOTAL_HAND_CARDS-len(hand))
                if rank_count[i]==2 and rank_count[i]==3:
                    return 1

                if rank_count[i]==1:
                    nProbability += (3/((Game.TOTAL_DECK_CARDS)-len(hand)))
                    cards_to_draw-=1
                if rank_count[i]==0:
                    nProbability += (4/((Game.TOTAL_DECK_CARDS)-len(hand))) * (3/((Game.TOTAL_DECK_CARDS)-len(hand)-1))
                    cards_to_draw-=2

                if rank_count[j]==2:
                    cards_to_draw-=1
                    nProbability *= (2/((Game.TOTAL_DECK_CARDS)-len(hand)-(2-rank_count[i])))
                if rank_count[j]==1:
                    cards_to_draw-=2
                    nProbability *= (3/((Game.TOTAL_DECK_CARDS)-len(hand)-(2-rank_count[i]))) * (2/((Game.TOTAL_DECK_CARDS)-len(hand)-(2-rank_count[i])-1))
                if rank_count[j]==0:
                    cards_to_draw-=3
                    nProbability *= (4/((Game.TOTAL_DECK_CARDS)-len(hand)-(2-rank_count[i]))) * (3/((Game.TOTAL_DECK_CARDS)-len(hand)-(2-rank_count[i])-1)) * (2/((Game.TOTAL_DECK_CARDS)-len(hand)-(2-rank_count[i])-2))

                if cards_to_draw>=0:
                    probability+=nProbability
        
        return probability

    @staticmethod
    def four_of_a_kind_probability(hand):
        rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            rank_count[card.rank] += 1

        open_poker_indexes = []
        for i in range(1, len(rank_count)):
            if rank_count[i] > 3:
                return 1
            if rank_count[i] == 0 and (((Game.TOTAL_HAND_CARDS)-len(hand))>3):
                open_poker_indexes.append(i)
            if rank_count[i] == 1 and (((Game.TOTAL_HAND_CARDS)-len(hand))>2):
                open_poker_indexes.append(i)       
            if rank_count[i] == 2 and (((Game.TOTAL_HAND_CARDS)-len(hand))>1):
                open_poker_indexes.append(i)
            if rank_count[i] == 3 and (((Game.TOTAL_HAND_CARDS)-len(hand))>0):
                open_poker_indexes.append(i)

        probability = 0
        for i in range(len(open_poker_indexes)):
            match rank_count[open_poker_indexes[i]]:
                case 0:
                    nProbability=1
                    for i in range(1,5):                        
                        nProbability*=((5-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability
                case 1:
                    nProbability=1
                    for i in range(1,4):                        
                        nProbability*=((4-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability
                case 2:
                    nProbability=1
                    for i in range(1,3):                        
                        nProbability*=((3-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability                                         
                case 3:
                    nProbability=1
                    for i in range(1,2):                        
                        nProbability*=((2-i)/((Game.TOTAL_DECK_CARDS)-len(hand)-i))
                    probability+=nProbability      
                case _:
                    probability+=0

        return probability
    
    @staticmethod
    def straight_flush_probability(hand):
        hearts_rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        diamonds_rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        clubs_rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        spades_rank_count = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        for card in hand:
            match card.suit.value:
                case 1:
                    hearts_rank_count[card.rank-1] = 1
                case 2:
                    diamonds_rank_count[card.rank-1] = 1
                case 3:
                    clubs_rank_count[card.rank-1] = 1
                case 4:
                    spades_rank_count[card.rank-1] = 1
                case _:
                    pass

        probability = 0
        for i in range(5, len(hearts_rank_count)):
            hearts_lack_card_count = 0
            diamonds_lack_card_count = 0
            clubs_lack_card_count = 0
            spades_lack_card_count = 0
            for j in range(i-5, i):
                if hearts_rank_count[j]==0:
                    hearts_lack_card_count+=1
                if diamonds_rank_count[j]==0:
                    diamonds_lack_card_count+=1
                if clubs_rank_count[j]==0:
                    clubs_lack_card_count+=1
                if spades_rank_count[j]==0:
                    spades_lack_card_count+=1                                                            
            
            hProbability = 1
            if (Game.TOTAL_HAND_CARDS)-len(hand)>=hearts_lack_card_count:
                for k in range(hearts_lack_card_count):
                    hProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
                probability+=hProbability

            dProbability = 1
            if (Game.TOTAL_HAND_CARDS)-len(hand)>=diamonds_lack_card_count:
                for k in range(diamonds_lack_card_count):
                    dProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
                probability+=dProbability

            cProbability = 1
            if (Game.TOTAL_HAND_CARDS)-len(hand)>=clubs_lack_card_count:
                for k in range(clubs_lack_card_count):
                    cProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
                probability+=cProbability

            pProbability = 1
            if (Game.TOTAL_HAND_CARDS)-len(hand)>=spades_lack_card_count:
                for k in range(spades_lack_card_count):
                    pProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
                probability+=pProbability                                

        return probability     
    
    @staticmethod
    def royal_flush_probability(hand):    
        hearts_rank_count = [0,0,0,0,0]
        diamonds_rank_count = [0,0,0,0,0]
        clubs_rank_count = [0,0,0,0,0]
        spades_rank_count = [0,0,0,0,0]
        for card in hand:
            match card.suit.value:
                case 1:
                    if card.rank>9:
                        hearts_rank_count[card.rank-10] = 1
                    if card.rank==1:
                        hearts_rank_count[4] = 1
                case 2:
                    if card.rank>9:
                        diamonds_rank_count[card.rank-10] = 1
                    if card.rank==1:
                        diamonds_rank_count[4] = 1
                case 3:
                    if card.rank>9:
                        clubs_rank_count[card.rank-10] = 1
                    if card.rank==1:
                        clubs_rank_count[4] = 1
                case 4:
                    if card.rank>9:
                        spades_rank_count[card.rank-10] = 1
                    if card.rank==1:
                        spades_rank_count[4] = 1
                case _:
                    pass

        probability = 0
        hearts_lack_card_count = 0
        diamonds_lack_card_count = 0
        clubs_lack_card_count = 0
        spades_lack_card_count = 0
        for j in range(len(hearts_rank_count)):
            if hearts_rank_count[j]==0:
                hearts_lack_card_count+=1
            if diamonds_rank_count[j]==0:
                diamonds_lack_card_count+=1
            if clubs_rank_count[j]==0:
                clubs_lack_card_count+=1
            if spades_rank_count[j]==0:
                spades_lack_card_count+=1

        hProbability = 1
        if (Game.TOTAL_HAND_CARDS)-len(hand)>=hearts_lack_card_count:
            for k in range(hearts_lack_card_count):
                hProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
            probability+=hProbability

        dProbability = 1
        if (Game.TOTAL_HAND_CARDS)-len(hand)>=diamonds_lack_card_count:
            for k in range(diamonds_lack_card_count):
                dProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
            probability+=dProbability

        cProbability = 1
        if (Game.TOTAL_HAND_CARDS)-len(hand)>=clubs_lack_card_count:
            for k in range(clubs_lack_card_count):
                cProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
            probability+=cProbability

        pProbability = 1
        if (Game.TOTAL_HAND_CARDS)-len(hand)>=spades_lack_card_count:
            for k in range(spades_lack_card_count):
                pProbability*=(1/((Game.TOTAL_DECK_CARDS)-len(hand)-k))
            probability+=pProbability

        return probability
    
    @staticmethod
    def build_probability_table(private_cards, community_cards):
        prob_table = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        all_cards = list(private_cards)
        all_cards.extend(community_cards)

        #one_pair_probability
        prob_table[0][0] = Game.one_pair_probability(all_cards)
        prob_table[0][1] = Game.one_pair_probability(community_cards)

        #two_pair_probability
        prob_table[1][0] = Game.two_pair_probability(all_cards)
        prob_table[1][1] = Game.two_pair_probability(community_cards)

        #three_of_a_kind_probability
        prob_table[2][0] = Game.three_of_a_kind_probability(all_cards)
        prob_table[2][1] = Game.three_of_a_kind_probability(community_cards)

        #straight_probability
        prob_table[3][0] = Game.straight_probability(all_cards)
        prob_table[3][1] = Game.straight_probability(community_cards)

        #flush_probability
        prob_table[4][0] = Game.flush_probability(all_cards)
        prob_table[4][1] = Game.flush_probability(community_cards)

        #full_house_probability
        prob_table[5][0] = Game.full_house_probability(all_cards)
        prob_table[5][1] = Game.full_house_probability(community_cards)

        #four_of_a_kind_probability
        prob_table[6][0] = Game.four_of_a_kind_probability(all_cards)
        prob_table[6][1] = Game.four_of_a_kind_probability(community_cards)

        #straight_flush_probability
        prob_table[7][0] = Game.straight_flush_probability(all_cards)
        prob_table[7][1] = Game.straight_flush_probability(community_cards)

        #royal_flush_probability
        prob_table[8][0] = Game.royal_flush_probability(all_cards)
        prob_table[8][1] = Game.royal_flush_probability(community_cards)

        return prob_table
    
    @staticmethod
    def winning_probability_with_table(probability_matrix, players: int, play: Play):
        player_probability = 0

        if (play is None):
            play = Play.UNKNOWN
        if (play.value>0):
            oponnent_probability = 1
            for i in range(play.value,7):
                oponnent_probability *= pow(1-probability_matrix[i-1][1], players-1)

            player_probability = probability_matrix[play.value-1][0]

            return player_probability * oponnent_probability
        else:
            for aPlay in Play:
                if (aPlay.value>0):
                    player_probability += Game.winning_probability_with_table(probability_matrix, players, aPlay)

        return player_probability

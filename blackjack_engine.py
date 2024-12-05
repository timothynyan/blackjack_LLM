import random

class Blackjack:
    def __init__(self):
        self.deck = ["S-A", "S-2", "S-3", "S-4", "S-5", "S-6", "S-7", "S-8", "S-9", "S-10", "S-J", "S-Q", "S-K",
                     "H-A", "H-2", "H-3", "H-4", "H-5", "H-6", "H-7", "H-8", "H-9", "H-10", "H-J", "H-Q", "H-K",
                     "D-A", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7", "D-8", "D-9", "D-10", "D-J", "D-Q", "D-K",
                     "C-A", "C-2", "C-3", "C-4", "C-5", "C-6", "C-7", "C-8", "C-9", "C-10", "C-J", "C-Q", "C-K"]
        self.current_deck = self.new_deck()
        self.players = []
        self.dealer = self.Dealer()

    def add_player(self, player_count: int):
        for i in range(player_count):
            player = self.Player()
            player.set_name(f"Player {i+1}")
            self.players.append(player)
        print(f"{player_count} players have been added to the game.")
    
    def remove_player(self, player_count: int):
        for i in range(player_count):
            if self.players:
                self.players.pop()
        print(f"{player_count} players have been removed from the game.")

    def shuffle_deck(self):
        random.shuffle(self.current_deck)

    def new_deck(self, deck_count: int = 1):
        return self.deck * deck_count

    def check_deck_count(self):
        return len(self.current_deck)
    
    def deal(self):
        for i in range(2):
            for player in self.players:
                player.hand.append(self.current_deck.pop())
            self.dealer.hand.append(self.current_deck.pop())
        for player in self.players:
            print(f"{player.name} has been dealt {player.hand[0]} and {player.hand[1]}.")
        print(f"Dealer has been dealt {self.dealer.hand[0]} and one hidden card.")

    def player_turn(self, player):
        while player.status:
            if player.hand_value == 21:
                player.stand()
            else:
                action = input("1. Hit\n2. Stand\n3. Double Down\n4. Surrender\n")
                if action == "1":
                    player.hit(self.current_deck)
                elif action == "2":
                    player.stand()
                elif action == "3":
                    player.double_down(self.current_deck)
                elif action == "4":
                    player.surrender()
                else:
                    print("Invalid input. Please try again.")
        return player.hand_value
    
    def dealer_turn(self):
        while self.dealer.status:
            self.dealer.check_hand(self.current_deck)
        return self.dealer.hand_value

    def check_winner(self):
        dealer_value = self.dealer.hand_value
        for player in self.players:
            player_value = player.hand_value
            if self.dealer.bust:
                player.balance += player.bet * 2
                print(f"{player.name} wins.")
                break
            if player_value > dealer_value and player_value <= 21:
                player.balance += player.bet * 2
                print(f"{player.name} wins.")
            elif player_value == dealer_value:
                player.balance += player.bet
                print(f"{player.name} ties.")
            else:
                print(f"{player.name} loses.")
            player.reset()
        self.dealer.reset()

    def play(self):
        print("Welcome to Blackjack!")
        player_count = int(input("How many players are playing? "))
        self.add_player(player_count)
        while self.check_deck_count() > 10:
            self.shuffle_deck()
            self.deal()
            for player in self.players:
                player.set_bet(int(input(f"{player.name}, place your bet: ")))
                player.calculate_hand_value()
                self.player_turn(player)
                if player.bust:
                    #remove player from game
                    self.players.remove(player)
            self.dealer.calculate_hand_value()
            self.dealer_turn()
            self.check_winner()
            for player in self.players:
                print(f"{player.name}'s balance is {player.balance}.")
            if input("Would you like to play another round? (Y/N) ") == "N":
                break
        print("Thank you for playing Blackjack!")

    class Player:
        def __init__(self):
            self.name = "Player"
            self.hand = []
            self.hand_value = 0
            self.status = True
            self.balance = 1000
            self.bet = 0
            self.bust = False
        
        def set_name(self, name):
            self.name = name
        
        def set_bet(self, bet):
            self.bet = bet
            self.balance -= bet
            print(f"{self.name} bets amount: {self.bet}.")

        def calculate_hand_value(self):
            value = 0
            aces = 0
            for card in self.hand:
                if card[2] == "A":
                    value += 11
                    aces += 1
                elif card[2] in ["J", "Q", "K"]:
                    value += 10
                else:
                    value += int(card[2])
            while value > 21 and aces:
                value -= 10
                aces -= 1
            self.hand_value = value
            print(f"{self.name}'s hand value is {self.hand_value}.")
            return value

        def hit(self, deck):
            print(f"{self.name} hits.")
            self.hand.append(deck.pop())
            self.calculate_hand_value()
            self.check_bust()
            
        def stand(self):
            self.status = False
            print(f"{self.name} stands.")
            return self.hand_value

        def double_down(self, deck):
            print(f"{self.name} doubles down.")
            self.balance -= self.bet
            self.bet *= 2
            self.hit(deck)
            self.stand()

        def surrender(self):
            print(f"{self.name} surrenders.")
            self.balance += self.bet / 2
            self.bet = 0
            self.status = False

        def reset(self):
            self.hand = []
            self.hand_value = 0
            self.bet = 0
            self.status = True

        def check_bust(self):
            if self.hand_value > 21:
                self.bust = True
                self.status = False
                print(f"{self.name} busts.")

    class Dealer:
        def __init__(self):
            self.hand = []
            self.hand_value = 0
            self.status = True
            self.bust = False
        
        def calculate_hand_value(self):
            value = 0
            aces = 0
            for card in self.hand:
                if card[2] == "A":
                    value += 11
                    aces += 1
                elif card[2] in ["J", "Q", "K"]:
                    value += 10
                else:
                    value += int(card[2])
            while value > 21 and aces:
                value -= 10
                aces -= 1
            self.hand_value = value
            print(f"Dealer's hand value is {self.hand_value}.")
            return value

        def hit(self, deck):
            print("Dealer hits.")
            self.hand.append(deck.pop())
            self.calculate_hand_value()
            self.check_bust()

        def stand(self):
            self.status = False
            print("Dealer stands.")
            return self.hand_value

        def reset(self):
            self.hand = []
            self.hand_value = 0
            self.status = True

        def check_bust(self):
            if self.hand_value > 21:
                self.status = False
                print("Dealer busts.")
                self.bust = True

        def check_hand(self, deck):
            while self.hand_value < 17:
                self.hit(deck)
            if self.status:
                self.stand()
            

import random

# Constants
CARD_VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
               'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
CARD_NAMES = list(CARD_VALUES.keys()) * 4
BLACKJACK = 21
DEALER_HIT_THRESHOLD = 17
STARTING_BALANCE = 100


def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


def calculate_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    # Ace is counted as 1 if otherwise the value would exceed 21
    if value > BLACKJACK and 'Ace' in hand:
        ace_count = hand.count('Ace')
        while value > BLACKJACK and ace_count > 0:
            value -= 10
            ace_count -= 1
    return value


def show_hands(player, dealer, end=False):
    print(f"Dealer: {dealer if end else ['Hidden', dealer[1]]} - Value: {'?' if not end else calculate_value(dealer)}")
    print(f"Player: {player} - Value: {calculate_value(player)}")


def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Your current balance is {balance}. How much would you like to bet? "))
            if 1 <= bet <= balance:
                return bet
            else:
                print("Invalid bet amount. Please enter a value within your balance.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def handle_double_down(player_hand, dealer_hand, deck, bet, balance):
    if balance >= bet * 2:
        player_hand.append(draw_card(deck))
        show_hands(player_hand, dealer_hand)
        return calculate_value(player_hand), bet * 2
    else:
        print("You do not have enough balance to double down.")
        return player_turn(player_hand, dealer_hand, deck, bet, balance)


def handle_split(player_hand, deck):
    first_hand = [player_hand[0], draw_card(deck)]
    second_hand = [player_hand[1], draw_card(deck)]
    return [first_hand, second_hand]


def player_turn(player_hand, dealer_hand, deck, bet, balance):
    results = []
    split_hands = [player_hand]

    while split_hands:
        hand = split_hands.pop()
        while True:
            print()
            show_hands(hand, dealer_hand)
            player_value = calculate_value(hand)

            if player_value == BLACKJACK:
                print("Player has Blackjack!")
                results.append((player_value, bet))
                break
            elif player_value > BLACKJACK:
                print("Player busts!")
                results.append((player_value, bet))
                break

            move = input("Choose an action: [h]it, [s]tay, [d]ouble down, [p]lay split: ").lower()
            if move == 'h':
                hand.append(draw_card(deck))
            elif move == 's':
                results.append((player_value, bet))
                break
            elif move == 'd':
                return handle_double_down(hand, dealer_hand, deck, bet, balance)
            elif move == 'p' and len(hand) == 2 and CARD_VALUES[hand[0]] == CARD_VALUES[hand[1]]:
                split_hands.extend(handle_split(hand, deck))
                break
            else:
                print("Invalid input. Please enter 'h', 's', 'd', or 'p'.")

    return results


def dealer_turn(dealer_hand, deck):
    while calculate_value(dealer_hand) < DEALER_HIT_THRESHOLD:
        dealer_hand.append(draw_card(deck))
    return calculate_value(dealer_hand)


def determine_winner(player_value, dealer_value, bet):
    if player_value > BLACKJACK:
        return -bet
    elif dealer_value > BLACKJACK or player_value > dealer_value:
        return bet
    elif player_value < dealer_value:
        return -bet
    else:
        return 0


def blackjack():
    balance = STARTING_BALANCE
    while True:
        print("\nNew round!")
        deck = CARD_NAMES.copy()
        random.shuffle(deck)

        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        bet = get_bet(balance)
        results = player_turn(player_hand, dealer_hand, deck, bet, balance)

        total_result = 0
        for player_value, bet in results:
            dealer_value = dealer_turn(dealer_hand, deck)
            show_hands(player_hand, dealer_hand, end=True)
            outcome = determine_winner(player_value, dealer_value, bet)
            total_result += outcome
            if outcome > 0:
                print("Player wins!")
            elif outcome < 0:
                print("Dealer wins!")
            else:
                print("It's a draw!")

        balance += total_result
        print(f"Current balance: {balance}")

        if balance <= 0:
            print("You are out of money! Game over.")
            if input("Do you want to restart the game? (y/n): ").lower() == 'y':
                balance = STARTING_BALANCE
            else:
                break
        elif input("Do you want to play again? (y/n): ").lower() != 'y':
            print(f"You left with a balance of {balance}. Thanks for playing!")
            break


if __name__ == "__main__":
    blackjack()

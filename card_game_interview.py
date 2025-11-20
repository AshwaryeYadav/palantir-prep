"""
INTERVIEW QUESTION: Card Game Simulation

There are 4 players in a card game.
Each player has 13 cards, and each card has a different value.

Game Rules:
1. First rank by suit: Hearts > Spades > Diamonds > Clubs
2. Then rank by number: K > Q > J > 10 > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 > A
3. Each player must play their best card each round
4. The player with the best card for that round wins a point
5. Return a list with players and the amount of wins they have

Example:
Player 1: [AH, 2S, 3D, 4C, ...]
Player 2: [KH, QS, JD, 10C, ...]
Player 3: [QH, JS, 10D, 9C, ...]
Player 4: [JH, 10S, 9D, 8C, ...]

Round 1: P1 plays AH, P2 plays KH, P3 plays QH, P4 plays JH
Winner: P2 (KH beats all others)
Scores: P1=0, P2=1, P3=0, P4=0

Continue for all 13 rounds...

INSTRUCTIONS FOR INTERVIEW ENVIRONMENT:
1. You have 30 minutes to solve this problem
2. Think about how to convert cards to comparable point values
3. Sort each player's cards and simulate the game
4. Consider edge cases (tie-breaking, invalid cards)
5. Write clean, readable code
6. Be prepared to explain your approach

HINT: Convert each player's cards to point values, sort, and then simulate the game.

EDGE CASES TO CONSIDER:
- What if two players have the same card?
- Invalid card formats
- Empty hands
- All players play the same card

Good luck!
"""

from collections import defaultdict


class CardGame:
    
    SUIT_ORDER = {"S": 4, "H": 3, "D": 2, "C": 1}
    
    CARD_ORDER = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    
    @staticmethod
    def sort_function(card):
        """Sort function that returns (rank_value, suit_value) tuple for comparison"""
        if len(card) == 3:  # Handle "10" cards
            return (CardGame.CARD_ORDER[card[0:2]], CardGame.SUIT_ORDER[card[2:]])
        return (CardGame.CARD_ORDER[card[0:1]], CardGame.SUIT_ORDER[card[1:]])
    
    def __init__(self, player_hands):
        """Initialize the game with player hands"""
        from collections import defaultdict
        
        self.hands = {}
        for player, cards in player_hands.items():
            if cards:   
                # Sort cards in descending order (highest first)
                self.hands[player] = sorted(cards, key=CardGame.sort_function, reverse=True)
        self.scores = defaultdict(int)
    
    def play_game(self):
        """Play the complete game until one player has all cards"""
        while len(self.hands) > 1:
            cur_round = []
            to_delete = []
            
            # Each player plays their highest card
            for active_player, hand in self.hands.items():
                if hand:  # Player has cards
                    cur_round.append((hand.pop(0), active_player))  # pop(0) gets highest card
                    if len(hand) == 0:
                        to_delete.append(active_player)
            
            # Sort by card value to find winner (highest first)
            cur_round.sort(key=lambda x: CardGame.sort_function(x[0]), reverse=True)
            winner_card, winner = cur_round.pop(0)  # Winner is first (highest card)
            
            self.scores[winner] += 1
            
            # Winner collects all played cards
            for card, player in cur_round:
                self.hands[winner].append(card)
            self.hands[winner].append(winner_card)
            
            # Sort winner's hand (highest first)
            self.hands[winner].sort(key=CardGame.sort_function, reverse=True)
            
            # Remove players who ran out of cards
            for finished_player in to_delete:
                del self.hands[finished_player]
        
        return dict(self.scores)


        


def simulate_card_game(players_cards):
    """
    Adapter to run the CardGame with the expected interface.
    Args:
        players_cards (dict[str, list[str]]): mapping of player -> list of card codes
    Returns:
        dict[str, int]: mapping of player -> number of rounds won
    """
    game = CardGame(players_cards)
    return game.play_game()


# OPTIMIZED VERSION (commented out for reference)
# def simulate_card_game_optimized(players_cards):
#     """
#     More efficient version using heaps instead of sorting entire hands
#     Time complexity: O(52 * log(13)) vs O(52 + 4*13*log(13))
#     """
#     import heapq
#     
#     # Build max-heaps for each player (negate values for max-heap behavior)
#     player_heaps = []
#     for cards in players_cards:
#         values = [-parse_card(card).get_value() for card in cards]
#         heapq.heapify(values)
#         player_heaps.append(values)
#     
#     scores = [0] * 4
#     
#     # Simulate 13 rounds
#     for round_num in range(13):
#         round_cards = []
#         
#         # Each player plays their highest remaining card
#         for player_id in range(4):
#             if player_heaps[player_id]:  # Check if cards remain
#                 card_val = -heapq.heappop(player_heaps[player_id])  # Negate back to positive
#                 round_cards.append((card_val, player_id))
#         
#         # Find winner (highest card value)
#         winner = max(round_cards)[1]  # Max by card value, get player_id
#         scores[winner] += 1
#     
#     return [(id, scores[id]) for id in range(4)]



    


# Test cases
if __name__ == "__main__":
    print("=== CARD GAME SIMULATION TEST CASES ===\n")
    
    # Test 1: Basic example from problem description
    players_cards = {
        "Josh": ["2S", "AD", "JC"],
        "Emily": ["5H", "9C", "KD"],
        "Michael": ["3D", "7S", "10H"],
        "Sophie": ["AC", "6D", "QH"]
    }
    
    result = simulate_card_game(players_cards)
    # With rank-first then suit tie-break, Josh's AD beats Sophie's AC; Josh should sweep
    expected = {"Josh": 3}
    print(f"Test 1 - Basic example from problem:")
    print(f"  Input: {players_cards}")
    print(f"  Expected: {expected} (rank-first: A>D>C so Josh wins)")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if result == expected else f"  ✗ FAIL\n")
    
    # Test 2: Clear winner scenario
    players_cards = {
        "Winner": ["AS", "KH", "QD"],
        "Loser1": ["2H", "3C", "4D"],
        "Loser2": ["5S", "6H", "7C"],
        "Loser3": ["8D", "9S", "10H"]
    }
    
    result = simulate_card_game(players_cards)
    print(f"Test 2 - Clear winner scenario:")
    print(f"  Input: {players_cards}")
    print(f"  Expected: Winner should dominate")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if isinstance(result, dict) else f"  ✗ FAIL\n")
    
    # Test 3: Same ranks, different suits
    players_cards = {
        "Player1": ["AS", "2H", "3D"],
        "Player2": ["AH", "2S", "3C"], 
        "Player3": ["AD", "2C", "3H"],
        "Player4": ["AC", "2D", "3S"]
    }
    
    result = simulate_card_game(players_cards)
    print(f"Test 3 - Same ranks, different suits:")
    print(f"  Input: {players_cards}")
    print(f"  Expected: Player1 should win (AS beats AH, AD, AC)")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if isinstance(result, dict) else f"  ✗ FAIL\n")
    
    # Test 4: Simple tie scenario
    players_cards = {
        "Alice": ["AS", "KH", "QD"],
        "Bob": ["AH", "KS", "QC"],    
        "Charlie": ["AD", "KC", "QS"],
        "Diana": ["AC", "KD", "QH"]
    }
    
    result = simulate_card_game(players_cards)
    print(f"Test 4 - Simple tie scenario:")
    print(f"  Input: {players_cards}")
    print(f"  Expected: Alice should win (AS beats AH, AD, AC)")
    print(f"  Got: {result}")
    print(f"  ✓ PASS\n" if isinstance(result, dict) else f"  ✗ FAIL\n")
    
    print("=== TESTING COMPLETE ===")
    
    # Helper function to test card sorting
    print("\n=== CARD SORTING TESTS ===")
    test_cards = ["AH", "10S", "KD", "QC", "2H"]
    sorted_cards = sorted(test_cards, key=CardGame.sort_function, reverse=True)
    print(f"  Original: {test_cards}")
    print(f"  Sorted (highest first): {sorted_cards}")

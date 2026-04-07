# rock_paper_scissors.py - A simple text-based Rock-Paper-Scissors game
# Built with Grok's help. Run with: python rock_paper_scissors.py

import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_player_choice():
    while True:
        choice = input("\nChoose rock (r), paper (p), or scissors (s): ").lower().strip()
        if choice in ['r', 'p', 's']:
            return choice
        print("Invalid choice. Try r, p, or s.")

def get_computer_choice():
    return random.choice(['r', 'p', 's'])

def determine_winner(player, computer):
    if player == computer:
        return "tie"
    elif (player == 'r' and computer == 's') or \
         (player == 'p' and computer == 'r') or \
         (player == 's' and computer == 'p'):
        return "player"
    else:
        return "computer"

def display_choice(choice):
    choices = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}
    return choices[choice]

def play_game():
    player_score = 0
    computer_score = 0
    ties = 0
    
    print("🎮 Rock-Paper-Scissors Game!")
    print("First to 3 points wins. Type 'q' to quit anytime.\n")
    
    while player_score < 3 and computer_score < 3:
        player = get_player_choice()
        if player == 'q':
            break
        
        computer = get_computer_choice()
        
        clear_screen()
        print(f"You chose: {display_choice(player)}")
        print(f"Computer chose: {display_choice(computer)}")
        
        winner = determine_winner(player, computer)
        if winner == "player":
            player_score += 1
            print("You win this round! 🎉")
        elif winner == "computer":
            computer_score += 1
            print("Computer wins this round. 😤")
        else:
            ties += 1
            print("It's a tie! 🤝")
        
        print(f"\nScore - You: {player_score} | Computer: {computer_score} | Ties: {ties}")
    
    if player == 'q':
        print("\nGame quit. Thanks for playing!")
    elif player_score == 3:
        print("\n🏆 You won the game!")
    else:
        print("\n🤖 Computer won the game!")

if __name__ == "__main__":
    play_game()

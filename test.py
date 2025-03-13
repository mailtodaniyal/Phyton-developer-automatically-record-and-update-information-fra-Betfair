import time
from datetime import datetime

bets = [
    {"bet_id": 101, "user": "JohnDoe", "event": "Football Match", "stake": 100, "odds": 2.5, "status": "Open"},
    {"bet_id": 102, "user": "Alice", "event": "Tennis Final", "stake": 50, "odds": 1.8, "status": "Open"},
    {"bet_id": 103, "user": "Bob", "event": "Basketball Game", "stake": 75, "odds": 3.0, "status": "Open"},
]

def fetch_bets():
    """Simulates fetching bets from a system (static data)."""
    print("\nFetching bets...\n")
    for bet in bets:
        print(f"Bet ID: {bet['bet_id']}, User: {bet['user']}, Event: {bet['event']}, Stake: {bet['stake']}, Odds: {bet['odds']}, Status: {bet['status']}")
    print("\n")

def update_bet_status(bet_id, new_status):
    """Simulates updating bet status."""
    for bet in bets:
        if bet["bet_id"] == bet_id:
            bet["status"] = new_status
            print(f"Updated Bet ID {bet_id}: New Status -> {new_status}")
            return
    print(f"Bet ID {bet_id} not found.")

def calculate_payouts():
    """Simulates calculating payouts based on static results."""
    print("\nCalculating payouts...\n")
    for bet in bets:
        if bet["status"] == "Open":
            if bet["bet_id"] % 2 == 0: 
                winnings = bet["stake"] * bet["odds"]
                bet["status"] = "Won"
                print(f"Bet ID {bet['bet_id']} won! Payout: {winnings}")
            else:
                bet["status"] = "Lost"
                print(f"Bet ID {bet['bet_id']} lost.")
    print("\n")

def main():
    """Main function to simulate the betting process."""
    fetch_bets()
    
    print("\nUpdating bet statuses...\n")
    update_bet_status(101, "Settled")
    update_bet_status(103, "Cancelled")
    
    calculate_payouts()
    
    print("\nFinal Bets Data:")
    fetch_bets()

if __name__ == "__main__":
    main()

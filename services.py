import random
from models import Accounts

"""Generates a unique-looking account number with a prefix and check digit."""
def generate_account_number():

    prefix = random.randint(10, 99)  # Two-digit prefix
    number = random.randint(100000, 999999) # Six-digit number
    # Calculate a check digit (e.g., using a simplified Mod 97 check)
    check = int((prefix * 10**10 + number) % 97)
    new_number = f"{prefix:0>2d}{number:0>6d}{check:0>2d}"
    return new_number

# Example usage:
# account_number = generate_account_number()
# print(account_number) # Output: Example: 4512345615

"""Create a new account_Id"""
def generate_account_id():
    max_id = 86
    new_id = max_id + 1
    return new_id
# Imports
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env
""" Directory Structure
.
├── .env
└── main.py
"""

# Functions


def add(a: int, b: int) -> int:
    """This function adds two numbers"""
    return a+b


def write_db(data: int) -> None:
    """This function writes to database"""
    # Code to create a database connection
    print(
        f"Attempting to make a connect to {os.environ.get('DATABASE_URL')} with \n \t user {os.environ.get('DATABASE_USER')} \n \t password {os.environ.get('DATABASE_PASSWORD')}")
    # *** Never print the secrets in logs or in console
    # INSERT statements
    sleep(1)
    return


def main():
    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")
    result = add(num1, num2)
    # write_db(result)


# Script stars from here
if __name__ == "__main__":
    main()


#!/usr/bin/env python3

from bank import Bank
from operations import handle_deposit, handle_withdrawal, handle_pix
from libs.bank_system_utils import get_new_user_credentials
from libs.color import RED, GREEN, YLOW, CYAN, DEFAULT
from libs.utils import clear, press_enter
import time as tm
import getpass

valid_operations = {
    "0": "Balance",
    "1": "Deposit",
    "2": "Withdrawal",
    "3": "Pix",
    "4": "Statement",
    "5": "exit account",
    "6": "finish session",
}

is_yes = ["y", "yes", "1"]


def pick_operation() -> str:
    """Prompt the user to select an operation."""
    print("Which operation do you want to make?")
    print("0: Check balance")
    print("1: Make a deposit")
    print("2: Withdrawal a value")
    print("3: Pix")
    print("4: Get bank statement")
    print("5: Exit account")
    print("6: Finish session")
    return input("Type an option:\n>>> ").strip()


def run_system(bank: Bank, login: str) -> int:
    """Run the banking system for a logged-in client."""
    client = bank.clients[login]
    while True:
        print("\nPress 'ENTER' to continue")
        press_enter()
        clear(0, 0)
        operation = pick_operation()
        if operation not in valid_operations:
            print(f"{RED}Invalid option. Try again!{DEFAULT}")
            continue
        if operation == "5":
            clear(0, 0)
            print("See you soon!")
            bank.reload_clients()
            return 0
        elif operation == "6":
            clear(0, 3)
            print("Finishing program...")
            return 1
        elif operation == "0":
            clear(0, 0)
            formatted_val = "{:.2f}".format(float(client.balance))
            print(f"Your current balance is: {CYAN}R${formatted_val}{DEFAULT}")
        elif operation == "1":
            clear(0, 0)
            client.balance = handle_deposit(client)
        elif operation == "2":
            clear(0, 0)
            client.balance = handle_withdrawal(client)
        elif operation == "3":
            clear(0, 0)
            client.balance = handle_pix(client)
        elif operation == "4":
            clear(0, 0)
            client.display_statement()


def main():
    '''Init the system'''
    bank = Bank(agency="0001")
    bank.registered_new_user(
        name="Vinicius Eduardo",
        cpf="12345678900",
        birthday="01/08/2000",
        street="none",
        house_nbr="none",
        neighborhood="none",
        city="none",
        state="NO",
        login="vinny",
        pin="access777",
        pix_key="1234567890"
    )
    bank.registered_new_user(
        name="Samuel Lacerda Osasco",
        cpf="23456789011",
        birthday="23/04/2005",
        street="none",
        house_nbr="none",
        neighborhood="none",
        city="none",
        state="NO",
        login="samuca",
        pin="access777",
        pix_key="2345678901"
    )
    print(f"{GREEN}Welcome to the bank system{DEFAULT}")
    tm.sleep(0.5)
    sigfinish = 0
    while sigfinish == 0:
        login = input("Access login: ")
        is_valid, ret = bank.account_exists(login=login)
        tm.sleep(2)
        if is_valid:
            client = bank.clients[login]
            pin = getpass.getpass("Enter your password: ")
            # pin = "access777" #FOR DEBUB
            log_stt, ret = client.handle_login(pin)
            if log_stt:
                clear(2, 0)
                print(f"Welcome, {CYAN}{ret or client.name}{DEFAULT}!")
                tm.sleep(1)
                sigfinish = run_system(bank=bank, login=login)
            else:
                clear(2, 0)
                print(f"{RED}{ret}{DEFAULT}")
                continue
        else:
            print(f"{YLOW}{ret}{DEFAULT}", end=" ")
            print("Would you like to create a new account?")
            if (
                input(
                    "Type '1', 'y' or 'yes' to create a new account, or any key to exit: "
                )
                .strip()
                .lower()
                in is_yes
            ):
                (
                    stts,
                    name,
                    cpf,
                    birthday,
                    street,
                    house_nbr,
                    neighborhood,
                    city,
                    state,
                    new_login,
                ) = get_new_user_credentials()
                if stts:
                    reg_stts, reg_ret = bank.registered_new_user(
                        name=name,
                        cpf=cpf,
                        birthday=birthday,
                        street=street,
                        house_nbr=house_nbr,
                        neighborhood=neighborhood,
                        city=city,
                        state=state,
                        login=new_login,
                    )
                    clear(0, 0)
                    print(GREEN if reg_stts else RED, reg_ret, DEFAULT)
                    if reg_stts:
                        tm.sleep(2)
                        sigfinish = run_system(bank=bank, login=new_login)
                else:
                    print(f"{RED}{name}{DEFAULT}")
            else:
                clear(2, 0)
    clear(2, 0)


if __name__ == "__main__":
    main()

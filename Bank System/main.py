#!/usr/bin/env python3

from bank import Bank
from operations import handle_deposit, handle_withdrawal
from libs.bank_system_utils import get_credentials, get_new_user_credentials
from libs.color import RED, GREEN, YLOW, CYAN, DEFAULT
from libs.utils import clear, press_enter
import time as tm
import getpass

valid_operations = {
    "0": "Balance",
    "1": "Deposit",
    "2": "Withdrawal",
    "3": "Statement",
    "4": "exit account",
    "5": "finish session",
}

is_yes = ["y", "yes", "1"]


def pick_operation() -> str:
    """Prompt the user to select an operation."""
    print("Which operation do you want to make?")
    print("0: Check balance")
    print("1: Make a deposit")
    print("2: Withdrawal a value")
    print("3: Get bank statement")
    print("4: Exit account")
    print("5: Finish session")
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
            print(RED, "Invalid option. Try again!", DEFAULT)
            continue
        if operation == "4":
            clear(0, 0)
            print("See you soon!")
            return 0
        elif operation == "5":
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
            client.display_statement()


def main():
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
    )
    print(GREEN, "Welcome to the bank system", DEFAULT)
    tm.sleep(0.5)
    sigfinish = 0
    while sigfinish == 0:
        agency, login, account, cpf_nbr = get_credentials()
        is_valid, ret = bank.account_exists(
            agency=agency, login=login, account=account, cpf=cpf_nbr
        )
        clear(2, 0)
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
                print(RED, ret, DEFAULT)
                continue
        else:
            print(YLOW, ret, DEFAULT, end=" ")
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
                    print(RED, name, DEFAULT)
    clear(2, 0)


if __name__ == "__main__":
    main()

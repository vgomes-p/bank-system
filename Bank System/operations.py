from client import Client
from libs.color import RED, PINK, CYAN, YLOW, DEFAULT
from libs.utils import clear, is_valid_number, is_negative_number


def handle_deposit(client: Client) -> float:
    '''Receive and check is the value that the user's wants to deposit is valid'''
    deposit = input("Type a value to deposit: ").strip()
    clear(2, 0)
    if is_negative_number(deposit):
        print(
            RED,
            "Error: negative number is not allowed, just type a number without signal",
            DEFAULT,
        )
    elif is_valid_number(deposit):
        client.mk_deposit(deposit)
        formated_balance = "{:.2f}".format(client.balance)
        print(f"Your current balance is: {CYAN}R$ {formated_balance}{DEFAULT}")
    else:
        formated_deposit = "{:.2f}".format(deposit)
        print(
            RED, f"Error: {PINK}{formated_deposit}{RED} is not a valid number", DEFAULT
        )
    return client.balance


def handle_withdrawal(client: Client) -> float:
    '''Receive and check is the value that the user's wants to withdrawal is valid'''
    if client.get_daily_withdrawal_cnt() >= 3:
        clear(0, 1.5)
        print(PINK, "Sorry, you cannot make more withdrawals today!", DEFAULT)
        return client.balance
    withdrawal_value = input("Type a value to withdrawal: ").strip()
    clear(2, 0)
    if is_negative_number(withdrawal_value):
        print(
            RED,
            "Error: negative number is not allowed, just type a number without signal",
            DEFAULT,
        )
    elif is_valid_number(withdrawal_value):
        nw_balance, success = client.mk_withdrawal(withdrawal_value)
        if not success:
            formatted_balance = "{:.2f}".format(client.balance)
            print(
                RED,
                f"You cannot withdrawal a value equal or bigger than R${formatted_balance}!",
                DEFAULT,
            )
        else:
            formatted_balance = "{:.2f}".format(client.balance)
            print(f"Your current balance is: {CYAN}R${formatted_balance}{DEFAULT}")
            remain_withdrawal = 3 - client.get_daily_withdrawal_cnt()
            if remain_withdrawal > 0:
                print(
                    YLOW,
                    f"You can now make {remain_withdrawal} more withdrawal!",
                    DEFAULT,
                )
            else:
                print(RED, "This was your LAST withdrawal for today!", DEFAULT)
    else:
        print(
            RED, f"Error: {PINK}{withdrawal_value}{RED} is not a valid number", DEFAULT
        )
    return client.balance

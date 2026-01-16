from curses.ascii import isalnum, isalpha
from client import Client
from libs.color import RED, GREEN, PINK, CYAN, YLOW, DEFAULT
from libs.utils import clear, is_valid_number, is_negative_number, there_is_punct, there_is_alpha


def handle_int_input(message: str=""):
    while True:
        entry = input(message)
        if not entry:
            print("You have to entry something!")
            continue
        if there_is_alpha(entry):
            print("You entry cannot have letter!")
            continue
        if there_is_punct(entry, ['.', ',']):
            print("You entry cannot have letter!")
            continue
        else:
            return entry


def handle_deposit(client: Client) -> float:
    '''Receive and check is the value that the user's wants to deposit is valid'''
    deposit = handle_int_input("Type a value to deposit: ").strip()
    if "," in deposit:
        deposit = deposit.replace(",", ".")
    deposit = "{:.2f}".format(float(deposit))
    clear(2, 0)
    real, cents = str(deposit).split(".")
    del(real)
    if len(cents) > 2:
        print(f"{RED}Error: three-decimals (or more) entry is not acceptable{DEFAULT}")
        return client.balance
    if is_negative_number(deposit):
        print(f"{RED}Error: negative number is not allowed, just type a number without signal{DEFAULT}")
        return client.balance
    elif is_valid_number(deposit):
        client.mk_deposit(deposit)
        formated_balance = "{:.2f}".format(client.balance)
        print(f"Your current balance is: {CYAN}R$ {formated_balance}{DEFAULT}")
    else:
        formated_deposit = "{:.2f}".format(deposit)
        print(f"{RED}Error: {PINK}{formated_deposit}{RED} is not a valid number{DEFAULT}")
    return client.balance


def handle_withdrawal(client: Client) -> float:
    '''Receive and check is the value that the user's wants to withdrawal is valid'''
    if client.get_daily_withdrawal_cnt() >= 3:
        clear(0, 1.5)
        print(f"{PINK}Sorry, you cannot make more withdrawals today!{DEFAULT}")
        return client.balance
    withdrawal_value = handle_int_input("Type a value to withdrawal: ").strip()
    if "," in withdrawal_value:
        withdrawal_value = withdrawal_value.replace(",", ".")
    withdrawal_value = "{:.2f}".format(float(withdrawal_value))
    real, cents = str(withdrawal_value).split(".")
    del(real)
    if len(cents) > 2:
        print(f"{RED}Error: three-decimals (or more) entry is not acceptable{DEFAULT}")
        return client.balance
    clear(2, 0)
    if is_negative_number(withdrawal_value):
        print(f"{RED}Error: negative number is not allowed, just type a number without signal{DEFAULT}")
        return client.balance
    elif is_valid_number(withdrawal_value):
        nw_balance, success = client.mk_withdrawal(withdrawal_value)
        del(nw_balance)
        if not success:
            formatted_balance = "{:.2f}".format(client.balance)
            print(f"{RED}You cannot withdrawal a value equal or bigger than R${formatted_balance}!{DEFAULT}")
        else:
            formatted_balance = "{:.2f}".format(client.balance)
            print(f"Your current balance is: {CYAN}R${formatted_balance}{DEFAULT}")
            remain_withdrawal = 3 - client.get_daily_withdrawal_cnt()
            if remain_withdrawal > 0:
                print(f"{YLOW}You can now make {remain_withdrawal} more withdrawal!{DEFAULT}")
            else:
                print(f"{RED}This was your LAST withdrawal for today!{DEFAULT}")
    else:
        print(f"{RED}Error: {PINK}{withdrawal_value}{RED} is not a valid number{DEFAULT}")
    return client.balance


def handle_pix(client: Client) -> None:
    pix_key = handle_int_input("Type the pix key: ").strip()
    pix = handle_int_input("Type a value to pix: ").strip()
    if "," in pix:
        pix = pix.replace(",", ".")
    pix = "{:.2f}".format(float(pix))
    real, cents = str(pix).split(".")
    del(real)
    if len(cents) > 2:
        print(f"{RED}Error: three-decimals (or more) entry is not acceptable{DEFAULT}")
        return client.balance
    clear(2, 0)
    if is_negative_number(pix):
        print(f"{RED}Error: negative number is not allowed, just type a number without signal{DEFAULT}")
        return client.balance
    elif is_valid_number(pix):
        formated_pix_amount = "{:.2f}".format(float(pix))
        ret, message = client.mk_pix(pix_key=pix_key, amount=float(pix))
        if ret:
            print(message)
        else:
            print(message)
    else:
        formated_pix_amount = "{:.2f}".format(float(pix))
        print(f"{RED}Error: R${PINK}{formated_pix_amount}{RED} is not a valid number{DEFAULT}")
    return client.balance

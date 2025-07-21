from libs.BBS_utils import make_deposit, withdrawal, update_statement, is_cpf_registered, new_user
from libs.color import RED, GREEN, YLOW, PINK, CYAN, INVERT, BOLD, DEFAULT
from libs.utils import clear, is_valid_number, press_enter, is_negative_number, update_dict

import os
import time as tm

bank_list = {
	"agency": "0001", "client": {"vinny": {"account": "1", "name": "Vinicius Eduardo", "cpf": "12345678900", "balance": 0, "statement": {"operation_0": {"Operation": "", "Value": ""}}}}
}

valid_operations = {
	"0": "Balance",
	"1": "Deposit",
	"2": "Withdrawal",
	"3": "Statement",
	"4": "exit",
}

def handle_deposit(balance: float, login: str, statement: dict) -> float:
	deposit = input("Type a value to deposit: ").strip()
	if is_negative_number(deposit):
		print(RED, f"{RED}Error:{DEFAULT} negative number is not allowed, just type a number without signal", DEFAULT)
	elif is_valid_number(deposit):
		balance = make_deposit(balance, deposit)
		print(f"Your current balance is: {CYAN}R$ {balance}{DEFAULT}")
		update_statement(clients_statement=statement, client_login=login, operation="Deposit: +", value=deposit)
	else:
		print(RED, f"Error: {PINK}{deposit}{RED} is not a valid number", DEFAULT)
	return balance

def handle_withdrawal(balance: dict, login: str, statement: dict, nbr_withdrawal: int) -> tuple[float, int]:
	if nbr_withdrawal == 3:
		print(PINK, "Sorry, you cannot make more withdrawals today!", DEFAULT)
		return balance, nbr_withdrawal
	withdrawal_value = input("Type a value to withdrawal: ")
	if is_negative_number(withdrawal_value):
		print(RED, f"{RED}Error:{DEFAULT} negative number is not allowed, just type a number without signal", DEFAULT)
	elif is_valid_number(withdrawal_value):
		if float(withdrawal_value) >= balance:
			print(RED, f"You cannot withdrawal a value equal or bigger than R${balance}!", DEFAULT)
		else:
			balance = withdrawal(cur_value=balance, value_taken=withdrawal_value)
			print(f"Your current balance is: {CYAN}R${balance}{DEFAULT}")
			update_statement(clients_statement=statement, client_login=login, operation="Withdrawal: -", value=withdrawal_value)
			nbr_withdrawal += 1
			if nbr_withdrawal == 2:
				print(YLOW, "You can now make one more withdrawal!", DEFAULT)
			elif nbr_withdrawal == 3:
				print(RED, "This was your LAST withdrawal for today!", DEFAULT)
	else:
		print(RED, f"Error: {PINK}{withdrawal_value}{RED} is not a valid number", DEFAULT)
	return balance, nbr_withdrawal

def display_statement(login: str, statement: dict, balance: float):
	print(f"Your bank statement is as following:\n{PINK}Operation: Value{DEFAULT}")
	for op_data in statement.get(login, {}).values():
		op, val = op_data["Operation"], op_data["Value"]
		if op:
			print(f"{op}R${val}")
	print(f"\nYour current balance is: {CYAN}{balance}{DEFAULT}!")

def pick_operation() -> str:
	print("Which operation do you want to make?")
	print("0: Check balance")
	print("1: Make a deposit")
	print("2: Withdrawal a value")
	print("3: Get bank statement")
	print("4: Exit account")
	return input("Type an option:\n>>> ").strip()

def run_system(bank_list: dict, agency: str, login: str, statement: dict):
	user_data = bank_list[agency][login]
	times_called = 0
	while True:
		print("\nPress 'ENTER' to continue")
		press_enter()
		clear()
		operation = input("Type a option: ")
		if operation not in valid_operations:
			print(RED, "Invalid option. Try again!", DEFAULT)
			continue
		if operation == "4":
			clear()
			print("See you soon!")
			break
		elif operation == "0":
			clear()
			print(f"Your current balance is: {CYAN}R${float(bank_client[login]['balance'])}{DEFAULT}")
		elif operation == "1":
			clear()
			user_data["balance"] = handle_deposit(user_data["balance"], login, clients_statement)
		elif operation == "2":
			clear()
			user_data["balance"], times_called = handle_withdrawal(user_data["balance"], login, statement, times_called)
		elif operation == "3":
			clear()
			display_statement(login, statement, user_data["balance"])

def account_exits(agency: str, login: str, account: str, cpf_nbr: str, bank_list: dict) -> tuple[bool, str]:
	if agency not in bank_list:
		return False, f"Agency '{agency}' not found!"
	if login not in bank_list[agency]:
		return False, f"Client for the login '{login}' not found!"
	client_data = bank_list[agency][login]
	client_name = client_data['name']
	if account != client_data["account"]:
		return False, f"The account '{account}' does not belong to {client_name}"
	if cpf_nbr != client_data["cpf"]:
		return False, f"Invalid CPF for {client_name}'s account!"
	return True, client_name

def get_credentials() -> tuple[str, str, str, str]:
	print("Please, enter your access informations:")
	agency = input("Agency: ").lower().strip()
	login = input("Access login: ").lower().strip()
	account = input("Account number: ").lower().strip()
	cpf_nbr = input("CPF number: ").lower().strip().replace(".", "").replace("-", "")
	return agency, login, account, cpf_nbr

def main():
	print(GREEN, "Welcome to the bank system", DEFAULT)
	tm.sleep(.5)
	agency, login, account, cpf_nbr = get_credentials()
	is_valid, ret = account_exits(agency=agency, account=account, login=login, cpf_nbr=cpf_nbr, bank_list=bank_list)
	tm.sleep(2)
	clear()
	if is_valid:
		print(f"Welcome, {CYAN}{ret}{DEFAULT}!")
		tm.sleep(2)
		statement = bank_list[agency][login]["statement"]
		run_system(bank_list, agency, login, statement)
	else:
		print(RED, ret, DEFAULT)

main()
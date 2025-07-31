#!/usr/bin/env python3

from libs.bank_system_utils import make_deposit, withdrawal, update_statement, is_cpf_registered, is_login_registered, registered_new_user, handle_withdrawal, handle_deposit, display_statement, account_exits, get_credentials, get_new_user_credentials
from libs.color import RED, GREEN, YLOW, PINK, CYAN, INVERT, BOLD, DEFAULT
from libs.utils import clear, is_valid_number, press_enter, is_negative_number
import time as tm

bank_list = {
	"agency": "0001", "client": {"vinny": {"account": "1", "pin": "access777", "name": "Vinicius Eduardo", "cpf": "12345678900", "balance": 0, "statement": {"operation_0": {"Operation": "", "Value": ""}}}}
}

valid_operations = {
	"0": "Balance",
	"1": "Deposit",
	"2": "Withdrawal",
	"3": "Statement",
	"4": "exit account",
	"5": "finish session",
}

is_yes = ['y', 'yes', '1']

def pick_operation() -> str:
	print("Which operation do you want to make?")
	print("0: Check balance")
	print("1: Make a deposit")
	print("2: Withdrawal a value")
	print("3: Get bank statement")
	print("4: Exit account")
	print("5: Finish session")
	return input("Type an option:\n>>> ").strip()

def run_system(bank_list: dict, login: str, statement: dict) -> int:
	user_data = bank_list["client"][login]
	times_called = 0
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
			print("Finishin program...")
			return 1
		elif operation == "0":
			clear(0, 0)
			formated_val = "{:.2f}".format(float(user_data['balance']))
			print(f"Your current balance is: {CYAN}R${formated_val}{DEFAULT}")
		elif operation == "1":
			clear(0, 0)
			user_data["balance"] = handle_deposit(balance=user_data["balance"], login=login, bank_list=bank_list)
		elif operation == "2":
			clear(0, 0)
			user_data["balance"], times_called = handle_withdrawal(balance=user_data["balance"], login=login, bank_list=bank_list, nbr_withdrawal=times_called)
		elif operation == "3":
			clear(0, 0)
			display_statement(statement=statement, balance=user_data["balance"])

def main():
	print(GREEN, "Welcome to the bank system", DEFAULT)
	tm.sleep(.5)
	sigfinish = 0
	while sigfinish == 0:
		agency, login, account, cpf_nbr = get_credentials()
		is_valid, ret = account_exits(agency=agency, account=account, login=login, cpf_nbr=cpf_nbr, bank_list=bank_list)
		clear(2, 0)
		if is_valid:
			clear(2, 0)
			print(f"Welcome, {CYAN}{ret}{DEFAULT}!")
			tm.sleep(1)
			statement = bank_list["client"][login]["statement"]
			sigfinish = run_system(bank_list=bank_list, login=login, statement=statement)
		elif is_valid == 2:
			clear(init_wait_time=2, final_wait_time=0)
			print("Restarting system...")
			tm.sleep(1)
			print("Please, wait!")
			clear(init_wait_time=0, final_wait_time=2)
			continue
		else:
			clear(2, 0)
			print(YLOW, ret, DEFAULT, end=" ")
			print("Would you like to create a new account?")
			if str(input("Type '1', 'y' or 'yes' to create a new account, or any key to exit: ").strip().lower()) in is_yes:
				stts, name, cpf, street, house_nbr, neighborhood, city, state, new_login = get_new_user_credentials()
				if stts:
					reg_stts, reg_ret = registered_new_user(bank_list=bank_list, name=name, cpf=cpf, street=street, house_nbr=house_nbr, neighborhood=neighborhood, city=city, state=state, login=new_login)
					clear(0, 0)
					print(GREEN if reg_stts else RED, reg_ret, DEFAULT)
					if reg_stts:
						tm.sleep(2)
						nw_statement = bank_list["client"][new_login]["statement"]
						sigfinish = run_system(bank_list=bank_list, login=new_login, statement=nw_statement)
				else:
					print(RED, name, DEFAULT)
	clear(2, 0)

main()
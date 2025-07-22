#!/usr/bin/env python3

from libs.BBS_utils import make_deposit, withdrawal, update_statement, is_cpf_registered, is_login_registered, registered_new_user, handle_withdrawal, handle_deposit, display_statement, account_exits, get_credentials, get_new_user_credentials
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

def pick_operation() -> str:
	print("Which operation do you want to make?")
	print("0: Check balance")
	print("1: Make a deposit")
	print("2: Withdrawal a value")
	print("3: Get bank statement")
	print("4: Exit account")
	return input("Type an option:\n>>> ").strip()

def run_system(bank_list: dict, login: str, statement: dict):
	user_data = bank_list["client"][login]
	times_called = 0
	while True:
		print("\nPress 'ENTER' to continue")
		press_enter()
		clear()
		operation = pick_operation()
		if operation not in valid_operations:
			print(RED, "Invalid option. Try again!", DEFAULT)
			continue
		if operation == "4":
			clear()
			print("See you soon!")
			break
		elif operation == "0":
			clear()
			print(f"Your current balance is: {CYAN}R${float(user_data['balance'])}{DEFAULT}")
		elif operation == "1":
			clear()
			user_data["balance"] = handle_deposit(balance=user_data["balance"], login=login, bank_list=bank_list)
		elif operation == "2":
			clear()
			user_data["balance"], times_called = handle_withdrawal(balance=user_data["balance"], login=login, bank_list=bank_list, nbr_withdrawal=times_called)
		elif operation == "3":
			clear()
			display_statement(login=login, statement=statement, balance=user_data["balance"])

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
		statement = bank_list["client"][login]["statement"]
		run_system(bank_list=bank_list, login=login, statement=statement)
	else:
		print(RED, ret, DEFAULT)
		print(YLOW, "Would you like to create a new account?", DEFAULT)
		if input("Type 'yes' to create a new account, or any key to exit: ").strip().lower() == "yes":
			success, name, cpf, street, house_nbr, neighborhood, city, state, new_login = get_new_user_credentials()
			if success:
				reg_success, reg_msg = registered_new_user(bank_list=bank_list, name=name, cpf=cpf, street=street, house_nbr=house_nbr, neighborhood=neighborhood, city=city, state=state, login=new_login)
				clear()
				print(GREEN if reg_success else RED, reg_msg, DEFAULT)
				if reg_success:
					tm.sleep(2)
					nw_statement = bank_list["client"][new_login]["statement"]
					run_system(bank_list=bank_list, login=new_login, statement=nw_statement)
			else:
				print(RED, name, DEFAULT)
		else:
			print(GREEN, "Goodbye!", DEFAULT)
	tm.sleep(2)
	clear()

main()
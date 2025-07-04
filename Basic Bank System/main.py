from libs.BBS_utils import make_deposit, withdrawal, update_statement
from libs.color import RED, GREEN, YLOW, PINK, CYAN, INVERT, BOLD, DEFAULT
from libs.utils import clear, is_valid_number, press_enter, is_negative_number

import os
import time as tm

bank_client = {
	"vinny": {"name": "Vinicius Eduardo", "balance": 0}
}

clients_statement = {
	"vinny": {"operation_0": {"Operation": "", "Value": ""}}
}

def main():
	print(GREEN, "Welcome to the bank system", DEFAULT)
	tm.sleep(.5)
	print("Please, enter your login:", end=" ")
	login = input().lower().strip()
	if login in bank_client:
		clear()
		exit_stt = "false"
		print(F"Welcome, {CYAN}{bank_client[login]['name']}{DEFAULT}!")
		nbr_withdrawal = 0
		while exit_stt != "true":
			print("\nPress 'ENTER' to continue")
			press_enter()
			clear()
			print("Which operation you want to make?\n0: Check balance\n1: Make a deposit\n2: Withdrawal a value\n3: Get bank statement\n4: Exit account")
			operation = input("Type a option: ")
			# print(YLOW, f"DEBUG: operation chosen: {operation}", DEFAULT)
			if operation.isnumeric():
				if int(operation) == 4:
					clear()
					print("See you soon!")
					exit_stt = "true"
					pass
				elif int(operation) == 0:
					clear()
					print(f"Your current balance is: {CYAN}R${float(bank_client[login]['balance'])}{DEFAULT}")
				elif int(operation) == 1:
					clear()
					deposit = input("Type a value to deposit: ")
					if is_negative_number(deposit):
							print(RED, f"{RED}Error:{DEFAULT} negative number is not allowed, just type a number without signal", DEFAULT)
					elif is_valid_number(deposit):
						bank_client[login]['balance'] = make_deposit(bank_client[login]['balance'], deposit)
						print(f"Your current balance is: {CYAN}R$ {bank_client[login]['balance']}{DEFAULT}")
						update_statement(clients_statement=clients_statement, client_login=login, operation="Deposit: +", value=deposit)
					else:
						print(RED, f"Error: {PINK}{deposit}{RED} is not a valid number", DEFAULT)
				elif int(operation) == 2:
					clear()
					if nbr_withdrawal == 3:
						print(PINK, "Sorry, you cannot make more withdrawals today!", DEFAULT)
					else:
						withdrawal_value = input("Type a value to withdrawal: ")
						if is_negative_number(withdrawal_value):
							print(RED, f"{RED}Error:{DEFAULT} negative number is not allowed, just type a number without signal", DEFAULT)
						elif is_valid_number(withdrawal_value):
							if float(withdrawal_value) >= float(bank_client[login]['balance']):
								print(RED, f"You cannot withdrawal a value bigger than R${float(bank_client[login]['balance'])}!", DEFAULT)
							else:
								bank_client[login]['balance'] = withdrawal(bank_client[login]['balance'], withdrawal_value)
								print(f"Your current balance is: {CYAN}R$ {bank_client[login]['balance']}{DEFAULT}")
								update_statement(clients_statement=clients_statement, client_login=login, operation="Withdrawal: -", value=withdrawal_value)
								nbr_withdrawal += 1
								if nbr_withdrawal == 2:
									print(YLOW, "You can now make one more withdrawal!", DEFAULT)
								elif nbr_withdrawal == 3:
									print(RED, "This was your LAST withdrawal for today!", DEFAULT)
								else:
									pass
						else:
							print(RED, f"Error: {PINK}{withdrawal_value}{RED} is not a valid number", DEFAULT)
				elif int(operation) == 3:
					clear()
					print(f"Your bank statement is as following:\n{PINK}Operation: Value{DEFAULT}")
					for op_key, op_data in clients_statement[login].items():
						operation_type = op_data["Operation"]
						value = op_data["Value"]
						if not operation_type:
							continue
						print(f"{operation_type}R${value}")
					print(f"\nYour current balance is: {CYAN}{bank_client[login]['balance']}{DEFAULT}!")
			else:
				print(RED, f"Error: {PINK}{operation}{RED} is not a valid number", DEFAULT)
	else:
		print(RED, "User not found", DEFAULT)
	pass

main()
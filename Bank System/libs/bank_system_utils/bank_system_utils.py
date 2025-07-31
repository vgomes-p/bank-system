from libs.color import RED, GREEN, YLOW, PINK, CYAN, INVERT, BOLD, DEFAULT
from libs.utils import clear, is_valid_number, press_enter, is_negative_number
import random
import string

def make_deposit(cur_value, new_value):
	after_deposit = float(cur_value) + float(new_value)
	return float(after_deposit)

def withdrawal(cur_value, value_taken):
	after_withdrawal = float(cur_value) - float(value_taken)
	return float(after_withdrawal)

def update_statement(bank_list, login, operation, value):
	statement = bank_list["client"][login].setdefault("statement", {})
	if statement:
		ids = [int(op.split("_")[1]) for op in statement.keys()]
		next_id = max(ids) + 1
	else:
		next_id = 0
	op_id = f"operation_{next_id}"
	statement[op_id] = {"Operation": operation, "Value": value}

def handle_deposit(balance: float, login: str, bank_list: dict) -> float:
	deposit = input("Type a value to deposit: ").strip()
	if is_negative_number(deposit):
		clear(2, 0)
		print(RED, f"{RED}Error:{DEFAULT} negative number is not allowed, just type a number without signal", DEFAULT)
	elif is_valid_number(deposit):
		balance = make_deposit(balance, deposit)
		clear(2, 0)
		formated_balance = "{:.2f}".format(balance)
		print(f"Your current balance is: {CYAN}R$ {formated_balance}{DEFAULT}")
		update_statement(bank_list=bank_list, login=login, operation="Deposit: +", value=deposit)
	else:
		clear(2, 0)
		formated_deposit = "{:.2f}".format(deposit)
		print(RED, f"Error: {PINK}{formated_deposit}{RED} is not a valid number", DEFAULT)
	return balance

def handle_withdrawal(balance: float, login: str, bank_list: dict, nbr_withdrawal: int) -> tuple[float, int]:
	if nbr_withdrawal == 3:
		clear(0, 1.5)
		print(PINK, "Sorry, you cannot make more withdrawals today!", DEFAULT)
		return balance, nbr_withdrawal
	withdrawal_value = input("Type a value to withdrawal: ")
	if is_negative_number(withdrawal_value):
		clear(2, 0)
		print(RED, f"{RED}Error:{DEFAULT} negative number is not allowed, just type a number without signal", DEFAULT)
	elif is_valid_number(withdrawal_value):
		if float(withdrawal_value) >= balance:
			clear(2, 0)
			formated_balance = "{:.2f}".format(balance)
			print(RED, f"You cannot withdrawal a value equal or bigger than R${formated_balance}!", DEFAULT)
		else:
			balance = withdrawal(cur_value=balance, value_taken=withdrawal_value)
			clear(2, 0)
			formated_balance = "{:.2f}".format(balance)
			print(f"Your current balance is: {CYAN}R${formated_balance}{DEFAULT}")
			update_statement(bank_list=bank_list, login=login, operation="Withdrawal: -", value=withdrawal_value)
			nbr_withdrawal += 1
			if nbr_withdrawal == 2:
				print(YLOW, "You can now make one more withdrawal!", DEFAULT)
			elif nbr_withdrawal == 3:
				print(RED, "This was your LAST withdrawal for today!", DEFAULT)
	else:
		clear(2, 0)
		print(RED, f"Error: {PINK}{withdrawal_value}{RED} is not a valid number", DEFAULT)
	return balance, nbr_withdrawal

def display_statement(statement: dict, balance: float):
	clear(2, 0)
	print(f"Your bank statement is as following:\n{PINK}Operation: Value{DEFAULT}")
	for op_data in statement.values():
		op, val = op_data["Operation"], op_data["Value"]
		if op:
			formated_val = "{:.2f}".format(float(val))
			print(f"{op}R${str(formated_val)}")
	print(f"\nYour current balance is: {CYAN}{balance}{DEFAULT}!")

def handle_login(pin: str) -> tuple[bool, str]: #debug this function: https://onlinegdb.com/uikcl7uOgb
	try_nbr = 1
	while try_nbr < 4:
		check_pin = input("Enter your pin: ")
		if check_pin != pin and try_nbr != 4:
			clear(init_wait_time=1, final_wait_time=0)
			if try_nbr == 3: #just to make sure the 'wrong pin message' does not appear 
				break
			elif try_nbr == 2:
				print(RED, "Wrong pin, please, try again!\n", YLOW, "[note: this is your last try for today]", DEFAULT)
				try_nbr += 1
				continue
			else:
				print(RED, "Wrong pin, please, try again!", DEFAULT)
				try_nbr += 1
				continue
		else:
			return True, ""
	return False, "Too many attempts to logged!"

def account_exits(agency: str, login: str, account: str, cpf_nbr: str, bank_list: dict) -> tuple[bool, str]:
	if bank_list.get("agency") != agency:
		return False, f"Agency '{agency}' not found!"
	if login not in bank_list.get("client", {}):
		return False, f"Client for the login '{login}' not found!"
	client_data = bank_list["client"][login]
	client_name = client_data.get("name")
	client_pin = client_data.get("pin")
	# account_ret, cpf_ret = client_data.get("account"), client_data.get("cpf")
	# print(YLOW, f"DEBUG:\nclient_data return: {client_data}\nclient_name return: {client_name}\naccount return: {account_ret}\ncpf return: {cpf_ret}", DEFAULT)
	if account != client_data.get("account"):
		return False, f"The account '{account}' does not belong to {client_name}"
	if cpf_nbr != client_data.get("cpf"):
		return False, f"Invalid CPF for {client_name}'s account!"
	log_stt, ret = handle_login(pin=client_pin)
	if log_stt:
		return True, client_name
	else:
		clear(init_wait_time=2)
		print(RED, ret, DEFAULT)
		return 2

def get_credentials() -> tuple[str, str, str, str]:
	print("Please, enter your access informations:")
	# agency, login, account, cpf_nbr = "0001", "vinny", "1", "12345678900" #for debug v1
	# agency, login, account, cpf_nbr = "0001", "doNotExit", "2", "234.567.890-11" #for debug v2
	agency = input("Agency: ")
	login = input("Access login: ").lower()
	account = input("Account number: ")
	cpf_nbr = input("CPF number: ").replace(".", "").replace("-", "")
	return str(agency), str(login), str(account), str(cpf_nbr)

def mk_pin() -> str:
	base = (random.sample(string.ascii_letters, k=4) +
	random.sample(string.digits, 3) +
	random.sample(["!", "#", "%", "*"], 2))
	random.shuffle(base)
	return ''.join(base)

def mk_login(name: str, cpf: str, state: str) -> str:
	if not (name and cpf and state):
		return ""
	if len(cpf) != 11 or not cpf.isdigit():
		return ""
	if len(state) != 2 or not state.isalpha():
		return ""
	name_splited = list(name.split(" "))
	first_name = str(name_splited[0]).replace("'", "").replace("[", "").replace("]", "")
	last_name = str(name_splited[-1]).replace("'", "").replace("[", "").replace("]", "")
	half_last_name, cpf_num_0, cpf_num_1, end = last_name[0].lower(), cpf[1], cpf[8], state.upper()
	return f"{first_name[:4].lower()}{cpf_num_0}{cpf_num_1}{half_last_name.title()}-{end}"

def get_new_user_credentials() -> tuple[bool, str, str, str, str, str, str, str, str]:
	print("Please, enter the following informations to create your account!")
	while True:
		# name, cpf, street, house_nbr, neighborhood, city, state = "Test debug entry", "23456789011", "Test St.", "42", "testing", "city", "TS" #for debug
		name = input("Full name: ").strip()
		cpf = input("CPF number: ").replace(".", "").replace("-", "")
		street = input("Street: ").strip()
		house_nbr = input("House Number: ").strip()
		neighborhood = input("Neighborhood: ").strip()
		city = input("City: ").strip()
		state = input("State [eg.: SP, MG]: ").strip().upper()
		if not all([name, cpf, street, house_nbr, neighborhood, city, state]):
			print(f"{RED}No item can be empty!{DEFAULT}\nPlease, enter the following information correctly!")
			continue
		if len(cpf) != 11 or not cpf.isdigit():
			print(f"{RED}CPF can only contains 11 numbers!{DEFAULT}\nPlease, enter the following information correctly!")
			continue
		login = mk_login(name=name, cpf=cpf, state=state)
		error_nbr = 0
		if login:
			return True, name, cpf, street, house_nbr, neighborhood, city, state, login
		else:
			if error_nbr >= 3:
				print(f"{YLOW}Please, contact the support to create your account!{DEFAULT}")
				exit
			print(f"{RED}Login could not be created. Please, try again!{DEFAULT}")
			error_nbr += 1
			continue
	return False, f"Error to register user", "", "", "", "", "", "", ""

def is_cpf_registered(bank_list: dict, user_cpf: str) -> tuple[bool, str]:
	for client in bank_list.get("client", {}).values():
		if client.get("cpf") == user_cpf:
			return True, "CPF {cpf} is already registered!"
	return False, f"CPF {user_cpf} not registered!"

def is_login_registered(bank_list: dict, login: str) -> tuple[bool, str]:
	if login in bank_list.get("client", {}):
		return True, f"Login {login} already registered!"
	return False, f"Login {login} not registered!"

def registered_new_user(bank_list: dict, name: str, cpf: str, street='none', house_nbr='none', neighborhood='none', city='none', state='none', login='') -> tuple[bool, str]:
	is_cpf_reg, cpf_ret = is_cpf_registered(bank_list=bank_list, user_cpf=cpf)
	if is_cpf_reg:
		return False, cpf_ret
	
	is_login_reg, login_ret = is_login_registered(bank_list=bank_list, login=login)
	if is_login_reg:
		return False, login_ret
	
	clients = bank_list.get("client", {})
	if clients:
		account_numbers = [int(client["account"]) for client in clients.values() if client.get("account").isdigit()]
		next_account = str(max(account_numbers) + 1) if account_numbers else "1"
	else:
		next_account = "1"
	init_pin = mk_pin()
	bank_list.setdefault("client", {})[login] = {
		"account": next_account,
		"pin": init_pin,
		"name": name,
		"cpf": cpf,
		"balance": 0,
		"statement": {"operation_0": {"Operation": "", "Value": ""}},
		"Address": {
			"street": street,
			"house_nbr": house_nbr,
			"neighborhood": neighborhood,
			"city": city,
			"state": state
		}
	}
	return True, f"User {name} registered successfully with login '{login}', account {next_account}, and your pin is {init_pin}."


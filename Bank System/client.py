from libs.color import RED, YLOW, PINK, CYAN, DEFAULT
from libs.utils import clear

class Client:
	def __init__(self, name: str, cpf: str, birthday: str, account: str, pin: str, street: str, house_nbr: str, neighborhood: str, city: str, state: str):
		self.name = name
		self.cpf = cpf
		self.birthday = birthday
		self.account = account
		self.pin = pin
		self.balance = 0.0
		self.address = {
			"street": street,
			"house_nbr": house_nbr,
			"neighborhood": neighborhood,
			"city": city,
			"state": state
		}
		self.statement = {"operation_0": {"Operation": "", "Value": ""}}

	def mk_deposit(self, amount: float) -> float:
		self.balance += float(amount)
		self._update_statement("Deposit: +", amount)
		return self.balance

	def mk_withdrawal(self, amount: float, withdrawal_count: int, protect_limit: int = 3) -> tuple[float, bool]:
		if withdrawal_count >= protect_limit:
			return self.balance, False
		if float(amount) > self.balance:
			return self.balance, False
		self.balance -= float(amount)
		self._update_statement("Withdrawal: -", amount)
		return self.balance, True

	def _update_statement(self, operation: str, value: float) -> None:
		next_id = max([int(op.split("_")[1]) for op in self.statement.keys()] + [-1]) + 1
		op_id = f"operation_{next_id}"
		self.statement[op_id] = {"Operation": operation, "Value": value}

	def display_statement(self) -> None:
		clear(2, 0)
		print(f"Your bank statement is as following:\n{PINK}Operation: Value{DEFAULT}")
		for op_data in self.statement.values():
			op, val = op_data["Operation"], op_data["Value"]
			if op:
				formatted_val = "{:.2f}".format(float(val))
				print(f"{op}R${formatted_val}")
		formatted_balance = "{:.2f}".format(self.balance)
		print(f"\nYour current balance is: {CYAN}{formatted_balance}{DEFAULT}!")

	def handle_login(self, input_pin: str, max_attempts: int = 3) -> tuple[bool, str]:
		try_nbr = 1
		check_pin = input_pin
		while try_nbr < max_attempts:
			if check_pin == self.pin:
				return True, ""
			clear(1, 0)
			if try_nbr == max_attempts - 1:
				print(RED, "Wrong password, please, try again!\n", YLOW, "[note: this is your last try for today]", DEFAULT)
			else:
				print(RED, "Wrong password, please, try again!", DEFAULT)
			check_pin = input("Enter your password: ")
			try_nbr += 1
		if check_pin == self.pin:
			return True, ""
		return False, "Too many attempts to login!"
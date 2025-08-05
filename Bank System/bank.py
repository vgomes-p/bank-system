import random
import string
from client import Client
from libs.color import YLOW, DEFAULT

class Bank:
	def __init__(self, agency: str):
		self.agency = agency
		self.clients = {}

	def registered_new_user(self, name: str, cpf: str, birthday: str, street: str, house_nbr: str, neighborhood: str, city: str, state: str, login: str, pin: str="no_pin") -> tuple[bool, str]:
		if self.is_cpf_registered(cpf):
			return False, f"CPF {cpf} is already registered!"
		if self.is_login_registered(login):
			return False, f"Login {login} already registered!"
		
		account_nbrs = [int(client.account) for client in self.clients.values() if client.account.isdigit()]
		next_account = str(max(account_nbrs) + 1) if account_nbrs else "1"
		if pin == "no_pin":
			pin = self._mk_pin()
		self.clients[login] = Client(
			name=name,
			cpf=cpf,
			birthday=birthday,
			account=next_account,
			pin=pin,
			street=street,
			house_nbr=house_nbr,
			neighborhood=neighborhood,
			city=city,
			state=state
		)
		return True, f"User {YLOW}'{name}'{DEFAULT} registered successfully with login {YLOW}'{login}'{DEFAULT}, account {YLOW}{next_account}{DEFAULT}, and initial access pin {YLOW}{pin}{DEFAULT}"

	def is_cpf_registered(self, cpf: str) -> bool:
		return any(client.cpf == cpf for client in self.clients.values())

	def is_login_registered(self, login: str) -> bool:
		return login in self.clients

	def account_exists(self, agency: str, login: str, account: str, cpf: str) -> tuple[bool, str]:
		if self.agency != agency:
			return False, f"Agency '{agency}' not found!"
		if login not in self.clients:
			return False, f"Client for the login '{login}' not found!"
		client = self.clients[login]
		if account != client.account:
			return False, f"The account '{account}' does not belong to {client.name}!"
		if cpf != client.cpf:
			return False, f"Invalid CPF for {client.name}'s account!"
		return True, client.name

	def _mk_pin(self) -> str:
		base = (random.sample(string.ascii_letters, k=4) +
				random.sample(string.digits, k=3) +
				random.sample(["!", "#", "%", "*"], k=2))
		random.shuffle(base)
		return ''.join(base)
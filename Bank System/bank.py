import random
import string
from client import Client
from libs.color import RED, YLOW, DEFAULT
import sqlite3
from sqlite3 import Error

class Bank:
	def __init__(self, agency: str):
		self.agency = agency
		self.clients = {}
		self.db_file = "bank.db"
		self.__init__db()
		self._load_clients()
	
	def __init__db(self) -> None:
		try:
			conn = sqlite3.connect(self.db_file)
			cursor = conn.cursor()
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS clients (
					login TEXT PRIMARY KEY,
					name TEXT NOT NULL,
					cpf TEXT NOT NULL UNIQUE,
					birthday TEXT NOT NULL,
					account TEXT NOT NULL UNIQUE,
					pin TEXT NOT NULL,
					balance REAL NOT NULL,
					street TEXT NOT NULL,
					house_nbr TEXT NOT NULL,
					neighborhood TEXT NOT NULL,
					city TEXT NOT NULL,
					state TEXT NOT NULL
				)
			''')
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS withdrawal_counts (
					login TEXT NOT NULL,
					date TEXT NOT NULL,
					count INTEGER NOT NULL,
					PRIMARY KEY (login, date),
					FOREIGN KEY (login) REFERENCES clients(login)
				)
			''')
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS statements (
					login TEXT NOT NULL,
					operation_id TEXT NOT NULL,
					operation TEXT NOT NULL,
					value REAL NOT NULL,
					operation_time TEXT NOT NULL,
					PRIMARY KEY (login, operation_id),
					FOREIGN KEY (login) REFERENCES clients(login)
				)
			''')
			
			conn.commit()
		except Error as e:
			print(f"{RED}Error initializing database:{e}{DEFAULT}")
		finally:
			conn.close()

	def _load_clients(self) -> None:
		try:
			conn =sqlite3.connect(self.db_file)
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM clients")
			for row in cursor.fetchall():
				login, name, cpf, birthday, account, pin, balance, street, house_nbr, neighborhood, city, state = row
				client = Client(
					name=name,
					cpf=cpf,
					birthday=birthday,
					account=account,
					pin=pin,
					street=street,
					house_nbr=house_nbr,
					neighborhood=neighborhood,
					city=city,
					state=state,
					login=login,
					db_file=self.db_file
				)
				cursor.execute("SELECT operation_id, operation, value, operation_time FROM statements WHERE login = ?", (login,))
				client.statement = {row[0]: {"Operation": row[1], "Value": row[2], "Operation_time": row[3]} for row in cursor.fetchall()}
				client.balance=balance
				cursor.execute("SELECT date, count FROM withdrawal_counts WHERE login = ?", (login,))
				client.withdrawal_cnt = {date: count for date, count in cursor.fetchall()}
				self.clients[login] = client
		except Error as e:
			print(f"{RED}Error loading clients: {e}{DEFAULT}")
		finally:
			conn.close()

	def registered_new_user(self, name: str, cpf: str, birthday: str, street: str, house_nbr: str, neighborhood: str, city: str, state: str, login: str, pin: str="no_pin") -> tuple[bool, str]:
		if self.is_cpf_registered(cpf):
			return False, f"CPF {cpf} is already registered!"
		if self.is_login_registered(login):
			return False, f"Login {login} already registered!"
		try:
			conn = sqlite3.connect(self.db_file)
			cursor = conn.cursor()
			cursor.execute("SELECT account FROM clients WHERE account GLOB '[0-9]*'")
			account_nbrs = [int(account) for account, in cursor.fetchall() if account.isdigit()]
			next_account = str(max(account_nbrs) + 1) if account_nbrs else "1"
		except Error as e:
			print(f"{RED}Error checking account numbers: {e}{DEFAULT}")
			return False, f"Failed to register user due to database error: {e}"
		finally:
			conn.close()
			
		if pin == "no_pin":
			pin = self._mk_pin()
		client = Client(
			name=name,
			cpf=cpf,
			birthday=birthday,
			account=next_account,
			pin=pin,
			street=street,
			house_nbr=house_nbr,
			neighborhood=neighborhood,
			city=city,
			state=state,
			login=login,
			db_file=self.db_file
		)
		self.clients[login] = client
		try:
			conn = sqlite3.connect(self.db_file)
			cursor = conn.cursor()
			cursor.execute('''
				INSERT INTO clients (login, name, cpf, birthday, account, pin, balance, street, house_nbr, neighborhood, city, state)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			''', (login, name, cpf, birthday, next_account, pin, 0.0, street, house_nbr, neighborhood, city, state))
			conn.commit()
		except Error as e:
			print(f"{RED}Error saving client: {e}{DEFAULT}")
			return False, f"Failed to register user due to database error: {e}"
		finally:
			conn.close()
		return True, f"User {name} registered successfully with login {YLOW}'{login}'{DEFAULT}, account {YLOW}{next_account}{DEFAULT}, and initial access pin {YLOW}{pin}{DEFAULT}"

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
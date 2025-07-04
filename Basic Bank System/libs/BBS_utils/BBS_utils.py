class BankSystem:
	@staticmethod
	def deposit(cur_value, new_value):
		after_deposit = float(cur_value) + float(new_value)
		return float(after_deposit)

	@staticmethod
	def withdrawal(cur_value, value_taken):
		after_withdrawal = float(cur_value) - float(value_taken)
		return float(after_withdrawal)

	@staticmethod
	def update_statement(clients_statement, client_login, operation, value):
		if client_login not in clients_statement:
			clients_statement[client_login] = {}
		operations = clients_statement[client_login]
		if operations:
			ids = [int(op.split("_")[1]) for op in operations.keys()]
			next_id = max(ids) + 1
		else:
			next_id = 0
		
		new_op_id = f"operation_{next_id}"
		operations[new_op_id] = {"Operation": operation, "Value": value}
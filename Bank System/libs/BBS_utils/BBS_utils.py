def make_deposit(cur_value, new_value):
	after_deposit = float(cur_value) + float(new_value)
	return float(after_deposit)

def withdrawal(cur_value, value_taken):
	after_withdrawal = float(cur_value) - float(value_taken)
	return float(after_withdrawal)

def update_statement(bank_list, agency, login, operation, value):
	statement = bank_list[agency][login].setdefault("statement", {})
	if statement:
		ids = [int(op.split("_")[1]) for op in statement.keys()]
		next_id = max(ids) + 1
	else:
		next_id = 0
	op_id = f"operation_{next_id}"
	statement[op_id] = {"Operation": operation, "Value": value}


def new_user(name, cpf, street='none', house_nbr='none', neighborhood='none', city='none', state='none'): #to-do
	pass



def is_cpf_registered(registered_cpfs, new_user_cpf): #to-do
	pass

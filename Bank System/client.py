from libs.color import GREEN, RED, YLOW, PINK, CYAN, DEFAULT
from libs.bank_system_utils import mk_file_name
from datetime import datetime
from libs.utils import clear
from sqlite3 import Error
from pathlib import Path
import getpass
import platform
import sqlite3
import os


def get_downloads_path() -> str:
    '''Find the correct path for the folder Download
    If the folder do not exits, it creates one'''
    try:
        if platform.system() == "Windows":
            return os.path.join(os.path.expanduser("~"), "Downloads")
        elif (
            platform.system() == "Linux"
            and "microsoft" in platform.uname().release.lower()
        ):
            username = None
            if "WSLENV" in os.environ and "USERPROFILE" in os.environ:
                userprofile = os.environ["USERPROFILE"]
                username = os.path.basename(userprofile)
            if not username and "USERNAME" in os.environ:
                username = os.environ["USERNAME"]
            if not username:
                username = os.getlogin()
            downloads_path = f"/mnt/c/Users/{username}/Downloads"
            if os.path.isdir(downloads_path):
                return downloads_path
            else:
                users_dir = "/mnt/c/Users"
                if os.path.isdir(users_dir):
                    for user in os.listdir(users_dir):
                        if user.lower() not in ["public", "default", "all users"]:
                            potential_path = f"/mnt/c/Users/{user}/Downloads"
                            if os.path.isdir(potential_path):
                                return potential_path
                return os.path.expanduser("~/Downloads")
        else:
            return os.path.expanduser("~/Downloads")
    except Exception:
        return os.path.expanduser("~/Downloads")


download_path = Path(get_downloads_path())


class Client:
    def __init__(
        self,
        name: str,
        cpf: str,
        birthday: str,
        account: str,
        pin: str,
        pix_key: str,
        street: str,
        house_nbr: str,
        neighborhood: str,
        city: str,
        state: str,
        login: str = "",
        db_file: str = "bank.db",
    ):
        self.name = name
        self.cpf = cpf
        self.birthday = birthday
        self.account = account
        self.pin = pin
        self.pix_key = pix_key
        self.login = login
        self.balance = 0.0
        self.address = {
            "street": street,
            "house_nbr": house_nbr,
            "neighborhood": neighborhood,
            "city": city,
            "state": state,
        }
        self.statement = {
            "operation_0": {"Operation": "", "Value": "", "Operator_name": "", "Receiver_name": "", "Operation_time": ""}
        }
        self.withdrawal_cnt = {}
        self.db_file = db_file

    def mk_deposit(self, amount: float) -> float:
        '''Add a value to the user's balance'''
        self.balance += float(amount)
        operation_time = datetime.now().replace(microsecond=0)
        self._update_statement(
            operation="deposit", value=amount, operator_name=self.name, receiver_name=self.name, operation_time=str(operation_time)
        )
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clients SET balance = ? WHERE account = ?",
                (self.balance, self.account),
            )
            conn.commit()
        except Error as e:
            print(f"{RED}Error saving deposit: {e}{DEFAULT}")
        finally:
            conn.close()
        return self.balance

    def mk_withdrawal(
        self, amount: float, protect_limit: int = 3
    ) -> tuple[float, bool]:
        '''Take a value out of the user's balance'''
        if self.get_daily_withdrawal_cnt() >= protect_limit:
            return self.balance, False
        if float(amount) > self.balance:
            return self.balance, False
        self.balance -= float(amount)
        operation_time = datetime.now().replace(microsecond=0)
        self._update_statement(
            operation="withdrawal", value=amount, operator_name=self.name, receiver_name=self.name, operation_time=str(operation_time)
        )
        self.increment_withdrawal_cnt()
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clients SET balance = ? WHERE account = ?",
                (self.balance, self.account),
            )
            current_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                """
                INSERT OR REPLACE INTO withdrawal_counts (login, date, count)
                VALUES (?, ?, ?)
                """,
                (self.login, current_date, self.get_daily_withdrawal_cnt()),
            )
            conn.commit()
        except Error as e:
            print(f"{RED}Error saving withdrawal: {e}{DEFAULT}")
        finally:
            conn.close()
        return self.balance, True

    def mk_pix(self, pix_key: str, amount) -> tuple[bool, str]:
        personal_keys = [self.cpf, self.pix_key]
        operation_time = datetime.now().replace(microsecond=0)
        if pix_key in personal_keys:
            return False, f"{RED}You cannot send pix to yourself!{DEFAULT}"
        if amount > self.balance:
            return False, f"You can only send a amount lower than R${self.balance}!"
        if len(pix_key) == 11:
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT login, name, balance FROM clients WHERE cpf = ?", (pix_key,))
                alian_login, alian_name, alian_balance = cursor.fetchone()
                new_balance = alian_balance + amount
                cursor.execute(
                    "UPDATE clients SET balance = ? WHERE login = ?",
                    (new_balance, alian_login)
                )
                personal_new_balance = self.balance - amount
                cursor.execute("UPDATE clients SET balance = ? WHERE login = ?", (personal_new_balance, self.login))
                conn.commit()
                self.balance -= amount
                self._update_statement(
                    operation="pix sent", value=amount, operator_name=self.name, receiver_name=alian_name, operation_time=str(operation_time)
                )
                self._update_somebody_statement(
                    operation="pix received", value=amount, operator_name=self.name, receiver_name=alian_name, operation_time=str(operation_time), login=alian_login
                )
                formated_pix_amount = "{:.2f}".format(float(amount))
                return True, f"{CYAN}You send R${formated_pix_amount} to {alian_name} using PIX!{DEFAULT}"
            except Error as e:
                return False, f"{RED}Error saving pix: {e}{DEFAULT}"
            finally:
                conn.close()
        elif len(pix_key) == 10:
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT login, name, balance FROM clients WHERE pix_key = ?", (pix_key,))
                alian_login, alian_name, alian_balance = cursor.fetchone()
                new_balance = alian_balance + amount
                cursor.execute(
                    "UPDATE clients SET balance = ? WHERE login = ?",
                    (new_balance, alian_login)
                )
                personal_new_balance = self.balance - amount
                cursor.execute("UPDATE clients SET balance = ? WHERE login = ?", (personal_new_balance, self.login))
                conn.commit()
                self.balance -= amount
                self._update_statement(
                    operation="pix sent", value=amount, operator_name=self.name, receiver_name=alian_name, operation_time=str(operation_time)
                )
                self._update_somebody_statement(
                    operation="pix received", value=amount, operator_name=self.name, receiver_name=alian_name, operation_time=str(operation_time), login=alian_login
                )
                formated_pix_amount = "{:.2f}".format(float(amount))
                return True, f"{CYAN}You send R${formated_pix_amount} to {alian_name} using PIX!{DEFAULT}"
            except Error as e:
                return False, f"{RED}Error saving pix: {e}{DEFAULT}"
            finally:
                conn.close()
        else:
            return False, f"{RED}Pix key is not valid!{DEFAULT}"

    def _update_statement(
        self, operation: str, value: float, operator_name: str, receiver_name: str, operation_time: str
    ) -> None:
        '''Update user's statement'''
        next_id = (
            max([int(op.split("_")[1]) for op in self.statement.keys()] + [-1]) + 1
        )
        op_id = f"operation_{next_id}"
        op_all_name = operator_name.split(" ")
        op_name = f"{op_all_name[0]} {op_all_name[-1]}"
        re_all_name = receiver_name.split(" ")
        re_name = f"{re_all_name[0]} {re_all_name[-1]}"
        self.statement[op_id] = {
            "Operation": operation,
            "Value": value,
            "Operator_name": op_name,
            "Receiver_name": re_name,
            "Operation_time": operation_time,
        }
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO statements (login, operation_id, operation, value, operator_name, receiver_name, operation_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (self.login, op_id, operation, value, op_name, re_name, operation_time),
            )
            conn.commit()
        except Error:
            print(f"{RED}Error saving personal statement: {e}{DEFAULT}")
        finally:
            conn.close()

    def _update_somebody_statement(
        self, operation: str, value: float, operator_name, receiver_name: str, operation_time: str, login: str
    ) -> None:
        '''Update user's statement'''
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT operation_id FROM statements WHERE login = ? ORDER BY operation_id DESC LIMIT 1", (login,))
        last_id = cursor.fetchone()
        next_id = int(last_id[0].split("_")[1]) + 1 if last_id else 1
        op_id = f"operation_{next_id}"
        op_id = f"operation_{next_id}"
        op_all_name = operator_name.split(" ")
        op_name = f"{op_all_name[0]} {op_all_name[-1]}"
        re_all_name = receiver_name.split(" ")
        re_name = f"{re_all_name[0]} {re_all_name[-1]}"
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO statements (login, operation_id, operation, value, operator_name, receiver_name, operation_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (login, op_id, operation, value, op_name, re_name, operation_time),
            )
            conn.commit()
        except Error:
            print(f"{RED}Error saving alian statement{DEFAULT}")
        finally:
            conn.close()

    def _print_statement(self, statement_path: str, balance: str) -> None:
        '''Print the user's statement in the terminal'''
        try:
            with open(statement_path, "w") as writing:
                writing.write("Your bank statement is as following:\n")
                writing.write("\nOn Time when operation happen -> Operation: Value\n")
                for op_data in self.statement.values():
                    op, val, operator_name, receiver_name, op_time = (
                        op_data["Operation"],
                        op_data["Value"],
                        op_data["Operator_name"],
                        op_data["Receiver_name"],
                        op_data["Operation_time"],
                    )
                    if op:
                        formatted_val = "{:.2f}".format(float(val))
                        if op == "deposit":
                            writing.write(f"You made a deposit of R${formatted_val} on {op_time}.\n")
                        elif op == "withdrawal":
                            writing.write(f"You made a deposit of R${formatted_val} on {op_time}.\n")
                        elif op == "pix received":
                            writing.write(f"You received a pix of R${formatted_val} from {operator_name} on {op_time}.\n")
                        elif op == "pix sent":
                            writing.write(f"You sent a pix of R${formatted_val} to {receiver_name} on {op_time}.\n")
                writing.write(f"\nYour current balance is: R${balance}!")
        except IOError as e:
            print(f"{RED}Error writing statement to file: {e}{DEFAULT}")

    def _is_to_print(self) -> tuple[bool, str]:
        '''Ask if the user's want's to download/print the statement'''
        while True:
            try:
                answer = input(
                    "Do you want to print this statement?\n[Please, answer 'y' for yes and 'n' for no]\n>>> "
                )
                if answer not in ["y", "n"]:
                    print(f"{YLOW}Please, answer as requested!{DEFAULT}")
                    continue
                if answer == "n":
                    return False, ""
                name = self.name.split(" ")
                return True, name[0]
            except ValueError:
                print(f"{RED}Please, enter a valid value!{DEFAULT}")

    def _handle_print_statement(self, name: str, date: str) -> str:
        '''Create a statement file in the folder 'Download' with the statement'''
        if name and date:
            try:
                file_name = mk_file_name(name, date.replace(" ", "_").replace(":", "-"))
                statement_path = download_path / file_name
                if not download_path.exists():
                    os.makedirs(download_path, exist_ok=True)
                if not os.access(download_path, os.W_OK):
                    return f"{RED}Error: Downloads directory ({download_path}) is not writable.{DEFAULT}"
                self._print_statement(
                    statement_path=str(statement_path), balance=self.balance
                )
                return f"Your statement were downloaded at {statement_path}."
            except PermissionError:
                return f"{RED}Error: Permission deniel when trying to write to {download_path}.{DEFAULT}"
            except Exception as e:
                return f"{RED}Error generating statement file: {e}{DEFAULT}"
        return f"{RED}Error: Could not generate statement file.{DEFAULT}"

    def display_statement(self) -> None:
        '''Print the user's statement in the terminal'''
        clear(2, 0)
        print(
            f"Your bank statement is as following:\n\n{PINK}On Time when operation happen -> Operation: Value{DEFAULT}"
        )
        for op_data in self.statement.values():
            # print(f"{YLOW}DEBUG:{DEFAULT} {op_data.keys()})
            op, val, operator_name, receiver_name, op_time = (
                op_data["Operation"],
                op_data["Value"],
                op_data["Operator_name"],
                op_data["Receiver_name"],
                op_data["Operation_time"],
            )
            if op:
                display_message = ""
                formatted_val = "{:.2f}".format(float(val))
                if op == "deposit":
                    display_message = f"You made a {GREEN}deposit{DEFAULT} of {YLOW}R${formatted_val}{DEFAULT} on {CYAN}{op_time}{DEFAULT}."
                elif op == "withdrawal":
                    display_message = f"You made a {RED}deposit{DEFAULT} of {YLOW}R${formatted_val}{DEFAULT} on {CYAN}{op_time}{DEFAULT}."
                elif op == "pix received":
                    display_message = f"You {GREEN}received a pix{DEFAULT} of {YLOW}R${formatted_val}{DEFAULT} from {PINK}{operator_name}{DEFAULT} on {CYAN}{op_time}{DEFAULT}."
                elif op == "pix sent":
                    display_message = f"You {RED}sent a pix{DEFAULT} of {YLOW}R${formatted_val}{DEFAULT} to {PINK}{receiver_name}{DEFAULT} on {CYAN}{op_time}{DEFAULT}."
                print(display_message)
        formatted_balance = "{:.2f}".format(self.balance)
        print(f"\nYour current balance is: {YLOW}R${formatted_balance}{DEFAULT}!")
        ret, name = self._is_to_print()
        if ret:
            today = datetime.now().strftime("%Y-%m-%d_%H-%M")
            ret = self._handle_print_statement(name=name, date=today)
            print(ret)

    def handle_login(self, input_pin: str, max_attempts: int = 3) -> tuple[bool, str]:
        '''Checks if the user's login credentials are correct'''
        try_nbr = 1
        check_pin = input_pin
        while try_nbr < max_attempts:
            if check_pin == self.pin:
                return True, ""
            clear(1, 0)
            if try_nbr == max_attempts - 1:
                print(f"{RED}Wrong password, please, try again!\n{YLOW}[note: this is your last try for today]{DEFAULT}")
            else:
                print(f"{RED}Wrong password, please, try again!{DEFAULT}")
            check_pin = getpass.getpass("Enter your password: ")
            try_nbr += 1
        if check_pin == self.pin:
            return True, ""
        return False, "Too many attempts to login!"

    def get_daily_withdrawal_cnt(self) -> int:
        '''Get what day the user is making the withdrawal'''
        current_date = datetime.now().strftime("%Y-%m-%d")
        return self.withdrawal_cnt.get(current_date, 0)

    def increment_withdrawal_cnt(self) -> None:
        '''Update how many withdrawals the user made in that day'''
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.withdrawal_cnt[current_date] = self.withdrawal_cnt.get(current_date, 0) + 1

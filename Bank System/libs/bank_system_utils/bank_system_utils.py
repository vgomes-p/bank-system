from libs.color import RED, DEFAULT


def mk_login(name: str, cpf: str, state: str) -> str:
    '''Create a login using user's data'''
    if not (name and cpf and state):
        return ""
    if len(cpf) != 11 or not cpf.isdigit():
        return ""
    if len(state) != 2 or not state.isalpha():
        return ""
    name_splited = list(name.split(" "))
    first_name = str(name_splited[0]).replace("'", "").replace("[", "").replace("]", "")
    last_name = str(name_splited[-1]).replace("'", "").replace("[", "").replace("]", "")
    half_last_name, cpf_num_0, cpf_num_1, end = (
        last_name[0].lower(),
        cpf[1],
        cpf[8],
        state.upper(),
    )
    return (
        f"{first_name[:4].lower()}{cpf_num_0}{cpf_num_1}{half_last_name.title()}-{end}"
    )


def is_date_valid(date: str) -> bool:
    '''Checks if a date is correct'''
    try:
        day, month, year = map(int, date.split("/"))
        if len(str(day)) <= 2 and len(str(month)) <= 2 and len(str(year)) == 4:
            if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2025:
                return True
        return False
    except (ValueError, AttributeError):
        return False


def get_new_user_credentials() -> (
    tuple[bool, str, str, str, str, str, str, str, str, str]
):
    '''Collect all data from new users for a user data base'''
    print("Please, enter the following informations to create your account!")
    while True:
        name = input("Full name: ").strip()
        cpf = input("CPF number: ").replace(".", "").replace("-", "")
        birthday = input("Date of Birth (DD/MM/YYYY): ").strip()
        street = input("Street: ").strip()
        house_nbr = input("House Number: ").strip()
        neighborhood = input("Neighborhood: ").strip()
        city = input("City: ").strip()
        state = input("State [eg.: SP, MG]: ").strip().upper()
        if not all([name, cpf, birthday, street, house_nbr, neighborhood, city, state]):
            print(
                f"{RED}No item can be empty!{DEFAULT}\nPlease, enter the following information correctly!"
            )
            continue
        if len(cpf) != 11 or not cpf.isdigit():
            print(
                f"{RED}CPF can only contains 11 numbers!{DEFAULT}\nPlease, enter the following information correctly!"
            )
            continue
        if not is_date_valid(birthday):
            print(f"{RED}Invalid date format! Use DD/MM/YYYY.{DEFAULT}")
            continue
        login = mk_login(name=name, cpf=cpf, state=state)
        if login:
            return (
                True,
                name,
                cpf,
                birthday,
                street,
                house_nbr,
                neighborhood,
                city,
                state,
                login,
            )
        print(f"{RED}Login could not be created. Please, try again!{DEFAULT}")
    return False, "Error to register user", "", "", "", "", "", "", "", ""


def mk_file_name(name: str, day: str) -> str:
    '''return a standardized name for the statement file'''
    return f"{name}_statement_{day}.txt"

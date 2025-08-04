# Medium Bank System – Santander Bootcamp 2025 (Back-End with Python)

### In this update, I implemented significant improvements and new features to make the system more secure, modular, and functional:

🔼 **Data structure reorganization** – All client information is now centralized in a single dictionary.

🔼 **Code modularization** – Refactored large functions into smaller ones, each with a specific responsibility, improving maintainability and scalability.

➕ **Monetary value formatting** – All monetary values are now displayed with two decimal places to ensure consistency.

➕ **Enhanced security validations** – The system now checks for duplicate logins and CPF (Brazilian ID) during user registration.

➕ **Full user registration** – Includes collection of full name, CPF, and address.

➕ **Automatic login generator** – Generates unique logins based on client information.

➕ **Security check system** – Ensures that no duplicate accounts are created using the same login or CPF.

## HOW TO TEST

### 1. Clone this branch
```bash
git clone --single-branch --branch v1.-medium_bank_system https://github.com/vgomes-p/bank-system.git
```

### 2. Navigate to the correct directory
```bash
cd bank-system/Bank\ System/
```

### 3. Call the program
```bash
python3 main.py
```

DEFAULT			=	\033[0m
RED				=	\033[1;31m
CYAN			=	\033[1;36m
PINK			=	\033[1;35m
GREEN			=	\033[1;32m
YELLOW			=	\033[1;33m
REWHITE			=	\033[1;7;97m
RECYAN			=	\033[1;7;36m
REPINK			=	\033[1;7;35m
RERED			=	\033[1;7;31m
REGREEN			=	\033[1;7;32m
REYELLOW		=	\033[1;7;33m


help:
		@clear
		@echo "$(YELLOW)help:$(DEFAULT) show all commands that the make for this project supports"
		@echo "$(YELLOW)run:$(DEFAULT) run the project"
		@echo "$(YELLOW)flake:$(DEFAULT) run flake8"
		@echo "$(YELLOW)flake_ign:$(DEFAULT) run flake8 ignoring some errors"
		@echo "$(YELLOW)clean:$(DEFAULT) delete all caches files and the database file"

run:
		@python3 main.py

flake:
		@clear
		@flake8 --max-line-length 150

flake_ign:
		@clear
		@flake8 --ignore=,W503,W504,F401,E501

clean:
		@clear
		@find . -name "__pycache__" -type d -exec rm -rf {} +
		@rm bank.db
		@echo "$(GREEN)Program cleaned successfully!$(DEFAULT)"
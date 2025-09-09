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


main_cache_dir		=	__pycache__/
bsu_cache_dir		=	libs/bank_system_utils/__pycache__/
color_cache_dir		=	libs/color/__pycache__/
utils_cache_dir		=	libs/utils/__pycache__/

run:
		@python3 main.py

clean:
		@rm -rfd main_cache_dir
		@rm -rfd bsu_cache_dir
		@rm -rfd color_cache_dir
		@rm -rfd utils_cache_dir
		@rm bank.db
		@echo "$(GREEN) Program cleaned successfully! $(DEFAULT)"%  
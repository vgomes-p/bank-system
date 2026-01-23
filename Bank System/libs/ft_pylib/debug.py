from .colors import RED, GREEN, YLOW, PINK, DEFAULT

def debug(debug_text: str=False, stats: str="valid stats: success of failed",
         error_text: str=False, output: list=False):
    """
    Display a formatted debug message in the terminal.
    
    This function prints colored debug information to stdout based on
    the execution status of a process. It supports success and failure
    states, optional output listings, and terminates the program with
    specific exit codes in error scenarios.
    
    The function has side effects:
    - Prints formatted output to the terminal
    - May terminate the program using ``exit()``

    :param debug_text: Informational message shown during successful
                       execution or generic debug output.
    :type debug_text: str | bool
    :param stats: Execution status indicator. Valid values are
                  ``"success"`` or ``"failed"`` (case-insensitive).
                  Any other value causes an error and exits the program.
    :type stats: str
    :param error_text: Error message displayed when the status is
                       ``"failed"``.
    :type error_text: str | bool
    :param output: Optional list of values to be displayed as output
                   details.
    :type output: list | bool
    :return: Returns 0 when execution is successful or when no
             failure condition is met.
    :rtype: int

    :raises SystemExit: Exits with code 1 if ``stats`` is ``"failed"``.
    :raises SystemExit: Exits with code 2 if ``stats`` is invalid.
    """
    valid_stats = ["success", "failed"]
    debug_init = f"{YLOW}<-------------------------------------------------------------------->\nDEBUG:"
    debug_end = f"\n{YLOW}<-------------------------------------------------------------------->{DEFAULT}"
    oput = f"{PINK}Outputs:"
    error = f"{RED}Error:"
    if stats == "valid stats: success of failed":
        pass
    elif stats.lower() not in valid_stats:
        print(debug_init, error, f"invalid stats entered!\nvalid entries: ['success', 'failed']",
              f"\n{oput}\n invalid entry: {valid_stats}{DEFAULT}", debug_end)
        exit(2)
    if stats.lower() == "success":
        print(debug_init, f"{GREEN}Process ran successfully!!!{YLOW}\n", debug_text)
        if output:
            print(oput)
            for i in output:
                print(" ", i)
        else:
            print(oput, "none!")
        print(debug_end)
        return 0
    if stats.lower() == "failed":
        print(debug_init, f"{RED}Process ran failed{YLOW}\n", error_text)
        if output:
            print(oput)
            for i in output:
                print(" ", i)
        else:
            print(oput, "none!")
        print(debug_end)
        exit(1)
    print(debug_init, debug_text)
    if output:
        print(oput)
        for i in output:
            print(" ", i)
    else:
        print(oput, "none")
    print(debug_end)
    return 0

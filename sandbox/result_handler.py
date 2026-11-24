
def handle_result(execution_result):
    exit_code = execution_result["exit_code"]
    stdout = execution_result["stdout"]
    stderr = execution_result["stderr"]

    if exit_code == 0:
        status = "Success"
    elif exit_code == -1:
        status = "Execution Failed"
    else:
        status = "Runtime Error"

    return {
        "status": status,
        "output": stdout,
        "error": stderr,
        "exit_code": exit_code
    }

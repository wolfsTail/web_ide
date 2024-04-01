from contextlib import redirect_stdout
from io import StringIO
import subprocess
import traceback
import concurrent.futures


def execute_code(code_input, language, timeout): 
    output = None
    
    if language == "python":
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(exec_python_code, code_input)
                output = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            output = "Error: Время выполнения кода превысило допустимый лимит."
        except Exception as err:
            output = f"Error: {str(err)}\n{traceback.format_exc()}"

    elif language in ("c", "go"):
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(exec_compiled_code, code_input, language)
                output = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            output = "Error: Время выполнения кода превысило допустимый лимит."
        except Exception as err:
            output = f"Error: {str(err)}\n{traceback.format_exc()}"

    return output

def exec_python_code(code_input):
    output_buffer = StringIO()
    with redirect_stdout(output_buffer):
        exec(code_input, {"__builtins__": __builtins__}, {})
    return output_buffer.getvalue()

def exec_compiled_code(code_input, language):
    try:
        language_params = {
            "c": ["gcc", "-o", "run", "run.c"],
            "go": ["go", "build", "-o", "run", "run.go"],
        }

        subprocess.run(language_params[language], check=True)

        result = subprocess.run(["tmp/run"], capture_output=True, text=True, check=True, timeout=1)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Процесс был прерван из-за таймаута."
    except Exception as err:
        return f"Error: {str(err)}"


def create_file(code_input, language):
    file_map = {"c": "run.c", "go": "run.go", "python": None}
    filename = file_map.get(language)
    if filename:
        with open(f"tmp/{filename}", "w") as f:
            f.write(code_input)

def run_code(code_input, language="python", timeout=1):
    create_file(code_input, language)  
    return execute_code(code_input, language, timeout)


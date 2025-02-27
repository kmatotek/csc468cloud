import os
import ollama
import subprocess
import re

# List of models to test
models = ["qwen2.5-coder"]

# Get the last non-empty line from text
def get_last_non_empty_line(text):
    clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)  # Remove ANSI escape codes
    lines = clean_text.splitlines()
    for line in reversed(lines):
        if line.strip():
            return line.strip()
    return ""

# Extract passed and total test cases from Kattis feedback
def get_test_cases_info(feedback):
    matches = re.findall(r"Test cases:\s*\[.*?\]\s*(\d+)\s*/\s*(\d+)", feedback)
    if matches:
        last_match = matches[-1]
        passed = int(last_match[0])
        total = int(last_match[1])
        return passed - 1, total  # Adjust passed count if needed
    return 0, 0

# Count the number of sample test cases
def get_num_sample_test_cases(test_cases_content):
    sample_inputs = re.findall(r"Sample Input \d+", test_cases_content)
    return len(sample_inputs)

# API call function using full conversation history
def api_call_conversation(conversation, model):
    print(conversation)
    response = ollama.chat(
        model=model,
        messages=conversation
    )
    return response["message"]["content"]

# Extract Python code from API response
def get_python(message):
    start_code_block = message.find("```Python")
    if start_code_block == -1:
        start_code_block = message.find("```python")
    if start_code_block == -1:
        start_code_block = message.find("```")
        cut_string = message[start_code_block + 3:]
    else:
        cut_string = message[start_code_block + 10:]
    end_code_block = cut_string.find("```")
    return cut_string[:end_code_block].strip()

# Directories and files
dir_path = "./auto_miningTesting"       # Root directory containing problem folders
file_name = "problem_text"              # Problem description file
test_cases = "sample_input_and_ouput"   # Test case file

for model in models:
    for folder_name in os.listdir(dir_path):
        # Get the folder path
        folder_path = os.path.join(dir_path, folder_name)

        # Only process directories
        if not os.path.isdir(folder_path):
            continue

        # Optional: Process only "1dfroggereasy" for testing
        if not folder_name == "1dfroggereasy":
            continue

        problem_id = folder_name

        # Create folders for submissions and results
        submissions_folder = os.path.join(folder_path, f"submissions_{model}")
        os.makedirs(submissions_folder, exist_ok=True)
        results_folder = os.path.join(folder_path, f"results_{model}")
        os.makedirs(results_folder, exist_ok=True)

        # Read problem description
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            problem_description = file.read()

        # Read test cases if available
        test_cases_path = os.path.join(folder_path, test_cases)
        test_cases_content = ""
        if os.path.exists(test_cases_path):
            with open(test_cases_path, "r", encoding="utf-8") as test_file:
                test_cases_content = "\n\nTest Cases:\n" + test_file.read()

        # Count sample test cases
        num_sample_test_cases = get_num_sample_test_cases(test_cases_content)

        # Combine problem description and test cases
        full_input_text = problem_description + test_cases_content

        # Build the base question prompt
        base_question = (
            "Write a Python program for this problem. Ensure that your solution reads input from standard input using input() and writes output using print(). "
            "Do not include any hardcoded test cases or example inputs in your code. The code should be a complete, runnable program that can be executed directly. "
            "Make sure that the variables' names and functions' names are different, and also only use internal Python libraries, not external ones:\n\n" +
            full_input_text
        )

        # Initialize conversation history
        conversation = [
            {"role": "system", "content": "You are the best competitive programmer in the world with 30 years of experience."},
            {"role": "user", "content": base_question}
        ]

        # Attempt to solve the problem (up to 3 tries)
        for attempt in range(1, 4):
            if attempt > 1:
                # Append feedback from the previous attempt
                conversation.append({"role": "user", "content": feedback})

            # Generate a solution based on the conversation history
            api_answer = api_call_conversation(conversation, model)
            conversation.append({"role": "assistant", "content": api_answer})

            # Extract Python code
            api_python = get_python(api_answer)

            # Save the generated code
            output_file = f"attempt_{attempt}.py"
            output_path = os.path.join(submissions_folder, output_file)
            with open(output_path, "w") as file:
                file.write(api_python)

            # Save the full API response
            api_output_file = f"attempt_{attempt}.txt"
            api_output_path = os.path.join(submissions_folder, api_output_file)
            with open(api_output_path, "w") as file:
                file.write(api_answer)

            # Submit to Kattis
            submit_script_path = os.path.join(os.getcwd(), "framework", "submit.py")
            result = subprocess.run(
                ["python3", submit_script_path, "-p", problem_id, output_path, "-f"],
                capture_output=True,
                text=True
            )

            print(result.stdout)

            # Save submission result
            result_file = f"attempt_{attempt}_result.txt"
            result_path = os.path.join(results_folder, result_file)
            with open(result_path, "w") as file:
                file.write(result.stdout)

            # Check if accepted
            if "Accepted" in result.stdout:
                print(f"Solution accepted on attempt {attempt} for {problem_id} with {model}")
                break
            else:
                # Parse submission results
                passed, total = get_test_cases_info(result.stdout)
                error_message = get_last_non_empty_line(result.stdout)

                # Construct enhanced feedback
                if total == 0:
                    test_cases_feedback = "No test cases were run due to an error."
                else:
                    test_cases_feedback = f"It passed {passed} out of {total} test cases."

                sample_feedback = ""
                if num_sample_test_cases > 0 and passed < num_sample_test_cases:
                    sample_feedback = " Additionally, your solution failed at least one of the sample test cases."

                feedback = (
                    f"The problem is '{problem_id}'. Your previous solution was:\n\n"
                    f"```python\n{api_python}\n```\n"
                    f"It was incorrect. The error type was: {error_message}. "
                    f"{test_cases_feedback} {sample_feedback} "
                    "Please review your code, identify the mistake, and provide a corrected version."
                )

                if attempt < 3:
                    print(f"Attempt {attempt} failed for {problem_id} with {model}. Reprompting...")
                else:
                    print(f"Failed to solve {problem_id} with {model} after 3 attempts.")
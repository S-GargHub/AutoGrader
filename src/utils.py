import re

def parse_test_cases(file_path):
    test_cases = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_test_case = {}
        current_input = None
        current_output = None
        function_name = None

        for line in lines:
            line = line.strip() 
            if line.startswith("Function Name"):
                function_name = line.split(":")[1].strip()  # Extract function name
            if line.startswith("Test Case"):
                # If current_test_case is not empty, add it to the list of test cases
                if current_test_case:
                    test_cases.append(current_test_case)
                    current_test_case = {}

            elif line.startswith("Input:"):
                current_input = line.split(":")[1].strip() 
            elif line.startswith("Output:"):
                current_output = line.split(":")[1].strip()
                # Add current test case to the list
                current_test_case = {'Input': current_input, 'Output': current_output}

        # Add the last test case if it exists
        if current_test_case:
            test_cases.append(current_test_case)

    return test_cases, function_name
    


def parse_problem_file(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Extract problem name
    problem_name_match = re.search(r'Problem Name: (.+)', content)
    if problem_name_match:
        problem_name = problem_name_match.group(1)
    else:
        problem_name = None

    # Extract problem description
    problem_description_match = re.search(r'Problem Description:(.+?)Sample Test Cases:(.+?)', content, re.DOTALL)
    if problem_description_match:
        problem_description = problem_description_match.group(1).strip()
    else:
        problem_description = None

    sample_test_cases_match = re.search(r'Sample Test Cases:(.+)', content, re.DOTALL)
    if sample_test_cases_match:
        sample_test_cases = sample_test_cases_match.group(1).strip()
    else:
        sample_test_cases = None

    return problem_name, problem_description, sample_test_cases
    

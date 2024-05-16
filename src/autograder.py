import ast
import time

from src.utils import *


class AutoGrader:
    def __init__(self, problem, test_case_file):
        self.problem = problem
        self.test_cases, self.funcName = parse_test_cases(test_case_file)
        self.grade = 0

    def grade_solution(self, student_solution):
        error = None
        test_cases_pass = 0
        test_cases_count = len(self.test_cases)
        timeout_ms = 2000
        test_results = []
        timeout = False
        try:
            context = {}
            
            # Execute student's code within the context
            exec(student_solution, context)
            
            # Retrieve the function name in the context
            solution_function = None
            for item in context.values():
                if callable(item) and item.__name__ == self.funcName:
                    solution_function = item
                    break

            if solution_function is None:
                error = "The 'solution' function is not defined or not callable."
                return test_cases_pass, error, test_results

            test_results.append(f"Testing {self.funcName}...")
            test_results.append("> building source...")

            # Evaluate student's code against test cases
            for index, test_case in enumerate(self.test_cases, start=1):
                input = test_case.get('Input', '')
                test_input = ast.literal_eval(input)
                output = test_case.get('Output', '')
                expected_output = ast.literal_eval(output)

                start_time = time.time()
                # if index == 2 or index == 4:
                #     time.sleep(2)
                output = solution_function(*test_input)
                execution_time = round((time.time() - start_time)*1000 , 2)
                if execution_time > timeout_ms:
                    test_results.append(f"test_{index:02} [TIMEOUT] {execution_time}ms")
                    timeout = True
                elif output == expected_output:
                    test_cases_pass += 1
                    test_results.append(f"test_{index:02} [PASS] {execution_time}ms")
                else:
                    test_results.append(f"test_{index:02} [FAIL] {execution_time}ms")
        except SyntaxError as e:
            error = "Compilation Error: " + str(e)
        except Exception as e:
            error = "Error occurred during execution: " + str(e)
        
        if timeout == True:
            error = "Timeout!! Try again"
            test_cases_pass = 0
        self.grade = test_cases_pass/test_cases_count * 100
        return test_cases_pass, error, test_results

    def get_grade(self):
        return self.grade
    

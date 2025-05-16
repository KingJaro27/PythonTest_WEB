import os
import subprocess
from difflib import Differ
from time import time
from typing import List, Tuple, Optional
import tempfile



class TestCase:
    def __init__(
        self,
        input_data: str,
        expected_output: str,
        time_limit: float = 2.0,
        memory_limit: int = 256,
    ):
        self.input_data = input_data
        self.expected_output = expected_output
        self.time_limit = time_limit
        self.memory_limit = memory_limit


class PythonTester:
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.results = []
        self.language_config = {
            "python": {"compile": None, "run": lambda f: ["python", f], "ext": ".py"},
            "cpp": {
                "compile": lambda s, t: ["g++", s, "-o", t],
                "run": lambda f: [f"./{f}"],
                "ext": ".cpp",
            },
            "java": {
                "compile": lambda s, t: ["javac", s],
                "run": lambda f: ["java", f[:-5]],  # без .class
                "ext": ".java",
            },
            "c": {
                "compile": lambda s, t: ["gcc", s, "-o", t],
                "run": lambda f: [f"./{f}"],
                "ext": ".c",
            },
            "go": {
                "compile": lambda s, t: ["go", "build", "-o", t, s],
                "run": lambda f: [f"./{f}"],
                "ext": ".go",
            },
        }
    def get_test_results(self):
        """Return detailed test results"""
        results = []
        for i, (test, result) in enumerate(zip(self.test_cases, self.results), 1):
            result_dict = {
                'test_case': i,
                'input': test.input_data,
                'expected': test.expected_output,
                'status': result.get('status', 'Not run')
            }

            if 'error' in result:
                result_dict['status'] = 'Error'
                result_dict['actual'] = result['error']
            elif 'actual' in result:
                result_dict['actual'] = result['actual']
                result_dict['diff'] = result.get('diff', '')
            else:
                result_dict['actual'] = test.expected_output

            results.append(result_dict)

        return results

    def test_python_code(self, code: str) -> bool:
        self.results = []
        all_passed = True

        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
            temp.write(code.encode('utf-8'))
            temp_path = temp.name

        try:
            for i, test in enumerate(self.test_cases, 1):
                result = {
                    'test_case': i,
                    'input': test.input_data,
                    'expected': test.expected_output,
                    'passed': False,
                    'actual': '',
                    'error': None
                }

                try:
                    process = subprocess.run(
                        ['python', temp_path],
                        input=test.input_data.encode(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=2.0
                    )

                    if process.returncode != 0:
                        result['error'] = process.stderr.decode().strip()
                    else:
                        actual_output = process.stdout.decode().strip()
                        result['actual'] = actual_output
                        result['passed'] = (actual_output == test.expected_output)

                        if not result['passed']:
                            # Generate diff for failed tests
                            d = Differ()
                            diff = list(d.compare(
                                test.expected_output.splitlines(),
                                actual_output.splitlines()
                            ))
                            result['diff'] = '\n'.join(diff)

                except subprocess.TimeoutExpired:
                    result['error'] = "Time limit exceeded"
                except Exception as e:
                    result['error'] = str(e)

                self.results.append(result)
                if not result['passed']:
                    all_passed = False

            return all_passed
        finally:
            os.unlink(temp_path)

    def get_test_results(self):
        return self.results

    def detect_language(self, filename: str) -> Optional[str]:
        """Определение языка программирования по расширению файла"""
        ext = os.path.splitext(filename)[1].lower()
        for lang, config in self.language_config.items():
            if config["ext"] == ext:
                return lang
        return None

    def add_test_case(
        self,
        input_data: str,
        expected_output: str,
        time_limit: float = 2.0,
        memory_limit: int = 256,
    ):
        """Добавить тестовый случай"""
        self.test_cases.append(
            TestCase(input_data, expected_output, time_limit, memory_limit)
        )

    def load_test_cases_from_files(
        self, input_files: List[str], output_files: List[str]
    ):
        """Загрузка тестов из файлов"""
        for in_file, out_file in zip(input_files, output_files):
            with open(in_file, "r") as f:
                input_data = f.read()
            with open(out_file, "r") as f:
                expected_output = f.read()
            self.add_test_case(input_data, expected_output)

    def compile_program(
        self, source_file: str, target: str = "program"
    ) -> Tuple[bool, str]:
        """Компиляция программы (если нужно)"""
        lang = self.detect_language(source_file)
        if not lang:
            return False, f"Unsupported file extension: {source_file}"

        if not os.path.exists(source_file):
            return False, f"File not found: {source_file}"

        compile_cmd = self.language_config[lang]["compile"]
        if compile_cmd is None:
            return True, "No compilation needed"

        try:
            process = subprocess.run(
                compile_cmd(source_file, target),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            if process.returncode != 0:
                return False, process.stderr.decode()
            return True, "Compilation successful"
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, str(e)

    def run_program(
        self, program_path: str, input_data: str, time_limit=1.0
    ) -> Tuple[Optional[str], Optional[str], float]:
        """Запуск программы с входными данными"""
        lang = self.detect_language(program_path)

        if not lang:
            return None, f"Unsupported file extension: {program_path}", 0.0

        run_cmd = self.language_config[lang]["run"]

        try:
            start_time = time()
            process = subprocess.run(
                run_cmd(program_path),
                input=input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=time_limit,
            )
            exec_time = time() - start_time

            if process.returncode != 0:
                return None, process.stderr.decode(), exec_time
            return process.stdout.decode().strip(), None, exec_time
        except subprocess.TimeoutExpired:
            return None, "Time limit exceeded", time_limit
        except Exception as e:
            return None, str(e), 0.0

    def normalize_output(self, output: str) -> str:
        """Нормализация вывода для сравнения"""
        lines = [line.rstrip() for line in output.splitlines()]
        lines = [line for line in lines if line != ""]
        return "\n".join(lines)

    def compare_outputs(self, actual: str, expected: str) -> Optional[str]:
        """Сравнение вывода с ожидаемым результатом"""
        actual_norm = self.normalize_output(actual)
        expected_norm = self.normalize_output(expected)

        if actual_norm == expected_norm:
            return None

        d = Differ()
        diff = list(
            d.compare(
                expected_norm.splitlines(keepends=True),
                actual_norm.splitlines(keepends=True),
            )
        )
        return "".join(diff)

    def run_tests(self, program_path: str) -> bool:
        self.results = []
        all_passed = True

        for i, test in enumerate(self.test_cases, 1):
            result = {
                'test_case': i,
                'input': test.input_data,
                'expected': test.expected_output
            }

            actual, error, exec_time = self.run_program(
                program_path, test.input_data, test.time_limit
            )

            if error:
                result.update({
                    'status': 'Error',
                    'actual': error,
                    'time': exec_time
                })
                all_passed = False
            else:
                diff = self.compare_outputs(actual, test.expected_output)
                if diff:
                    result.update({
                        'status': 'Failed',
                        'actual': actual,
                        'diff': diff,
                        'time': exec_time
                    })
                    all_passed = False
                else:
                    result.update({
                        'status': 'Passed',
                        'actual': actual,
                        'time': exec_time
                    })

            self.results.append(result)

        return all_passed

    def generate_report(self, filename: str = "test_report.txt"):
        with open(filename, "w") as f:
            f.write("=== Test Report ===\n\n")

            total = len(self.results)
            passed = sum(1 for r in self.results if r["status"] == "Passed")
            failed = total - passed

            f.write(f"Total tests: {total}\n")
            f.write(f"Passed: {passed}\n")
            f.write(f"Failed: {failed}\n\n")
            for result in self.results:
                f.write(
                    f"Test {result['test']}: {result['status']} ({result['time']:.3f}s)\n"
                )
                if result["status"] != "Passed":
                    if "error" in result:
                        f.write(f"Error: {result['error']}\n")
                    if "diff" in result:
                        f.write("Difference:\n")
                        f.write(result["diff"] + "\n")

                f.write("\n")

        print(f"Report generated: {filename}")

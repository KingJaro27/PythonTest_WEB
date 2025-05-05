import os
import subprocess
import sys
from difflib import Differ
from time import time
from typing import Dict, List, Tuple, Optional
import sqlite3


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


class TestingSystem:
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
        # Удаление лишних пробелов и пустых строк в конце
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
        """Запуск всех тестов"""
        lang = self.detect_language(program_path)
        if not lang:
            print(f"Error: Unsupported file extension for {program_path}")
            return False

        print(f"Testing {program_path} ({lang} program)")

        # Компиляция (если требуется)
        if self.language_config[lang]["compile"] is not None:
            print("Compiling...")
            success, message = self.compile_program(program_path)
            if not success:
                print(f"Compilation failed: {message}")
                return False
            print("Compilation successful")

        total = len(self.test_cases)
        passed = 0

        print(f"\nRunning {total} test cases...")
        for i, test in enumerate(self.test_cases, 1):
            print(f"\nTest {i}/{total}:")
            print(f"Input:\n{test.input_data.strip()}")

            actual, error, exec_time = self.run_program(
                program_path, test.input_data, test.time_limit
            )

            if error:
                print(f"✗ FAILED (Runtime error, {exec_time:.3f}s):")
                print(error)
                self.results.append(
                    {
                        "test": i,
                        "status": "Runtime error",
                        "error": error,
                        "time": exec_time,
                    }
                )
                continue

            diff = self.compare_outputs(actual, test.expected_output)

            if diff:
                print(f"✗ FAILED (Wrong answer, {exec_time:.3f}s):")
                print("Expected output:")
                print(test.expected_output.strip())
                print("\nActual output:")
                print(actual.strip())
                print("\nDifference:")
                print(diff)
                self.results.append(
                    {
                        "test": i,
                        "status": "Wrong answer",
                        "expected": test.expected_output,
                        "actual": actual,
                        "diff": diff,
                        "time": exec_time,
                    }
                )
            else:
                print(f"✓ PASSED ({exec_time:.3f}s)")
                passed += 1
                self.results.append({"test": i, "status": "Passed", "time": exec_time})

        print(f"\nSummary: {passed}/{total} tests passed")
        return passed == total

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







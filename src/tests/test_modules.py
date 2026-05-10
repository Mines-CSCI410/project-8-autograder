from os.path import isfile
import unittest
import os
import subprocess

from gradescope_utils.autograder_utils.decorators import weight, number

class TestBase(unittest.TestCase): 
    def runStudentCode(self, dirname, name):
        try:
            process = subprocess.run(['./run_student_code.sh', dirname], check=True, text=True, capture_output=True, timeout=30)
            if len(process.stdout.strip()) > 0:
                print(process.stdout.strip())
            if len(process.stderr.strip()) > 0:
                print(process.stderr.strip())
        except subprocess.CalledProcessError as err:
            error_message = str(err.stderr).strip()
            raise AssertionError(f'Unable to run student code on {dirname}/{name}.vm: "{error_message}"\n{err.stdout}'.strip())
        except subprocess.TimeoutExpired as err:
            raise TimeoutError(f'Student code timed out after {err.timeout} seconds:\n{str(err.stdout).strip()}')

    def assertValidAssembly(self, dirname, name):
        try:
            subprocess.run(['n2tAssembler', f'/autograder/source/{dirname}/{name}.asm'], check=True, text=True, capture_output=True, timeout=30)
        except subprocess.CalledProcessError as err:
            error_message = str(err.stderr).strip()
            raise AssertionError(f'Student\'s generated ASM is invalid, and could not be assembled: "{error_message}"\n{err.stdout}'.strip())
        except subprocess.TimeoutExpired as err:
            raise TimeoutError(f'Assembler timed out out after {err.timeout} seconds:\n{str(err.stdout).strip()}')

    def runCPUEmulator(self, dirname, name):
        try:
            subprocess.run(['n2tCPUEmulator', f'/autograder/source/{dirname}/{name}.tst'], check=True, text=True, capture_output=True, timeout=30)
        except subprocess.CalledProcessError as err:
            if os.path.isfile(f'/autograder/source/{dirname}/{name}.out'):
                diff = subprocess.check_output(['/bin/sh', '-c', f'diff /autograder/source/{dirname}/{name}.cmp /autograder/source/{dirname}/{name}.out --strip-trailing-cr ; exit 0'], text=True)
                if len(diff.strip()) != 0:
                    print(diff)

            error_message = str(err.stderr).strip()
            raise AssertionError(f'Student\'s generated ASM did not pass the provided TST file: "{error_message}"\n{err.stdout}'.strip())
        except subprocess.TimeoutExpired as err:
            raise TimeoutError(f'Emulator timed out out after {err.timeout} seconds:\n{str(err.stdout).strip()}')

    def assertFileExists(self, path):
        if not os.path.isfile(path):
            raise AssertionError(f'File "{path}" does not exist!')

    def assertCorrectTranslator(self, dirname):
        _, name = dirname.split('/')
        self.runStudentCode(dirname, name)
        self.assertFileExists(f'/autograder/source/{dirname}/{name}.asm')
        self.assertValidAssembly(dirname, name)
        self.runCPUEmulator(dirname, name)

class TestModules(TestBase): 
    @weight(47.5)
    @number(1)
    def test_fibonacci_element(self):
        self.assertCorrectTranslator('FunctionCalls/FibonacciElement')
    #
    # @weight(47.5/4)
    # @number(2)
    # def test_nested_call(self):
    #     self.assertCorrectTranslator('FunctionCalls/NestedCall')
    #
    # @weight(47.5/4)
    # @number(3)
    # def test_simple_function(self):
    #     self.assertCorrectTranslator('FunctionCalls/SimpleFunction')

    @weight(47.5)
    @number(4)
    def test_statics_test(self):
        self.assertCorrectTranslator('FunctionCalls/StaticsTest')

    # @weight(47.5/2)
    # @number(5)
    # def test_basic_loop(self):
    #     self.assertCorrectTranslator('ProgramFlow/BasicLoop')
    #
    # @weight(47.5/2)
    # @number(6)
    # def test_fibonacci_series(self):
    #     self.assertCorrectTranslator('ProgramFlow/FibonacciSeries')

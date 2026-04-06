import unittest
import subprocess

from gradescope_utils.autograder_utils.decorators import weight, number

class TestBase(unittest.TestCase): 
    def runStudentCode(self, dirname, name):
        res = subprocess.call(['./run_student_code.sh', dirname])
        if res != 0:
            raise AssertionError(f'Unable to run student\'s virtual machine translator on {name}.vm!')

    def assertValidAssembly(self, dirname, name):
        res = subprocess.call(['n2tAssembler', f'/autograder/source/{dirname}/{name}.asm'])
        if res != 0:
            raise AssertionError(f'Unable to assemble student\'s ASM output!')

    def runCPUEmulator(self, dirname, name):
        res = subprocess.call(['n2tCPUEmulator', f'/autograder/source/{dirname}/{name}.tst'])
        if res != 0:
            diff = subprocess.check_output(['/bin/sh', '-c', f'diff /autograder/source/{dirname}/{name}.cmp /autograder/source/{dirname}/{name}.out --strip-trailing-cr ; exit 0'], text=True)
            print(f'Files differ!\n{diff}')
            raise AssertionError(f'Student\'s ASM did not pass the provided TST file!')

    def assertCorrectTranslator(self, dirname):
        _, name = dirname.split('/')
        self.runStudentCode(dirname, name)
        self.assertValidAssembly(dirname, name)
        self.runCPUEmulator(dirname, name)
        subprocess.run(['mv', f'/autograder/source/{dirname}/{name}.out', '/autograder/outputs/'])

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

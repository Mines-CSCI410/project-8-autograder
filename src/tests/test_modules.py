import unittest
import subprocess

from gradescope_utils.autograder_utils.decorators import weight, number

class TestBase(unittest.TestCase): 
    def runStudentCode(self, name):
        res = subprocess.call(['./run_student_code.sh', name])
        if res != 0:
            raise AssertionError(f'Unable to run student\'s virtual machine translator on {name}.vm!')

    def assertValidAssembly(self, name):
        res = subprocess.call(['n2tAssembler', f'/autograder/source/{name}.asm'])
        if res != 0:
            raise AssertionError(f'Unable to assemble student\'s ASM output!')

    def runCPUEmulator(self, name):
        res = subprocess.call(['n2tCPUEmulator ', f'/autograder/source/{name}.tst'])
        if res != 0:
            raise AssertionError(f'Unable to run student\'s ASM on CPU emulator!')

    def assertNoDiff(self, file, expected_file):
        res = subprocess.call(['diff', file, expected_file, '-qsw', '--strip-trailing-cr'])
        if res != 0:
            raise AssertionError(f'Output does not match the expected!')

    def assertCorrectTranslator(self, name):
        self.runStudentCode(name)
        self.assertValidAssembly(name)
        self.runCPUEmulator(name)
        subprocess.run(['mv', f'/autograder/source/{name}.out' '/autograder/output/'])
        self.assertNoDiff(f'/autograder/output/{name}.out', f'/autograder/grader/tests/expected-outputs/{name}.cmp')

class TestModules(TestBase): 

import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = BASE_DIR + '\\file'
print(A)
sys.path.append(BASE_DIR)

import file
file.test.test_main
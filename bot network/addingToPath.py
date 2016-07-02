import os
import sys
print("Adding: " + os.getcwd() + " to PATH")
sys.path.append(os.getcwd())
print("PATH appended")

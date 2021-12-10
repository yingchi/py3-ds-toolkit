import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
projdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, projdir)

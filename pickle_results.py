import pickle
from lib.events import Results
import sys

sys.setrecursionlimit(50000)

results = Results()
pickle.dump(results, file = open('results/results01.pickle', 'wb'))
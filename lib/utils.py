import sys
import pickle
from .events import Results

def pickle_results(action:str, filepath:str, results:Results=None):
    # Write out pickle
    if action == 'dump':
        sys.setrecursionlimit(50000)
        if results is None:
            results = Results()
        pickle.dump(results, file = open(filepath, 'wb'))
        return
    # Read pickle
    elif action == 'load':
        results = pickle.load(open('results1.pickle', 'rb'))
        return results


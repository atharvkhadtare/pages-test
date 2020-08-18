import json
import requests
from time import time


def to_json_file(json_data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def progressBar(iterable, prefix='Progress: ', suffix='Complete', decimals=1, length=50, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    percentPerIteration = 100/float(total)
    percentCompleted = 0
    stTime = time()
    # Progress Bar Printing Function

    def printProgressBar(iteration, percentCompleted):
        percent = ("{0:." + str(decimals) + "f}").format(percentCompleted)
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        try:
            remainingTime = (time() - stTime) * float(float(total-iteration)/iteration)
        except:
            remainingTime = 0
        print('\r%s |%s| (%s / %s) (%ds left) %s%% %s' %
              (prefix, bar, iteration, total, remainingTime, percent, suffix), end=printEnd)

    # Initial Call
    printProgressBar(0, 0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1, percentCompleted)
        percentCompleted = percentCompleted + percentPerIteration
    # Print New Line on Complete
    printProgressBar(total, 100)
    print()

def download_json_data(url):
	r = requests.get(url)
	return r.json()

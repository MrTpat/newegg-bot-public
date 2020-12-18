from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printInfo(s):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(bcolors.OKCYAN + '[info] :: ' + current_time + ' :: ' + s + bcolors.ENDC)

def printSuccess(s):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(bcolors.OKGREEN + '[success] :: ' + current_time + ' :: ' + s + bcolors.ENDC)

def printFail(s):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(bcolors.FAIL + '[fail] :: ' + current_time + ' :: ' + s + bcolors.ENDC)

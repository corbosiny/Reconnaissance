import os, sys

def nmapScan(options = [" -F ", " -sV "], ip = 127.0.0.1):
    command = "namp "
    for x in options:
        command += x
    process = os.popen(command)
    results = str(process.read())
    return results

def main(options, ip):
    print(nmapScan(options, ip))

if __name__ == "__main__":
    main(sys.argv[0:len(sys.argv) - 2], sys.argv[len(sys.argv) - 1])

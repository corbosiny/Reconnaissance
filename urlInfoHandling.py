import argparse
import os
import urlib
from tld import get_tld


def getDomainName(url):
    domainName = get_tld(url)
    return domainName

def getIpAddress(url):
    osCommand = "host " + url
    process = os.popen(command)
    results = str(process.read())

    marker = results.find('has address') + 12
    return results[marker:].splitlines()[0]

def getRobots(url):
    if not url.endswith('/'):
        url += "/"

    url += "robots.txt"
    request = urlib.request.urlopen(url, data= None)
    request.encode('utf-8')

def getWhois(url):
    command = "whois " + url
    process = os.popen(command)
    results = process.read()
    
def main():
    parser = argsparse.ArgumentParser()

    parser.add_argument("-d", "--domain", help= "Enter a url to have the domain name checked", type= str)
    parser.add_argument("-i", "--ip", help= "Enter a domain name to get the ip of it", type= str)
    parser.add_argument("-r", "--robot", help= "Enter a url to recieve the robots.txt file from it", type= str)
    parser.add_argument("-w", "--whos", help= "Enter a url to have a whois check preformed", type= str)
    
    parser.parse_args();

    if parser.domain:
        print(getDomainName(parser.domain))

    if parser.ip:
        print(getIpAddress(parser.ip))

    if parser.robot:
        print(getRobots(parser.robot))

    if parser.whos:
        print(getWhois(parser.whos))
    
if __name__ == "__main__":
    main()

import argparse
from socket import *
import threading
from queue import Queue

class portScanner:


    def __init__(self, host = "127.0.0.1", lowPortNum= 0, highPortNum= 65000, output= False, fileName= None):
        self.host = host
        self.lowPort = lowPortNum #holds the lowest port it will scan up to
        self.highPort = highPortNum #holds the highest port it will scan up to
        self.output = output
        self.fileName = fileName

        self.queue = Queue()
        self.activePorts = []
    
        if self.output:
                    if fileName is None:
                        fileName = "PortScan_" + time.strftime("%d_%m_%y")

                    self.file = open(fileName, "a")
        
    def checkPort(self):
        portCon = socket(AF_INET, SOCK_STREAM)

        while True:
            portNum = 1;
            try:
                portNum = self.queue.get()

            except:
                break;

            try:
                portCon.connect((self.host, portNum))

                self.printLock.acquire()
                print("Port number:", portNum, "is open!\t")
                if fileName is not None:
                    self.file.write("Port number:", portNum, "is open!")
                self.printLock.release()
                
            except:
                pass
                        
                   

                self.printLock.release()
                pass

            finally:
                portCon.close()
                self.queue.task_done()
                    
    def scanPorts(self):
        for i in range(self.lowPort, self.highPort + 1):
                self.queue.put(i)

        threads = []
        for j in range(100):
            thread = threading.Thread(target = self.checkPort) 
            threads.append(thread)
            thread.start()
            
        self.queue.join()
            
        print("Finished Scanning ports")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--Host", help= "the ip of the host that the scanner will connect to", type = str)

    parser.add_argument("-low", "--lowPort", help= "The number of the lowest port it will start scanning at", type = int)
    parser.add_argument("-high", "--highPort", help= "The number of the highest port it will stop scanning at", type = int)

    parser.add_argument("-o", "--output", help= "Prints results to a file", action = "store_true")
    parser.add_argument("-f", "--file", help= "Designate the file name to write to", type = str)
    
    args = parser.parse_args()

    scanner = portScanner()
    scanner.scanPorts()

if __name__ == "__main__":
    main()

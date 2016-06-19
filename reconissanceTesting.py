import urlInfoHandling
import portScanner
import nmapScan
import pickle
import os


def main():
    dateFile = open("dateFile.txt", "wb")
    lastScanDate = int(pickle.load(dataFile))

    currentDate = int(time.strftime("%d"))
    
    while True:
        if currentDate - lastScanDate > 0:
            if not os.path.exist("Company Info"):
                os.makedirs("CompanyInfo")

            with file as open("CompanyList.txt", "r"):
                lines = file.readlines()

                for line in lines:
                        splitLine = " ".split(line)
                        directoryName = splitLine[0] + "Info"
                        if not os.path.exist(directoryName):
                            os.makedirs(directoryName)

                        file2 = open(os.path.join(directoryName, "urlInfo.txt"), "w")
                        
                        file2.write(getDomainName(splitLine[1]) + "\n")
                        file2.write(getIpAddress(getDomainName(splitLines[1])) + "\n")
                        file2.write(getWhois(splitLine[1]) + "\n")

                        file2.close()

                        file2 = open(os.path.join(directoryName, "Robots.txt"), "w")
                        file2.write(getRobots(splitLine[1]))

                        file2.close()

                        scanner = portScanner(getIpAddress(getDomainName(splitLines[1])), 0, 65000, True, os.path.join(directoryName, "BasicPortScanInfo.txt"))
                        scanner.scanPorts()
                        
                        file2 = open(os.path.join(directoryName, "nmapScanInfo.txt"), "w")

                        file2.write(nmapScan([" -sV ", " -r ", " -O ", " -sS ", " -sU "], getIpAddress(getDomainName(splitLines[1]))))
                        
                        file2.close()

                file.close()

            dateFile = open("dateFile.txt", "wb")
            pickle.dump(time.strftime("%d"),dateFile)
            dateFile.close()
    
if __name__ == "__main__":
    main()

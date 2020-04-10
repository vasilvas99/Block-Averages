# distutils: language = c++

from libcpp.vector cimport vector
import csv
from libc.math cimport sqrt as csrt
import matplotlib.pyplot as plt

def parseCsv(path, delim):
    if delim is None:
        delim = ","
    cdef vector[double] arr
    print("Using \'" + delim + "\' as the csv delimiter. Be careful!")
    with open(path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        for lines in csv_reader:
            try:
                arr.push_back(float(lines[0]))
            except:
                print("Could not parse value: " + str(lines[0]) + ", please check the data! (value skipped)")
                continue
    return arr

def findAllDivisors(long num):
    cdef vector[double] divList
    for i in range(2, num):
        if (num % i == 0):
            divList.push_back(i)
    return divList

def calculateBlockAverage(vector[double] data, long blockSize):
    cdef vector[double] averages
    cdef long count = 0
    cdef double sum = 0
    cdef double num = 0
    cdef long dataSize = data.size()
    for i in range(0, dataSize+1):
        if (i < dataSize):
            num = data[i]
        if (count == blockSize):
            averages.push_back(sum / blockSize)
            count = 1
            sum = num
        else:
            sum += num
            count += 1
    return averages

#since C++ maps are a huuge pain compared to python dictionaries, all vectors with names which end in DC have a zeroth element v[0] = the dict key
# it's hacky, but it works, i think
def blockAveragesPerDivisor(vector[double] data, vector[double] divisors):
    cdef long dataSize = data.size()
    cdef long divSize = divisors.size()
    cdef double div
    cdef vector[vector[double]] avgPerDivDC
    cdef vector[double] current
    cdef double blockSize

    if (divSize == 0):
        divisors=findAllDivisors(dataSize)
        divSize = divisors.size()

    for i in range(0, divSize):
         current.clear()
         blockSize = dataSize / divisors[i]
         current = calculateBlockAverage(data, blockSize)
         current.insert (current.begin(), blockSize)
         avgPerDivDC.push_back(current)
    return avgPerDivDC
#aa

def calculateMean(vector[double] data):
    cdef long dataSize = data.size()
    cdef double sum = 0.0
    for i in range(0,dataSize):
        sum += data[i]
    return sum/dataSize

def calculateStdevAndSe(vector[double] data, double mean):
    cdef long dataSize = data.size()
    cdef double sum = 0.0
    cdef vector[double] devSe
    cdef double avgMean
    for i in range(0,dataSize):
        dif = data[i]-mean
        sum += dif*dif
    avgMean = sum/(dataSize-1)
    devSe.push_back(csrt(avgMean))
    devSe.push_back(csrt(avgMean/dataSize))
    return devSe



def calculateStatistics(vector[vector[double]] avgPerSize):
    cdef long vectorLen = avgPerSize.size()
    cdef double mean
    cdef vector[double] stdevSE
    cdef vector[vector[double]] statsDCCSV
    cdef vector[double] current
    cdef double blockSize
    cdef vector[double] temp
    cdef vector[vector[double]] statsForPlot
    cdef vector[double] blockSizes
    cdef vector[double] SEs
    cdef vector[vector[double]] returnArr[2]
    for i in range(0,vectorLen):
            current = avgPerSize[i]
            blockSize = current[0]
            current.erase(current.begin())

            mean = calculateMean(current)
            stdevSE = calculateStdevAndSe(current, mean)

            temp.push_back(blockSize)
            temp.push_back(mean)
            temp.push_back(stdevSE[0])
            temp.push_back(stdevSE[1])

            statsDCCSV.push_back(temp)
            temp.clear()
            blockSizes.push_back(blockSize)
            SEs.push_back(stdevSE[1])

    statsForPlot.push_back(blockSizes)
    statsForPlot.push_back(SEs)

    returnArr[0] = statsDCCSV
    returnArr[1] = statsForPlot
    return returnArr

def plotData(data, figureName):
    if(figureName is None):
        figureName = "plot.png"
    forplot = data[1]
    plt.plot(forplot[0], forplot[1])
    plt.savefig(figureName)
    plt.show()

def generateOutputCsv(vector[vector[double]]csvData, filepath, filename):
    if(filename is None):
        filename = "output.csv"
    if (filepath is None):
        filepath = ""
    cdef double blockSize
    cdef double mean
    cdef double stdev
    cdef double se
    cdef long dataLen = csvData.size()
    with open(filepath + filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Block Size', 'Average', 'Standart Deviation', 'Standart Error'])
        for i in range(0,dataLen):
            filewriter.writerow([csvData[i][0],
                                 csvData[i][1],
                                 csvData[i][2],
                                 csvData[i][3]])





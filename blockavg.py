import csv
from statistics import variance
from math import sqrt
import matplotlib.pyplot as plt
import click
import calc
def parseCsv(path, delim=','):
    print("Using \'" + delim + "\' as the csv delimiter. Be careful!")
    arr = []
    with open(path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        for lines in csv_reader:
            try:
                arr.append(float(lines[0]))
            except:
                print("Could not parse value: " + str(lines[0]) + ", please check the data! (value skipped)")
                continue
    return arr


def findAllDivisors(num):
    divList = []
    for i in range(2, num):
        if (num % i == 0):
            divList.append(i)
    return divList


def calculateBlockAverage(data: list, blockSize: int):
    averages = []
    count = 0
    sum = 0
    num = 0
    for i in range(0, len(data) + 1):
        if (i < len(data)):
            num = data[i]
        if (count == blockSize):
            averages.append(sum / blockSize)
            count = 1
            sum = num
        else:
            sum += num
            count += 1
    return averages


def blockAveragesPerDivisor(data: list, divisors=None):
    # returns in format avgPerDiv[blockSize] = [array of block averages corresponding to that divisor]
    if divisors is None:
        divisors = findAllDivisors(len(data))
    avgPerDiv = {}
    for divisor in divisors:
        blockSize = len(data) / divisor
        avgPerDiv[blockSize] = calculateBlockAverage(data, blockSize)
    return avgPerDiv


def calculateStatistics(avgPerSize: dict):
    stats = {}  # in format (stats[blockSize] = (average, standard deviation, standart error), statsForPlotting = [[
    # block size], [se]])
    statsForPlotting = ([], [])  # format [[x vals],[y vals]]
    for blockSize in avgPerSize:
        avg = sum(avgPerSize[blockSize]) / len(avgPerSize[blockSize])
        stdev = sqrt(variance(avgPerSize[blockSize]))
        se = stdev / sqrt(len(avgPerSize[blockSize]))
        stats[blockSize] = (avg, stdev, se)
        statsForPlotting[0].append(blockSize)
        statsForPlotting[1].append(se)
    return (stats,statsForPlotting)


def plotData(data: tuple, figureName="plot.png"):
    forplot = data[1]
    plt.plot(forplot[0], forplot[1])
    plt.savefig(figureName)
    plt.show()


def generateOutputCsv(csvData: dict, filepath="", filename='output.csv'):
    with open(filepath + filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Block Size', 'Average', 'Standart Deviation', 'Standart Error'])
        for blockSize in csvData:
            filewriter.writerow([str(blockSize),
                                 str(csvData[blockSize][0]),
                                 str(csvData[blockSize][1]),
                                 str(csvData[blockSize][2])])


@click.command()
@click.argument('path')
@click.option(
    '--outputpath', '-op', default="",
    help='Specify an output path. Default: ""'
)
@click.option(
    '--outputname', '-on', default="output",
    help='Specify an output file name. Default: "output"'
)
@click.option(
    '--delimiter', '-d', default=",",
    help='Specify a delimiter. Default: ","'
)
@click.option('--plot/--no-plot', default=True,
              help='Generate (or not) the block size vs standart error plot. Default: --plot')
@click.option(
    '--plotname', '-pn', default="plot",
    help='Specify plot file name. Default: "plot"')
@click.option('--highspeed/--no-highspeed', default=False,
              help='Uses pre-compiled C++ versions of the functions that do the calculations.Not completely memory safe! Default: --no-highSpeed')
def main(path, outputpath, plot, delimiter, plotname, outputname, highspeed):
    'PATH should be a direct or a relative (to the script) path to the file (including the filename)!\n\nThis simple script deals with the problem of calculating block averages fast. Takes a single-column csv with numerical data and outputs another csv with calculated statistical parameters such as the average of the block averages, the standart deviation and the standart error of said blocks. Optinally can output a plot of the block size vs SE.'

    if(highspeed):
        data = calc.parseCsv(path, delimiter)
        statistics = calc.calculateStatistics(calc.blockAveragesPerDivisor(data,[]))
        calc.generateOutputCsv(statistics[0], outputpath, outputname + ".csv")
        if (plot):

            calc.plotData(statistics, outputpath + plotname + ".png")
        else:
            print("Plot generation turned off!")
    else:
        data = parseCsv(path, delimiter)
        statistics = calculateStatistics(blockAveragesPerDivisor(data))
        generateOutputCsv(statistics[0], outputpath, outputname + ".csv")
        if (plot):
            plotData(statistics, outputpath + plotname + ".png")
        else:
            print("Plot generation turned off!")



if __name__ == "__main__":
    main()

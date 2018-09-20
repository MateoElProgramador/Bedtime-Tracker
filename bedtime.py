import statistics as stat
import sys
import matplotlib.pyplot as plt

def getTimeValue(time):
    #time = sanitiseTime(time)   # Sanitise time first
    hour = int(time[0:2])
    minute = int(time[3:])
    timeVal = (hour * 60) + minute

    # Adds 1440 to timeVal if timeVal is 'before' noon (maintains consistent number line):
    if (timeVal < 720):
        timeVal += 1440

    #return f"Hour: {hour}, minute: {minute}, timeVal: {timeVal}"
    return timeVal

def timeValToTime(timeVal):
    # Subtract the 1440 that may have been added when converting to timeVal:
    if (timeVal >= 1440):
        timeVal -= 1440
    hour = int(timeVal // 60)
    minute = str(int(round( timeVal - (hour * 60) )))
    if (len(str(hour)) == 1):
        hour = f"0{hour}"
    if (len(minute) == 1):
        minute = f"0{minute}"
    return str(hour) + ":" + minute

def sanitiseTime(time):
    # If colon is in position 1 (second character), leading zero is prepended:
    if (time.find(":") == 1):
        time = f"0{time}"
    # If the hour is midnight, time is changed to 12 for number line reasons:
    if (time[0:2] == "12"):
        time = f"00{time[2:]}"
    return time


# TODO: Write validation function for time, so it isn't saved to file if inavlid
#def validateTime(time):


def getAverageBedtime(times):
    timeVals = list( map (getTimeValue, times) )
    print(f"TimeVals: {timeVals}")
    return stat.mean(timeVals)


def main():
    try:
        f = open("times.txt", "r")
        times = f.read().split("\n")
        f.close()
        print ("(Times file exists)")

    except IOError:
        f = open("times.txt","w")
        f.close()
        times = []
        print("(Times file created)")

    # Filters out blank lines, generated from "empty" file:
    times = [x for x in times if x != ""]

    # If new time has been entered as parameter to the program:
    if (len(sys.argv) > 1):
        newTime = sanitiseTime(sys.argv[1])
        print(f"Sanitised newTime - {newTime}")
        print (f"Hello World! Tonight's time: {newTime}")

        f = open("times.txt", "a")

        # To prevent blank first line of a new times file being part of the list:
        if (times == []):
            # Adds new time (on first line) to times.txt:
            f.write(newTime)
        else:
            # Adds new time to times.txt:
            f.write(f"\n{newTime}")

        times.append(newTime)   # Add new time to times list
        f.close()
    else:
        print ("No time entered, just peeking")

    print (times)
    if (times == []):
        print ("No times in file.")
    else:
        print (f"Average timeVal: {getAverageBedtime(times)}")
        plotBedtimes(times)


# Plots graph of bedtimes over time:
def plotBedtimes(times):
    timeVals = list( map (getTimeValue, times) )

    xTicks = []
    for i in range(1, len(timeVals)+1):
        xTicks.append(i)

    plt.xticks(xTicks)

    plt.title(f"Average time: {timeValToTime(getAverageBedtime(times))}")
    plt.plot(xTicks, timeVals)

    #print("CURRENT Y LIM: " + str(plt.ylim()))

    ylocs, _ = plt.yticks() # Gets values used as y axis

    # Creates a list of time strings converted from y axis values (list comprehension!):
    ylabels = [timeValToTime(y) for y in ylocs]

    # Despite documentation referring to an array of Text objects for labels,
    # a list of strings will serve:
    plt.yticks(ylocs, ylabels)  # Sets time labels for y axis!
    plt.show()


def filterList(list):
    print(f"List: {list}")

    # Filters out blank lines, generated from "empty" file:
    list = [x for x in list if isinstance(x, int)]

    print(f"New list: {list}")


def timeTests(times):
    for time in times:
        print(f"{time} - {getTimeValue(time)}")

main()
#timeTests(["22:00", "23:00", "00:00", "01:00", "02:00"])

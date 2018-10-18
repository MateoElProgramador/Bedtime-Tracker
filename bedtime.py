import statistics as stat
import sys
import datetime
import matplotlib.pyplot as plt

TIMES_FILENAME = "times.txt"
YTICK_OFFSET = 10

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


# TODO: Write validation function for time, so it isn't saved to file if invalid
#def validateTime(time):


def getAverageBedtime(timeVals):
    #timeVals = list( map (getTimeValue, times) )
    return stat.mean(timeVals)


def main():
    try:
        f = open(TIMES_FILENAME, "r")
        times = f.read().split("\n")
        f.close()
        print ("(Times file exists)")

    except IOError:
        f = open(TIMES_FILENAME,"w")
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

        f = open(TIMES_FILENAME, "a")

        # To prevent blank first line of a new times file being part of the list:
        if (times == []):
            # Adds new time (on first line) to times txt file:
            f.write(newTime)
        else:
            # Adds new time to times txt file:
            f.write(f"\n{newTime}")

        times.append(newTime)   # Add new time to times list
        f.close()
    else:
        print ("No time entered, just peeking")

    print ("Times:")
    for time in times:
        print(time)
    if (times == []):
        print ("No times in file.")
    else:
        plotBedtimes(times, "all")
        plotBedtimes(times, "weekly")
        plt.show()

# Plots graph of bedtimes over time:
def plotBedtimes(times, view):
    # Gets timeVals of time strings from txt file:
    timeVals = list( map (getTimeValue, times) )
    #print(f"TimeVals: {timeVals}")

    xTicks = []
    xLabels = []
    dates = []
    FIRST_DATE = datetime.date(2018, 9, 15)     # First date that bedtime is recorded

    dates.append(FIRST_DATE)
    xLabels.append(FIRST_DATE.strftime('%d/%m'))    # The first xLabel is assigned
    xTicks.append(1)    # xTicks seems to need a list of numbers of length len(timeVals)

    date = FIRST_DATE

    # date is incremented by a day and appended to xLabels and dates:
    for i in range(2, len(timeVals)+1):
        date += datetime.timedelta(days=1)  # Date is incremented by 1 day
        dates.append(date)
        xLabels.append(date.strftime('%d/%m'))
        xTicks.append(i)


    # For weekly view (since last Monday):
    # TODO Optimise reversal of list for finding last Monday
    if (view == "weekly"):
        plt.subplot(2, 1, 2)
        # Get all days for dates:
        days = [d.strftime('%A') for d in dates]
        # Find position in dates where the last Monday features:
        lastMonPos = (len(days) - 1) - (list(reversed(days)).index("Monday"))
        #print(days)
        #print("Position of last Monday: " + str(lastMonPos))

        # Slice lists to only account for since last Monday:
        xTicks = xTicks[lastMonPos:]
        xLabels = xLabels[lastMonPos:]
        timeVals = timeVals[lastMonPos:]
        print("New timeVals:")
        print(timeVals)
    else:
        plt.subplot(2, 1, 1)

    plt.xticks(xTicks, xLabels)

    plt.title(f"Average time: {timeValToTime(getAverageBedtime(timeVals))}")
    plt.plot(xTicks, timeVals)

    #print("Current y lim: " + str(plt.ylim()))

    setYTicks(timeVals)


# Finds and sets the labels for the y axis, using round times:
def setYTicks(timeVals):
    yTicks = []
    minTimeLim, maxTimeLim = plt.ylim()

    # 'Rounds down' minimum time limit to the nearest hour:
    #minTimeLim = (minTimeLim // 60) * 60       # Using the ylim already generated
    minTimeLim = ((min(timeVals) // 60) * 60) - YTICK_OFFSET     # Using the lowest timeVal data point

    print("Min time lim: " + str(minTimeLim) + " (" + str(timeValToTime(minTimeLim)) + ")")

    if (minTimeLim < getTimeValue("23:00")):
        print("Min time ytick and ylim changed")
        minTimeLim = getTimeValue("23:00") - YTICK_OFFSET



    # 'Rounds up' maximum time limit to the nearest hour:
    #maxTimeLim = (((maxTimeLim // 60)) * 60) + 60  # Using the ylim already generated
    maxTimeLim = ((max(timeVals) // 60) * 60) + 60 + YTICK_OFFSET  # Using the greatest timeVal data point

    print(f"Old ylims: {plt.ylim()}")
    plt.ylim(minTimeLim, maxTimeLim)
    print(f"New ylims: {plt.ylim()}")

    time = minTimeLim + YTICK_OFFSET
    yTicks.append(time) # First ytick value is appended to the list

    Y_AXIS_INCREMENT = 30
    # Increment by Y_AXIS_INCREMENT and set as next yTick, until greater than maximum time limit:
    while (time < (maxTimeLim - YTICK_OFFSET)):
        time += Y_AXIS_INCREMENT
        yTicks.append(time)

    # Creates a list of time strings converted from y axis values (list comprehension!):
    yLabels = [timeValToTime(y) for y in yTicks]

    # Despite documentation referring to an array of Text objects for labels,
    # a list of strings will serve:
    plt.yticks(yTicks, yLabels)  # Sets time labels for y axis!

    # Gets current axes:
    ax = plt.gca()
    # Sets tick params of y axis to display ticks and tick labels on right side as well as left:
    ax.tick_params(axis='y', right=True, labelright=True)

def correctYMinSkew(timeVals, maxTimeLim):
    minTime = min(timeVals)

    # 'Rounds down' minimum time limit to the nearest hour:
    #minTimeLim = (minTimeLim // 60) * 60       # Using the ylim already generated
    minTimeLim = (minTime // 60) * 60     # Using the lowest timeVal data point

    print("Min time lim: " + str(minTimeLim) + " (" + str(timeValToTime(minTimeLim)) + ")")

    if (minTimeLim < getTimeValue("23:00")):
        print("Min time ytick and ylim changed")
        minTimeLim = correctYMinSkew(timeVals.remove(minTime), maxTimeLim)  # Method recursively calls itself until minTimeLim >= 23:00
    else:
        plt.ylim(minTimeLim, maxTimeLim)


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

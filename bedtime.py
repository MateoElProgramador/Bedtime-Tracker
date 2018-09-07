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

def sanitiseTime (time):
    # If colon is in position 1 (second character), leading zero is prepended:
    if (time.find(":") == 1):
        time = f"0{time}"
    # If the hour is midnight, time is changed to 12 for number line reasons:
    if (time[0:2] == "12"):
        time = f"00{time[2:]}"
    return time

def getAverageBedtime(times):
    timeVals = list( map (getTimeValue, times) )
    print(f"TimeVals: {timeVals}")
    return stat.mean(timeVals)


def main():
    try:
        f = open("times.txt", "r")
        times = f.read().split("\n")
        if (times[0] == ""):
            times = []

        f.close()
        print ("(Times file exists)")
    except IOError:
        f = open("times.txt","w")
        f.close()
        times = []
        print("(Times file created)")

    # If new time has been entered as parameter to the program:
    if (len(sys.argv) > 1):
        print(f"Unsanitised newTime - {sys.argv[1]}")
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
    if (times[0] == ""):
        print ("No times in file.")
    else:
        print (f"Average timeVal: {getAverageBedtime(times)}")

    #print(sanitiseTime("1:35"))
    #print (getTimeValue("01:00"))
    print (f"Time of timeVal 0: {timeValToTime(0)}")

    timeVals = list( map (getTimeValue, times) )

    xTicks = []
    for i in range(1, len(timeVals)+1):
        xTicks.append(i)

    print(f"xTicks: {xTicks}")

    plt.title(f"Average time: {timeValToTime(getAverageBedtime(times))}")
    plt.plot(xTicks, timeVals)
    plt.yticks(timeVals, times)
    plt.show()


def timeTests(times):
    for time in times:
        print(f"{time} - {getTimeValue(time)}")

main()
#timeTests(["22:00", "23:00", "00:00", "01:00", "02:00"])

import math
import numpy as np
from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt

# Open the file with the data
f1 = open("raw5_1.txt", "r")

# Open file to write
f2 = open('sequence5_1.txt', 'w')
f3 = open('perfectchanges.txt', 'w')
f4 = open('visits5_1.txt', 'w')

# Set number of vehicles
vehicles = 5
static_nodes = 24
entries = 250
columns = 23
summa = 1

# Create an array for storing the time spend in each Static Nodes visited by each Mobile node
timestayed = np.array(range(vehicles * entries))
timestayed = timestayed.reshape(vehicles, entries)

# Create an array for storing the Static Nodes visited by each Mobile node
sequence = np.array(range(vehicles * entries))
sequence = sequence.reshape(vehicles, entries)

# Initialize the array with zeros since there won't be Static node = 0
for a in range(vehicles):
    for b in range(entries):
        timestayed[a][b] = 0
        sequence[a][b] = 0

# Create an array for storing how many differentvisits we have to each Static Node by each Mobile node
differentvisits = np.array(range(vehicles * summa))
differentvisits = differentvisits.reshape(vehicles, summa)

# Create an array with the perfect changes
perfectchanges = np.array(range(1035 * 3))
perfectchanges = perfectchanges.reshape(1035, 3)

# Initialize the array with zeros
for a in range(1035):
    for b in range(3):
        perfectchanges[a][b] = 0

# Initialize the array with zeros
for a in range(vehicles):
    for b in range(summa):
        differentvisits[a][b] = 0

# counter for perfectchanges array
perfectcounter = 0

# Check every line from CARLA output
for line in f1:

    # Input the line to data
    data = line.split()

    for y in range(1, vehicles + 1):
        # print(y)
        if int(data[0]) == y:
            if differentvisits[y - 1] == 0:
                # Store the first Static node and the first timestamp
                timestayed[y - 1][differentvisits[y - 1]] = data[1]
                # Store the first Static node and the first timestamp
                sequence[y - 1][differentvisits[y - 1]] = data[2]
                # Step
                differentvisits[y - 1] = differentvisits[y - 1] + 1
                # perfectchanges array
                perfectchanges[perfectcounter][0] = data[0]
                perfectchanges[perfectcounter][1] = data[1]
                perfectchanges[perfectcounter][2] = data[2]
                perfectcounter = perfectcounter + 1

            # Check if the next static node is different from the previous
            elif int(data[2]) != sequence[y - 1][differentvisits[y - 1] - 1]:
                # Calculate the time stayed in this Static node
                timestayed[y - 1][differentvisits[y - 1] - 1] = int(data[1]) - timestayed[y - 1][
                    differentvisits[y - 1] - 1]
                # We are using the next slot to store the previous timestamp:
                # timestayed[y-1][differentvisits[y-1]] == timestayed[y-1][differentvisits[y-1]-1] for the next loop
                timestayed[y - 1][differentvisits[y - 1]] = int(data[1])
                # Store the new Static node
                sequence[y - 1][differentvisits[y - 1]] = data[2]
                # Step
                differentvisits[y - 1] = differentvisits[y - 1] + 1
                # perfectchanges array
                perfectchanges[perfectcounter][0] = data[0]
                perfectchanges[perfectcounter][1] = data[1]
                perfectchanges[perfectcounter][2] = data[2]
                perfectcounter = perfectcounter + 1

f1.close()

# we do not want to calculate the last visit
for i in range(0, vehicles):
    differentvisits[i] = int(differentvisits[i]) - 1

# Create an array to store the sum of time stayed each mobile node to each static node
sumtimestayed = np.array(range(vehicles * static_nodes))
sumtimestayed = sumtimestayed.reshape(vehicles, static_nodes)

# Create an array to store the sum of time visited each mobile node to each static node
sumtimesvisited = np.array(range(vehicles * static_nodes))
sumtimesvisited = sumtimesvisited.reshape(vehicles, static_nodes)

# Create an array to store the average of time stayed each mobile node to each static node
averagetimestayed = np.array(range(vehicles * static_nodes))
averagetimestayed = averagetimestayed.reshape(vehicles, static_nodes)

# Create an array to store the mean of time stayed each mobile node to each static node
meantimestayed = np.array(range(vehicles * static_nodes))
meantimestayed = meantimestayed.reshape(vehicles, static_nodes)

# Create an array for storing the time spend in each Static Nodes visited by each Mobile node 1
mn1_timestayed = np.array(range(static_nodes * columns))
mn1_timestayed = mn1_timestayed.reshape(static_nodes, columns)

# Create an array for storing the time spend in each Static Nodes visited by each Mobile node 2
mn2_timestayed = np.array(range(static_nodes * columns))
mn2_timestayed = mn2_timestayed.reshape(static_nodes, columns)

# Create an array for storing the time spend in each Static Nodes visited by each Mobile node 3
mn3_timestayed = np.array(range(static_nodes * columns))
mn3_timestayed = mn3_timestayed.reshape(static_nodes, columns)

# Create an array for storing the time spend in each Static Nodes visited by each Mobile node 4
mn4_timestayed = np.array(range(static_nodes * columns))
mn4_timestayed = mn4_timestayed.reshape(static_nodes, columns)

# Create an array for storing the time spend in each Static Nodes visited by each Mobile node 5
mn5_timestayed = np.array(range(static_nodes * columns))
mn5_timestayed = mn5_timestayed.reshape(static_nodes, columns)

# Create an array to store the standard deviation of time stayed each mobile node to each static node
standarddeviationtimestayed = np.array(range(vehicles * static_nodes))
standarddeviationtimestayed = standarddeviationtimestayed.reshape(vehicles, static_nodes)

# Initialize the array with zeros
for a in range(0, vehicles):
    for b in range(0, static_nodes):
        sumtimestayed[a][b] = 0
        sumtimesvisited[a][b] = 0
        averagetimestayed[a][b] = 0
        meantimestayed[a][b] = 0
        standarddeviationtimestayed[a][b] = 0

# Calculate the sum time stayed each mobile node at each static node
for i in range(0, vehicles):
    for j in range(0, static_nodes):
        for z in range(0, int(differentvisits[i])):
            if int(sequence[i][z]) == j + 1:
                sumtimestayed[i][j] = sumtimestayed[i][j] + timestayed[i][z]
                sumtimesvisited[i][j] = sumtimesvisited[i][j] + 1

# Calculate the averagetimestayed each mobile node at each static node
for i in range(0, vehicles):
    for j in range(0, static_nodes):
        if sumtimesvisited[i][j] != 0:
            averagetimestayed[i][j] = sumtimestayed[i][j] / sumtimesvisited[i][j]

# Initialize the array with zeros since there won’t be Static node = 0
for a in range(static_nodes):
    for b in range(0, columns):
        mn1_timestayed[a][b] = 0
        mn2_timestayed[a][b] = 0
        mn3_timestayed[a][b] = 0
        mn4_timestayed[a][b] = 0
        mn5_timestayed[a][b] = 0

# Create the time sequence for each visit of each mobile node
for i in range(0, vehicles):
    for j in range(0, int(differentvisits[i])):
        for z in range(0, 2500):
            if i == 0:
                if int(mn1_timestayed[sequence[i][j] - 1][z]) == 0:
                    mn1_timestayed[sequence[i][j] - 1][z] = timestayed[i][j]
                    break
            elif i == 1:
                if int(mn2_timestayed[sequence[i][j] - 1][z]) == 0:
                    mn2_timestayed[sequence[i][j] - 1][z] = timestayed[i][j]
                    break
            elif i == 2:
                if int(mn3_timestayed[sequence[i][j] - 1][z]) == 0:
                    mn3_timestayed[sequence[i][j] - 1][z] = timestayed[i][j]
                    break
            elif i == 3:
                if int(mn4_timestayed[sequence[i][j] - 1][z]) == 0:
                    mn4_timestayed[sequence[i][j] - 1][z] = timestayed[i][j]
                    break
            elif i == 4:
                if int(mn5_timestayed[sequence[i][j] - 1][z]) == 0:
                    mn5_timestayed[sequence[i][j] - 1][z] = timestayed[i][j]
                    break

# Calculate the meantimestayed each mobile node at each static node
for i in range(0, vehicles):
    for j in range(0, static_nodes - 1):
        for z in range(0, int(sumtimesvisited[i][j])):
            if i == 0:
                meantimestayed[i][j] = meantimestayed[i][j] + (mn1_timestayed[j][z] - averagetimestayed[i][j]) ** 2
            if i == 1:
                meantimestayed[i][j] = meantimestayed[i][j] + (mn2_timestayed[j][z] - averagetimestayed[i][j]) ** 2
            if i == 2:
                meantimestayed[i][j] = meantimestayed[i][j] + (mn3_timestayed[j][z] - averagetimestayed[i][j]) ** 2
            if i == 3:
                meantimestayed[i][j] = meantimestayed[i][j] + (mn4_timestayed[j][z] - averagetimestayed[i][j]) ** 2
            if i == 4:
                meantimestayed[i][j] = meantimestayed[i][j] + (mn5_timestayed[j][z] - averagetimestayed[i][j]) ** 2

# Calculate the standarddeviationtimestayed each mobile node at each static node
for i in range(0, vehicles):
    for j in range(0, static_nodes - 1):
        if (int(sumtimesvisited[i][j]) - 1) != 0:
            standarddeviationtimestayed[i][j] = math.sqrt(
                (int(meantimestayed[i][j])) / (int(sumtimesvisited[i][j]) - 1))

# Create an array with the combination of sequence and timestayed, one array for each mobile node
comparisonrefreshrate = np.array(range(2 * 208))
comparisonrefreshrate = comparisonrefreshrate.reshape((2, 208))

# Initialize the array with zeros
for a in range(2):
    for b in range(208):
        comparisonrefreshrate[a][b] = 0

# Create an array with the combination of sequence and timestayed, one array for each mobile node
maxrefreshrate = np.array(range(2 * 84))
maxrefreshrate = maxrefreshrate.reshape((2, 84))

# Initialize the array
for a in range(2):
    for b in range(84):
        maxrefreshrate[a][b] = 50

# Create an array with the combination of sequence and timestayed, one array for each mobile node
minrefreshrate = np.array(range(2 * 838))
minrefreshrate = minrefreshrate.reshape((2, 838))

# Initialize the array
for a in range(2):
    for b in range(838):
        minrefreshrate[a][b] = 5

# Create an array with the combination of sequence and timestayed, one array for each mobile node
averagerefreshrate = np.array(range(2 * 208))
averagerefreshrate = averagerefreshrate.reshape((2, 208))

# Initialize the array with zeros
for a in range(2):
    for b in range(208):
        averagerefreshrate[a][b] = 0

# Create an array with the combination of sequence and timestayed, one array for each mobile node
standarddeviationfreshrate = np.array(range(2 * 208))
standarddeviationfreshrate = standarddeviationfreshrate.reshape((2, 208))

# Initialize the array with zeros
for a in range(2):
    for b in range(208):
        standarddeviationfreshrate[a][b] = 0

# Fill the comparisonrefreshrate
for i in range (0, 208):
    if (i ==0):
        #perfect refresh rate
        comparisonrefreshrate[0][i]=timestayed[0][i]
        #time
        comparisonrefreshrate[1][i]=timestayed[0][i]
    else:
        if (timestayed[0][i]>0 and timestayed[0][i] <= 4190):
            #perfect refresh rate
            comparisonrefreshrate[0][i]=timestayed[0][i]
            #time
            comparisonrefreshrate[1][i]=comparisonrefreshrate[1][i-1]+timestayed[0][i]

for i in range (0, 84):
    if (i == 0):
        maxrefreshrate[1][i]=maxrefreshrate[1][i]
    else:
        maxrefreshrate[1][i]=maxrefreshrate[1][i] + maxrefreshrate[1][i-1]

for i in range (0, 838):
    if (i == 0):
        minrefreshrate[1][i]=minrefreshrate[1][i]
    else:
        minrefreshrate[1][i]=minrefreshrate[1][i] + minrefreshrate[1][i-1]

# Fill the average refresh rate
for i in range (0, 208):
    if (i==0):
        #perfect refresh rate
        averagerefreshrate[0][i]=averagetimestayed[0][sequence[0][i]-1]
        #time
        averagerefreshrate[1][i]=averagetimestayed[0][sequence[0][i]-1]
    else:
        if (int(sequence[0][i]) != 0):
            #perfect refresh rate
            averagerefreshrate[0][i]=averagetimestayed[0][sequence[0][i]-1]
            #time
            averagerefreshrate[1][i]=averagerefreshrate[1][i-1]+averagetimestayed[0][sequence[0][i]-1]       

# Fill the average refresh rate
for i in range (0, 208):
    if (i==0):
        #perfect refresh rate
        standarddeviationfreshrate[0][i]=standarddeviationtimestayed[0][sequence[0][i]-1]
        #time
        standarddeviationfreshrate[1][i]=standarddeviationtimestayed[0][sequence[0][i]-1]
    else:
        if (int(sequence[0][i]+1) != 0):
            #perfect refresh rate
            standarddeviationfreshrate[0][i]=standarddeviationtimestayed[0][sequence[0][i]-1]
            #time
            standarddeviationfreshrate[1][i]=standarddeviationfreshrate[1][i-1]+standarddeviationtimestayed[0][sequence[0][i]-1] 

#print(sequence[0])
#print(comparisonrefreshrate)
#print(standarddeviationfreshrate)
#print(np.count_nonzero(comparisonrefreshrate[0]))
#print(np.count_nonzero(standarddeviationfreshrate[0]))

# ------------------------------OUTPUT/PRINT START---------------------------------------
"""
#printing the 2D-sequence
print("\nThe 2D-sequence is:")
for i in sequence:
    for j in i:
        if j !=0:
            print(j, end=" ")
    print()

#printing the 2D-timestayed
print("\nThe 2D-timestayed is:")
for i in timestayed:
    for j in i:
        if j !=0:
            print(j, end=" ")
    print()

#printing the differentvisits len(sequence[1-vehicles])
print("\nThe differentvisits are:")
for i in differentvisits:
    print(i, end=" ")
print()

print("\nThe 2D-sumtimestayed is:")
print(sumtimestayed)
print("\nThe 2D-sumtimesvisited is:")
print(sumtimesvisited)
print("\nThe 2D-averagetimestayed is:")
print(averagetimestayed)
print("\nThe meantimestayed is:")
print(meantimestayed)
print("\nThe standarddeviationtimestayed is:")
print(standarddeviationtimestayed)
print("\nThe mn1_timestayed is:")
print(mn1_timestayed)
print("\nThe mn2_timestayed is:")
print(mn2_timestayed)
print("\nThe mn3_timestayed is:")
print(mn3_timestayed)
print("\nThe mn4_timestayed is:")
print(mn4_timestayed)
print("\nThe mn5_timestayed is:")
print(mn5_timestayed)
"""

for i in range(0, vehicles):
   for j in range(0, static_nodes):
        print('%s' % (i+24) + ' %s' % (j+1) + ' %s' % averagetimestayed[i][j] + ' %s' % standarddeviationtimestayed[i][j] + ' %s' % sumtimesvisited[i][j], file=f2)

#printing the perfectchanges
for i in range(0, 1035):
    print('%s' % (perfectchanges[i][0] + 23) + ' %s' % perfectchanges[i][1] + ' %s' % perfectchanges[i][2], file=f3)

#printing the sequence
for i in sequence:
    print(' '.join(map(str, i)), file=f4)

print(comparisonrefreshrate)
print(averagerefreshrate)

# ------------------------------OUTPUT/PRINT END---------------------------------------

# ------------------------------GUI START---------------------------------------

# creates a Tk() object
master = Tk()

# sets the geometry of main
# root window
master.geometry("500x800")

label = Label(master,
              text="This is the main window")
label.pack(pady=10)

def printcomparisonrefreshrate():
    # Add Title
    plt.title("Perfect changes for Mobile node 1 -> Static node")

    # Add Axes Labels
    plt.xlabel("Total time passed")
    plt.ylabel("Beacon timing(sec)")

    plt.scatter(comparisonrefreshrate[1],comparisonrefreshrate[0], label = "Perfect", marker = 'P')
    #plt.plot(comparisonrefreshrate[1],comparisonrefreshrate[0], label = "Perfect", marker = 'P')
    #plt.plot(maxrefreshrate[1],maxrefreshrate[0], label = "Max", marker = 's')
    #plt.plot(minrefreshrate[1],minrefreshrate[0], label = "Min", marker = '*')
    #plt.plot(averagerefreshrate[1],averagerefreshrate[0], label = "Average", marker = 's')
    err=10
    plt.errorbar(standarddeviationfreshrate[1],standarddeviationfreshrate[0], label = "SD", yerr=err, fmt='o')

    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 4500, 100.0))
    plt.yticks(np.arange(0, 100, 10.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="TEST",
             command = printcomparisonrefreshrate)
btn.pack(pady = 10)

def printsequence():
    # Add Title
    plt.title("Sequence of each Mobile node -> Static node")

    # Add Axes Labels
    plt.xlabel("Timestamp")
    plt.ylabel("Static Node")
    
    plt.plot(sequence[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(sequence[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(sequence[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(sequence[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(sequence[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 250, 1.0))
    plt.yticks(np.arange(1, 25, 1.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the 2D-sequence",
             command = printsequence)
btn.pack(pady = 10)

def printtimestayed():
    # Add Title
    plt.title("Time stayed of each Mobile node -> Static node")

    # Add Axes Labels
    plt.xlabel("Number of visit")
    plt.ylabel("Time stayed")
    
    plt.plot(timestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(timestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(timestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(timestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(timestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 200, 1.0))
    plt.yticks(np.arange(1, 100, 10.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the 2D-timestayed",
             command = printtimestayed)
btn.pack(pady = 10)

def printsumtimestayed():
    # Add Title
    plt.title("Sum Time Stayed of each Mobile node/ Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Sum-Time")
    
    plt.plot(sumtimestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(sumtimestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(sumtimestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(sumtimestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(sumtimestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(50, 600, 50.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the 2D-sum time stayed",
             command = printsumtimestayed)
btn.pack(pady = 10)

def printsumtimesvisited():
    # Add Title
    plt.title("Sum Times visited of each Mobile node/ Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Visits")
    
    plt.plot(sumtimesvisited[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(sumtimesvisited[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(sumtimesvisited[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(sumtimesvisited[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(sumtimesvisited[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(0, 25, 1.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the 2D-Sum Times visited",
             command = printsumtimesvisited)
btn.pack(pady = 10)

def printaveragetimestayed():
    # Add Title
    plt.title("Average time stayed of each Mobile node / Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Time")
    
    plt.plot(averagetimestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(averagetimestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(averagetimestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(averagetimestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(averagetimestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(1, 80, 5.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the 2D-Average time stayed",
             command = printaveragetimestayed)
btn.pack(pady = 10)

def printstandarddeviationtimestayed():
    # Add Title
    plt.title("Standard deviation time stayed of each Mobile node / Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("SD")
    
    plt.plot(standarddeviationtimestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(standarddeviationtimestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(standarddeviationtimestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(standarddeviationtimestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(standarddeviationtimestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(1, 40, 5.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the 2D-Standard deviation time stayed",
             command = printstandarddeviationtimestayed)
btn.pack(pady = 10)
"""
def printmn1_timestayed():
    # Add Title
    plt.title("mn1_timestayed time stayed of  Mobile node 1 / Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Time")
    
    plt.plot(mn1_timestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn1_timestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn1_timestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn1_timestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn1_timestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(0, 80, 3.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the mn1_timestayed",
             command = printmn1_timestayed)
btn.pack(pady = 10)

def printmn2_timestayed():
    # Add Title
    plt.title("mn2_timestayed time stayed of  Mobile node 2 / Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Time")
    
    plt.plot(mn2_timestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn2_timestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn2_timestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn2_timestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn2_timestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(0, 80, 3.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the mn2_timestayed",
             command = printmn2_timestayed)
btn.pack(pady = 10)

def printmn3_timestayed():
    # Add Title
    plt.title("mn3_timestayed time stayed of  Mobile node 3 / Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Time")
    
    plt.plot(mn3_timestayed[0], label = "Mobile node 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn3_timestayed[1], label = "Mobile node 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn3_timestayed[2], label = "Mobile node 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn3_timestayed[3], label = "Mobile node 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn3_timestayed[4], label = "Mobile node 5", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(0, 80, 3.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the mn3_timestayed",
             command = printmn3_timestayed)
btn.pack(pady = 10)

def printmn4_timestayed():
    # Add Title
    plt.title("mn4_timestayed time stayed of  Mobile node 4 / Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Time")
    
    plt.plot(mn4_timestayed[0], label = "Visit 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn4_timestayed[1], label = "Visit 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn4_timestayed[2], label = "Visit 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn4_timestayed[3], label = "Visit 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn4_timestayed[4], label = "Visit 5", linestyle='dashed', marker='8', linewidth = 1)
    plt.plot(mn4_timestayed[5], label = "Visit 6", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn4_timestayed[6], label = "Visit 7", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn4_timestayed[7], label = "Visit 8", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn4_timestayed[8], label = "Visit 9", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn4_timestayed[9], label = "Visit 10", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(0, 80, 3.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the mn4_timestayed",
             command = printmn4_timestayed)
btn.pack(pady = 10)

def printmn5_timestayed():
    # Add Title
    plt.title("mn5_timestayed time stayed of  Mobile node 5/ Static node")

    # Add Axes Labels
    plt.xlabel("Static Node")
    plt.ylabel("Time")
    
    plt.plot(mn5_timestayed[0], label = "Visit 1", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn5_timestayed[1], label = "Visit 2", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn5_timestayed[2], label = "Visit 3", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn5_timestayed[3], label = "Visit 4", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn5_timestayed[4], label = "Visit 5", linestyle='dashed', marker='8', linewidth = 1)
    plt.plot(mn5_timestayed[5], label = "Visit 6", linestyle='dashed', marker='*', linewidth = 1)
    plt.plot(mn5_timestayed[6], label = "Visit 7", linestyle='dashed', marker='P', linewidth = 1)
    plt.plot(mn5_timestayed[7], label = "Visit 8", linestyle='dashed', marker='s', linewidth = 1)
    plt.plot(mn5_timestayed[8], label = "Visit 9", linestyle='dashed', marker='p', linewidth = 1)
    plt.plot(mn5_timestayed[9], label = "Visit 10", linestyle='dashed', marker='8', linewidth = 1)
    
    # show a legend on the plot
    plt.legend()
    
    # setting x and y axis range
    plt.xticks(np.arange(0, 24, 1.0))
    plt.yticks(np.arange(0, 80, 3.0))
    plt.show()

# a button widget which will open a
# new window on button click
btn = Button(master,
             text ="Click to open the mn5_timestayed",
             command = printmn5_timestayed)
btn.pack(pady = 10)
"""
# mainloop, runs infinitely to show the window
mainloop()
# ------------------------------GUI END-----------------------------------------

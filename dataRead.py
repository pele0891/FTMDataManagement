from numpy import array
import pandas as pd
import os
from graphFTM import *

def listCreation(prodName: str, date: str, timeLinetemplate: list, timeLinedates: list):
    list1 = []
    list2 = []
    #create two different lists in order to compute both scenarios of CTU being too close to the beginning date or end date
    dateInt = 0
    for index, i in enumerate(timeLinedates):
        if date == i:
            dateInt = index
    #find the numerical index of the desired CTU date

    listIndex = 0
    if dateInt < 27:
        startValue = 27 - dateInt
        #if the CTU date is going to have possible values cut off from the front of the list....
        #compute the new start index for the list to start at
        list1.insert(0, [prodName])
        listIndex = listIndex + 1
        #insert product name at the beginning of lsit
        for i in range(startValue, 27):
            list1.append(timeLinetemplate[i])
            listIndex = listIndex + 1
            #from the new start index to day 0, insert all values into the first list
        for i in range(27, 54):
            list2.insert(listIndex, timeLinetemplate[i])
            listIndex = listIndex + 1
            #from day zero to end of template list, insert into first list
        for i in range(startValue):
            list2.insert(listIndex, 0)
            listIndex = listIndex + 1
            #If there were values that were cut off in the beginning, the same corresponding amount of zeroes must be added to the end of the list
        returnList = list1 + list2
        return returnList
        #combine lists and return list
    elif dateInt > 27:
        startValue = 54 - dateInt
        #If the CTU date will have possible cut off values from the end of the list compute the new end index
        for i in range(27, dateInt):
            list1.append(timeLinetemplate[i])
            listIndex = listIndex + 1
            #since append function adds to the end of the list, append values from half to new end value to second iist
        list2.insert(0, [prodName])
        listIndex = listIndex + 1
        for i in range(startValue):
            list2.insert(listIndex, 0)
            listIndex = listIndex + 1
            #Insert function adds values after the next, add the corresponding amount of zeros to create a list of 54 values
        for i in range(0, 27):
            list2.insert(listIndex, timeLinetemplate[i])
            listIndex = listIndex + 1
            #insert values from start to day 0
        returnList = list2 + list1
        return returnList
        #return combined list
    else:
        return timeLinetemplate
        #if CTU date is day 0 return original template list

templateDates = []
#create empty list to hold all dates
userdB = pd.read_excel('productdB.xlsx', sheet_name='productdB')
timeLine = pd.read_excel('productdB.xlsx', sheet_name='dB')
#read user input product information and template information


for index, i in enumerate(timeLine.columns):
    templateDates.insert(index, i)
#insert timeline dates into an array
templateDates.insert(0, 'Product Name')

timeLinetemplate = []
index = 0
for i in timeLine.columns[0:54]:
    timeLinetemplate.insert(index, float(timeLine[i]))
    index = index + 1
#insert timeline template into an array
#note-excel cells are read as objects so must convert to float or int

df = pd.DataFrame(columns=[templateDates])
#create empty dataFrame with columns

for i in range(len(userdB.index)):
    timeLine = listCreation(userdB['Product'][i], userdB['CTU'][i], timeLinetemplate, templateDates)
    df.loc[i] = timeLine
   #for each product inputted by user, create a list 

df.to_csv('temp.csv', index=False)
temp = pd.read_csv('temp.csv')
#export to csv, because when exporting to excel, there is an error with indexing
temp.to_excel('prodData.xlsx', index = False)
os.remove('temp.csv')
#convert csv back to excel and remove temporary csv file
createGraph('prodData.xlsx', 'Sheet1')
#create graph with data

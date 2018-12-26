# My First Data Miner Program
import sys

'''
This program
a) performs data cleaning process to remove missing attribute values present in the database.
b) calculates probability of being breast cancer of an imaginary patient
   by evaluationg his/her sample results provided as command-line argument.
'''

# Starter code that reads database named 'WBC.data' and loads it into a dictionary 'dataDic'

# Reads the datafile. Note: WBC.data should be located where this file belongs.
dataFile = open('WBC.data','r').read()

# Makes data file ready to use by assigning every record to a dictionary class name dataDic.
dataDic = {i.split(',')[0]: i.split(',')[1:]  for i in dataFile.split('\n')}

# Do not alter any upper lines so that you do not get trouble in loading data file

# Performs data cleaning process, design the content and arguments depending on your design


def funDataClean():
    benign = dict()
    malignant = dict()
    changed_missing_points = []
    all_missing_points = dict()

    for d in dataDic:
        if "?" in dataDic[d]:
            all_missing_points[d] = dataDic[d]
        if "benign" in dataDic[d]:
            benign[d] = dataDic[d]
        else:
            malignant[d] = dataDic[d]

    for q in all_missing_points:

        sum_of_attr = 0
        counter = 0
        missing_attr = all_missing_points[q].index("?")

        if "benign" in all_missing_points[q]:
            for b in benign:
                if benign[b][missing_attr] != "?":
                    sum_of_attr += int(benign[b][missing_attr])
                    counter += 1
            avg = round(sum_of_attr / counter)
            dataDic[q][missing_attr] = str(avg)
            benign[q][missing_attr] = str(avg)
            changed_missing_points.append(avg)

        else:

            for m in malignant:
                if malignant[m][missing_attr] != "?":
                    sum_of_attr += int(malignant[m][missing_attr])
                    counter += 1
            avg = round(sum_of_attr / counter)
            dataDic[q][missing_attr] = str(avg)
            malignant[q][missing_attr] = str(avg)
            changed_missing_points.append(avg)

    sum_of_avg = 0
    for a in changed_missing_points:
        sum_of_avg += a

    result = sum_of_avg / len(all_missing_points)

    return dataDic, result


# Performances step-wise search in WBC database, design the content and arguments depending on your design


def performStepWiseSearch(dataDic2):

    arg_attr = []
    dataDic3 = dict()

    for j in sys.argv[1].split(","):

        if j != "?" and j != "":
            arg_attr.append(j)
        elif j == "?":
            arg_attr.append("?")
        else:
            print("Invalid command")
            exit()

    if len(arg_attr) != 9:
        print("Please run with nine commands")
        exit()

    for x in dataDic2:
        dataDic3[x] = dataDic2[x]

    for number in arg_attr:

        if number != "?":
            if ":" not in number:
                print("Invalid command")
                exit()
            attr = arg_attr.index(number)
            limit = number.split(":")[1]
            if limit == "":
                print("Invalid command")
                exit()

            for i in dataDic2:
                if i in dataDic3:
                    if number.split(":")[0] == "<":
                        if int(dataDic3[i][attr]) >= int(limit):
                            dataDic3.pop(i)
                    elif number.split(":")[0] == "<=":
                        if int(dataDic3[i][attr]) > int(limit):
                            dataDic3.pop(i)
                    elif number.split(":")[0] == ">":
                        if int(dataDic3[i][attr]) <= int(limit):
                            dataDic3.pop(i)
                    elif number.split(":")[0] == ">=":
                        if int(dataDic3[i][attr]) < int(limit):
                            dataDic3.pop(i)
                    elif number.split(":")[0] == "!=":
                        if int(dataDic3[i][attr]) == int(limit):
                            dataDic3.pop(i)
                    elif number.split(":")[0] == "=":
                        if int(dataDic3[i][attr]) != int(limit):
                            dataDic3.pop(i)
                    else:
                        print("Invalid command at", number)
                        exit()

    positive = dict()
    negative = dict()
    for j in dataDic3:
        if "malignant" in dataDic3[j]:
            positive[j] = dataDic3[j]
        else:
            negative[j] = dataDic3[j]

    return positive, negative


# 1st phase: Cleaning WBC Database
dataDic2, result = funDataClean()
print('The average of all missing values is  : ' + '{0:.4f}'.format(result))


# 2nd phase: Retrieving knowledge from WBC dataset
positive, negative = performStepWiseSearch(dataDic2)
if len(positive) and len(negative) != 0:
    probability = len(positive) / (len(positive) + len(negative))
else:
    probability = 0
print('\nTest Results:\n'
      '----------------------------------------------'
      '\nPositive (malignant) cases            : ' + str(len(positive)) +
      '\nNegative (benign) cases               : ' + str(len(negative)) +
      '\nThe probability of being positive     : ' + '{0:.4f}'.format(probability) +
      '\n----------------------------------------------')

# end of the 1.py file

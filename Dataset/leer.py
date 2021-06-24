import csv
 
with open("./DB/data.csv", newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        print(row)
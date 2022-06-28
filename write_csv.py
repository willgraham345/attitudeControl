import time
import csv
def write_csv_header(filename, headerNames):
    with open(filename, 'a') as output:
        writer = csv.writer(output)
        writer.writerow(headerNames)
def write_csv_append(filename, dataWrite):
    with open(filename, 'a') as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerow(dataWrite)
    return;


if __name__ == "__main__":
    headerNames = {"time", "frame"}
    write_csv_header('outputData.csv', headerNames)

    for i in range(0,4):
        timeVal = time.time()
        time.sleep(1)
        frame = i
        data = {timeVal, frame}
        print("data = ", data)
        print("i = ", i)
        write_csv_append('outputData.csv', data)

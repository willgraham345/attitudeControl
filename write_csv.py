import time
import csv
def init_csv(filename, headerNames):
    # Returns object you wrote with
def write_csv_header(filename, headerNames):
    with open(filename, 'a') as output:
        writer = csv.writer(output)
        writer.writerow(headerNames)
def write_csv_append(filename, dataWrite):
    with open(filename, 'a') as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerow(dataWrite)
    return;

def read_csv_lastLines(filename, n):
    data = np.array([])
    with open(filename, 'r') as file:
        for line in (file.readlines(), [-n:]):
            print(line)



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

import time
import csv

def write_csv_header(filename, headerNames):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headerNames)
def write_csv_append(filename):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
    return writer;
def read_csv_lastLines(filename, n):
    data = np.array([])
    with open(filename, 'r', newline='') as file:
        for line in (file.readlines(), [-n]):
            print(line)



if __name__ == "__main__":
    filename = 'outputData.csv'
    with open(filename, 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow({"Time", "Frame"})
        for i in range(0,15):
            timeVal = time.time()
            frame = i
            data = [timeVal, frame]
            writer.writerow(data)
            # time.sleep(.005)
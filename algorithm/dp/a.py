import os;


def main():
    dataArr = [5,3,6,4,2,1,8,7,9]
    sortArr = []        
    sortArr.append(dataArr[0])

    for index in range(1, len(dataArr)):
        if dataArr[index] > sortArr[len(sortArr)-1]:
            sortArr.append(dataArr[index])
        else:
            pos = binSearch(sortArr, dataArr[index])
            sortArr[pos] = dataArr[index]
        print(sortArr)

def binSearch (dataArr, data):
    begin = 0
    end   = len(dataArr) - 1

    while begin <= end :
        mid = (begin + end) / 2
        if dataArr[mid] < data:
            begin = mid + 1
        elif dataArr[mid] > data:
            end = mid - 1
        else:
            return mid
    return begin


if __name__ == '__main__':
    main();

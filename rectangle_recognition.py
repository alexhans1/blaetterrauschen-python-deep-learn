def findend(i, j, a, output, lookupValue):
    x = len(a)
    y = len(a[0])

    maxM = x
    maxN = y

    for m in range(i, maxM):
        # loop breaks where first non-lookupValue encounters
        if a[m][j][1] != lookupValue:
            maxM = m
            break

        for n in range(j, maxN):
            # loop breaks where first non-lookupValue encounters
            if a[m][n][1] != lookupValue:
                maxN = n
                break

    output.append(maxM-1)
    output.append(maxN-1)


def Get_rectangle(a, lookupValue):
    # retrieving the column size of array
    size_of_array = len(a)

    # output array where we are going
    # to store our output
    output = []

    for i in range(0, size_of_array):
        for j in range(0, len(a[0])):
            if a[i][j][1] == lookupValue:

                # storing initial position
                # of rectangle
                output.extend([i, j])

                # will be used for the
                # last position
                findend(i, j, a, output, lookupValue)
                return output

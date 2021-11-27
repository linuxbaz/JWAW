import datetime


def listToString(s):

    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


# Driver code
s = ['Geeks', 'for', 'Geeks']
print(listToString(s))


x = datetime.datetime.now()

print(x.year)
print(x.strftime("%Y"))
print(x.strftime("%m"))
print(x.strftime("%d"))

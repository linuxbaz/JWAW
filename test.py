import datetime


def listToString(s):

    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


# Driver code
s = ['Geeks', 'for', 'Geeks']
print(listToString(s))
my_date = datetime.date.today() + datetime.timedelta(days=1)
if datetime.date.today() < my_date:
    print(u"Wrong Date time !")

# Gregorian & Jalali ( Hijri_Shamsi , Solar ) Date Converter  Functions
# Author: JDF.SCR.IR =>> Download Full Version :  http://jdf.scr.ir/jdf
# License: GNU/LGPL _ Open Source & Free :: Version: 2.80 : [2020=1399]
# ---------------------------------------------------------------------
# 355746=361590-5844 & 361590=(30*33*365)+(30*8) & 5844=(16*365)+(16/4)
# 355666=355746-79-1 & 355668=355746-79+1 &  1595=605+990 &  605=621-16
# 990=30*33 & 12053=(365*33)+(32/4) & 36524=(365*100)+(100/4)-(100/100)
# 1461=(365*4)+(4/4)   &   146097=(365*400)+(400/4)-(400/100)+(400/400)


#convert miladi to shamsi
def gregorian_to_jalali(gy, gm, gd):
 g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
 if (gm > 2):
  gy2 = gy + 1
 else:
  gy2 = gy
 days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99)
                                                  // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
 jy = -1595 + (33 * (days // 12053))
 days %= 12053
 jy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  jy += (days - 1) // 365
  days = (days - 1) % 365
 if (days < 186):
  jm = 1 + (days // 31)
  jd = 1 + (days % 31)
 else:
  jm = 7 + ((days - 186) // 30)
  jd = 1 + ((days - 186) % 30)
 return [jy, jm, jd]


#Create Report Table Data
def to_persion_date(absent_list):
    counter = 0
    for absent_object in absent_list:
        counter += 1
        year = absent_object.absent_date.strftime('%Y')
        month = absent_object.absent_date.strftime('%m')
        day = absent_object.absent_date.strftime('%d')
        #[dd,mm,dd]
        l = gregorian_to_jalali(
            int(year), int(month), int(day))
        A = [str(x) for x in l]
        str_date = " "
        str_date = str_date.join(A)
        #Save from the first of tuple instead of second place
        if counter == 1:
            absent_tuple_info = (
             (str_date, absent_object.absent_type, absent_object.student),)
        else:
            absent_tuple_info += ((str_date,
                                  absent_object.absent_type, absent_object.student),)
    return absent_tuple_info

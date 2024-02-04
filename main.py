import easyocr
import pgeocode
import glob
from geotext import GeoText
from PIL import Image

reader = easyocr.Reader(['de', 'en'])
import cv2
import re

lst = []

filename = r"C:\Users\umaRf\OneDrive\Desktop\separated straight pics\Scan_.jpg"
pic1 = cv2.imread(filename)
rows1, cols1, _ = pic1.shape
crop1 = pic1[int((rows1) / 1.94):rows1, 0: int((cols1) / 3.2)]
cv2.imwrite('crop1.png', crop1)
pic1crop1 = cv2.imread('crop1.png')

result1 = reader.readtext(pic1crop1, detail=0)
increasingcol = 3.2
data1 = []

for i in range(0, len(result1[0])):
    # print(i, ' ', result1[0][i], ' ', 'newphoto')
    data1.append(result1[0][i])

if ('V9' in data1):
    data1.remove('V9')
if ('14' in data1):
    data1.remove('14')
if ('P3' in data1):
    data1.remove('P3')
if ('10' in data1):
    data1.remove('10')


# for i in range(0, len(data1)):
#     if(data1[i].__contains__('Vor')):
#         del data1[i]


def getname(data):
    if (data[0].__contains__('name')):  # phle maine Name kia wa tha 0711 mai Name nahe likha wa aya
        del data[0]
        print('First Name: ', data[0])
    else:
        print('First Name: ', data[0])


def getsurname(data):
    print('Surname:', data[2])
    # there is an another logic that check which index has 'vorname', cause after that surname occurs.


def getstreet(data):
    print('Street:', data[4], data[5])


zipindex = 0
from math import isnan


def getzip_city(data):
    for i in range(0, len(data)):
        zip = re.sub('\s', '', data[i])
        germanyinfo = pgeocode.Nominatim('DE')
        if (isnan(germanyinfo.query_postal_code(zip).accuracy)):
            pass
        else:
            zipindex = i
            city = data[i + 1]
            print('City: ', city)
            print('City Corrected By Logic : ', pgeocode.Nominatim('DE').query_postal_code(59069).place_name)
            print('Zip code: ', zip)
            return zipindex


streetaddress = []


def getfulladdress(data):
    for i in range(0, len(data)):
        if (data[i].__contains__('Anschrift') or data[i].__contains__(r'chift')):
            for j in range(i + 1, getzip_city(data)):
                streetaddress.append(data[j])
    # print('treet: ', streetaddress[0])
    # print('Apartment/House: ', streetaddress[1])
    print('First Line Address: ', ' '.join(streetaddress))
    streetaddress.clear()


nextcheck = []

datum = []


def getnextcheck(data):
    try:
        for i in range(0, len(data)):
            if (data[i].__contains__(r'Datu') or data[i].__contains__('Dat')):
                endingindex = i
            if (data[i].__contains__('chste HU') or data[i].__contains__('chste')):
                startingindex = i
        for i in range(startingindex + 1, endingindex):
            # print('Next Check date month:', data[i])
            nextcheck.append(data[i])
    except UnboundLocalError:
        pass
    try:
        for i in range(0, len(data)):
            if (data[i].lower().__contains__('der')):
                endingindexdatum = i
        for i in range(endingindex + 1, endingindexdatum):
            datum.append(data[i])

        actualdata = ' '.join(nextcheck)
        print('Next Check Date:    ', actualdata)
        nextcheck.clear()
        print('Date:    ', datum)
        datum.clear()
    except UnboundLocalError:
       print('Next Date algo can not be run on this picture.')



pic1 = cv2.imread(filename)
rows1, cols1, _ = pic1.shape
pic1 = pic1[0:rows1, int((cols1) / 3.3): cols1]  # 3.2

cv2.imwrite('crop1_2.png', pic1)
pic1 = cv2.imread('crop1_2.png')
result1 = reader.readtext(pic1, detail=0)

crop1_2 = []

for i in range(0, len(result1[0])):
    print(i, ' ', result1[0][i], ' ', 'crop1_2')
    crop1_2.append(result1[0][i])


def get_first_submission(data):
    listhas = ['2,1', '2.1', '12,1', '12.1', '21', '121', '2.21']

    for i in range(0, 6):  # 4 tha phle maine 6 kia
        for j in range(0, len(listhas)):
            if (data[i].__contains__(listhas[j])):
                firstsubmission = data[0: i]
                manucode = data[i + 1]
                break
    try:
        print('First submission: ', ' '.join(firstsubmission))
        print('manufacturer code: ', manucode)
    except UnboundLocalError:
        print('This algo can not run on First Submission')



def codemodel(data):
    for i in range(0, 8):  # 6 tha 8 kardia
        if (data[i].__contains__('2.2') or data[i].__contains__('12.2') or data[i].__contains__('2,2') or data[
            i].__contains__(r'2.21')):
            if len(data[i + 1]) > 5:
                if (str(data[i][0]).isalpha()):  # AND HAS ALPHANUMBERIC
                    print('Code Model 1ST ALGO: ', data[i + 1])
                    break
        elif str(data[i][0]).isalpha():
            if len(data[i]) > 5:
                print('Code Model 1ST ALGO: ', data[i])
                break


def get_vincode(data):
    for i in range(0, 25):
        if (len(data[i]) > 15):  # AND HAS ALPHANUMBERIC
            vincode = data[i]
            print('Vin Code: ', re.sub('\s', '', vincode)
                  )
            break


import re


def get_brandname(data):
    cartxt = open(r'car brands.txt')
    xx = cartxt.readlines()
    for i in range(0, 30):
        for j in range(0, len(xx)):
            if (data[i].lower() == re.sub('\n', '', xx[j].lower())):
                print('Manufacturer: ', data[i], '   ****  Corrected Name:', xx[j])


carmodel = []


def get_carmodel(data):
    listhas = ['D3', 'D.3', '8 3']  # 121 khud dala
    for i in range(0, len(data)):
        for j in range(0, len(listhas)):
            tempstr = re.sub(r'\.', '', data[i])
            abb = re.sub('\|', '', tempstr)
            if (listhas[j] == abb):
                carmodel.append(data[i + 1])
                carmodel.append(data[i + 2])
                carmodel.append(data[i + 3])
                break
            if(data[i].__contains__('D3')):
                carmodel.append(data[i + 1])
                carmodel.append(data[i + 2])
                carmodel.append(data[i + 3])
    print('Potential Car Model: ', ' '.join(carmodel))
    print('****Note: If potential car model is not accurate then I have some logic in order to make it right****')
    carmodel.clear()


capacitylist = []


def get_tankcapacity(data):
    # pipep1 , ppipie '[P1' PT
    listhas = ['P1', 'P|', 'P|', '[P1', 'PT', 'PI', 'IP1', 'Pl']

    try:
        for i in range(0, len(data)):
            for j in range(0, len(listhas)):
                tempstr = re.sub(r'\.', '', data[i])
                if (listhas[j] == tempstr):
                    Capacity = data[i + 1]
                    print('Engine Capacity, Algo 1: ', Capacity)
    except UnboundLocalError:
        print('1st algo can not run on Tank Capacity')

    for i in range(0, len(data)):
        if (data[i].lower().startswith('36w')):
                capacitylist.append(data[i: len(data)])
    try:
        print('Engine Capacity, Algo 2, Here it is the Potential Cubic Capacity ´LIST´ , so after some cleaning we might be able to grab the value: ',  capacitylist)
        capacitylist.clear()
    except UnboundLocalError:
        print('This algo can not run on Tank Capacity second except')


carpower = []


def getpower(data):
    for i in range(0, len(data)):
        if (data[i].__contains__('P2') or data[i].__contains__('P.2')):
            if (data[i + 1].__contains__('P4')):

                carpower.append(data[i + 2])
            else:
                carpower.append(data[i + 1])

    print('Car Power by Algo 1: ', ' '.join(carpower))
    carpower.clear()

    for i in range(0, len(data)):
        if (data[i].__contains__('P.4') or data[i].__contains__('P4')):
            carpower.append(data[i + 1])
    print('Car Power by Algo 2(A list which contains the value, so after some cleaning we might grab the value: ',
          ''.join(carpower))
    carpower.clear()

    for i in range(0, len(data)):
        if re.match(r'\/[0-9]+', data[i]) != None:
            carpower.append(data[i - 1])
            break

    print('Car Power by Algo 3: ', ' '.join(carpower))
    carpower.clear()

    for i in range(0, len(data)):
        if (data[i].__contains__('P2') or data[i].__contains__('P.2')):
            carpower.append(data[i + 1])
            carpower.append(data[i + 2])
            carpower.append(data[i + 3])
            carpower.append(data[i + 4])

    print('Car Power by Algo 4 (This whole list will contain the car power in it: ', ' '.join(carpower))
    carpower.clear()


def playallsecond(data):
    get_first_submission(data)
    codemodel(data)
    get_vincode(data)
    get_brandname(data)
    get_tankcapacity(data)
    get_carmodel(data)
    getpower(data)


def playallfirst(data):
    getname(data)
    getsurname(data)
    getstreet(data)
    getfulladdress(data)
    getnextcheck(data)


playallfirst(data1)
playallsecond(crop1_2)

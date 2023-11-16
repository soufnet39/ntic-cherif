# -*- coding: utf-8 -*-
# !/usr/bin/env python

# **NOTES :** good improvings have been draft in the following page.
#    http://www.developpez.net/forums/d864956/autres-langages/python-zope/general-python/ecrire-nombre-toutes-lettres

# There are three conventions used for very big numbers:
#
#    1) The first one named "everyday" is the every day convention :
# 132*10^9 = "cent-trent-deux milliards"
# 10^12 = "mille milliards"
# 124*10^6 * 10*9 = "cent-vingt-quatre millions de milliards" ... etc
#
#    2) The second convention named "chuquet", which is very easy to learn,
# is defined in the following link :
#        http://fr.wikipedia.org/wiki/Nom_des_grands_nombres#Famille_des_-llions
# For number bigger or equal to 10^60 , we use a convention similar to the first one.
#
#    3) The third convention named "rowlett" is defined here :
#        http://fr.wikipedia.org/wiki/Nom_des_grands_nombres#Syst.C3.A8me_Gillion
# For number bigger or equal to 10^90 , we use a convention similar to the first one.
#
# **NOTE :** we use to write "huit-cent-quatre" for "804".
# The dashes are used ONLY for numbers between 101 and 999.
# This is not the official convention but by doing this
# we make the groups of three digits more visible.

#import config_fr
SPECIAL_NUMBERS_NAMES = {
    '0': "Zéro",
    '1': "Un",
    '2': "Deux",
    '3': "Trois",
    '4': "Quatre",
    '5': "Cinq",
    '6': "Six",
    '7': "Sept",
    '8': "Huit",
    '9': "Neuf",

    '10': "Dix",
    '11': "Onze",
    '12': "Douze",
    '13': "Treize",
    '14': "Quatorze",
    '15': "Quinze",
    '16': "Seize",

    '20': "Vingt",
    '30': "Trente",
    '40': "Quarante",
    '50': "Cinquante",
    '60': "Soixante",
    '70': "Soixante dix",
    '80': "Quatre Vingts",
    '90': "Quatre Vingt Dix",

    '100': "Cent"
}

TEN_POWERS_NAMES = {}

# 10^3 and 10 9 are given at the end.

TEN_POWERS_NAMES['everyday'] = {
    9: "milliard"  # 10^9
}

TEN_POWERS_NAMES['chuquet'] = {
    12: "billion",  # 10^12
    18: "trillion",  # 10^18 ...
    24: "quadrillion",
    30: "quintillion",
    36: "sextillion",
    42: "septillion",
    48: "octillion",
    54: "nonillion",
    60: "decillion"
}

TEN_POWERS_NAMES['rowlett'] = {
    9: "Milliard",  # 10^9
    12: "tetrillion",  # 10^12
    15: "pentillion",  # 10^15 ...
    18: "hexillion",
    21: "eptillion",
    24: "oktillion",
    27: "ennillion",
    30: "dekillion",
    33: "hendekillion",
    36: "dodekillion",
    39: "trisdekillion",
    42: "tetradekillion",
    45: "pentadekillion",
    48: "hexadekillion",
    51: "heptadekillion",
    54: "oktadekillion",
    57: "enneadekillion",

    60: "icosillion",
    63: "icosihenillion",
    66: "icosidillion",
    69: "icositrillion",
    72: "icositetrillion",
    75: "icosipentillion",
    78: "icosihexillion",
    81: "icosiheptillion",
    84: "icosioktillion",
    87: "icosiennillion",

    90: "triacontillion"
}

for oneConvention in ['everyday', 'chuquet', 'rowlett']:
    TEN_POWERS_NAMES[oneConvention][3] = "Mille"
    TEN_POWERS_NAMES[oneConvention][6] = "Million"


SPECIAL_NUMBERS_NAMES = SPECIAL_NUMBERS_NAMES
TEN_POWERS_NAMES = TEN_POWERS_NAMES

# We add 01, 02, 03,...
for i in range(0, 10):
    SPECIAL_NUMBERS_NAMES['0' + str(i)] = SPECIAL_NUMBERS_NAMES[str(i)]

####################################
# SPECIFIC NAMES FOR FRENCH == START
#
# We add 'dix sept', 'dix huit' and 'dix neuf'.
for i in range(7, 10):
    SPECIAL_NUMBERS_NAMES['1' + str(i)] = "dix " + SPECIAL_NUMBERS_NAMES[str(i)]

# We add 'vingt-et-un', ... , 'soixante-et-un'.
for i in range(2, 7):
    SPECIAL_NUMBERS_NAMES[str(i) + '1'] = SPECIAL_NUMBERS_NAMES[str(i) + '0'] + " et un"

# We add 'soixante-et-onze'.
SPECIAL_NUMBERS_NAMES['71'] = "soixante et onze"

# We add 'deux cents', 'trois cents', ... such as
# to not treat the very boring gramatical rules.
for i in range(2, 10):
    SPECIAL_NUMBERS_NAMES[str(i) + '00'] = SPECIAL_NUMBERS_NAMES[str(i)] + " cents"

# For "trente-..." and co.
TEN_PREFIXES = {}
for i in range(2, 10):
    if i == 7:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i - 1) + '0'] + " "
    elif i == 8:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i) + '0'][:-1] + " "
    elif i == 9:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i - 1) + '0'][:-1] + " "
    else:
        TEN_PREFIXES[str(i)] = SPECIAL_NUMBERS_NAMES[str(i) + '0'] + " "

#
# SPECIFIC NAMES FOR FRENCH == END
##################################


# We build the range to build so as to split big numbers.
THE_POWERS = {}
MAX_POWER = {}
THE_BIGGER_NAME = {}

for oneConvention in TEN_POWERS_NAMES:
    # We add zero so as to facilitate the procedures.
    THE_POWERS[oneConvention] = sorted([0] + [x for x in TEN_POWERS_NAMES[oneConvention] if x != 3])
    MAX_POWER[oneConvention] = THE_POWERS[oneConvention][-1]
    THE_BIGGER_NAME[oneConvention] = TEN_POWERS_NAMES[oneConvention][THE_POWERS[oneConvention][-1]]


###############
# THE FUNCTIONS

# TODO   orderMagnitude à améliorer....
def orderMagnitude(number):
    """
    For example, 123456 becomes 123000, and 12345 becomes 12000
    """
    l = len(number) // 3
    i = len(number) - 3 * l

    if i == 0:
        i += 3
        l -= 1

    return number[:i] + '0' * l * 3


def floor(number, tenPowerPrecision=0):
    """
    This function changes the tenPowerPrecision right digits with zeros.
    """
    if type(tenPowerPrecision) != int or \
            tenPowerPrecision < 0:
        raise ValueError("""tenPowerPrecision = "' + str(tenPowerPrecision) + '" is not allowed.

tenPowerPrecision can only be equal to a natural n with 10^n is the precision needed.
""")
    number = str(number)

    if tenPowerPrecision > 0 and len(number) > tenPowerPrecision:
        number = number[:len(number) - tenPowerPrecision] + '0' * (tenPowerPrecision)

    return number


def cleanInteger(number):
    """
    None is return when the number is not an integer.
    """

    number = str(number).replace('.', '').replace(',', '')

    test = number
    for i in range(10):
        test = test.replace(str(i), '')

    if test:
        return '0'

    return number


def boringFrenchGrammaticalRuleForCENT(litteralNumber):
    if litteralNumber[-5:] == 'cents':
        litteralNumber = litteralNumber[:-1]
    return litteralNumber

def hawel(number,omla):
    try:
        idx_crnc = ['DZD', 'EUR', 'USD'].index(omla)
    except:
        idx_crnc = -1
    big_unity=['NaN', 'Dinars', 'Euros', 'Dollars'][idx_crnc + 1]
    small_unity=['NaN', 'Centimes', 'Cent', 'Cent'][idx_crnc + 1]
    if isinstance(number, float):
        vl = str(number).strip()
         
        a = vl
        b = "0"
        pos = vl.find(".")
        if (pos > -1):
            a = vl[0:pos]
            b = vl[pos + 1 :].ljust(2,'0')
         
        ret= printer(a)+ ' '+big_unity+' '
        if int(b)!=0:
            ret=ret+printer(b)+' '+small_unity

        return ret

    else:
        return printer(number)

def printer(number, checkValidity=True, convention="everyday"):
    if checkValidity:
        if convention not in TEN_POWERS_NAMES:
            raise ValueError('convention = "' + str(convention) + '" is unknown.')

        # We work with a string.
        # number = cleanInteger(number)
        if not number:
            raise ValueError('number = "' + str(number) + '" is not an integer.')

    # We have directly the name of the number.
    if number in SPECIAL_NUMBERS_NAMES:
        # We have to take care of 10*6
        answer = SPECIAL_NUMBERS_NAMES[number]

        if answer == TEN_POWERS_NAMES[convention][6]:
            answer = 'un ' + answer

        return answer

    # We have a number lower than 100.
    #
    # 0, 1, ... , 9 have been already treated.
    # 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 have been already treated.
    # 20, 21, 30, 31, ... , 70, 71, 80 and 90 have been already treated.
    if len(number) == 2:
        if number[0] in ['7', '9']:
            return TEN_PREFIXES[number[0]] + SPECIAL_NUMBERS_NAMES['1' + number[1]]
        else:
            return TEN_PREFIXES[number[0]] + SPECIAL_NUMBERS_NAMES[number[1]]

    # We have a number between 101 and 999.
    #
    # 100, 200, 300, ... , 800 and 900 has been already treated.
    # So we do not have to take care of french boring rules.
    if len(number) == 3:
        if number[0] == '0':
            hundredName = ''
        else:
            hundredName = SPECIAL_NUMBERS_NAMES['100']
            if number[0] != '1':
                hundredName = SPECIAL_NUMBERS_NAMES[number[0]] + ' ' + hundredName
            hundredName += ' '

        return hundredName + printer(number=number[1:],
                                     checkValidity=False)

    # We begin to treat number bigger than 1000.
    ten_powers_names = TEN_POWERS_NAMES[convention]

    # We have a number between 1000 and 999 999.
    #
    # We do that because later, "6 digits" is the bigger size of
    # the "intermediate" part like "77" and "124 345" in 77 124 345 000 000.
    if len(number) <= 6:
        hundredPart = printer(number=number[-3:],
                              checkValidity=False)
        # We can have 123000.
        if hundredPart == SPECIAL_NUMBERS_NAMES['0']:
            hundredPart = ''
        else:
            hundredPart = ' ' + hundredPart

        thousandPart = printer(number=number[:-3],
                               checkValidity=False)

        # We can have 000123 because of the recursive calls.
        if thousandPart == SPECIAL_NUMBERS_NAMES['0']:
            thousandPart = ''
        elif thousandPart == SPECIAL_NUMBERS_NAMES['1']:
            thousandPart = ten_powers_names[3]
        else:
            # Gramatical french boring rules for 'cent' like in 'quatre-cent mille'.
            thousandPart = boringFrenchGrammaticalRuleForCENT(thousandPart) + ' ' + ten_powers_names[3]

        return thousandPart + hundredPart


    the_powers = THE_POWERS[convention]
    max_power = MAX_POWER[convention]
    len_number = len(number)

    if len_number <= max_power:
        answer = printer(number=number[-the_powers[1]:],
                         checkValidity=False)
        # We can have ...000.
        if answer == SPECIAL_NUMBERS_NAMES['0']:
            answer = ''

        for i in range(1, len(the_powers) - 1):
            if the_powers[i] > len_number:
                break

            numberOfIntermediatePart = printer(number=number[-the_powers[i + 1]:-the_powers[i]],
                                               checkValidity=False)
            # We can have ...000...
            if numberOfIntermediatePart not in [SPECIAL_NUMBERS_NAMES['0'], '']:
                # Gramatical french boring rules for 'cent' like in 'quatre-cent millions'.
                numberOfIntermediatePart = boringFrenchGrammaticalRuleForCENT(numberOfIntermediatePart)

                if numberOfIntermediatePart == SPECIAL_NUMBERS_NAMES['1']:
                    numberOfIntermediatePart += ' ' + ten_powers_names[the_powers[i]]
                else:
                    numberOfIntermediatePart += ' ' + ten_powers_names[the_powers[i]] + 's'

                if answer:
                    answer = numberOfIntermediatePart + ' ' + answer
                else:
                    answer = numberOfIntermediatePart

        return answer


    theBiggerName = THE_BIGGER_NAME[convention]
    currentBigPartName = ''

    answer = printer(number=number[-max_power:],
                     checkValidity=False)
    number = number[:-max_power]
    # We can have ...000.
    if answer == SPECIAL_NUMBERS_NAMES['0']:
        answer = ''

    while (number):
        numberOfIntermediatePart = printer(number=number[-max_power:],
                                           checkValidity=False)
        number = number[:-max_power]

        # We can have ...000...
        if numberOfIntermediatePart not in [SPECIAL_NUMBERS_NAMES['0'], '']:
            # Gramatical french boring rules for 'cent' like in 'quatre-cent millions'.
            numberOfIntermediatePart = boringFrenchGrammaticalRuleForCENT(numberOfIntermediatePart)

            if numberOfIntermediatePart == SPECIAL_NUMBERS_NAMES['1']:
                numberOfIntermediatePart += ' ' + theBiggerName + currentBigPartName
            # We have to take care of case like "un million de milliards" = 10^12
            else:
                for onePower in ten_powers_names:
                    if onePower != 3:
                        nameToTest = ten_powers_names[onePower]
                        l = len(nameToTest)

                        if numberOfIntermediatePart[-l:] == nameToTest or \
                                numberOfIntermediatePart[-l - 1:] == nameToTest + 's':
                            numberOfIntermediatePart += ' de'
                            break

                numberOfIntermediatePart += ' ' + theBiggerName + 's' + currentBigPartName

            if answer:
                answer = numberOfIntermediatePart + ' ' + answer
            else:
                answer = numberOfIntermediatePart

        currentBigPartName += ' de ' + theBiggerName + 's'

    return answer


###############
###############
##           ##
## FOR TESTS ##
##           ##
###############
###############

if __name__ == '__main__':
    myConvention = "everyday"
    myConvention = "rowlett"
    myConvention = "chuquet"

    mytenPowerPrecision = 0
    #    mytenPowerPrecision = 3

    onlyTheOrderOfMagnitude = False
    #    onlyTheOrderOfMagnitude = True

    randomTest = True
    randomTest = False
    nMin = 0
    nMax = 10 ** 18 - 1
    nbOfTest = 5

    test = [
        4,
        400, 5000, 600000,
        107,
        80, 1080,
        91, 71,
        184, 1840, 18400, 181000,
        400567,
        "1 200 000 567",
        "123 456 789",
        "123 456 789 012 345",
        10 ** 6, 134 * 10 ** 6, 10 ** 9,

        #### mille millards
        "1000" + '0' * 9,
        #### un million de millards
        "1" + '0' * 6 + '0' * 9,
        #### deux millions de millards
        "2" + '0' * 6 + '0' * 9,
        #### sept milliards de milliards de milliards
        "7" + '0' * (9 * 4),
    ]

    if randomTest:
        import random

        nMax += 1
        test = [random.randint(nMin, nMax) for x in range(nbOfTest)]

    for oneNumber in test:
        print(str(oneNumber))

        oneNumber = str(oneNumber).strip().replace(' ', '')

        if onlyTheOrderOfMagnitude:
            oneNumber = orderMagnitude(number=oneNumber)
            print('\torder of magnitude : ' + str(oneNumber))

        elif mytenPowerPrecision:
            oneNumber = floor(number=oneNumber,
                              tenPowerPrecision=mytenPowerPrecision)
            print('\tfloor : ' + str(oneNumber))

        print('\t' + printer(number=oneNumber,
                             convention=myConvention))
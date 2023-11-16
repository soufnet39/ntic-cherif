# -*- coding: utf-8 -*-
# !/usr/bin/env python

SPECIAL_NUMBERS_NAMES = {
    '0': "zéro",
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
    '70': "Soixante-dix",
    '80': "Quatre Vingts",
    '90': "Quatre Vingt Dix",

    '100': "Cent"
}

TEN_POWERS_NAMES = {}

# 10^3 and 10 9 are given at the end.

TEN_POWERS_NAMES['everyday'] = {
    9: "Milliard"  # 10^9
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
    9: "milliard",  # 10^9
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
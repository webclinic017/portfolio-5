from enum import  Enum


'''
    ORDERS ENUMS
'''
class ORDER_TYPE(Enum):
    
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'

class PUT_CALL(Enum):

    PUT = 'PUT'
    CALL = 'CALL'


'''
    OPTION CHAIN ENUMS
'''


class OPTION_CHAIN_STRATEGY(Enum):

    SINGLE = 'SINGLE'
    ANALYTICAL = 'ANALYTICAL'
    COVERED = 'COVERED'
    VERTICAL = 'VERTICAL'
    CALENDAR = 'CALENDAR'
    STRANGLE = 'STRANGLE'
    STRADDLE = 'STRADDLE'
    BUTTERFLY = 'BUTTERFLY'
    CONDOR = 'CONDOR'
    DIAGONAL = 'DIAGONAL'
    COLLAR = 'COLLAR'
    ROLL = 'ROLL'


class OPTION_CHAIN_RANGE(Enum):

    ITM = 'ITM'
    NTM = 'NTM'
    OTM = 'OTM'
    SAK = 'SAK'
    SBK = 'SBK'
    SNK = 'SNK'
    ALL = 'ALL'


class OPTION_CHAIN_EXP_MONTH(Enum):

    ALL = 'ALL'
    JAN = 'JAN'
    FEB = 'FEB'
    MAR = 'MAR'
    APR = 'APR'
    MAY = 'MAY'
    JUN = 'JUN'
    JUL = 'JUL'
    AUG = 'AUG'
    SEP = 'SEP'
    OCT = 'OCT'
    DEC = 'DEC'


class OPTION_CHAIN_OPTION_TYPE(Enum):

    S = 'S'
    NS = 'NS'
    ALL = 'ALL'


class STREAM_ACTIVES(Enum):
    pass

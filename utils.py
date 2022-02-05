# _*_ coding: utf-8 _*_

def fmtDouble(val) -> float:
    if '-' == val:
        return 0.0
    return float(val)

def fmtDate(val: str, based_year = ''):
    if '-' == val:
        return None
    tmp = val
    nPos = val.find(' ')
    if -1 != nPos:
        tmp = val[:nPos]
    else:
        nPos = -1
        nPos = val.find('>>')
        if -1 != nPos:
            tmp = val[:nPos]
    if based_year != '':
        return based_year + '-' + tmp
    return tmp

def DateToInt(val) -> int:
    s = ''
    s = fmtDate(val)
    return int(s.replace('-', ''))

def isShiftToPriousYear(curr_val, prious_val):
    if 0 == prious_val:
        return False
    #20220202
    #如果是YYMMDD
    if curr_val / 10000000:
        d_c = int(curr_val / 10000)
        d_p = int(prious_val / 10000)
        if d_c >= d_p:
            return False
    elif curr_val <= prious_val:
        return False
    return True
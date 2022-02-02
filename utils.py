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
    d = fmtDate(val)
    nPos = d.find('-')
    if -1 != nPos:
        tmp = d[ :nPos] + d[nPos + 1:]
        return int(tmp)
    return int(d)

def isShiftToPriousYear(curr_val, prious_val):
    if 0 == prious_val:
        return False
    if curr_val <= prious_val:
        return False
    return True
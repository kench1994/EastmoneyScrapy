# _*_ coding: utf-8 _*_
import locale, csv, pymysql, time
from io import StringIO
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

QtCore.qInstallMessageHandler(lambda *args: None)
APP = None

mysql_config = {'host':'172.21.82.234',
          'port':3306,
          'user':'root',
          'passwd':'kench',
          'charset':'utf8mb4',
          'database':'Finance'
          }

def conn_to_mysql():
    #mysql连接方法
    #MySQLdb.connect()
    #postgl连接
    conn = pymysql.connect(**mysql_config)
    cur = conn.cursor()
    cur.execute("set names utf8;")
    cur.execute("SET character_set_connection=utf8;")
    return cur, conn          

class MobileBrowser(QWebEngineView):
    def __init__(self):
        QWebEngineView.__init__(self)

        self.set_trigger()
        self.dictEvnets = {}

    def set_trigger(self):
        self.urlChanged.connect(self.url_changed)
        self.loadFinished.connect(self.load_finished)

    def load(self, url: QUrl, cb = None):
        #regist callback
        self.dictEvnets[url.toString()] = cb
        #单线程阻塞操作?
        super().load(url)

    def url_changed(self, url: QUrl):
        print("start jump To %s" % url.toString())

    def onToPlainText(self, plainText):
        try:
            url = QUrl(self.url()).toString()
            cb = self.dictEvnets.pop(url)
            if cb is not None:
                cb(True, url, plainText)
            self.close()
            global APP
            APP.quit()
        except Exception as e:
            print(e)

    def load_finished(self, success):
        try:
            url = QUrl(self.url()).toString()
            if False == success:
                cb = self.dictEvnets.pop(url)
                if cb is not None:
                    cb(False, url, '')
                self.close()
                global APP
                APP.quit()
                return

            self.page().toPlainText(self.onToPlainText)            
        except Exception as e:
            print(e)

class Resultcoll():
    def Clear(self):
        self.url = ''
        self.result = ''
        self.success = False

    def Getter(self, success, url: str, plainText: str):
        self.success = success
        self.url = url
        self.result = plainText


def fetch_data(url: str, coll: Resultcoll):
    starting_up = QApplication.startingUp()

    if starting_up:
        global APP
        APP = QApplication([])
        locale.setlocale(locale.LC_TIME, 'C')

    the_browser = MobileBrowser()
    the_browser.load(QUrl(url), coll.Getter)
    APP.exec()

#TODO: put int utils
def fmtDouble(val) -> float:
    if '-' == val:
        return 0.0
    return float(val)

def fmtWithQuote(val: str):
    if val == "NULL":
        return val
    return '"' + val + '"'

def fmtDate(val: str, based_year = '') -> str:
    if '-' == val:
        return 'NULL'
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

def DateToInt(val):
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

def anslyser(plainTex: str):
    header = '股票代码,股票简称,相关资料,申购代码,发行总数(万股),网上发行(万股),顶格申购需配市值(万元),申购上限(万股),发行价格,最新价,首日收盘价,申购日期,中签号公布日,中签缴款日期,上市日期,发行市盈率,行业市盈率,中签率(%),询价累计报价,倍数,配售对象,报价家数,连续一字板数量,涨幅%,每中一签获利(元),招股说明书/意向书'
    ifs = StringIO()
    csv_writer = csv.writer(ifs)
    csv_writer.writerow(header.split(','))
    
    rows = plainTex.split("\n")
    for row in rows:
        if -1 == row.find('详细'):
            continue
        elif 0 < row.find('下一页'):
            break
        csv_writer.writerow(row.split("\t"))

    cursor, conn = conn_to_mysql()
    
    csv_reader = csv.DictReader(ifs.getvalue().split('\n'))
    ifs.close()
    prious_date = 0
    based_year_str = time.strftime('%Y')   

    for dict_row in csv_reader:
        current_date = DateToInt(dict_row['申购日期'])
        if isShiftToPriousYear(current_date, prious_date):
            based_year_str = str(DateToInt(based_year_str) - 1)
        prious_date = current_date

        sql_statement = 'INSERT INTO tblIPOStock(股票代码,申购代码,股票简称,申购上限,发行价格,首日收盘价,申购日期,中签号公布日,中签缴款日期,上市日期,发行市盈率,行业市盈率,中签率) \
            VALUES ("%s","%s","%s",%.2f,%.3f,%.3f,%s,%s,%s,%s,%f,%.2f,%f);'\
                                %(dict_row['股票代码'],\
                                dict_row['申购代码'],\
                                dict_row['股票简称'],\
                                fmtDouble(dict_row['申购上限(万股)']),\
                                fmtDouble(dict_row['发行价格']),\
                                fmtDouble(dict_row['首日收盘价']),\
                                fmtWithQuote(fmtDate(dict_row['申购日期'], based_year_str)),\
                                fmtWithQuote(fmtDate(dict_row['中签号公布日'], based_year_str)),\
                                fmtWithQuote(fmtDate(dict_row['中签缴款日期'], based_year_str)),\
                                fmtWithQuote(fmtDate(dict_row['上市日期'], based_year_str)),\
                                fmtDouble(dict_row['发行市盈率']),\
                                fmtDouble(dict_row['行业市盈率']),\
                                fmtDouble(dict_row['中签率(%)']))
        print(sql_statement)

    try:
        cursor.execute(sql_statement)
        conn.commit()
    except Exception as e:
        # 插入数据失败时, 回滚事务
        conn.rollback()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    coll = Resultcoll()
    url_list = {'https://data.eastmoney.com/xg/xg/default.html'}#, 'https://data.eastmoney.com/kzz/default.html'}
    for url in url_list:
        coll.Clear()
        fetch_data(url, coll)
        if coll.success is False:
            continue
        anslyser(coll.result)

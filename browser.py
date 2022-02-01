# _*_ coding: utf-8 _*_
import locale, csv, time, datetime
from io import StringIO
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from sqlalchemy import Column, String, Date, Float, create_engine, null
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

QtCore.qInstallMessageHandler(lambda *args: None)
APP = None

# 初始化数据库连接
engine = create_engine('mysql+pymysql://root:kench@172.21.82.234:3306/Finance?charset=utf8')
# 创建DBSession类型
DBSession = sessionmaker(bind = engine)

# 创建对象的基类
class IPOStock(declarative_base()):
    __tablename__ = 'tblIPOStock'
    股票代码 = Column(String(10), primary_key = True, nullable = False)
    申购代码 = Column(String(10), nullable = False)
    股票简称 = Column(String(10), nullable = False)
    申购上限 = Column(Float(10, 2))
    发行价格 = Column(Float(10, 2))
    首日收盘价 = Column(Float(10, 2))
    申购日期 = Column(Date, nullable = True)
    中签号公布日 = Column(Date, nullable = True)
    中签缴款日期 = Column(Date, nullable = True)
    上市日期 = Column(Date, nullable = True)
    发行市盈率 = Column(Float(10, 2))
    行业市盈率 = Column(Float(10, 2))
    中签率 = Column(Float(10, 6))



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

    # 创建session对象:
    session = DBSession()
    
    csv_reader = csv.DictReader(ifs.getvalue().split('\n'))
    ifs.close()
    prious_date = 0
    based_year_str = time.strftime('%Y')   

    for dict_row in csv_reader:
        try:
            current_date = DateToInt(dict_row['申购日期'])
            if isShiftToPriousYear(current_date, prious_date):
                based_year_str = str(DateToInt(based_year_str) - 1)
            prious_date = current_date
            qryResult = session.query(IPOStock).filter(IPOStock.股票代码 == dict_row['股票代码'])
            ipo_stock = qryResult.first()
            if not ipo_stock:
                new_ipo = IPOStock( 股票代码 = dict_row['股票代码'],\
                                    申购代码 = dict_row['申购代码'],\
                                    股票简称 = dict_row['股票简称'],\
                                    申购上限 = fmtDouble(dict_row['申购上限(万股)']),\
                                    发行价格 = fmtDouble(dict_row['发行价格']),\
                                    首日收盘价 = fmtDouble(dict_row['首日收盘价']),\
                                    申购日期 = fmtDate(dict_row['申购日期'], based_year_str),\
                                    中签号公布日 = fmtDate(dict_row['中签号公布日'], based_year_str),\
                                    中签缴款日期 = fmtDate(dict_row['中签缴款日期'], based_year_str),\
                                    上市日期 = fmtDate(dict_row['上市日期'], based_year_str),\
                                    发行市盈率 = fmtDouble(dict_row['发行市盈率']),\
                                    行业市盈率 = fmtDouble(dict_row['行业市盈率']),\
                                    中签率 = fmtDouble(dict_row['中签率(%)']))
                # 添加到session:
                session.add(new_ipo)
            else:
                ipo_stock.申购代码 = dict_row['申购代码']
                ipo_stock.股票简称 = dict_row['股票简称']
                ipo_stock.申购上限 = fmtDouble(dict_row['申购上限(万股)'])
                ipo_stock.发行价格 = fmtDouble(dict_row['发行价格'])
                ipo_stock.首日收盘价 = fmtDouble(dict_row['首日收盘价'])
                if fmtDate(dict_row['申购日期'], based_year_str):
                    ipo_stock.申购日期 = fmtDate(dict_row['申购日期'], based_year_str)
                if fmtDate(dict_row['中签号公布日'], based_year_str):
                    ipo_stock.中签号公布日 = fmtDate(dict_row['中签号公布日'], based_year_str)
                if fmtDate(dict_row['中签缴款日期'], based_year_str):
                    ipo_stock.中签缴款日期 = fmtDate(dict_row['中签缴款日期'], based_year_str)
                if fmtDate(dict_row['上市日期'], based_year_str):
                    ipo_stock.上市日期 = fmtDate(dict_row['上市日期'], based_year_str)
                ipo_stock.发行市盈率 = fmtDouble(dict_row['发行市盈率'])
                ipo_stock.行业市盈率 = fmtDouble(dict_row['行业市盈率'])
                ipo_stock.中签率 = fmtDouble(dict_row['中签率(%)'])
        except Exception as e:
            print(e)
        session.commit()
    session.close()

    


if __name__ == '__main__':
    coll = Resultcoll()
    url_list = {'https://data.eastmoney.com/xg/xg/default.html'}#, 'https://data.eastmoney.com/kzz/default.html'}
    for url in url_list:
        coll.Clear()
        fetch_data(url, coll)
        if coll.success is False:
            continue
        anslyser(coll.result)

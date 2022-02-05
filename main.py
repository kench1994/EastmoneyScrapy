# _*_ coding: utf-8 _*_
import locale, csv, time
import utils
from model import IPOCvtBond, IPOStock
from browser import ToPlaintTextBrowser
from io import StringIO
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

QtCore.qInstallMessageHandler(lambda *args: None)
APP = None

# 初始化数据库连接
engine = create_engine('mysql+pymysql://root:kench@172.29.130.85:3306/Finance?charset=utf8')
# 创建DBSession类型
DBSession = sessionmaker(bind = engine)


class ResultCollector():
    def __init__(self):
        self.url = ''
        self.result = ''
        self.success = False

    def Getter(self, success, url: str, plainText: str):
        self.success = success
        self.url = url
        self.result = plainText


def CsvMaker(plainTex: str, header: str):
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

    csv_reader = csv.DictReader(ifs.getvalue().split('\n'))
    ifs.close()
    return csv_reader

def IPOToSql(csv_reader, CModel, idPrimary, skeyPrimary, skeyDate):
    session = DBSession()

    prious_date = 0
    based_year_str = time.strftime('%Y')   

    for cv in csv_reader:
        try:
            current_date = utils.DateToInt(cv[skeyDate])
            if utils.isShiftToPriousYear(current_date, prious_date):
                based_year_str = str(utils.DateToInt(based_year_str) - 1)
            prious_date = current_date
            qryResult = session.query(CModel).filter(idPrimary == cv[skeyPrimary])
            exist_ipo = qryResult.first()
            if not exist_ipo:
                new_ipo = CModel(cv, based_year_str)
                session.add(new_ipo)
            else:
                exist_ipo = CModel(cv, based_year_str)
        except Exception as e:
             print(e)
        session.commit()
    session.close()



if __name__ == '__main__':

    if QApplication.startingUp():
        APP = QApplication([])
        locale.setlocale(locale.LC_TIME, 'C')

    the_browser = ToPlaintTextBrowser()

    url_list = {'https://data.eastmoney.com/xg/xg/default.html', 'https://data.eastmoney.com/kzz'}
    collection = []
    for url in url_list:
        collect = ResultCollector()
        collection.append(collect)
        the_browser.load(url, collect.Getter)


    APP.exec()

    if len(url_list) == len(collection):
        cvt_collect = collection.pop()
        if cvt_collect.success:
            csvReader = CsvMaker(cvt_collect.result, '债券代码,债券简称,相关,申购日期,申购代码,申购上限(万元),正股代码,正股简称,正股价,转股价,转股价值,债现价,转股溢价率,股权登记日,每股配售额,发行规模(亿元),中签号发布日,中签率(%),上市时间')
            IPOToSql(csvReader, IPOCvtBond, IPOCvtBond.债券代码, "债券代码", "申购日期")

        stock_collect = collection.pop()
        if stock_collect.success:
            csvReader = CsvMaker(stock_collect.result, '股票代码,股票简称,相关资料,申购代码,发行总数(万股),网上发行(万股),顶格申购需配市值(万元),申购上限(万股),发行价格,最新价,首日收盘价,申购日期,中签号公布日,中签缴款日期,上市日期,发行市盈率,行业市盈率,中签率(%),询价累计报价,倍数,配售对象,报价家数,连续一字板数量,涨幅%,每中一签获利(元),招股说明书/意向书')
            IPOToSql(csvReader, IPOStock, IPOStock.股票代码, "股票代码", "申购日期")



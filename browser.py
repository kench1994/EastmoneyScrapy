# _*_ coding: utf-8 _*_
import locale, csv
from io import StringIO
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

QtCore.qInstallMessageHandler(lambda *args: None)

APP = None


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

def anslyser(plainTex: str):
    header = '股票代码,股票简称,相关资料,申购代码,发行总数(万股),网上发行(万股),顶格申购需配市值(万元),申购上限(万股),发行价格,最新价,首日收盘价,申购日期 ,中签号公布日,中签缴款日期,上市日期,发行市盈率,行业市盈率,中签率(%),询价累计报价,倍数,配售对象,报价家数,连续一字板数量,涨幅%,每中一签获利(元),招股说明书/意向书'
    
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
    for dict_row in csv_reader:
       print(dict_row['股票代码'])

    ifs.close()


if __name__ == '__main__':
    coll = Resultcoll()
    url_list = {'https://data.eastmoney.com/xg/xg/default.html'}#, 'https://data.eastmoney.com/kzz/default.html'}
    for url in url_list:
        coll.Clear()
        fetch_data(url, coll)
        if coll.success is False:
            continue
        anslyser(coll.result)

# _*_ coding: utf-8 _*_
from ast import Global
from glob import glob
from http.client import NO_CONTENT
import locale, functools, threading, time
from sys import platlibdir
from tkinter.messagebox import NO
#import urllib.parse
import urllib.request
from xmlrpc.client import Boolean
#from http.cookies import SimpleCookie
#from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl#, QTimer
#from PyQt5.QtGui import QIcon
#from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
#from requests.cookies import RequestsCookieJar


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

class ResultCollector():
    def Clear(self):
        self.url = ''
        self.result = ''
        self.success = False

    def Getter(self, success: Boolean, url: str, plainText: str):
        self.succcess = success
        self.url = url
        self.result = plainText


def fetch_data(url: str, collector: ResultCollector):
    starting_up = QApplication.startingUp()

    if starting_up:
        global APP
        APP = QApplication([])
        locale.setlocale(locale.LC_TIME, 'C')

    the_browser = MobileBrowser()
    the_browser.load(QUrl(url), collector.Getter)
    APP.exec()

if __name__ == '__main__':
    collector = ResultCollector()
    url_list = {'https://data.eastmoney.com/xg/xg/default.html', 'https://data.eastmoney.com/kzz/default.html'}
    for url in url_list:
        collector.Clear()
        fetch_data(url, collector)
        print(collector.result)

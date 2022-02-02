from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class ToPlaintTextBrowser(QWebEngineView):
    def __init__(self):
        QWebEngineView.__init__(self)

        self.set_trigger()
        self.dictEvnets = {}

    def set_trigger(self):
        self.urlChanged.connect(self.url_changed)
        self.loadFinished.connect(self.load_finished)

    def load(self, url, cb = None):
        self.dictEvnets[url] = cb
        if 1 == len(self.dictEvnets):
            super().load(QUrl(url))

    def url_changed(self, url: QUrl):
        print("start jump To %s" % url.toString())

    #True 触发下个任务, False 任务列表空
    def next(self):
        remain_tasks = self.dictEvnets.keys()
        if 0 == len(remain_tasks):
            super().close()
            return False
        #get next target
        next_key = next(iter(remain_tasks))
        super().load(QUrl(next_key))
        return True

    #TODO:Thread safe
    def onToPlainText(self, plainText):
        try:
            url = self.url().toString()
            cb = self.dictEvnets.pop(url)
            if cb is not None:
                cb(True, url, plainText)
            
            self.next()
        except Exception as e:
            print(e)


    def load_finished(self, success):
        try:
            url = self.url().toString()
            print("page %s load finished" % url)
            if False == success:
                cb = self.dictEvnets.pop(url)
                if cb is not None:
                    cb(False, url, '')
                self.next()
                return
            self.page().toPlainText(self.onToPlainText)            
        except Exception as e:
            print(e)

import utils
from sqlalchemy import Column, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类
class IPOStock(declarative_base()):

    def __init__(self, dict, based_year_str: str) -> None:
        super().__init__()
        self.股票代码 = dict['股票代码']
        self.申购代码 = dict['申购代码']
        self.股票简称 = dict['股票简称']
        self.申购上限 = utils.fmtDouble(dict['申购上限(万股)'])
        self.发行价格 = utils.fmtDouble(dict['发行价格'])
        self.首日收盘价 = utils.fmtDouble(dict['首日收盘价'])
        self.申购日期 = utils.fmtDate(dict['申购日期'], based_year_str)
        self.中签号公布日 = utils.fmtDate(dict['中签号公布日'], based_year_str)
        self.中签缴款日期 = utils.fmtDate(dict['中签缴款日期'], based_year_str)
        self.上市日期 = utils.fmtDate(dict['上市日期'], based_year_str)
        self.发行市盈率 = utils.fmtDouble(dict['发行市盈率'])
        self.行业市盈率 = utils.fmtDouble(dict['行业市盈率'])
        self.中签率 = utils.fmtDouble(dict['中签率(%)'])

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
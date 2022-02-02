CREATE TABLE IF NOT EXISTS `tblIPOStock`(
   `股票代码` CHAR(10) NOT NULL,
   `申购代码` CHAR(10) NOT NULL,
   `股票简称` CHAR(10) NOT NULL,
   `申购上限` DOUBLE comment '万股',
   `发行价格` DOUBLE,
   `首日收盘价` DOUBLE,
   `申购日期` DATE DEFAULT NULL,
   `中签号公布日` DATE DEFAULT NULL,
   `中签缴款日期` DATE DEFAULT NULL,
   `上市日期` DATE DEFAULT NULL,
   `发行市盈率` DOUBLE,
   `行业市盈率` DOUBLE,
   `中签率` DOUBLE comment '%',
   PRIMARY KEY ( `股票代码` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
# 东方财富数据中心爬虫
选型上直接使用pyqt的webengine
不需要解析js动态加载或者折腾chrome driver的配套环境
数据清洗落地上还未进行太多重构,需要后面进一步解耦

```
mysql> SELECT * FROM `Finance`.`tblIPOStock` LIMIT 0,1000;
+----------+----------+----------+----------+----------+------------+------------+--------------+--------------+------------+------------+------------+----------+
| 股票代码 | 申购代码 | 股票简称 | 申购上限 | 发行价格 | 首日收盘价 | 申购日期   | 中签号公布日 | 中签缴款日期 | 上市日期   | 发行市盈率 | 行业市盈率 | 中签率   |
+----------+----------+----------+----------+----------+------------+------------+--------------+--------------+------------+------------+------------+----------+
| 001227   | 001227   | 兰州银行 |    17.05 |     3.57 |       5.14 | 2022-01-05 | 2022-01-07   | 2022-01-07   | 2022-01-17 |      22.97 |        6.1 |  0.13546 |
| 001234   | 001234   | 泰慕士   |     1.05 |    16.53 |       23.8 | 2021-12-29 | 2021-12-31   | 2021-12-31   | 2021-01-11 |      22.99 |      15.74 | 0.019874 |
| 001313   | 001313   | 粤海饲料 |        3 |     5.38 |          0 | 2022-01-27 | 2022-02-07   | 2022-02-07   | NULL       |      22.96 |      30.44 | 0.048365 |
| 300834   | 300834   | 星辉环材 |     1.35 |    55.57 |       50.5 | 2022-01-04 | 2022-01-06   | 2022-01-06   | 2022-01-13 |      49.48 |      44.79 | 0.018562 |
| 301106   | 301106   | 骏成科技 |      1.8 |    37.75 |      43.64 | 2022-01-18 | 2022-01-20   | 2022-01-20   | 2022-01-28 |      42.61 |      49.39 | 0.012177 |
| 301116   | 301116   | 益客食品 |     0.75 |     11.4 |      35.62 | 2022-01-06 | 2022-01-10   | 2022-01-10   | 2022-01-18 |      41.01 |      29.93 | 0.020086 |
| 301117   | 301117   | 佳缘科技 |     0.55 |     46.8 |      81.99 | 2022-01-05 | 2022-01-07   | 2022-01-07   | 2022-01-17 |      82.01 |      61.11 | 0.015804 |
| 301122   | 301122   | 采纳股份 |     0.65 |    50.31 |      72.46 | 2022-01-17 | 2022-01-19   | 2022-01-19   | 2022-01-26 |      83.85 |       42.2 | 0.016571 |
| 301123   | 301123   | 奕东电子 |     1.45 |    37.23 |      49.33 | 2022-01-12 | 2022-01-14   | 2022-01-14   | 2022-01-25 |      50.74 |      49.88 | 0.020183 |
| 301127   | 301127   | 天源环保 |      1.9 |    12.03 |      23.27 | 2021-12-21 | 2021-12-23   | 2021-12-23   | 2021-12-30 |      34.53 |       24.8 | 0.025161 |
| 301130   | 301130   | 西点药业 |     0.55 |        0 |          0 | 2022-02-14 | 2022-02-16   | 2022-02-16   | NULL       |          0 |       38.6 |        0 |
| 301136   | 301136   | 招标股份 |     1.65 |    10.52 |         24 | 2021-12-29 | 2021-12-31   | 2021-12-31   | 2021-01-11 |      36.74 |      32.88 | 0.019906 |
| 301158   | 301158   | 德石股份 |     1.05 |    15.64 |      26.59 | 2022-01-05 | 2022-01-07   | 2022-01-07   | 2022-01-17 |      41.62 |         43 | 0.017174 |
| 301159   | 301159   | 三维天地 |      1.9 |    30.28 |       60.1 | 2021-12-27 | 2021-12-29   | 2021-12-29   | 2021-01-07 |      44.81 |      61.03 |  0.01223 |
| 301181   | 301181   | 标榜股份 |      0.6 |        0 |          0 | 2022-02-09 | 2022-02-11   | 2022-02-11   | NULL       |          0 |      33.07 |        0 |
| 301189   | 301189   | 奥尼电子 |     0.85 |    66.18 |      58.19 | 2021-12-17 | 2021-12-21   | 2021-12-21   | 2021-12-28 |      40.18 |      49.66 | 0.016656 |
| 301196   | 301196   | 唯科科技 |     0.85 |    64.08 |      60.19 | 2021-12-30 | 2021-01-04   | 2021-01-04   | 2021-01-11 |      58.79 |      27.87 | 0.017648 |
| 301200   | 301200   | 大族数控 |     0.75 |        0 |          0 | 2022-02-16 | 2022-02-18   | 2022-02-18   | NULL       |          0 |      40.19 |        0 |
| 301201   | 301201   | 诚达药业 |      0.6 |    72.69 |     128.55 | 2022-01-10 | 2022-01-12   | 2022-01-12   | 2022-01-20 |       83.1 |       38.9 | 0.017114 |
| 301206   | 301206   | 三元生物 |     0.95 |    109.3 |          0 | 2022-01-24 | 2022-01-26   | 2022-01-26   | NULL       |      63.39 |      43.85 | 0.019064 |
| 301207   | 301207   | 华兰疫苗 |     0.65 |        0 |          0 | 2022-02-08 | 2022-02-10   | 2022-02-10   | NULL       |          0 |      39.05 |        0 |
| 301217   | 301217   | 铜冠铜箔 |      3.5 |    17.27 |       21.7 | 2022-01-18 | 2022-01-20   | 2022-01-20   | 2022-01-27 |     249.03 |      49.39 | 0.036135 |
| 301228   | 301228   | 实朴检测 |     0.75 |    20.08 |      36.45 | 2022-01-19 | 2022-01-21   | 2022-01-21   | 2022-01-28 |      56.42 |      33.66 | 0.016867 |
| 301235   | 301235   | 华康医疗 |     0.65 |     39.3 |      46.62 | 2022-01-19 | 2022-01-21   | 2022-01-21   | 2022-01-28 |      81.56 |      33.73 | 0.017224 |
| 600941   | 730941   | 中国移动 |     25.3 |    57.58 |      57.88 | 2021-12-22 | 2021-12-24   | 2021-12-24   | 2021-01-05 |      12.02 |      22.78 | 0.124119 |
| 603102   | 732102   | 百合股份 |      1.6 |    42.14 |      60.68 | 2022-01-14 | 2022-01-18   | 2022-01-18   | 2022-01-25 |      22.99 |       44.2 | 0.013218 |
| 603122   | 732122   | 合富中国 |      3.9 |     4.19 |          0 | 2022-02-07 | 2022-02-09   | 2022-02-09   | NULL       |      22.99 |      18.74 |        0 |
| 603132   | 732132   | 金徽股份 |      2.9 |     10.8 |          0 | 2022-02-11 | 2022-02-15   | 2022-02-15   | NULL       |      22.98 |       45.8 |        0 |
| 603150   | 732150   | 万朗磁塑 |      0.8 |    34.19 |      49.23 | 2022-01-13 | 2022-01-17   | 2022-01-17   | 2022-01-24 |      22.02 |      27.64 | 0.023921 |
| 603176   | 732176   | 汇通集团 |      3.4 |      1.7 |       2.45 | 2021-12-22 | 2021-12-24   | 2021-12-24   | 2021-12-31 |       8.24 |       8.27 |  0.05122 |
| 603215   | 732215   | 比依股份 |      1.8 |     12.5 |          0 | 2022-02-09 | 2022-02-11   | 2022-02-11   | NULL       |      22.98 |      47.06 |        0 |
| 688062   | 787062   | 迈威生物 |     1.65 |     34.8 |       24.5 | 2022-01-04 | 2022-01-06   | 2022-01-06   | 2022-01-18 |          0 |      38.73 | 0.035927 |
| 688171   | 787171   | 纬德信息 |     0.55 |    28.68 |      35.44 | 2022-01-18 | 2022-01-20   | 2022-01-20   | 2022-01-27 |      45.52 |      61.14 | 0.027682 |
| 688173   | 787173   | 希荻微   |      0.6 |    33.57 |      44.05 | 2022-01-11 | 2022-01-13   | 2022-01-13   | 2022-01-21 |          0 |      61.25 | 0.033115 |
| 688176   | 787176   | 亚虹医药 |     2.05 |    22.98 |       17.6 | 2021-12-27 | 2021-12-29   | 2021-12-29   | 2021-01-07 |          0 |      38.63 | 0.035244 |
| 688220   | 787220   | 翱捷科技 |     0.65 |   164.54 |        109 | 2022-01-04 | 2022-01-06   | 2022-01-06   | 2022-01-14 |          0 |      49.88 | 0.032396 |
| 688223   | 787223   | 晶科能源 |       28 |        5 |      10.55 | 2022-01-17 | 2022-01-19   | 2022-01-19   | 2022-01-26 |       54.9 |       48.8 | 0.149621 |
| 688225   | 787225   | 亚信安全 |     0.65 |    30.51 |          0 | 2022-01-24 | 2022-01-26   | 2022-01-26   | NULL       |      87.17 |      61.19 | 0.033392 |
| 688227   | 787227   | 品高股份 |      0.7 |    37.09 |      32.82 | 2021-12-21 | 2021-12-23   | 2021-12-23   | 2021-12-30 |     111.34 |      60.86 | 0.026936 |
| 688234   | 787234   | 天岳先进 |     0.65 |    82.79 |       85.5 | 2021-12-31 | 2021-01-05   | 2021-01-05   | 2021-01-12 |          0 |      49.86 | 0.033472 |
| 688236   | 787236   | 春立医疗 |     0.95 |    29.81 |      28.62 | 2021-12-21 | 2021-12-23   | 2021-12-23   | 2021-12-30 |      41.41 |      43.38 | 0.026934 |
| 688259   | 787259   | 创耀科技 |      0.5 |     66.6 |      88.15 | 2021-12-31 | 2021-01-05   | 2021-01-05   | 2021-01-12 |      83.65 |      61.11 | 0.027353 |
| 688261   | 787261   | 东微半导 |      0.4 |      130 |          0 | 2022-01-24 | 2022-01-26   | 2022-01-26   | NULL       |      429.3 |      49.01 | 0.031973 |
| 688262   | 787262   | 国芯科技 |      1.5 |    41.98 |      46.72 | 2021-12-24 | 2021-12-28   | 2021-12-28   | 2021-01-06 |     418.95 |      60.99 | 0.030726 |
| 688265   | 787265   | 南模生物 |     0.45 |    84.62 |      69.37 | 2021-12-17 | 2021-12-21   | 2021-12-21   | 2021-12-28 |     201.59 |        100 | 0.030901 |
| 688267   | 787267   | 中触媒   |      1.1 |     41.9 |          0 | 2022-02-07 | 2022-02-09   | 2022-02-09   | NULL       |      85.98 |      42.78 |        0 |
| 688270   | 787270   | 臻镭科技 |     0.65 |    61.88 |       56.2 | 2022-01-18 | 2022-01-20   | 2022-01-20   | 2022-01-27 |      92.63 |      49.39 |  0.03015 |
| 688283   | 787283   | 坤恒顺维 |      0.5 |     33.8 |          0 | 2022-01-28 | 2022-02-08   | 2022-02-08   | NULL       |      64.83 |      38.98 |        0 |
| 870204   | 889888   | 沪江材料 |    39.11 |    18.68 |      30.59 | 2022-01-04 | NULL         | NULL         | 2022-01-18 |      18.45 |          0 |        0 |
| 871245   | 889688   | 威博液压 |    40.27 |     9.68 |         26 | 2021-12-22 | NULL         | NULL         | 2021-01-06 |      18.59 |          0 |        0 |
```
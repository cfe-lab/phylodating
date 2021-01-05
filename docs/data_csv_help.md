A comma separated file containing the estimated dates. The columns included are:

1. `ID` - the sequence ID.
2. `Date` - collection date in the format yyyy-mm-dd, as indicated in the user input file
3. `Query` - `0` if the sequence is used to calibrate the linear regression, and `1` otherwise, as indicated in the user input file
4. `EstimatedDate` - estimated date in the format yyyy-mm-dd.
5. `EstimatedDate95Low` - lower bound of the 95% confidence interval of the estimated date in the format yyyy-mm-dd.
6. `EstimatedDate95High` - upper bound of the 95% confidence interval of the estimated date in the format yyyy-mm-dd.

Example:
```
"ID","Date","Query","EstimatedDate","EstimatedDate95Low","EstimatedDate95High"
"DNA1","2018-09-05",1,"2011-07-28","2010-02-19","2013-01-02"
"DNA3","2018-09-05",1,"2011-08-18","2010-03-14","2013-01-21"
"DNA2","2018-09-05",1,"2012-08-02","2011-03-22","2013-12-15"
"DNA4","2018-09-05",1,"2015-07-08","2013-12-21","2017-01-23"
"RNA1","2011-03-08",0,"2010-12-16","2009-06-15","2012-06-18"
"RNA2","2011-03-08",0,"2011-09-20","2010-04-19","2013-02-20"
"RNA5","2012-11-05",0,"2012-10-29","2011-06-20","2014-03-11"
"RNA3","2012-11-05",0,"2012-04-06","2010-11-18","2013-08-24"
"RNA4","2012-11-05",0,"2012-12-01","2011-07-23","2014-04-12"
"RNA6","2015-05-07",0,"2014-12-10","2013-06-21","2016-05-30"
"RNA7","2015-05-07",0,"2015-12-17","2014-05-06","2017-07-28"
```

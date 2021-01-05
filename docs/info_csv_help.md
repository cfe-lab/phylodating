A comma separated file containing information on each sequence in the phylogeny. The file must have at least three columns labeled and described as follows:

1. `ID` - the sequence IDs exactly matching the tip labels of the unrooted tree.
2. `Date` - collection date in the format yyyy-mm-dd (e.g. 2018-09-18).
3. `Query` - `0` if the sequence is to be used to calibrate the linear regression, and `1` otherwise. Usually, pre-therapy plasma HIV sequences are coded as `0` and HIV reservoir sequences are coded as `1`.

\* Note that collection date is required for all sequences if you wish to generate the divergence versus time plot

Please ensure that input files DO NOT contain any personally identifying information

Example:
```
ID,Date,Query
RNA1,2011-03-08,0
RNA2,2011-03-08,0
RNA3,2012-11-05,0
RNA4,2012-11-05,0
RNA5,2012-11-05,0
RNA6,2015-05-07,0
RNA7,2015-05-07,0
DNA1,2018-09-05,1
DNA2,2018-09-05,1
DNA3,2018-09-05,1
DNA4,2018-09-05,1
```

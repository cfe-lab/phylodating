A comma separated file containing information on each sequence in the phylogeny. The file must have at least three columns labeled and described as follows:

1. `ID` - the sequence IDs, exactly matching the tip labels of the unrooted tree.
2. `Date` - collection date in the format yyyy-mm-dd (e.g. 2018-09-18).
3. `Query` - `0` if the sequence is to be used to calibrate the linear regression, and `1` otherwise. Usually, pre-therapy plasma HIV sequences are coded as `0` and HIV reservoir sequences are coded as `1`.

\* Note that collection date is required for all sequences, even query data, as this information is used to generate the divergence versus time plot
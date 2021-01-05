A comma separated file that contains information about the linear regression performance and parameters. The columns included are:

1. `RunID` - run ID of the job created by Phylodating.
2. `dAIC` - difference between the Akaike Information Criteria of the null model (where the regression’s slope is zero) and the linear regression inferred from the data.
3. `EstimateRootDate` - estimated root date of the tree calculated by the linear regression in the format yyyy-mm-dd.
4. `EstimatedRootDate95Low` - lower bound of the 95% confidence interval of the estimated root date in the format yyyy-mm-dd.
5. `EstimatedRootDate95High` - upper bound of the 95% confidence interval of the estimated root date in the format yyyy-mm-dd.
6. `EstimatedEvolutionaryRate` - estimated evolutionary rate calculated by the linear regression in substitutions per site per day.
7. `Fit`  - the model fit. Designated as `1` if the linear regression passes both predefined quality control criteria (dAIC > 10, and the lower bound of the 95% confidence interval of the estimated root date precedes the earliest collection date) and `0` otherwise.

Example:
```
"RunID","dAIC","EstimatedRootDate","EstimatedRootDate95Low","EstimatedRootDate95High","EstimatedEvolutionaryRate","Fit"
"12528060",17.1483031836612,"2009-12-06","2008-04-08","2011-08-04",4.32745826454141e-05,1
```

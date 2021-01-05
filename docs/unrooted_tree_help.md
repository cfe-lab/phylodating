An unrooted phylogeny (newick tree file) inferred from the query and calibration sequences contained in the CSV file.

\* Tip labels must exactly match sequence IDs in the info CSV file.

**A note on identical HIV sequences:** *Identical HIV sequences commonly occur in within-host HIV sequence datasets.  While phylodating will accept tree files containing terminal branches of zero length (caused by identical sequences), large numbers of identical calibration sequences can bias the regression. Similarly, large numbers of identical query sequences can bias the average inferred sequence ages in the dataset.  To avoid this, consider identifying identical HIV sequences in the calibration dataset, and include only the earliest instance of each sequence when inferring your phylogeny.  As for query sequences, consider whether you are primarily interested in the age distribution of distinct HIV sequences only, or whether you are interested in the age distribution of all sequences.  If the former, restrict the query dataset to distinct HIV sequences before inferring your phylogeny.*

Example:
```
(DNA1:0.000857,(RNA1:0.001053,((RNA5:0.019962,DNA3:0.001):0.040048,(RNA2:0.007126,((DNA2:0.005841,RNA3:0.000712):0.004969,(RNA4:0.008952,(DNA4:0.019875,(RNA6:0.003845,RNA7:0.01993):0.006931):0.030149):0.007087):0.010048):0.00697):0.001021):0.009876);
```
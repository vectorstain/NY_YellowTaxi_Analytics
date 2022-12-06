
# Univariate vs Bivariate and Graphical vs Non-Graphical

| Univariate  | Graphical                                                  | Non-Graphical                                                               |
| ----------- | ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| Categorical | Bar char of frequencies (count/percent)                    | Contingency table (count/percent)                                           |
| Continuous  | Histogram/rugplot/KDE, box/violin/swarm, qqplot, fat tails | central tendency -mean/median/mode, spread - variance, std, skew, kurt, IQR |

| Bivariate/multivariate     | Graphical                                                                                             | Non-Graphical                             |
| -------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Categorical vs Categorical | heat map, mosaic plot                                                                                 | Two-way Contingency table (count/percent) |
| Continuous vs Continuous   | all pairwise scatterplots, kde, heatmaps                                                              | all pairwise correlation/regression       |
| Categorical vs Continuous  | [bar, violin, swarm, point, strip seaborn plots](http://seaborn.pydata.org/tutorial/categorical.html) | Summary statistics for each level         |

## Univariate Analysis
* Look at one variable at a time.
### Categorical variables
* There is less available options with categorical variables
* Count the frequency of each variable
* Low frequency strings might be outliers
* You might want to relabel low frequency strings 'other'
* Find the number of unique labels for each column
* In pandas, change the data type to categorical (better when there aren't too many unique values)
* Bar plots of counts
* String columns allow for feature engineering by splitting the string, counting certain letters, finding the length of, etc... Feature engineering can be done later when modeling

### Continuous variables
* There are a lot more options for continuous variables
* Use the five number summary - with **`.describe`**
* Boxplots are great ways to find outliers
* Use histograms and kernel density estimators to visualize the distribution.
* Know the shape of the distribution
* Think about making categorical variables out of continuous variables by cutting them into bins.


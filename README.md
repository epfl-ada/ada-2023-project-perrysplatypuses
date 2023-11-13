# Title
As a movie director perspective, we want to find a good combination of character architypes.

## Methods(Analysis part)
### making vectors for each movie
It must include all archtypes . And it also they need to have the value for box ofiice. 
If we have N architypes. Then each movies have vector of N+1 demensions. First N demnsion might be  sum of the number of the character which have those architypes  and  the last demension is the value for  box office. 
So those vectors will look like this (1,2,0,・・・,3,3594000)


### regression
If the model is simple model. The optimized point will be analyticaly found. But it will likeyly to be on the boundary or known points.
We want to add uncertainty to the model somehow for finding unknow points.

### Gaussian Process Regression
we can predict box plots of every points wiht mean and variance. So we can find good points where nobody tries and also it is high possibility of success.
https://jamesbrind.uk/posts/2d-gaussian-process-regression/
This site shows how to implement it for multi dimensions.

### notes
need to limit the space for optimization. 　ex. each value of architypes vectors will be less than 5.
need to round values to integer after optimization.

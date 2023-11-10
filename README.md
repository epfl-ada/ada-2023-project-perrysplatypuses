# Title

## Methods(Analysis part)
### making vectors for each movie
It must include all archtypes . And it also they need to have the value for box ofiice. 
If we have N architypes. Then each movies have vector of N+1 demensions. First N demnsion might be  sum of the number of the character which have those architypes  and  the last demension is the value for  box office. 
So those vectors will look like this (1,2,0,・・・,3,3594000)


### Interpolation
need to choose an appropriate one.
https://docs.scipy.org/doc/scipy/reference/interpolate.html
If we want to find optimized parameter, just need to sort ?
### regression
if the model is simple model. The optimized point will be analyticaly found. But it will likeyly to on the boundary or known points.

### Gaussian Process Regression
we can predict box plots of every points wiht mean and variance. So we can find good points where nobody tries and also it is high possibility of success.

### notes
need to limit the space for optimization. 　ex. each value of architypes vectors will be less than 5.
need to round values to integer after optimization.

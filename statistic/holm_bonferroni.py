# https://islp.readthedocs.io/en/latest/labs/Ch13-multiple-lab.html
from statsmodels.stats.multitest import \
     multipletests as mult_test

###### facet
f_w_pvals = [0.006,0.122, 0.740]
print('facet: Welch\'s adjusted p value')
print(mult_test(f_w_pvals, alpha=0.05, method='holm', maxiter=1, is_sorted=False, returnsorted=False))
###### subfacet
sf_w_pvals = [0.007,0.488,0.619,0.071,0.491,0.767]
print('subfacet: Welch\'s adjusted p value')
print(mult_test(sf_w_pvals, alpha=0.05, method='holm', maxiter=1, is_sorted=False, returnsorted=False))


###### facet
f_u_pvals = [0.0111,0.181,0.886]
print('facet Mann-Whitney U adjusted p value')
print(mult_test(f_u_pvals, alpha=0.05, method='holm', maxiter=1, is_sorted=False, returnsorted=False))
##### subfacet
sf_u_pvals = [0.025,0.225,0.546,0.046,0.826,0.963]
print('subfacet: Mann-Whitney U adjusted p value')
print(mult_test(sf_u_pvals, alpha=0.05, method='holm', maxiter=1, is_sorted=False, returnsorted=False))
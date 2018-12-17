from __future__ import division
import math

total = 750
favour = 1
against = 699
abst = 50

if favour + against + abst != total:
  print "Wrong sum"
else:
  favAndAgai = favour + against
  term1 = (abst/total)*favour/favAndAgai * math.log(total/abst)
  term2 = (1-abst/total)*favour/favAndAgai * math.log(1/(1-abst/total))
  term3 = (abst/total)*against/favAndAgai * math.log(total/abst)
  term4 = (1-abst/total)*against/favAndAgai * math.log(1/(1-abst/total))
  result =  term1 +  term2 + term3 +  term4
  print result
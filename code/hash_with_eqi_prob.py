from __future__ import division
import random
import csv
import numpy as np
from math import exp, expm1
import math
from scipy.stats import norm

_memomask = {}
def convert_cor_to_index_eqi(x , bounds):
	k = 0
	while x > bounds[k] and k<len(bounds)-1:
		k = k+1
	return k			
def square_list(x):
    return [i ** 2 for i in x]			
def shifted_cor (x,y):
	z = np.correlate(x,y,'full')
	cx = np.cumsum(x)
	cy = np.cumsum(y)
	cx2 = np.cumsum(square_list(x))
	cy2 = np.cumsum(square_list(y))
	n = len(z)
	m = len(x)
	C = [-2 for x in range(n)]
	for i in range(m-1):
		xy = z[i]
		mx = cx[i]/(i+1)
		my = (cy[m-1]-cy[m-i-2])/(i+1)
		ex2 = cx2[i]
		ey2 = cy2[m-1] - cy2[m-i-2]
		sx=(ex2/(i+1))-(mx**2)
		sy=(ey2/(i+1))-(my**2)
		if sx<= 0 or sy <=0:
			sx=1
			sy=1
		else:
			sx = math.sqrt(sx)	
			sy = math.sqrt(sy)	
		C[i] = (xy-(i+1)*mx*my) / ((i+1)*sx*sy)	
	xy = z[m-1]
	mx = cx[m-1]/m
	my = cy[m-1]/m
	ex2 = cx2[m-1]
	ey2 = cy2[m-1]
	sx = (ex2/m)-(mx**2)
	sy = (ey2/m)-(my**2)
	
	if sx <= 0 or sy <= 0:
		sx = 1;
		sy = 1;
	else:
		sx = math.sqrt(sx);
		sy = math.sqrt(sy);
	C[m-1] = ( xy - m*mx*my ) / ( m*sx*sy )
	for i in range(m,n):
		xy = z[i]
		len1 = n - (i+1) + 1
		my = cy[len1-1]/len1
		mx = (cx[m-1] - cx[m-len1-1])/len1
		ey2 = cy2[len1-1]
		ex2 = cx2[m-1] - cx2[(m-1)-len1]
		sx = (ex2/(len1))-(mx**2)
		sy = (ey2/(len1))-(my**2)
		if sx <= 0 or sy <= 0:
			sx = 1
			sy = 1
		else:
			sx = math.sqrt(sx);
			sy = math.sqrt(sy);	
    
		C[i] = ( xy - len1*mx*my ) / ( len1*sx*sy )
	return C
					
def get_bounds(num_bins , sigma):
	out = [0 for i in range(num_bins-1)]
	for i in range(num_bins-1):
		out[i] = norm.ppf(((i+1)/num_bins) , loc=0, scale=sigma)
	return out	

def hash_equi_prob (sig, num_bins, r, sigma):
	
	bounds = get_bounds(num_bins , sigma)
	ran_ind = random.randint(0,len(sig)-1)
	rand_sig = sig[ran_ind]
	#print ran_ind
	bins = [[] for i in xrange(num_bins)]
	for s_ind in range(len(sig)):
		s = sig[s_ind]
		sh = shifted_cor(s,rand_sig)
		mid = int(len(sh)/2)
		sh = sh[mid-int(r/2):mid+int(r/2)]
		for i in range(len(sh)):
			to_be_added_ind = convert_cor_to_index_eqi(sh[i],bounds)
			bins[to_be_added_ind].append(s_ind)
	return bins

def get_all_indices(s , hf, num_bins):
	out = []
	for f in hf:
		out.append(f(str(s)) % num_bins)
	return out	
		


def hash_function(n):
  mask = _memomask.get(n)
  if mask is None:
    random.seed(n)
    mask = _memomask[n] = random.getrandbits(32)
  def myhash(x):
    return hash(x) ^ mask
  return myhash
  
def multi_hash (sig , num_bins, r):
	hf=[]
	for i in range(r):
		hf.append(hash_function(i*17))
	bins = [[] for i in xrange(num_bins)]
	for s_ind in range(len(sig)):
		s = sig[s_ind]
		sh = get_all_indices(s , hf, num_bins)
		for i in range(len(sh)):
			bins[sh[i]].append(s_ind)
	return bins		

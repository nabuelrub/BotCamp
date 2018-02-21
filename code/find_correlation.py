from __future__ import division
import numpy as np
from math import exp, expm1
import math
from datetime import *
from scipy.stats.stats import pearsonr
import sys
import re
import string
import glob
import os
import csv
import json

#___________________________________________ remove duplicate array

def rm_duplicate_2D (arr):
	res = []
	res.append([])
	res[0] = arr[0]
	c = 1
	for i in range(len(arr)):
		
		if not arr[i] in res:
			res.append([])
			res[c] = arr[i]
			c = c + 1
	return res 	
#___________________________________________ check equality of two array

def is_array_equal (arr_1,arr_2):
	if len(arr_1) != len(arr_2):
		return False
	for i in range (len(arr_1)):	
		if arr_1[i] != arr_2[i]:
			return False
	return True	
#__________________________________________

def get_ts_arr(user_ts):
	check_list = []
	column_temp = 0
	activity = [0]*tl_size
	#offset = 18 * 24 * 60
	for i in range(len(user_ts)):
		time_stamp =  user_ts[i]
		delta = (time_stamp - base_time).total_seconds()
		#month = int(time_stamp.strftime('%m'))
		#day = int(time_stamp.strftime('%d'))
		#hour = int(time_stamp.strftime('%H'))
		#minute = int(time_stamp.strftime('%M'))
		column_temp = int(delta/win_size)
		try:
			activity[column_temp] = activity[column_temp] + 1
		except:
			#print str(day) + "-" + str(month) + " " + str(hour) + ":" + str(minute) + "====>" + str(column_temp)
			print str(base_time) + "" + str(time_stamp) +  "   " +  str(delta) + "   "+ str(column_temp) + "   " +str(tl_size)
		
	return activity

#_____________________________________write array in to the file

def wrt_to_file (arr_type,arr,f_name):
	f = open(f_name,'w')
	if(arr_type == 2):
		for i in range (len(arr)):
			for j in range (len(arr[i])-1):
				f.write(str(arr[i][j])+ ',')
			f.write(str(arr[i][len(arr[i])-1])+ '\n')
			
	elif(arr_type == 1):
		for j in range (len(arr)):
				f.write(str(arr[j])+ '\n')

#_________________________________________calculationg shifted correlation

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
	#print cx2
	#print cy2
	for i in range(m-1):
		xy = z[i]
		mx = cx[i]/(i+1)
		#print mx
		my = (cy[m-1]-cy[m-i-2])/(i+1)
		#print 'my=' + str(my)
		#print cy[m-1]
		#print cy[m-i-2]
		ex2 = cx2[i]
		#print "ex2=" + str(ex2)
		ey2 = cy2[m-1] - cy2[m-i-2]
		#print "ey2=" + str(ey2)
		sx=(ex2/(i+1))-(mx**2)
		#print "sx=" + str(sx)
		sy=(ey2/(i+1))-(my**2)
		#print "sy=" + str(sy)
		if sx<= 0 or sy <=0:
			sx=1
			sy=1
		else:
			sx = math.sqrt(sx)	
			sy = math.sqrt(sy)	
		#print "sx: " + str(sx)
		#print "sy: " + str(sy)
		C[i] = (xy-(i+1)*mx*my) / ((i+1)*sx*sy)	
		#print "C[i]: " + str(C[i])
	xy = z[m-1]
	mx = cx[m-1]/m
	my = cy[m-1]/m
	ex2 = cx2[m-1]
	ey2 = cy2[m-1]
	sx = (ex2/m)-(mx**2)
	sy = (ey2/m)-(my**2)
	#print "sx= " + str(sx)
	#print "sy= " + str(sy)
	
	if sx <= 0 or sy <= 0:
		sx = 1;
		sy = 1;
	else:
		sx = math.sqrt(sx);
		sy = math.sqrt(sy);
	C[m-1] = ( xy - m*mx*my ) / ( m*sx*sy )
	#print "C[m-1]= " + str(C[m-1])
	
    
	for i in range(m,n):
		
		xy = z[i]
		len1 = n - (i+1) + 1
		#print "len1: " + str(len1)
		my = cy[len1-1]/len1
		#print "my= "+ str(my)
		mx = (cx[m-1] - cx[m-len1-1])/len1
		#print "mx= "+ str(mx)
		
		ey2 = cy2[len1-1]
		
		ex2 = cx2[m-1] - cx2[(m-1)-len1]
		#print "ex2= "+ str(ex2)
		
		sx = (ex2/(len1))-(mx**2)
		sy = (ey2/(len1))-(my**2)
		#print "sx= "+ str(sx)
		#print "sy= "+ str(sy)
		
		
		if sx <= 0 or sy <= 0:
			sx = 1
			sy = 1
		else:
			sx = math.sqrt(sx);
			sy = math.sqrt(sy);	
    
		C[i] = ( xy - len1*mx*my ) / ( len1*sx*sy )
	return C
#_______________________________________ hash function

def get_correlation():
	global log_file
	active_user_ind = []
	
	print "#Listened user:" + str(len(ts))
	log_file.write("#Listened user:" + str(len(ts)) + '\n')
	
	for i in range (len(ts)):
		if(len(ts[i]) >= num_activity):
			active_user_ind.append(i)
	active_user = len(active_user_ind)		
	#all_active_user_correlation = [[0 for x in range(active_user)] for x in range(active_user)]
	all_active_user_timeline = [[] for x in range(active_user)]
	names = ['' for x in range(active_user)]
	
	#cor_temp = [0]*shifting_times*2
	for i in range (active_user):
		this_ts = get_ts_arr(ts[active_user_ind[i]])
		all_active_user_timeline[i] = this_ts
		names[i] = reverse_user_dict[active_user_ind[i]]
	print len(all_active_user_timeline)
	log_file.write("#active listened user:" + str(len(ts)) + '\n')
	
	t = datetime.now()
	# commented to do calculation in matlab
	'''for p in range (active_user):
		for q in range (p+1,active_user):	
			cor_temp = shifted_cor(all_active_user_timeline[p],all_active_user_timeline[q])
			#for m in range (shifting_times):
				#cor_temp[m] = shifted_cor(all_user_timeline[p][m:],all_user_timeline[q][:len(all_user_timeline[q])-m])[0]
				#cor_temp[m+shifting_times] = shifted_cor(all_user_timeline[q][m:],all_user_timeline[p][:len(all_user_timeline[p])-m])[0]
			
			b1 = int((len(cor_temp)/2))
			cor_temp = cor_temp[b1-20:b1+20]
			all_active_user_correlation[p][q] = max(cor_temp)
	
	wrt_to_file(2,all_active_user_correlation,corr_output_file)'''
	wrt_to_file(1,names,name_file)
	wrt_to_file(2,all_active_user_timeline,tl_file)
	#return all_active_user_correlation

#================================== Global variable 

# argument from terminal
input_file = sys.argv[1]
name_file = str(sys.argv[2]) + '.txt'
tl_file =  str(sys.argv[3]) + '.txt'

# defined variable and parameters
win_size = 10 #second
num_activity = 10
#shifting_times = 10 #round
tl_size = 0
flag = False
base_time = datetime.now()
last_time = datetime.now()
start_time = datetime.now()

#corr_output_file = 'shift_cor_more_than_'+ str(num_activity)+'_res_'+str(win_size)+'_'+str(datetime.now())+'.txt'
user_dict = dict()
reverse_user_dict = dict()
id_dict = dict()
user_count = 0
ts = []

loc =input_file.rfind('/')
loc2 = input_file[:loc].rfind('/')
log_file_name = input_file[:loc2+1] + "log.txt"
log_file=open(log_file_name,'a')

input_file = open(input_file + '.txt','r') # to read tweets from file information
#csv_reader = csv.reader(input_file, delimiter=',',quotechar='\n')
#csv_arr = list(csv_reader)
for line in input_file:
	try:
		if(len(line) > 1000):
			x = json.loads(line)
			created_at = datetime.strptime(str(x['created_at']), '%a %b %d %H:%M:%S +0000 %Y')
			last_time = created_at
			screen_name = str(x['user']['screen_name'])
			user_id =  str(x['user']['id'])
			if not flag:
				base_time = datetime.strptime(str(x['created_at']), '%a %b %d %H:%M:%S +0000 %Y')
				print 'base_time: ' + str(base_time)
				log_file.write('base_time: ' + str(base_time) + '\n')
				flag =True
			if screen_name not in user_dict:
				user_dict[screen_name] = user_count
				reverse_user_dict[user_count] = screen_name
				id_dict [screen_name] = user_id 
				ts.append([])
				ts[user_count].append(created_at)
				user_count = user_count + 1
			else:
				ts[user_dict[screen_name]].append(created_at)
	except:
		continue
#call the fuction to find the correlation
listen_time_duration = (last_time - base_time).total_seconds()
tl_size = int(listen_time_duration / win_size) + 1
#print ('Time for finding correlation')
get_correlation()
				
print (datetime.now() - start_time )
log_file.write("Timelines are ready in: " + str((datetime.now() - start_time )) + '\n')

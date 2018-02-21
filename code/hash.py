from __future__ import division
from datetime import *
import sys
import re
import string
import glob
import os
import csv
import json
from hash_with_eqi_prob import hash_equi_prob

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
	column_temp = 0
	global tl_size
	global base_time
	activity = [0 for x in range(tl_size)] 
	for i in range(len(user_ts)):
		time_stamp =  user_ts[i]
		delta = (time_stamp - base_time).total_seconds()
		column_temp = int(delta/win_size)	
		if not (delta < 0):				
			try:
				activity[column_temp] = activity[column_temp] + 1
			except:
				print str(base_time) + " " + str(time_stamp) +  "   " +  str(delta) + "   "+ str(column_temp) + "   " +str(tl_size)
	return activity

#_____________________________________write array in to the file
def wrt_to_file (arr_type,arr,f_name):
	f = open(str(f_name) + '.txt','w')
	if(arr_type == 2):
		for i in range (len(arr)):
			for j in range (len(arr[i])-1):
				f.write(str(arr[i][j])+ ',')
			f.write(str(arr[i][len(arr[i])-1])+ '\n')
			
	elif(arr_type == 1):
		for j in range (len(arr)):
				f.write(str(arr[j])+ '\n')
				
#__________________________________________

def get_num_good_usr(x,th):
	x2 = list(set(x))
	#cnt = [0 for i in range (len(x2))]
	out = []
	for i in range (len(x2)):
		c = x.count(x2[i])
		if(c > th):
			out.append(x2[i])
	return out
	
def sort_list_based_len(x):
	out = [[] for i in range(len(x))]
	s = [0 for i in range(len(x))]
	for i in range(len(x)):
		s[i] = len(x[i])
	ind = sorted(range(len(s)), key=lambda k: s[k])	
	ind = list(reversed(ind))
	for i in (range(len(ind))):
		out[i] = x[ind[i]]
	return out	

#_______________________________________ hash function

def hash_user(step):
	global is_continue
	global overal_duration
	global good_user_th
	global good_bin_th
	global round_path
	global log_file
	s_time = datetime.now()
	#reverse_bucket_dict = dict()
	#bucket_dict = dict()
	print '#user: '+ str(len(ts))
	log_file.write('#user: '+ str(len(ts)) + '\n')
	active_user_ind = []
	for i in range (len(ts)):
		if(len(ts[i]) >= num_activity):
			active_user_ind.append(i)
	active_user = len(active_user_ind)
	print  "#active_user: " + str(active_user)
	log_file.write("#active_user: " + str(active_user) + '\n')
	users_tl = [[] for i in range (active_user)]
	name_list = ['' for i in range (active_user)]
	for i in range (active_user):
		users_tl[i] = get_ts_arr(ts[active_user_ind[i]])
		name_list[i] = reverse_user_dict[active_user_ind[i]]
	bucket_user = hash_equi_prob(users_tl,modul,shifting_times,sigma)
	
	#------------------find if we have are done or not
	to_report = []
	good_bin = 0
	bucket_user = sort_list_based_len (bucket_user)
	for i in range (len(bucket_user)):
		cur_good_user = get_num_good_usr(bucket_user[i],good_user_th)
		if (len(cur_good_user) > good_bin_th): 
			good_bin = good_bin + 1
			for j in range (len(cur_good_user)):
				cur_name = name_list[cur_good_user[j]]
				if not(id_dict[cur_name] in to_report):
					to_report.append(id_dict[cur_name])
			if len(to_report) >= 5000:
				is_continue = False
				break
	print "#to_report: "+str(len(to_report))
	log_file.write("#to_report: "+str(len(to_report)) + '\n')
	# find the reported users
	if not is_continue or overal_duration >= overal_duration_th:
		is_done_file = open(str(round_path)+'/is_done','w')
		is_done_file.write("1")
		report_file_name = str(round_path)+'/reported_user_' + str(step)
		#write reported users into file
		wrt_to_file (1,to_report,report_file_name)
	

#================================== Global variable 

# argument from terminal
in_files = int(sys.argv[1])
step = int(sys.argv[2])
listen_time = int(sys.argv[3])
round_path = sys.argv[4]

# defined variable and parameters
good_user_th = 5
good_bin_th = 5
win_size = 1 #second
num_activity = 2
shifting_times = 40 #round
is_continue = True
tl_size = 0
flag = False
base_time = datetime.now()
last_time = datetime.now()
start_time = datetime.now()
user_dict = dict()
reverse_user_dict = dict()
id_dict = dict()
user_count = 0
ts = []
modul = 5000
sigma = 0.024
overal_duration = in_files * listen_time
overal_duration_th = listen_time * 4

loc=round_path.rfind('/')
log_file_name = round_path[:loc+1] + "log.txt"
log_file=open(log_file_name,'a')

for i in range(in_files):
	input_file = open(str(round_path)+'/'+str(i+1) + '.txt','r') # to read tweets from file information
	for line in input_file:
		try:
			if len(line) > 1000:
				x = json.loads(line)
				created_at = datetime.strptime(x['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
				last_time = created_at
				screen_name = str(x['user']['screen_name'])
				user_id =  str(x['user']['id'])
			if not flag:
				base_time = datetime.strptime(x['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
				print 'Hash base_time: ' + str(base_time)
				log_file.write('Hash base_time: ' + str(base_time) + '\n')
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
#call the fuction to hash the users 
listen_time_duration = (last_time - base_time).total_seconds()
tl_size = int(listen_time_duration / win_size) + 1
hash_user(step)
				
print "Hashing Function Lasts: " + str(datetime.now() - start_time )
log_file.write("Hashing Function Lasts: " + str(datetime.now() - start_time ) + '\n' )

# -*- coding: utf-8 -*-

import json
from datetime import datetime
import numpy as np

def get_age(birt_year):
	'''
	Doğum tarihini yaş aralığına çevirir.
	'''
	if birt_year:
		age = int(2018-int(birt_year))
		if age < 18:
			return 0
		elif age < 25:
			return 1
		elif age < 30:
			return 2
		elif age < 40:
			return 3
		elif age < 60:
			return 4
		else:
			return 5
	return 'NaN'

def get_education(education):
	'''
	String şeklindeki eğitim düzeyini integer labellara çevirir.
	'''
	if education:
		if education == 'Lise':
			return 1
		elif education[1:] == 'niversite':
			return 2
		elif 'Lisans' in str(education.encode('utf-8')):
			return 3
		return 0
	return 'NaN'

def return_row(row, user, job_dict, category_dict):
	gender = 1 if user['gender'] == 'E' else 0

	age = get_age(user.get('birt_year'))

	education = get_education(user.get('education'))

	marital = 0
	if user['marital_status'] == 'Evli':
		marital = 1

	job = job_dict[user['job']] if user['job'] else 'NaN'

	part_of_day = int(datetime.utcfromtimestamp(int(row['event_date'])).strftime('%H'))/4 if row['event_date'] else 'NaN'

	category = category_dict[row['event_category']] if row['event_category'] else 'NaN'

	click = 0 if row['event_type'] == 'IMPRESSION' else 1

	return [gender, age, education, marital, job, part_of_day, category, click]

def get_scikit_data():
	'''
	Json'ı parçalayarak iş türlerini, kategorileri ve verinin scikit için uygun halini döndürür.
	'''
	file = open("all_data/all_data3.json")
	json_data = json.loads(file.read())

	ads = {}
	users = {}
	for each in json_data:

		# ADDING ADS
		if not ads.get(each['ad_id']):
			ads[each['ad_id']] = {'count': 0, 'impression': 0, 'click': 0, 'dailyCountLimit': float(each['ad_daily_budget_kurus'])/float(each['ad_bid_price_kurus'])}
		ads[each['ad_id']]['count'] += 1
		# -----------------------------------------

		# ADDING USERS
		uid = each['viewer_user_id']
		if not users.get(uid):
			users[uid] = {}
			users[uid]['education'] = each['viewer_education']
			users[uid]['job'] = each['viewer_job']
			users[uid]['marital_status'] = each['viewer_marital_status']
			users[uid]['birt_year'] = each['viewer_birt_year']
			users[uid]['gender'] = each['viewer_gender']
		
		# ADDING EVENTS TO ADS AND USERS
		if each['event_type'] == 'IMPRESSION':
			ads[each['ad_id']]['impression'] += 1
		else:
			ads[each['ad_id']]['click'] += 1

	# CREATING JOB DICT
	category_list = set([x['event_category'] for x in json_data])
	category_list = filter(lambda x: x, category_list)
	category_dict = {x: cnt for cnt, x in enumerate(category_list)}

	# CREATING CATEGORIES
	job_list = set([users[key]['job'] for key in users])
	job_list = filter(lambda x: x, job_list)
	job_dict = {x: cnt for cnt, x in enumerate(job_list)}

	scikit_data = []
	for row in json_data:
		scikit_data.append(return_row(row, users[row['viewer_user_id']], job_dict, category_dict))

	return scikit_data, category_dict, job_dict
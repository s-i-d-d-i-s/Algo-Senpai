import json
import requests
import random
import time

def getProblemsNearRating(l,r,lim):
	problem_cache = json.loads(open('problem_cache.json','r').read())
	last_updated = problem_cache['last_updated']
	all_problems = problem_cache['all_problems']
	if int(time.time()) > last_updated + 6*60*60:
		all_problems = json.loads(requests.get("https://codeforces.com/api/problemset.problems").content)
		cache_data = {'all_problems':all_problems,'last_updated': int(time.time())}
		cache_data = json.dumps(cache_data)
		with open('problem_cache.json','w') as f:
			f.write(cache_data)
	else:
		print("Using Cache")
	
	all_problems=all_problems['result']
	all_problems = all_problems['problems']
	random.shuffle(all_problems)
	res = []
	for x in all_problems:
		if len(res)==lim:
			return res
		if 'rating' not in x.keys():
			continue
		if 'tags' in x.keys():
			if '*special' in x['tags']:
				continue
		if  x['rating']>=l and x['rating']<=r:
			res.append(x)
	return res

def getPset(lower_rating,upper_rating,count):
	data = getProblemsNearRating(lower_rating,upper_rating,count)
	data.sort(key=lambda x:x['rating'])
	for i in range(len(data)):
		data[i]['url']="https://codeforces.com/contest/{}/problem/{}".format(data[i]['contestId'],data[i]['index'])
	msg = ""
	alphas = "ABCDEFGH"
	alphas = alphas[:count]
	msg = '\n'.join(f"{alphas[i]}: [{p['name']}]({p['url']}) [{p['rating']}]" for i, p in enumerate(data))
	return msg

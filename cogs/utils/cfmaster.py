import json
import requests
import random

def getSolvedProblems(handle):
    solved = set()
    done = {}
    scanned=False
    for i in range(1,10):
        print(i)
        url = "https://codeforces.com/api/user.status?handle={}&from={}&count=1000".format(handle,i)
        data = json.loads(requests.get(url).content)['result']
        if scanned:
            break
        for d in data:
            if d['id'] in done.keys():
                scanned=True
                break
            done[d['id']]=True
            solved.add(d['problem']['name'])
    return solved

def getProblemsNearRating(l,r,solved):
    all_problems = json.loads(requests.get("https://codeforces.com/api/problemset.problems").content)
    all_problems=all_problems['result']
    all_problems = all_problems['problems']
    random.shuffle(all_problems)
    res = []
    for x in all_problems:
        if len(res)==4:
            return res
        if 'rating' not in x.keys():
            continue
        if x['name'] not in solved and x['rating']>=l and x['rating']<=r:
            res.append(x)
    return res

def getDailyPset(whitelist):
	ignore = set()
	for x in whitelist:
		cur = getSolvedProblems(x)
		ignore = ignore.union(cur)
	data = getProblemsNearRating(1000,1100,ignore)
	data.sort(key=lambda x:x['rating'])
	for i in range(len(data)):
		data[i]['url']="https://codeforces.com/contest/{}/problem/{}".format(data[i]['contestId'],data[i]['index'])
	msg = '\n'.join(f"{'ABCD'[i]}: [{p['name']}]({p['url']}) [{p['rating']}]" for i, p in enumerate(data))
	return msg


def getRanklist(content,handles):
	if content.find("\n\nRanklist::") == -1:
		## New Ranklist
		content += "\n\nRanklist::"
		content += "\n\n"
		for x in handles:
			content += f"{x}\n"
		return content
	else:
		## Old Ranklist
		content = content[:content.find('\n\nRanklist::')]
		content += "\n\nRanklist::"
		content += "\n\n"
		for x in handles:
			content += f"{x}\n"
		return content

import requests, json
import time
import urllib.parse as urlparse
import os

from requests.api import request

DEBUG=False

class DB:
	def __init__(self):
		self.baseUrl = os.getenv("DB_URL","DB_URL_NOT_FOUND") 


	def add_ranklist(self,guildid,channelid):
		obj = {'guildid':guildid,'channelid':channelid,'last_sent':0}
		requests.post(self.baseUrl + 'ranklist.json',json.dumps(obj))
		def fetch_ranklist_with_id(baseUrl,guildId):
			data = json.loads(requests.get(baseUrl + 'ranklist.json').content)
			for d in data:
				if data[d]['guildid'] == guildId:
					obj = data[d]
					obj['id'] = d
					return obj
			return None
		obj = fetch_ranklist_with_id(self.baseUrl,guildid)
		requests.patch(self.baseUrl + 'ranklist/'+obj['id']+'.json',json.dumps(obj))


	def fetch_ranklist(self,guildId):
		data = json.loads(requests.get(self.baseUrl + 'ranklist.json').content)
		if data == None:
			return None
		for d in data:
			if data[d]['guildid'] == guildId:
				return data[d]
		return None

	def add_static_ranklist(self,guildid,channelid,msgid):
		obj = {'guildid':guildid,'channelid':channelid,'msg':msgid,'last_updated':0}
		requests.post(self.baseUrl + 'static_ranklist.json',json.dumps(obj))
		def fetch_ranklist_with_id(baseUrl,guildId):
			data = json.loads(requests.get(baseUrl + 'static_ranklist.json').content)
			for d in data:
				if data[d]['guildid'] == guildId and data[d]['channelid']==channelid:
					obj = data[d]
					obj['id'] = d
					return obj
			return None
		obj = fetch_ranklist_with_id(self.baseUrl,guildid)
		requests.patch(self.baseUrl + 'static_ranklist/'+obj['id']+'.json',json.dumps(obj))
	
	def fetch_static_ranklist(self,guildId):
		data = json.loads(requests.get(self.baseUrl + 'static_ranklist.json').content)
		if data == None:
			return None
		for d in data:
			if data[d]['guildid'] == guildId:
				return data[d]
		return None

	def fetch_all_static_ranklist(self):
		data = json.loads(requests.get(self.baseUrl + 'static_ranklist.json').content)		
		res = []
		if data==None:
			return res
		for d in data:
			res.append(data[d])
		return res

	def fetch_all_ranklist(self):
		data = json.loads(requests.get(self.baseUrl + 'ranklist.json').content)		
		res = []
		if data==None:
			return res
		for d in data:
			res.append(data[d])
		return res

	def update_ranklist(self,guildid,channelid):
		def fetch_ranklist_with_id(baseUrl,guildId):
			data = json.loads(requests.get(baseUrl + 'ranklist.json').content)
			for d in data:
				if data[d]['guildid'] == guildId:
					return data[d]
			return None
		obj = fetch_ranklist_with_id(self.baseUrl,guildid)
		obj['channelid'] = channelid
		obj['last_sent'] = 0
		data = json.loads(requests.patch(self.baseUrl + 'ranklist/'+obj['id']+'.json',json.dumps(obj)).content)

	def update_static_ranklist_last_sent(self,id):
		def fetch_ranklist_with_id(baseUrl,id):
			data = json.loads(requests.get(baseUrl + 'static_ranklist.json').content)
			for d in data:
				if data[d]['id'] == id:
					return data[d]
			return None
		obj = fetch_ranklist_with_id(self.baseUrl,id)
		print("In update_static_ranklist_last_sent",obj)
		obj['last_sent'] = int(time.time())
		data = json.loads(requests.patch(self.baseUrl + 'static_ranklist/'+obj['id']+'.json',json.dumps(obj)).content)

	def update_ranklist_last_sent(self,id):
		def fetch_ranklist_with_id(baseUrl,id):
			data = json.loads(requests.get(baseUrl + 'ranklist.json').content)
			for d in data:
				if data[d]['id'] == id:
					return data[d]
			return None
		obj = fetch_ranklist_with_id(self.baseUrl,id)
		obj['last_sent'] = int(time.time())
		data = json.loads(requests.patch(self.baseUrl + 'ranklist/'+obj['id']+'.json',json.dumps(obj)).content)


	def add_mashup_data(self,guildid,channelid,msgid):
		obj = {'guildid':guildid,'channelid':channelid,'msgid':msgid}
		requests.post(self.baseUrl + 'mashups_data.json',json.dumps(obj))
		def fetch_mashup_with_id(baseUrl,guildid,channelid,msgid):
			data = json.loads(requests.get(self.baseUrl + 'mashups_data.json').content)
			for d in data:
				if data[d]['guildid'] == guildid and data[d]['channelid'] == channelid and data[d]['msgid'] == msgid:
					obj = data[d]
					obj['id'] = d
					return obj
			return None
		obj = fetch_mashup_with_id(self.baseUrl,guildid,channelid,msgid)
		requests.patch(self.baseUrl + 'mashups_data/'+obj['id']+'.json',json.dumps(obj))

	def fetch_mashup_data(self,guildid):
		data = json.loads(requests.get(self.baseUrl + 'mashups_data.json').content)
		res = []
		for d in data:
			if data[d]['guildid'] == guildid:
				res.append(data[d])
		return res

	def add_mashup(self,guildid,channelid,mashuptype,lower_rating,upper_rating,problem_count):
		obj = {
			'guildid':guildid,
			'channelid':channelid,
			'mashuptype':mashuptype,
			'lower_rating':lower_rating,
			'upper_rating': upper_rating,
			'last_sent': 0,
			'problem_count': problem_count,
		}
		requests.post(self.baseUrl + 'mashups.json',json.dumps(obj))
		def fetch_mashup_with_id(baseUrl,guildid,channelid,mashuptype,lower_rating,upper_rating,problem_count):
			data = json.loads(requests.get(baseUrl + 'mashups.json').content)
			for d in data:
				if data[d]['guildid'] == guildid and data[d]['channelid'] == channelid and data[d]['mashuptype'] == mashuptype and data[d]['lower_rating']==lower_rating and data[d]['upper_rating'] == upper_rating and data[d]['problem_count']==problem_count:
					obj = data[d]
					obj['id'] = d
					return obj
			return None
		obj = fetch_mashup_with_id(self.baseUrl,guildid,channelid,mashuptype,lower_rating,upper_rating,problem_count)
		requests.patch(self.baseUrl + 'mashups/'+obj['id']+'.json',json.dumps(obj))

	def fetch_mashup(self,guildid,channelid,mashuptype,lower_rating,upper_rating):
		data = json.loads(requests.get(self.baseUrl + 'mashups.json').content)
		if data==None:
			return None
		for d in data:
			if data[d]['guildid'] == guildid and data[d]['channelid'] == channelid and data[d]['mashuptype'] == mashuptype and data[d]['lower_rating']==lower_rating and data[d]['upper_rating'] == upper_rating:
				return data[d]
		return None

	def fetch_all_mashup(self):
		data = json.loads(requests.get(self.baseUrl + 'mashups.json').content)
		res = []
		if data == None:
			return res
		for d in data:
			res.append(data[d])
		return res
		
	def update_mashup(self,id):
		def fetch_mashup_with_id(baseUrl,id):
			data = json.loads(requests.get(baseUrl + 'mashups.json').content)
			for d in data:
				if data[d]['id'] == id:
					obj = data[d]
					return obj
			return None
		obj = fetch_mashup_with_id(self.baseUrl,id)
		obj['last_sent'] = int(time.time())
		requests.patch(self.baseUrl + 'mashups/'+obj['id']+'.json',json.dumps(obj))
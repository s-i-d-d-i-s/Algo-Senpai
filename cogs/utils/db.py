import psycopg2
import time
import urllib.parse as urlparse
import os

DEBUG=False

class DB:
	def __init__(self):
		self.con=""
		if DEBUG != True:
			url = urlparse.urlparse(os.environ['DATABASE_URL'])
			dbname = url.path[1:]
			user = url.username
			password = url.password
			host = url.hostname
			port = url.port
			self.con = con = psycopg2.connect(
				dbname=dbname,
				user=user,
				password=password,
				host=host,
				port=port
			)
		else:
			host = "localhost"
			dbname = "eric"
			user = "postgres"
			password = "admin"
			self.con = con = psycopg2.connect(
				host = host,
				dbname=dbname,
				user=user,
				password=password
			)

		self.create_tables()

	def __del__(self): 
		self.con.close()
		
	def create_tables(self):
		cur = self.con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS mashups_data(
			id SERIAL PRIMARY KEY,
			guildid VARCHAR (255) NOT NULL,
			channelid VARCHAR (255) NOT NULL,
			msgid VARCHAR (255) NOT NULL
			);
			""")

		cur.execute("""
			CREATE TABLE IF NOT EXISTS mashups(
			id SERIAL PRIMARY KEY,
			guildid VARCHAR (255) NOT NULL,
			channelid VARCHAR (255) NOT NULL,
			mashuptype INTEGER NOT NULL,
			lower_rating INTEGER NOT NULL,
			last_sent VARCHAR (255) NOT NULL,
			upper_rating INTEGER NOT NULL,
			problem_count INTEGER NOT NULL
			);
			""")
		
		cur.execute("""
			CREATE TABLE IF NOT EXISTS ranklist(
			id SERIAL PRIMARY KEY,
			guildid VARCHAR (255) NOT NULL,
			channelid VARCHAR (255) NOT NULL,
			last_sent VARCHAR (255) NOT NULL
			);
			""")

		cur.close()
		self.con.commit()

	def add_ranklist(self,guildid,channelid):
		cur = self.con.cursor()
		cur.execute(f"INSERT INTO ranklist(guildid,channelid,last_sent) VALUES('{guildid}','{channelid}','{0}')")
		self.con.commit()
		cur.close()

	def fetch_ranklist(self,guildid):
		cur = self.con.cursor()
		cur.execute(f"SELECT * from ranklist WHERE guildid='{guildid}'")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def fetch_all_ranklist(self):
		cur = self.con.cursor()
		cur.execute(f"SELECT * from ranklist")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def update_ranklist(self,guildid,channelid):
		cur = self.con.cursor()
		cur.execute(f"UPDATE ranklist SET channelid='{channelid}',last_sent='{0}' WHERE guildid='{guildid}'")
		self.con.commit()
		cur.close()

	def update_ranklist_last_sent(self,id):
		cur = self.con.cursor()
		cur.execute(f"UPDATE ranklist SET last_sent='{int(time.time())}' WHERE id='{id}'")
		self.con.commit()
		cur.close()

	def add_mashup_data(self,guildid,channelid,msgid):
		cur = self.con.cursor()
		cur.execute(f"INSERT INTO mashups_data(guildid,channelid,msgid) VALUES('{guildid}','{channelid}',{msgid})")
		self.con.commit()
		cur.close()

	def fetch_mashup_data(self,guildid):
		cur = self.con.cursor()
		cur.execute(f"SELECT * from mashups_data WHERE guildid='{guildid}'")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def add_mashup(self,guildid,channelid,mashuptype,lower_rating,upper_rating,problem_count):
		cur = self.con.cursor()
		cur.execute(f"INSERT INTO mashups(guildid,channelid,mashuptype,lower_rating,last_sent,upper_rating,problem_count) VALUES('{guildid}','{channelid}',{mashuptype},{lower_rating},0,{upper_rating},{problem_count})")
		self.con.commit()
		cur.close()

	def fetch_mashup(self,guildid,channelid,mashuptype,lower_rating,upper_rating):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM mashups where guildid= '{guildid}' AND channelid ='{channelid}' AND mashuptype={mashuptype} AND lower_rating={lower_rating} AND upper_rating={upper_rating}")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data

	def fetch_all_mashup(self):
		cur = self.con.cursor()
		cur.execute(f"SELECT * FROM mashups")
		data = cur.fetchall()
		self.con.commit()
		cur.close()
		return data
		
	def update_mashup(self,id):
		cur = self.con.cursor()
		cur.execute(f"UPDATE mashups SET last_sent = {int(time.time())} WHERE id= {id}")
		self.con.commit()
		cur.close()
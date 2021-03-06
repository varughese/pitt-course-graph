import requests
import json
import db 

SCHOOL_ID = 1247  # Pitt
# This was found quickly by just inspecting RMP's network calls. If you paste it into a tool like Postman, it is much easier to read
URL = "https://search-production.ratemyprofessors.com/solr/rmp/select/?solrformat=true&rows=1000&wt=json&q=*%3A*+AND+schoolid_s%3A{}+AND+teacherlastname_engram%3A{}&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq="

class Professor():
	def __init__(self, data):
		self.id = data["pk_id"]
		if "averageratingscore_rf" in data:
			self.score = data["averageratingscore_rf"]
			self.total_of_ratings = data["total_number_of_ratings_i"]
		else:
			self.score = "N/A"
			self.total_of_ratings = 0
		self.first_name = data["teacherfirstname_t"]
		self.last_name = data["teacherlastname_t"]
	
	def __str__(self):
		return "Prof {} [{}]".format(self.last_name, self.score)

	def __repr__(self):
		return "<RMP Teacher {}>".format(self.last_name)


f= open("saved.txt","w+")
for letter in 'abcdefghijklmnopqrstuvwyxz':
	f.write(letter)
	print("Getting all " + letter)
	res = requests.get(URL.format(SCHOOL_ID, letter))
	profs = [Professor(d) for d in res.json()["response"]["docs"]]
	for p in profs:
		print(p)
		db.prof.document(str(p.id)).set(p.__dict__)
	
f.close()
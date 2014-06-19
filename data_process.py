import requests, csv, json
def process():
	r = requests.get('https://gist.githubusercontent.com/jedisct1/372560a9f0f6f225bddc/raw/ctest.out.txt')
	with open('dns.txt','w') as f:
		f.write(r.content)
	reader = csv.reader(open('dns.txt'), delimiter='\t')
	rows = []
	header = ['timestamp', 'name', 'client_id','qtype','rcode', 'lat','long', 'country_code']
	for line in reader:
		rows.append({header[i]:line[i] for i in xrange(len(line))})
	json.dump(rows, open('dns.json','wb'))

if __name__ == '__main__':
	process()

import json
import itertools
from datetime import datetime
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

class DNSClassifier(object):

  def __init__(self, filename):
    self.dv = DictVectorizer()
    self.X_raw = json.load(open(filename))
    self.clf = KMeans(n_clusters = 5)
    self.preprocess()

  def preprocess(self):
    # features = subset of self.X_raw
    features = []
    for row in self.X_raw:
      feature = {}
      feature['tld'] = row['name'].split('.')[-1]
      feature['sub_domain'] = len(row['name'].split('.')) > 2
      int_portion = lambda s: str(int(float(s)))
      feature['timestamp_hamming'] = sum(c1 != c2 for c1, c2 in itertools.izip(int_portion(row['timestamp']), row['name']))
      feature['country_code'] = row['country_code'] in ['RU', 'CN', 'RO']
      feature['domain_length'] = len(row['name'])
      feature['rcode'] = row['rcode']
      features.append(feature)

    self.X = normalize(self.dv.fit_transform(features))

  def process(self):
    self.results = self.clf.fit_predict(self.X)

  def graph_output(self):
    mod_rows = []
    fills = {
      '1': '#1f77b4',
      '2': '#9467bd',
      '3': '#ff7f0e',
      '4': '#2ca02c',
      '5': '#e377c2',
    }
    with open('dns_cluster_data.js', 'w') as f:
      for row, prediction in itertools.izip(self.X_raw[:10], self.results[:10]):
        row['timestamp'] = datetime.fromtimestamp(float(row['timestamp'])).strftime("%c")
        row['latitude'] = float(row['lat'])
        row['longitude'] = float(row['long'])
        row['radius'] = 5
        row['country'] = row['country_code']
        row['fillKey'] = str(prediction)
        mod_rows.append(row)
      f.write("var data = %s;" % json.dumps(mod_rows))

if __name__ == '__main__':
  d = DNSClassifier('dns.json')
  d.process()
  d.graph_output()

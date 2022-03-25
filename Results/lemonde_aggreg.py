from bs4 import BeautifulSoup
import pandas as pd
import nltk
from collections import Counter
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import re
import sys

#ngram_length = int(sys.argv[1])


links = pd.read_csv("~/lemonde.csv")
dates = links.date.unique()
#dates = dates[25242:]
engine = create_engine('sqlite:///3gram_lemonde.db', echo = True)
engine2 = create_engine('sqlite:///4gram_lemonde.db', echo = True)

meta = MetaData()
monogram = Table(
	'gram', meta,
	Column('n', Integer),
	Column('gram', String),
	Column('annee', Integer),
	Column('mois',Integer),
	Column('jour',Integer)
 )

meta.create_all(engine)
meta.create_all(engine2)

def namefile(url):
	if "article/" in url:
		return url.split("article/")[1].replace("/","_")
	else:
		return url.split("/")[-1]


tokenizer = nltk.RegexpTokenizer(r"[a-zà-ÿ']+")

for date in dates:
	print(date)
	urls = links.table[links.date==date].values
	files = [namefile(url) for url in urls]
	text = ""
	for i,file in enumerate(files):
		page = open("/shared/projects/project_gallica/lemonde/"+file,"rb")
		page = page.read()
		pageSoup = BeautifulSoup(page, 'html.parser')
		title = pageSoup.find("title")
		if title is not None:
			text += title.text + "\n"
		sous_titre = pageSoup.find("p",{"class":"article__desc"})
		if sous_titre is not None:
			text += re.split("[<>]",str(sous_titre))[-3] + "\n"
		legendes_photo = pageSoup.find_all("figure",{"class":"article__media"})
		if legendes_photo is not None:
			text += "\n".join([i.img["alt"] for i in legendes_photo])
		if "live" in urls[i]:
			a = pageSoup.find_all("p",{"class":"post__live-container--answer-text post__space-node"})
		else:
			a = pageSoup.find_all("p", {"class": "article__paragraph"})
		text += '\n'.join([z.text for z in a]) + "\n"
	text_split = re.split('[!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~\n]',text.lower())
	ngrams = []
	for sentence in text_split:
		tokens = tokenizer.tokenize(sentence)
		ngrams += list(nltk.ngrams(tokens,3))
	matrix = pd.DataFrame.from_dict(Counter(ngrams),orient="index")
	matrix.columns = ["n"]
	matrix["gram"] = [' '.join(gram) for gram in matrix.index]
	matrix["annee"] = date.split("-")[0]
	matrix["mois"] = date.split("-")[1]
	matrix["jour"] = date.split("-")[2]
	matrix.to_sql("gram",engine,if_exists="append",index=False)
	ngrams = []
	if len(matrix.index)>1:
		for sentence in text_split:
			tokens = tokenizer.tokenize(sentence)
			ngrams += list(nltk.ngrams(tokens,4))
		matrix = pd.DataFrame.from_dict(Counter(ngrams),orient="index")
		matrix.columns = ["n"]
		matrix["gram"] = [' '.join(gram) for gram in matrix.index]
		matrix["annee"] = date.split("-")[0]
		matrix["mois"] = date.split("-")[1]
		matrix["jour"] = date.split("-")[2]
		matrix.to_sql("gram",engine2,if_exists="append",index=False)








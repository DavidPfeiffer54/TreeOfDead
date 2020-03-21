from collections import defaultdict 
import csv

input_file = csv.DictReader(open("in.csv"))

fout = open("test_out.csv", 'w')
headers = input_file.fieldnames
headers.append("songNumAct")
fout.write(",".join(headers) + "\n")

shows = defaultdict(lambda: defaultdict(list))
showSetLen = defaultdict(dict)


for row in input_file:
    shows[row["SSN"]][row["Setnum"]].append(row)

for show, sets in shows.items():
	for s, songs in sets.items():
		showSetLen[show]["setSongTot"+str(s)] = len(songs)


for show, sets in shows.items():
	for s, songs in sets.items():
		for song in songs:

			song["songNumAct"] = int(song["Song_Position"])
			if song["Setnum"] > 1:
				for i in range(1,int(song["Setnum"])):
					if "setSongTot"+str(i) in showSetLen[show]:
						song["songNumAct"] += showSetLen[show]["setSongTot"+str(i)]
					else:
						print("MISSING A SET : " + show)

			for h in headers:
				fout.write("\"" + str(song[h]) + "\"" + ",")
			fout.write("\n")


\
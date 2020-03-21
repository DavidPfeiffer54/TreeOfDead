from collections import defaultdict 
import csv

input_file = csv.DictReader(open("in.csv"))

fout = open("test_out.csv", 'w')
headers = input_file.fieldnames
headers.append("songNumAct")
fout.write(",".join(headers) + "\n")

shows = defaultdict(lambda: defaultdict(list))
showsInfo = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for row in input_file:
    shows[row["SSN"]][row["Setnum"]].append(row)

for show, sets in shows.items():
	for s, songs in sets.items():
		showsInfo[show]["setLens"][s] = len(songs)
		showsInfo[show]["setBreakouts"][s] = [int(song["Breakout"]) for song in songs]
	showsInfo[show]["totalSongs"] = sum(showsInfo[show]["setLens"].values())
	showsInfo[show]["totalBreakout"] = sum([sum(breaks) for breaks in showsInfo[show]["setBreakouts"].values()])


for show, sets in shows.items():
	for s, songs in sets.items():
		for song in songs:

			song["songNumAct"] = int(song["Song_Position"])
			if song["Setnum"] > 1:
				for i in range(1,int(song["Setnum"])):
					if str(i) in showsInfo[show]["setLens"].keys():
						song["songNumAct"] += showsInfo[show]["setLens"][str(i)]
					else:
						print("MISSING A SET : " + show)

			for h in headers:
				fout.write("\"" + str(song[h]) + "\"" + ",")
			fout.write("\n")


showOut = open("show_out.csv", "w")
showOut.write("show,showLen,set1Len,set2Len,set3Len,showBreakout,set1Breakout,set2Breakout,set3Breakout\n")
for show, info in showsInfo.items():
	showOut.write(str(show)+ ",")
	showOut.write(str(info["totalSongs"])+ ",")
	for i in range(1,4):
		showOut.write(str(info["setLens"][str(i)])+ ",")

	showOut.write(str(info["totalBreakout"])+ ",")
	for i in range(1,4):
		showOut.write(str(sum(info["setBreakouts"][str(i)]))+ ",")
		
	showOut.write("\n")



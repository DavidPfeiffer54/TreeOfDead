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
	showsInfo[show]["lineup"] = []
	showsInfo[show]["guests"] = []

	for s, songs in sets.items():

		for song in songs:
			if len(song["Lineup"]) > len(showsInfo[show]["lineup"]):
				showsInfo[show]["lineup"] = song["Lineup"]
			showsInfo[show]["guests"].append(song["Guests"])


		showsInfo[show]["setLens"][s] = len(songs)
		showsInfo[show]["setBreakouts"][s] = [int(song["Breakout"]) for song in songs]

		showsInfo[show]["set_total_song_segues"][s] = sum(1 if ">" in song["Current"] else 0 for song in songs)
		showsInfo[show]["set_total_song_stops"][s]  = sum(0 if ">" in song["Current"] else 1 for song in songs)
		showsInfo[show]["set_total_encore"][s]      = sum(1 if "E" in song["E:"] else 0 for song in songs)
		showsInfo[show]["set_kind"][s] = songs[0]["Set_kind"]

	showsInfo[show]["guests"] = set(showsInfo[show]["guests"])
	showsInfo[show]["totalSets"] = len(sets)
	showsInfo[show]["totalSongs"] = sum(showsInfo[show]["setLens"].values())

	showsInfo[show]["totalSongSegues"] = sum(showsInfo[show]["set_total_song_segues"].values())
	showsInfo[show]["totalSongsStops"] = sum(showsInfo[show]["set_total_song_stops"].values())
	showsInfo[show]["totalEncore"] = sum(showsInfo[show]["set_total_encore"].values())
	showsInfo[show]["totalBreakout"] = sum([sum(breaks) for breaks in showsInfo[show]["setBreakouts"].values()])
	showsInfo[show]["totalElectricSets"] = sum(1 if "E" in s else 0 for s in showsInfo[show]["set_kind"])
	showsInfo[show]["totalAcusticSets"] =  sum(1 if "A" in s else 0 for s in showsInfo[show]["set_kind"])


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
showOut.write("show,showLen,showStops,showSegues,showEncore,showBereakout,showSets,showSetsAcustic,showSetsElectric,")
showOut.write("set1Len,set1Stops,set1Segues,set1Breakouts,")
showOut.write("set2Len,set3Stops,set2Segues,set2Breakouts,")
showOut.write("set3Len,set3Stops,set3Segues,set3Breakouts,")
showOut.write("showType,linup,guests\n")

for show, info in showsInfo.items():
	showOut.write(str(show)+ ",")
	showOut.write(str(info["totalSongs"])+ ",")
	showOut.write(str(info["totalSongsStops"])+ ",")
	showOut.write(str(info["totalSongSegues"])+ ",")
	showOut.write(str(info["totalEncore"])+ ",")
	showOut.write(str(info["totalBreakout"])+ ",")
	showOut.write(str(info["totalSets"])+ ",")
	showOut.write(str(info["totalAcusticSets"])+ ",")
	showOut.write(str(info["totalElectricSets"])+ ",")

	for i in range(1,4):
		showOut.write(str(info["setLens"][str(i)])+ ",")
		showOut.write(str(info["set_total_song_stops"][str(i)])+ ",")
		showOut.write(str(info["set_total_song_segues"][str(i)])+ ",")
		showOut.write(str(sum(info["setBreakouts"][str(i)]))+ ",")

	if info["totalElectricSets"] > info["totalElectricSets"]:
		 showOut.write("Electric,")
	else:showOut.write("Acustic,")

	showOut.write(str(info["lineup"].replace(",", " "))+ ",")
	showOut.write(str(" ".join(list(showsInfo[show]["guests"])).replace(",",' '))+ ",")

	showOut.write("\n")



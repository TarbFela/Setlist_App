import bigjson
import string
from copy import deepcopy
from re import sub

def json_state_machine(file):
    _LOOKAHEAD_AMOUNT = 100
    c = 0
    for line in file:
        c += 1
        if c>10000: break
        line = sub(r'"relations":\[.*]', '', line)
        if '"type":"Song"' in line and 'title' in line:
            print(line, end="\t")

            title_pos = line.find("title")
            title = line[title_pos:title_pos + _LOOKAHEAD_AMOUNT]
            title = title.replace('"','').replace("}",'').replace("\n",'').split(",")[0].split(":")[1]
            print(f"\tTitle: {title}",end="\t")


            if '"genres":[{' in line:
                genre_pos = line.find("genre")
                genre = line[genre_pos:genre_pos + _LOOKAHEAD_AMOUNT]
                genre = genre.replace('"','').replace("}",'').replace("\n",'').split(",")[0].split(":")[1]
                print(f"\tGenre: {genre}",end="\t")
            if '"tags":[{' in line:
                genre_pos = line.find("genre")
                tags = line[genre_pos:genre_pos + _LOOKAHEAD_AMOUNT]
                tags = tags.replace('"','').replace("}",'').replace("\n",'').split(",")[0].split(":")[1]
                print(f"\ttags: {tags}",end="\t")
                print("TAG FOUND TAG FOUND TAG FOUND")
            print()







with open('work.json', 'r') as f:
    json_state_machine(f)





'''
fr = open('work.json', 'r')
fw = open('work_short.json', 'w')

w = ""
for i in range(1000):
    w += fr.readline()
fw.write(w)
fr.close()
fw.close()
'''
import sys
from jap_prereq_creator import ConceptMapper
import re

# 35882 54020

kanji_id = "35882"
words_id = "54020"

reference = [x.split(";") for x in open("id_reference.csv", "r").read().splitlines()]
words = {}
for line in reference[1:]:
    if line[1] == words_id:
        match = re.search("from ([^A-Za-z ]+) produce ([A-Za-z 0-9(（\"!…/　é)\-.,']+)", line[2])
        if match:
            word = match.group(1)
            if word not in words.keys():
                words[word] = {"read_id": line[0]}
            else:
                words[word] = {**words[word], "read_id": line[0]}
        else:
            match = re.search("from ([A-Za-z 0-9(（,　\"/…!é.\-')]+) produce ([^A-Za-z ]*)", line[2])
            word = match.group(2)
            if word not in words.keys():
                words[word] = {"prod_id": line[0]}
            else:
                words[word] = {**words[word], "prod_id": line[0]}
words_csv = [x.split(";") for x in open("all_words.txt", "r").readlines()]
for line in words_csv:
    kanji, pron, meaning = line
    if kanji in words:
        words[kanji] = {**words[kanji], "pron": pron, "kanji": kanji, "meaning": meaning.strip()}
mapper = ConceptMapper("id_reference.csv", kanji_id)
to_write = ""
i = 0
print(len(words.keys()))
for word in words.keys():
    prereqs = mapper.word_prereqs(word)
    prereqs = list(set(prereqs + mapper.word_prereqs(words[word]['pron'])))
    to_write += words[word]['read_id'] + ";" + " ".join(prereqs) + "\n"
    prod_prereqs = mapper.word_production_prereqs(word)
    prod_prereqs = list(set(prod_prereqs + mapper.word_production_prereqs(words[word]['pron'])))
    to_write += words[word]['prod_id'] + ";" + " ".join(prod_prereqs) + "\n"
    i += 1
    print(i/5872)
open("word_prereqs.txt", "w+").write(to_write.strip())
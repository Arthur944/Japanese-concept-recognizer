import sys
from jap_prereq_creator import ConceptMapper
import re

# 35882 54020

kanji_id = "293"
words_id = "490"

reference = [x.split(";") for x in open("id_reference.csv", "r").read().splitlines()]
words = {}
for line in reference[1:]:
    if line[1] == words_id:
        word = line[2]
        if word not in words.keys():
            words[word] = {"id": line[0]}
        else:
            if "duplicate_ids" in words[word]:
                words[word]["duplicate_ids"].append(line[0])
            else:
                words[word]["duplicate_ids"] = [line[0]]
words_csv = [x.split(";") for x in open("all_words.txt", "r").readlines()]
for line in words_csv:
    kanji, pron, meaning = line
    if kanji in words:
        if 'meaning' in words[kanji].keys():
            words[kanji] = {**words[kanji], "pron": pron, "kanji": kanji,
                            "meaning": ", ".join([x.strip() for x in list(set((words[kanji]['meaning'] + ", " +
                                                          meaning.strip()).split(",")))]).strip()}
        else:
            words[kanji] = {**words[kanji], "pron": pron, "kanji": kanji, "meaning": meaning.strip()}
meaning_dict = {}
for key in words.keys():
    meanings = [x.strip() for x in words[key]['meaning'].split(",")]
    for meaning in meanings:
        if meaning not in meaning_dict:
            meaning_dict[meaning] = [key]
        else:
            meaning_dict[meaning] = list(set(meaning_dict[meaning] + [key]))
mapper = ConceptMapper("id_reference.csv", kanji_id)
to_write = ""
i = 0
for word in words.keys():
    prereqs = mapper.word_prereqs(word)
    prereqs = list(set(prereqs + mapper.word_prereqs(words[word]['pron'])))
    prereqs = [x.split(",")[0] for x in prereqs]
    to_write += words[word]['id'] + ";" + " ".join(prereqs) + "\n"
    i += 1
open("word_prereqs.txt", "w+").write(to_write.strip())
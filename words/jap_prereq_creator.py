# Create cards from the supplied words
import re
import romkan

hiragana = "かたさははせけてへへくすつふふこそとほほきちしひひあならわまやえねれめうぬるむゆおのろをもよいにりみん"
katakana = "カタサハハセケテヘヘクスツフフコソトホホキチシヒヒアナラワマヤエネレメウヌルムユオノロヲモヨイニリミン"
romanji = ["ka", "ta", "sa", "ha", "ha", "se", 'ke', 'te', 'he', 'he', 'ku', 'su', 'tsu', 'fu', 'fu', 'ko', 'so',
           'to', "ho", "ho", "ki", "chi", "shi", "hi","hi", "a", "na", "ra", "wa", "ma", "ya", "e", "ne", "re", "me",
           "u", "nu", "ru", "mu", "yu", "o", "no", "ro", "wo", "mo", "yo", "i", "ni", "ri", "mi", "n"]
muddy_hiragana = "がだざばぱぜげでべぺぐずづぶぷごぞどぼぽぎぢじびぴ"
muddy_katakana = "ガダザバパゼゲデベペグズヅブプゴゾドボポギヂジビピ"


class Concept:
    def __init__(self, id, name, character, muddy=None):
        self.id = id
        self.name = name
        self.character = character
        self.muddy = muddy


class ConceptMapper:
    def __init__(self, concept_reference, kanji_id):
        lines = open(concept_reference, "r", encoding="utf-8").readlines()
        self.kana = []
        self.additional_sounds_id = None
        self.little_tsu_id = None
        self.long_vowel_id = None
        self.y_vowel_id = None
        self.concepts = [{"id": x.split(";")[0], "parent_id": x.split(";")[1], "name": x.split(";")[2]} for x in lines[1:]]
        for line in lines[1:]:
            id, parent_id, name = line.split(";")
            name = name.strip()
            character = re.search('from (.*) produce', name)
            if character and character.group(1) in hiragana:
                character = character.group(1)
                if hiragana.index(character) < 25:
                    self.kana.append(Concept(id, name, character, muddy=muddy_hiragana[hiragana.index(character)]))
                self.kana.append(Concept(id, name, character))
            elif character and character.group(1) in katakana:
                character = character.group(1)
                if katakana.index(character) < 25:
                    if len(katakana) > katakana.index(character) + 1 and katakana[katakana.index(character) + 1] == character:
                        self.kana.append(Concept(id, name, character, muddy=muddy_katakana[katakana.index(character) + 1]))
                    self.kana.append(Concept(id, name, character, muddy=muddy_katakana[katakana.index(character)]))
                self.kana.append(Concept(id, name, character))
            if 'Voiced' in name:
                self.additional_sounds_id = id
            if name == "Little tsu":
                self.little_tsu_id = id
            if name == "Long vowel sound":
                self.long_vowel_id = id
            if name == "Y vowel sound":
                self.y_vowel_id = id
        readings = {}
        for line in [x.split(";") for x in lines[1:]]:
            if line[1] == kanji_id:
                match = re.search("from (.*?) produce (.*)", line[2])
                one, other = match.group(1), match.group(2)
                if len(one) == 1 and re.search("[A-Za-z0-9]", one) is None:
                    readings[one] = Concept(line[0], other, one)
        self.kanji_readings = readings
        produces = {}
        for line in lines[1:]:
            if line[1] == kanji_id:
                match = re.search("from (.*?) produce (.*)", line[2])
                one, other = match.group(1), match.group(2)
                if len(other) == 1 and re.search("[A-Za-z0-9]", other) is None:
                    produces[other] = Concept(line[0], one, other)
        self.kanji_productions = produces

    def concepts_to_character(self, character):
        if character == "っ":
            return [self.little_tsu_id]
        if character == "ー":
            return [self.long_vowel_id]
        if character in "ゃゅょャュョ":
            return [self.y_vowel_id]
        for concept in self.kana:
            if concept.character == character:
                return [concept.id]
            if concept.muddy == character:
                return [concept.id, self.additional_sounds_id]
        if character in self.kanji_readings.keys():
            return [self.kanji_readings[character].id]
        return []

    def word_prereqs(self, word):
        prereqs = []
        for character in word:
            prereqs += self.concepts_to_character(character)
        return list(set(prereqs))

    def word_production_prereqs(self, word):
        prod_prereqs = []
        prereqs = self.word_prereqs(word)
        for prereq in prereqs:
            concept = self.concepts[[x['id'] for x in self.concepts].index(prereq)]
            # reverse concept name
            name = re.sub("from (.*?) produce (.*)", r"from \2 produce \1", concept['name'])
            # find id from concept name
            prod_prereqs.append(self.concepts[[x['name'] for x in self.concepts].index(name)]['id'])
        return prod_prereqs

    def word_to_romanji(self, word):
        return romkan.to_roma(word)

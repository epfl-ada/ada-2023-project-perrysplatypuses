import spacy

nlp = spacy.load("en_core_web_md")


SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]
ADJECTIVES = ["acomp", "advcl", "advmod", "amod", "appos", "nn", "nmod", "ccomp", "complm",
              "hmod", "infmod", "xcomp", "rcmod", "poss"," possessive"]


def character_names_from_text(plot_text):
    doc = nlp(plot_text)
    ents = [(e.start, e.end, e.text) for e in doc.ents if e.label_ == 'PERSON']
    character_names = set()
    for i in range(len(ents)):
        t = doc[ents[i][0]]
        if (t.pos_ == 'PROPN'):
            character_names.add(ents[i][2])
    
    ents = character_names.copy()
    for e in ents:
        if len(e.split())>1:
            for s in e.split():
                character_names.discard(s)
    return character_names
    
    
def character_names_parts(character_names):
    character_names_dict = dict()
    for name in character_names:
        character_names_dict[name] = name
        for s in name.split():
            character_names_dict[s] = name
    return character_names_dict


def character_attributes_from_text(plot_text):
    character_names = character_names_from_text(plot_text)
    doc = nlp(plot_text)
    parts_to_full_names = character_names_parts(character_names)
    character_names = parts_to_full_names.keys()

    character_attributes = {}
    for sent in doc.sents:
        for tok in sent:
            character = None
            adj = None

            if tok.text in character_names:
                if tok.dep_ == "appos":
                    character = tok.text
                    adj = tok.head.text
            elif tok.dep_ in ADJECTIVES:
                if tok.head.text in character_names:
                    character = tok.head.text
                    adj = tok.text

            if character:
                name = parts_to_full_names[character]
                if name not in character_attributes:
                    character_attributes[name] = []
                character_attributes[name].append(adj)
    return character_attributes

def character_active_verbs_from_text(plot_text):
    character_names = character_names_from_text(plot_text)
    doc = nlp(plot_text)
    parts_to_full_names = character_names_parts(character_names)
    character_names = parts_to_full_names.keys()

    character_active_verbs = {}
    for sent in doc.sents:
        verbs = [tok for tok in sent if tok.pos_ == "VERB"]
        for v in verbs:
            subs = [tok for tok in v.lefts if tok.dep_ in SUBJECTS and tok.pos_ != "DET"]
            for tok in subs:
                if tok.text in character_names:
                    name = parts_to_full_names[tok.text]

                    if name not in character_active_verbs:
                        character_active_verbs[name] = []
                    character_active_verbs[name].append(v.text)
    return character_active_verbs

def character_patient_verbs_from_text(plot_text):
    character_names = character_names_from_text(plot_text)
    doc = nlp(plot_text)
    parts_to_full_names = character_names_parts(character_names)
    character_names = parts_to_full_names.keys()

    character_patient_verbs = {}
    for sent in doc.sents:
        verbs = [tok for tok in sent if tok.pos_ == "VERB"]
        for v in verbs:
            objs = [tok for tok in v.rights if tok.dep_ in OBJECTS]
            for tok in objs:
                if tok.text in character_names:
                    name = parts_to_full_names[tok.text]

                    if name not in character_patient_verbs:
                        character_patient_verbs[name] = []
                    character_patient_verbs[name].append(v.text)
    return character_patient_verbs
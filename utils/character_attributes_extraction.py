import spacy

nlp = spacy.load("en_core_web_md")


SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]
ADJECTIVES = [
    "acomp",
    "advcl",
    "advmod",
    "amod",
    "appos",
    "nn",
    "nmod",
    "ccomp",
    "complm",
    "hmod",
    "infmod",
    "xcomp",
    "rcmod",
    "poss",
    " possessive",
]


def add_attribute(name, attr, character_dict):
    if name not in character_dict:
        character_dict[name] = []
    character_dict[name].append(attr)


def get_verbs(sent):
    return [tok for tok in sent if tok.pos_ == "VERB"]


def get_subj(v):
    subj = [tok for tok in v.lefts if tok.dep_ in SUBJECTS and tok.pos_ != "DET"]
    conj_subj = []
    for s in subj:
        conj_subj.extend([tok for tok in s.rights if tok.dep_ == "conj"])
    return subj + conj_subj


def get_obj(v):
    obj = [tok for tok in v.rights if tok.dep_ in OBJECTS]
    conj_obj = []
    for o in obj:
        conj_obj.extend([tok for tok in o.rights if tok.dep_ == "conj"])
    return obj + conj_obj


def get_conj_verbs(v):
    return [tok for tok in v.rights if tok.dep_ == "conj" and tok.pos_ == "VERB"]


def character_names_from_text(plot_text):
    doc = nlp(plot_text)
    ents = [(e.start, e.end, e.text) for e in doc.ents if e.label_ == "PERSON"]
    character_names = set()
    for i in range(len(ents)):
        full_name = True
        for j in range(ents[i][0], ents[i][1]):
            t = doc[j]
            if t.pos_ == "PROPN" and t.text.isalpha():
                character_names.add(t.text)
            else:
                full_name = False
        if full_name:
            character_names.add(ents[i][2])
            

    ents = character_names.copy()
    for e in ents:
        if len(e.split()) > 1:
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
    character_attributes = {}

    character_names = character_names_from_text(plot_text)
    doc = nlp(plot_text)
    parts_to_full_names = character_names_parts(character_names)
    character_names = parts_to_full_names.keys()

    for sent in doc.sents:
        for tok in sent:
            if tok.text in character_names:
                name = parts_to_full_names[tok.text]
                if tok.dep_ == "appos":
                    add_attribute(name, tok.head.lemma_, character_attributes)
                for child in tok.children:
                    if child.dep_ in ADJECTIVES:
                        add_attribute(name, child.lemma_, character_attributes)

    return character_attributes


def character_active_verbs_from_text(plot_text):
    character_active_verbs = {}

    character_names = character_names_from_text(plot_text)
    doc = nlp(plot_text)
    parts_to_full_names = character_names_parts(character_names)
    character_names = parts_to_full_names.keys()

    for sent in doc.sents:
        verbs = get_verbs(sent)
        for v in verbs:
            subs = get_subj(v)
            conj_verbs = get_conj_verbs(v)
            for tok in subs:
                if tok.text in character_names:
                    name = parts_to_full_names[tok.text]
                    add_attribute(name, v.lemma_, character_active_verbs)
    return character_active_verbs


def character_patient_verbs_from_text(plot_text):
    character_patient_verbs = {}

    character_names = character_names_from_text(plot_text)
    doc = nlp(plot_text)
    parts_to_full_names = character_names_parts(character_names)
    character_names = parts_to_full_names.keys()

    for sent in doc.sents:
        verbs = get_verbs(sent)
        for v in verbs:
            objs = get_obj(v)
            conj_verbs = get_conj_verbs(v)
            for tok in objs:
                if tok.text in character_names:
                    name = parts_to_full_names[tok.text]
                    add_attribute(name, v.lemma_, character_patient_verbs)
    return character_patient_verbs


def word2vec(w):
    """Get vector representation of the word"""
    return nlp(w).vector


def attributes2vec(r):
    """
    Get vector representation for all the words attributes of the character.
    Returns 3 arrays for ajectives, active verbs and patient verbs.
    """
    adj = []
    active = []
    patient = []
    for w in r["adj"]:
        if w:
            adj.append(word2vec(w))
    for w in r["active"]:
        if w:
            active.append(word2vec(w))
    for w in r["patient"]:
        if w:
            patient.append(word2vec(w))
    return adj, active, patient

def attributes_extraction(
        path_to_plots = 'data/MovieSummaries/plot_summaries.txt'
):
    
    plots =  pd.read_csv(
    path_to_plots, 
    sep='\t', 
    names=['wiki_id', 'plot']
    )

    plots['plot'] = plots['plot'].apply(lambda x: ' '.join(x.split()))
    character_list = []

# for every plot we find characters and their dependencies in 3 groups: attributes, active verbs and patient verbs and save it to csv file
    for index, row in tqdm([row for row in plots.iterrows()]):
        plot = row['plot'] 
        character_names = character_names_from_text(plot)
        character_attributes = character_attributes_from_text(plot)
        character_active_verbs = character_active_verbs_from_text(plot)
        character_patient_verbs = character_patient_verbs_from_text(plot)
        for name in character_names:
            character_list.append(
                {
                    'wiki_id': row['wiki_id'],
                    'character': name,
                    'adj': character_attributes.get(name, []),
                    'active': character_active_verbs.get(name, []),
                    'patient': character_patient_verbs.get(name, []),
                }
            )

    character_df = pd.DataFrame(character_list)
    character_df.to_csv('data/character_attributes.csv')
    character_df[character_df['active'].map(len)>5]

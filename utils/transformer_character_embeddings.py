from transformers import AutoTokenizer, BertModel
import torch
from utils.character_attributes_extraction import character_names_from_text, character_names_parts

def embeddings_from_text(plot_text):
    """returns dict with embeddings for each character"""
    characters = character_names_parts(character_names_from_text(plot_text))
    sents = plot_text.split('. ')

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    
    character_emb_dict = {}
    character_count = {}
    for s in sents:
        inputs_and_mapping = tokenizer(s, return_tensors="pt", return_offsets_mapping=True)
        inputs = {i:inputs_and_mapping[i] for i in inputs_and_mapping if i!='offset_mapping'}
        offset_mapping = inputs_and_mapping['offset_mapping'][0][:, 1]
        outputs = model(**inputs)

        last_hidden_states = outputs.last_hidden_state

        for name in character_names_from_text(s):
            v = s.index(name) + len(name)
            idx = torch.where(offset_mapping == v)[0]
            if len(idx) > 0:
                idx = idx.item()
            else:
                continue
            temp_emb = last_hidden_states[0][idx] # embedding of the last token of the name

            if name in characters:
                if characters[name] in character_emb_dict:
                    character_emb_dict[characters[name]] += temp_emb
                    character_count[characters[name]] += 1
                else:
                    character_emb_dict[characters[name]] = temp_emb
                    character_count[characters[name]] = 1

    # compute mean of all the embeddings for one character
    for k in character_emb_dict.keys():
        character_emb_dict[k] /= character_count[k]
    return character_emb_dict

from collections import defaultdict
import json 

def visualize_spacy_ents(full_text):
    global nlp, spacy
    if not('nlp' in globals() and type(nlp) == spacy.lang.en.English):
        import spacy
        nlp = spacy.load('en')
        
    spacy_document = nlp(full_text)
    spacy.displacy.render(spacy_document, style='ent')
    return spacy_document

def group_by_labels(list_of_tuples):
    group_of_labels = defaultdict(list)
    for i in list_of_tuples:
        assert len(i) > 1
        group_of_labels[i[-1]].append(i[:-1])
    return group_of_labels

def view_one_doc(combined_csv, doc_index):
    from data_preprocess import clean_text

    print('Path:', combined_csv.filepath.values[doc_index])
    target_labels = dict(combined_csv.iloc[doc_index, :-2])
    print(json.dumps(target_labels, indent=2))
    full_text = combined_csv.text.values[doc_index]
    visualize_spacy_ents(full_text)






from collections import defaultdict

def test_docx_module_on_folder(folder_path): #goes into utilities
    """check if docx module is able to open files in folder_path"""
    import docx
    from tqdm import tqdm
    error_files = []
    training_files_path = get_files_path(folder_path)
    i, j = 0, 0
    for doc_path in tqdm(training_files_path):
        try:
            document = docx.Document(doc_path)
            for paragraphs in document.paragraphs:
                paragraphs.text
        except:
            error_files(doc_path)
            j += 1
        i += 1

    print(f'Successfully parsed {i-j} documents out of {i} documents')
    
    return error_files




def visualize_spacy_ents(full_text):
    global nlp, spacy
    if not('nlp' in globals() and type(nlp) == spacy.lang.en.English):
        import spacy
        nlp = spacy.load('en')
        
    spacy_document = nlp(full_text)
    spacy.displacy.render(spacy_document, style='ent')
    return spacy_document

# clean_text
# write rules
### cleaning rules section start ###


import string

def remove_repeated_punctuations(text):
    for i in string.punctuation:
        while i*2 in text:
            text = text.replace(i*2, i)
    return text

def remove_multiple_next_lines(text):
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')    
    return text

def remove_noisy_puctuations(text):
    punct_to_keep = ',.:)(-/' 
    punct_to_remove = [i for i in string.punctuation if i not in punct_to_keep]
    all_chars = list(set(text))
    for i in all_chars:
        if ord(i) > 126 or i in punct_to_remove:
            text = text.replace(i, '')
    return text

def remove_multiple_spaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def remove_tab_with_four_spaces(text):
    while '\t' in text:
        text = text.replace('\t', '    ')    
    return text

def merge_shorter_paragraphs(text):
    paragraphs = text.split('\n\n')
    final_paragraphs = []
    buffer = ''
    for para in paragraphs:
        
        para = para.replace('\n', ' ')
        if len(para) < 40:
            buffer += ' ' + para
        
        else:
            buffer += ' ' + para
            final_paragraphs.append(buffer.strip())
            buffer = ''
            
    return '\n\n'.join(final_paragraphs)   

### cleaning rules section ends ###

def clean_text(text):    
    text = remove_repeated_punctuations(text)
    text = remove_multiple_next_lines(text)
    text = remove_noisy_puctuations(text)
    text = remove_multiple_spaces(text)
    text = remove_tab_with_four_spaces(text)
    
    text = merge_shorter_paragraphs(text)
    
    
    return text.strip()

def group_by_labels(list_of_tuples):
    group_of_labels = defaultdict(list)
    for i in list_of_tuples:
        assert len(i) > 1
        group_of_labels[i[-1]].append(i[:-1])
    return group_of_labels

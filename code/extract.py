import re

def get_index_of(regex_pattern=None, subject_strings=None):    
#     print(subject_string, regex_pattern)
    j=0;
    extracted_texts_and_span = []

    for ind, subject_string in enumerate(subject_strings):
#         print(subject_string)
        subject_string = subject_string.lower()
        for i in re.finditer(regex_pattern, subject_string):
            j+=1
            # print(f'-->in:ind {ind} At:', i.start(), i.end(), 'extracted', i.group())
            extracted_texts_and_span.append([i.group(0), (i.start(), i.end()), ind])
#             extracted_texts_and_span.append(i)
            
    # print(j)
    return extracted_texts_and_span

def extract_date_spans(text):
    months_and_abbr = '|'.join('january february march april may june july august september october november december'.split())
    months_and_abbr += '|'+'|'.join('jan feb mar apr may jun jul aug sept sep oct nov dec'.split())

    regex_pattern1 = r'(\d{1,4})(.{0,10}?)('+months_and_abbr+')(.{0,5}?)(\d{4})'
    regex_pattern2 = r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})'
    
    span_collection1 = get_index_of(regex_pattern1, [text])
    span_collection2 = get_index_of(regex_pattern2, [text])
    
    span_collection1.extend(span_collection2)
    span_collection1.sort(key=lambda x: x[1][0])
    return span_collection1

def extract_timedelta(text):
    regex_pattern3 = r'(.{0,5}\d{2}(.{0,3}?)(month|days).{0,20})' # useful for end date    
    return get_index_of(regex_pattern3, [text])


def extract_amount_spans(text):
    regex_for_digits = '|'.join('one two three four five six seven eight nine zero'.split())
    regex_two_digit = '|'.join('eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen ninteen twenty\
     thirty fourty fifty sixty seventy eighty ninety'.split())
    regex_orders = '|'.join('hundred thousand'.split())
    regex_for_numeric = r'[0-9]{1,2}'
    regex_for_numbers = '|'.join([regex_for_digits, regex_two_digit, regex_orders, regex_for_numeric])
    
    # print(get_index_of(regex_for_numbers, [text])[0])
    # spans = [(start, end) for i, (start, end), k in get_index_of(regex_for_numbers, [text])]
    spans = get_index_of(regex_for_numbers, [text])
    return spans


def extract_name_spans(text):
    # this is done with spacy not with regex
    import spacy
    nlp = spacy.load('en')
    spacy_doc = nlp(text)
    ent_spans = [[ent, (ent.start_char, ent.end_char), 1] for ent in spacy_doc.ents if ent.label_ in ['PERSON','ORG', 'PRODUCT']]
    noun_chunks_span = [[ent, (ent.start_char, ent.end_char), 1] for ent in spacy_doc.noun_chunks]
    
    ent_spans.extend(noun_chunks_span)
    ent_spans.sort(key=lambda x: x[1][0])
    
    return ent_spans



def extract_continuous_span(spans):
    '''merging spans that are 4 character apart, extracted with same regex'''
    
    # assert all of them from same paragraph
    if len(spans) == 0: return None
    assert set([para_no for ent, (start, end), para_no in spans]).__len__() == 1
    spans = [(start, end) for ent, (start, end), para_no in spans]
    final_spans = []
    curr_start, curr_end = spans[0]
    
    
    for new_start, new_end in spans[1:]:
        if new_start - curr_end > 4:
            final_spans.append([curr_start, curr_end])
            curr_start = new_start
            
        curr_end = new_end
    
    final_spans.append([curr_start, curr_end])
    # for start, end in final_spans:
    #     print(text[start:end])
    return final_spans
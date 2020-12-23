import numpy as np
# add features and labels for each candidate

def not_nan(a_variable):
    if a_variable is None: return False
    if a_variable == 'NA': return False
    if isinstance(a_variable, str):return True
    try:
        if np.isnan(a_variable): return False
    except:
        print('nan np: ',a_variable)
    
    
    return True


def label_date_candidates(candidates, date_labels):
    date_labels = [date_label for date_label in date_labels if not_nan(date_label)]
    date_labels_month_year = ['_'.join(map(str, (map(int, label.split('.')[1:])))) for label in date_labels]
    candidates_month_year = ['_'.join(map(str, (k[1:]))) if k is not None else k for i, j, k in candidates]
    matches = [candidate in date_labels_month_year for candidate in candidates_month_year]
    return list(zip(candidates, matches))


def label_duration_candidates(candidates, start_date, end_date, notice):
    if not (not_nan(start_date) and not_nan(end_date) and not_nan(notice)):
        return [(candidate, False) for candidate in candidates]
    if not_nan(start_date) and not_nan(end_date):
        day_start, month_start, year_start, day_end, month_end, year_end = list(map(int, (start_date+'.'+end_date).split('.')))
        days_difference = (month_end - month_start) * 30 + (year_end - year_start) * 365 + (day_end - day_start)
    else:
        days_difference = 10_000
    if not not_nan(notice):
        notice = 10_000
    
    def valid_candidate(candidate):
        if candidate is None:
            return False
        if candidate > 30*5 and abs(days_difference - (candidate+30)) < 36:
            return "end_date"
        if abs(candidate - int(notice)) < 6:
            return 'notice'
        return False
    
    return [(candidate, valid_candidate(candidate[-1])) for candidate in candidates]


def label_name_candidates(candidates, name_labels):
    from data_preprocess import super_clean
    name_labels = [name_label for name_label in name_labels if not_nan(name_label)]
    ifmatch = lambda candidate: any([i in candidate for i in name_labels]) or\
     any([super_clean(i) in super_clean(candidate) for i in name_labels])
    
    return [(candidate, ifmatch(candidate[-1])) for candidate in candidates]

def mse(x, y):
    return ((x - y)**2)/(x**2+y**2)

def label_amount_candidates(candidates, value):
    if not_nan(value):
        value = float(value)
    else: value = 30_000_000
    return [[candidate, isinstance(candidate[-1], int) and mse(int(candidate[-1]), value) < 0.05] for candidate in candidates]
    


def label_candidates(candidates, labels=False):
    if not labels:
        return dict([(i, [[candidate, False] for candidate in candidates_]) for i, candidates_ in candidates.items()])

    date_labels = labels['Aggrement Start Date'], labels['Aggrement End Date']
    start_date, end_date = date_labels
    notice = labels['Renewal Notice (Days)']
    name_labels = labels['Party One'], labels['Party Two']
    amount_labels = labels['Aggrement Value']
    
    date_candidates = candidates['date']
    duration_candidates = candidates['duration']
    name_candidates = candidates['names']
    amount_candidates = candidates['amount']
    
    
    labelled_date_candidates = label_date_candidates(date_candidates, date_labels)
    labelled_duration_candidates = label_duration_candidates(duration_candidates, start_date, end_date, notice)
    labelled_amount_candidates = label_amount_candidates(amount_candidates, amount_labels)
    labelled_name_candidates = label_name_candidates(name_candidates, name_labels)
    
    return dict(
        date=labelled_date_candidates,
        duration=labelled_duration_candidates,
        amount=labelled_amount_candidates,
        names=labelled_name_candidates)
    

def flatten_labelled_candidates(candidates):
    candidates_list = []
    
    label_dictionary = {
        ('date', False): 'DATE_FALSE',
        ('date', True): 'DATE_TRUE',
        ('names', False): 'NAME_FALSE',
        ('names', True): 'NAME_TRUE',
        ('amount', False): 'AMOUNT_FALSE',
        ('amount', True): 'AMOUNT_TRUE',
        ('duration', False): 'DURATION_FALSE',
        ('duration', 'end_date'): 'DURATION_END_DATE',
        ('duration', 'notice'): 'DURATION_NOTICE'
    }

    for type_, candidates_ in candidates.items():
        for candidate in candidates_:
            label = label_dictionary[type_, candidate[-1]]
            start_end = candidate[0][1]
            candidates_list.append(dict(
                candidate=candidate,
                span_char_index=start_end,
                type=type_,
                label=label,
                features=None))
    
    return candidates_list

def get_closest_spacy_span(span, starts, ends):
    start, end = span 
    better_start = [i for i in starts if i<=start][-1]
    better_end = [i for i in ends if i>=end][0]
    return better_start, better_end

def get_spacy_vector_as_feature(candidates_list, full_text, lm=None, meta=None):
    import spacy
    nlp = lm or spacy.load('en')
    doc = nlp(full_text)
    starts_ends = start_end = [(i.idx, i.idx+len(i.text)) for i in doc]
    starts, ends = list(zip(*start_end))

    for candidate in candidates_list:
        span = candidate['span_char_index']
        spacy_span = span
        
        doc_span = doc.char_span(*spacy_span)
        if doc_span is None:
            spacy_span = get_closest_spacy_span(span, starts, ends)
            doc_span = doc.char_span(*spacy_span)
        
        vector = doc_span.vector

        features = candidate['features'] or {}
        features.update(dict(spacy_vector=vector))
        candidate['features'] = features
        candidate['spacy_span'] = spacy_span
        candidate['meta'] = meta

    return candidates_list


def get_candidates_features_and_labels_all_together(combined_csv):
    from extract_and_normalize import extract_candidates
    from tqdm import tqdm 
    texts = combined_csv.text
    candidates_global = [extract_candidates(text) for text in tqdm(texts, 'Extracting...')]

    labels_columns = ['Aggrement Value', 'Aggrement Start Date',
       'Aggrement End Date', 'Renewal Notice (Days)', 'Party One', 'Party Two']
    label_csv = combined_csv[labels_columns]
    labels = [dict(zip(labels_columns, i)) for i in label_csv.values]

    candidates_global_with_labels = [label_candidates(candidates, label) for candidates, label in tqdm(zip(candidates_global, labels), 'Labeling...')]

    flattened_candidates_with_features_labels = []
    for i, (text, candidates) in tqdm(enumerate(list(zip(texts, candidates_global_with_labels))), 'Featuring...'):
        flattened_candidates = flatten_labelled_candidates(candidates)
        meta = dict(text_no=i)
        flattened_candidates_with_features = get_spacy_vector_as_feature(flattened_candidates, text, meta=meta)
        flattened_candidates_with_features_labels.extend(flattened_candidates_with_features)
    
    return flattened_candidates_with_features_labels

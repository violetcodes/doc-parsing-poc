import re, string
import datetime
from data_preprocess import is_valid_date

import word2number.w2n as w2n 

# regex patterns 
months_and_abbr = '|'.join('january february march april may june july august september october november december'.split())
months_and_abbr += '|'+'|'.join('jan feb mar apr may jun jul aug sept sep oct nov dec'.split())

day_month_year_alnum_pattern = r'(\d{1,4})(.{0,10}?)('+months_and_abbr+')(.{0,5}?)(\d{4})' # <ith> day of the <month>, <year> pattern
day_month_year_numeric_pattern = r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})' # 1/2/2013 like



digit_alpha = '|'.join('one two three four five six seven eight nine zero'.split())
two_digit_alpha = '|'.join('eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen ninteen twenty\
 thirty fourty fifty sixty seventy eighty ninety'.split())
cent_alpha = '|'.join('hundred thousand'.split())
numeric = r'([0-9]{1,2})'
any_numbers = '|'.join([digit_alpha, two_digit_alpha, cent_alpha, numeric])

duration_pattern = r'(' + any_numbers + '{2})(.{0,10}?)(month|days)' # 11 months

string_to_numeric_map = {'one': 1, 'two': 2, 'three': 3,
                        'four': 4, 'five': 5, 'six': 6,
                        'seven': 7, 'eight': 8, 'nine': 9,
                        'eleven': 11, 'twelve': 12, 'thirteen': 13,
                        'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
                        'seventeen': 17, 'eighteen': 18, 'ninteen': 19,
                        'twenty': 20, 'thirty': 30, 'fourty': 40,
                        'fifty': 50, 'sixty': 60, 'seventy': 70,
                        'eighty': 80, 'ninety': 90}
hundred_and_thousand = 'hundred thousand'.split()

## normalize extracted patterns

def get_num_from_side_char_wise(split_text, which_side='left'):    
    all_found = re.findall(r'\d{1,4}', split_text)
    return all_found[-1] if which_side=='left' else all_found[0]

def get_num_from_side(split_text, which_side='left'):
    '''let's say you have 'for 30 days he gains 89 pounds', which is a left split of a string
    and you wand to extract rightest num'''    
    words_ = reverse_left_words = split_text.split()
    
    if which_side == 'left':
        words_ = words_[::-1]
    
    numbers_as_text = list(string_to_numeric_map.keys()) + hundred_and_thousand
    
    free_punct = lambda word: ''.join([i for i in word if i not in string.punctuation])
    result = 'NA'
    for i, word in enumerate(words_):
        if free_punct(word) in numbers_as_text:
            j = i + 1
            while j<len(words_) and free_punct(words_[j]) in numbers_as_text:
                j+=1
            result = words_[i:j]
            break
        elif free_punct(word).isdecimal():
            j = i + 1
            while j<len(words_) and free_punct(words_[j]).isdecimal():
                j+=1
            result = words_[i:j]
            break
        
    if isinstance(result, str):
        return result
    
    if which_side == 'left':
        return ' '.join([free_punct(i) for i in result[::-1]])    
    return ' '.join([free_punct(i) for i in result])

def get_rightest_num(text):
    return get_num_from_side(text, which_side='left')

def get_leftest_num(text):
    return get_num_from_side(text, which_side='right')

def normalize_duration(extracted_text):
    """duration or period in days"""
    if 'days' in extracted_text:
        num_left = get_rightest_num(extracted_text.split('days')[0])
        type_ = 'days'
    elif 'month' in extracted_text:
        num_left = get_rightest_num(extracted_text.split('month')[0]) 
        type_ = 'month'
    
    if num_left.isdecimal():
        return float(num_left) * 30 if type_ == 'month' else float(num_left)
    else:
        try: return w2n.word_to_num(num_left) * 30 if type_ == 'month' else w2n.word_to_num(num_left)
        except:
            return None


def get_normal_date_day_month_year_alnum(extracted_text):
    # from pattern1 e.g ith day of <month>, year
    global month_and_abbr
    months_and_abbr_splitted = months_and_abbr.split('|')
    month = [i for i in months_and_abbr_splitted if i in extracted_text][0]
    left_split, right_split = extracted_text.split(month)[:2]
    
    number_from_left = get_rightest_num(left_split)
    if number_from_left == 'NA':
        number_from_left = get_num_from_side_char_wise(left_split, which_side='left')
    

    number_from_right = get_leftest_num(right_split)
    if number_from_right == 'NA':
        number_from_left = get_num_from_side_char_wise(right_split, which_side='right')
    
    # print('number from left and right', number_from_left, number_from_right)
    
    
    if number_from_left.isdecimal():
        day = int(number_from_left)

    else:
        try:
            day = w2n.word_to_num(number_from_left)
        except:
            # print('error')
            return None
    
    if number_from_right.isdecimal():
        year = int(number_from_right)
    else:
        try:
            year = w2n.word_to_num(number_from_right)
        except:
            # print('error')
            return None
    
    month_map = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
                'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sept': 9,
                'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

    
    month = month_map[month]
    # is_valid_date(day, month, year)
    
    return [day, month, year]

def get_normal_date_day_month_year_numeric(extracted_text):
    '''for patterns like dd/mm/yyyy or yyyy/mm/dd or mm/dd/yyyy'''
    splitter = [i for i in '.\-/' if i in extracted_text][0]    
    left, center, right = list(map(int, extracted_text.split(splitter)))
    # if it's dd mm yyyy
    if is_valid_date(left, center, right):
        return [left, center, right]
    elif is_valid_date(center, left, right):
        return [center, left, right]
    elif is_valid_date(right, center, left):
        return [right, center, left]    
    else:
        return None

def normalize_amount(text):
    "extracted text converted to a numeric value"
    text_ = text.lower()
    text_ = text.split('.')[0]
    text_ = ''.join([i for i in text_ if i not in string.punctuation])
    if text_.isdecimal(): return int(text_)
    else:
        try:
            return w2n.word_to_num(text_)
        except:
            return 'NA'

## Extract with patterns
def extract_timedelta(text):
    text = text.lower()
    text_and_spans = extract_with_pattern(duration_pattern, text)
    # print(text_and_spans)
    return [[i, j, normalize_duration(i)] for i, j in text_and_spans]

def extract_continuous_span(spans):
    '''merging spans that are 4 character apart, extracted with same regex'''    
    # assert all of them from same paragraph
    final_spans = []
    curr_start, curr_end = spans[0]   
    
    for new_start, new_end in spans[1:]:
        if new_start - curr_end > 2:
            final_spans.append([curr_start, curr_end])
            curr_start = new_start
            
        curr_end = new_end    
    final_spans.append([curr_start, curr_end])
    # for start, end in final_spans:
    #     print(text[start:end])
    return final_spans

def extract_amount_spans(text):
    spans = extract_with_pattern(any_numbers, text)
    spans_ = [(start, end) for ent, (start, end) in spans]
    spans_ = extract_continuous_span(spans_)
    extracted = [[text[start:end], (start, end)] for start, end in spans_]
    extracted_normalized = [[i, j, normalize_amount(i)] for i, j in extracted]
    return extracted_normalized

def extract_name_spans(text):
    # this is done with spacy not with regex
    import spacy
    nlp = spacy.load('en')
    spacy_doc = nlp(text)
    ent_spans = list(set([(ent.text, (ent.start_char, ent.end_char), ent.text) for ent in spacy_doc.ents if ent.label_ in ['PERSON','ORG', 'PRODUCT']]))
    noun_chunks_span = list(set([(ent.text, (ent.start_char, ent.end_char), ent.text) for ent in spacy_doc.noun_chunks]))
    ent_spans.extend(noun_chunks_span)
    ent_spans.sort(key=lambda x: x[1][0])

    return ent_spans

def extract_with_pattern(regex_pattern=None, subject_string=None):    
    # print(subject_string, regex_pattern)
    subject_string = subject_string.lower()
    extracted_texts_and_span = []
    for i in re.finditer(regex_pattern, subject_string):
        # print(f'-->in:ind {ind} At:', i.start(), i.end(), 'extracted', i.group())
        extracted_texts_and_span.append([i.group(0), (i.start(), i.end())])
        # extracted_texts_and_span.append(i)    
    return extracted_texts_and_span


def extract_date_spans(text):
    span_collection = extract_with_pattern(day_month_year_alnum_pattern, text)
    span_collection_normalized = [[i, j, get_normal_date_day_month_year_alnum(i)] for i, j in span_collection]

    span_collection2 = extract_with_pattern(day_month_year_numeric_pattern, text)
    span_collection_normalized2 = [[i, j, get_normal_date_day_month_year_numeric(i)] for i, j in span_collection2]
    
    result = span_collection_normalized + span_collection_normalized2    
    return result

def extract_candidates(text):
    date_candidates = extract_date_spans(text)
    duration_candidates = extract_timedelta(text)
    amount_candidates = extract_amount_spans(text)

    n_start, n_end = 5, 2
    selected_paragraphs = '\n\n'.join(text.split('\n\n')[:n_start] + text.split('\n\n')[-n_end:])
    names_candidates = extract_name_spans(selected_paragraphs)

    return dict(
        date=date_candidates,
        duration=duration_candidates,
        amount=amount_candidates,
        names=names_candidates)
    

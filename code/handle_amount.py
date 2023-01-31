
def get_amount_from_numeric_span(text):
    
    #if in the form of eleven thousand nine hundred thirty two
    numbers = 'one two three four five six seven eight nine'.split()
    numbers += 'eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen ninteen twenty\
     thirty fourty fifty sixty seventy eighty ninety'.split()
    hundred_and_thousand = 'hundred thousand'.split()
    
    string_to_numeric_map = {'one': 1, 'two': 2, 'three': 3,
                             'four': 4, 'five': 5, 'six': 6,
                             'seven': 7, 'eight': 8, 'nine': 9,
                             'eleven': 11, 'twelve': 12, 'thirteen': 13,
                             'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
                             'seventeen': 17, 'eighteen': 18, 'ninteen': 19,
                             'twenty': 20, 'thirty': 30, 'fourty': 40,
                             'fifty': 50, 'sixty': 60, 'seventy': 70,
                             'eighty': 80, 'ninety': 90}
    
    found_in_search = []
    text_copy = text
    found_any = 0
    
    while text_copy:
        
        for i in numbers:
            if text_copy.startswith(i):
                text_copy = text_copy[len(i):]
                found_in_search.append(i)
                found_any = 1
                
        if not text_copy: break
        
        digits = ''
        if text_copy[0].isdigit():
            while text_copy and text_copy[0].isdigit():
                digits += text_copy[0]
                text_copy = text_copy[1:]
                if text_copy and text_copy[0] == ',': text_copy = text_copy[1:]
            digits = int(digits)
            if digits > 10:
                found_in_search.append(digits)
                found_any = 1
                
        
        if not text_copy: break
        
        if found_any == 1:
            for i in hundred_and_thousand:
                if text_copy.startswith(i):
                    text_copy = text_copy[len(i):]
                    found_in_search.append(i)
            
        text_copy = text_copy[1:]
        
    fvalue, buffer = 0, 0
    for i in found_in_search:
        if i in string_to_numeric_map:
            buffer += string_to_numeric_map[i]
        
        elif isinstance(i, int):
            buffer += i
        
        elif i in ['hundred', 'thousand']:
            buffer *= 100 if i=='hundred' else 1000
            fvalue += buffer
            buffer = 0
            
    fvalue += buffer
        
    return fvalue
          
    

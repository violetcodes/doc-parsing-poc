
import datetime

def get_rightest_num(left_split):
    '''let's say you have 'for 30 days he gains 89 pounds', which is a left split of a string
    and you wand to extract rightest num'''
    
    i=len(left_split)-1
    while i>=0:
        if left_split[i].isdigit():
            if i-1>=0 and left_split[i].isdigit():
                number_from_left = left_split[i-1:i+1]
                return number_from_left
            else:
                number_from_left = left_split[i]
                return number_from_left
        i -= 1
    



def get_normal_from_text(extracted_text):
    # from pattern1 e.g ith day of <month>, year
    global month_and_abbr
    months_and_abbr_splitted = months_and_abbr.split('|')
    month = [i for i in months_and_abbr_splitted if i in extracted_text][0]
    left_split, right_split = extracted_text.split(month)[:2]
    
    number_from_left = get_rightest_num(left_split)
    
    # get first neumeric value from right
    for i, char in enumerate(right_split):
        if char.isdigit():
            j = 1
            while j<4 and i+j<len(right_split) and right_split[i+j].isdigit():
                j += 1
            if j==1: continue #don't save single digit from right                
            else:
                number_from_right = right_split[i:i+j]
                break
    
    day = int(number_from_left)
    year = int(number_from_right)
    month_map = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
                 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
                 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sept': 9,
                 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

    
    month = month_map[month]
    # is_valid_date(day, month, year)
    
    return [day, month, year]

def get_normal_from_text2(extracted_text):
    #for pattern 2 e.g. dd/mm/yyyy or yyyy/mm/dd or mm/dd/yyyy
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
    
    
def get_time_delta(extracted_text):
    if 'days' in extracted_text:
        num_days = int(get_rightest_num(extracted_text.split('days')[0]))    
        return {'days': num_days}
    elif 'month' in extracted_text:
        num_months = int(get_rightest_num(extracted_text.split('month')[0])) 
        return {'months': num_months}
        

def is_valid_date(day, month, year):
    import datetime
    try:
        datetime.datetime(year=year,month=month,day=day)
        return True
    except ValueError:
        return False
    
    
def normalize_date(dates):
    formated_dt_index = pd.to_datetime(dates, dayfirst=True)
    year = formated_dt_index.year
    month = formated_dt_index.month
    day = formated_dt_index.day
    
    triplets_of_day_month_year = list(zip(day, month, year))
    triplets_of_day_month_year = [list(map(int, i)) if all([float(j).is_integer() for j in i]) else None \
                                   for i in triplets_of_day_month_year]
    return triplets_of_day_month_year
    
    

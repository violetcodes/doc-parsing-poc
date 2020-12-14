#remove special character

# character freq inspection
# from collections import Counter

# c = Counter(all_text_concatenated)
# d = {ord(i): (i, j) for i, j in c.items()}

# chr(8217)

# all_text_concatenated = '\n\n\n\n'.join(combined_csv.full_text.apply(lambda x:x).values.tolist())

# sorted(list({i:j for i, j in d.items() if i>126 or j[0] in string.punctuation}.items()), key=lambda x: x[1][1], reverse=True)

# Paragraph len analysis

# all_text_concatenated_cleaned = clean_text(all_text_concatenated)

# import matplotlib.pyplot as plt

# paragraphs_len = {}
# for i in all_text_concatenated_cleaned.split('\n\n'):
#     paragraphs_len[len(i)] = (paragraphs_len.get(len(i)) or []) + [i]

# print(all_text_concatenated_cleaned)

# paragraphs_len[31]

# clean_text(s)

# plt.figure(figsize=(40,10))
# plt.bar(list(paragraphs_len.keys()), [len(j) for j in paragraphs_len.values()])
# plt.yscale('log')
# plt.xticks(range(0,2000, 20));
# plt.show()

# # paragraphs_len

# # what is in the shorter paragraphs
# for i in range(30,70):
#     print(i, paragraphs_len[i], '\n\n')

# # best_way to handle_shorter paragraphs is to merge them into next paragraph
# # if they are last merge them into previous
# # if line is shorter inside the paragraph merge all lines

# # pipeline
# def get_results(text):
#     paragraphs = text.split('\n\n')
    
#     # alternatively_
#     tag_tokens
#     date_tokens
    
#     candidates = get_candidates(text)
#     regex_runners on entire text for dates, enddate, notice period
#     amount and name
    
#     convert these candidtaes --> span index --> spacy span --> get_vectore and other features
    
#     use normalizers to normalize them into proper format
#     --> tag targets with them one of six
#     and train return these key value pairs for training
# onece training is complete, get inferencing score and choose from these candidate for each target

    
#     spacy_docs = [nlp(para) in paragraphs]    
#     ents = [(ent, i) for i, doc in enumerate(spacy_docs) for ent in doc.ents]
#     noun_chunks = [(nc, i) for i, doc in enumerate(spacy_docs) for nc in doc.noun_chunks]
    
#     # these are the candidates
#     ents_and_nouns = sorted(ents + noun_chunks, lambda x: x[1])
    
#     scores = get_respective_score_for_each_one(ents_and_nouns)
    
#     results = get_best_with_results(scores)    
#     results = post_process_result(results)    
#     return results  


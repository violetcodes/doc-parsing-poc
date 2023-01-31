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

# get positive words list
file = open('myapp/lexicons/positive-words.txt', 'r')
pos_words = [word.replace('\n', '') for word in file.readlines() if word[0] != ';' and word != '\n']
file.close()

# get negative words list
file = open('myapp/lexicons/negative-words.txt', 'r')
neg_words = [word.replace('\n', '') for word in file.readlines() if word[0] != ';' and word != '\n']
file.close()


# detect polarity of comment
def detect_polarity(comment, show_details=False, check_neutral=False):
    # tokenize comment
    comment = comment.replace('-', ' ')
    comment = comment.replace('_', ' ')
    words = comment.split()
    i = 0
    while i < len(words):
        words[i] = words[i].lower()
        words[i] = words[i].strip()
        for symbol in ['.', ',', ':', ';', '!', '?', '"', '`', '#', '(', ')', '[', ']', '{', '}', '<', '>']:
            words[i] = words[i].replace(symbol, '')
        if words[i].endswith("n't") and len(words[i]) > 3:
            words[i] = words[i].replace("n't", '')
            words.insert(i+1, "n't")
        if len(words[i]) == 0:
            words.pop(i)
        i += 1
    # detect polarity
    polarity = 0
    negation_flag = False
    negation_distance_counter = 0
    negation_max_distance = 3
    comment_features = []
    for word in words:
        if word in ['not', "n't", 'nor', 'neither', 'non', 'never', 'isnt', 'arent', 'wasnt', 'werent', 'dont', 'doesnt', 'didnt', 'havent', 'hasnt', 'hadnt', 'wont', 'wouldnt', 'mustnt', 'cant', 'couldnt', 'shant', 'shouldnt', 'maynt', 'mightnt']:
            negation_flag = True
            negation_distance_counter = 0
            continue
        if word == 'such':
            negation_flag = False
            negation_distance_counter = 0
        if negation_flag:
            negation_distance_counter += 1
        if negation_distance_counter > negation_max_distance:
            negation_distance_counter = 0
            negation_flag = False
        p = 0
        if word in pos_words:
            p = 1
        elif word in neg_words:
            p = -1
        if negation_flag and p != 0:
            p *= -1
            negation_flag = False
            negation_distance_counter = 0
            comment_features.append(('NOT ' + word, p))
        elif p != 0:
            comment_features.append((word, p))
        polarity += p
    if show_details:
        print('----------------------------------')
        print('Comment:', words)
        print('Keywords:', comment_features)
        print('Polarity:', polarity)
        print('----------------------------------')
    if polarity > 0:
        return 'pos'
    else:
        if check_neutral and polarity == 0:
            return 'neu'
        else:
            return 'neg'

# ---------------------------------------------------------------------------------------------------


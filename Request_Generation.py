from SpecificWords import Specific_Words
from NumToTextKZ import Numer
from out2 import negiz, sozgebolu
import pymysql.cursors
import operator

'''
CURRENT SITUATION:
    SIMPLE SEARCH THAT CAN:
        1. FIND SYNONYMS OF REQUESTED WORDS AND ADD THEM TO REQUEST;
        2. FIND BASE OF REQUESTED WORDS AND ADD THEM TO REQUEST;
        3. FIND NUMBERS IN REQUEST (DIGITS, WORD AND IN ROMAN FORM) AND ADD THEM TO REQUEST;
        4. FIND ARTICLES IN SMALL MYSQL DB ONLY USING 'Text' FIELD.

REQUIRED TO ADD IN SYSTEM:
    1. TF-IDF INTEGRATION (FINDING WEIGHTS FOR WORDS);
    2. KEYWORD SEARCH (GET KEYWORDS FROM NEW DB);
    3. SEARCH TIME OPTIMIZATION (CREATE INDEXING SYSTEM, PARALLEL ALGORITHMS);
    4. OPTIMIZE NUMBER/DATE SEARCH, ADD VARIATIVITY OF USING DIGITS;
    5. SIMPLE USER INTERFACE;
    6. ADD SEARCH SUGGESTIONS.

    OPTIONAL:
        1. ADD MORE STOPWORDS BASE;
        2. CREATE BASE OF BASIS OF THE WORD TO OPTIMIZE NEGIZ() FUNCTION.
'''


def flat_list(lst):
    result = []
    if lst is not None:
        for sublist in lst:
            for item in sublist:
                result.append(item)
    return result


def rem_dup(lst):
    return list(dict.fromkeys(lst))


def tokenize(text):
    text = text.replace('\n', ' ').replace('  ', ' ')
    return sozgebolu(str.lower(text))


def encount(word, tokenized):   # encount of word/words in text
    enc = 0
    if type(tokenized) is list:         # !!! SIMPLE ENCOUNT JUST COUNTING WORDS, 
        for w in tokenized:             # i.e LARGE TEXT GOT BETTER CHANSES AGAINST
            if word == w:               # SMALL, EVEN IF IT LOSE SENSE !!!
                enc += 1
    elif type(tokenized) is str:    # first element of f_request must be undivided
        return str.lower(tokenized).count(word)   # therefore text isn't tokenized
    return enc


def splitter(request):      # Creates subrequests
    request = request.strip()   # Check for empty request
    if request != '':
        request = ' '.join([word for word in sozgebolu(str.lower(request)) if word not in Specific_Words.stop_words_base])
        splitted = request.split()  # Removed stop words

        nums_in_request = []
        for word in splitted:
            if word.isdigit():
                nume = int(word)
                nums_in_request.append(word)
                if nume < 999999:   # Convert small numbers to alternative forms
                    nums_in_request.append(Numer.num2text(nume))
                    if nume < 9999:
                        nums_in_request.append(Numer.num2roman(nume))
            elif Numer.is_roman(str.upper(word)):
                nums_in_request.append(word)
                t = Numer.roman2numITER(word)
                nums_in_request.append(str(t))
                nums_in_request.append(str(Numer.num2text(t)))
            elif word in Numer.units:
                nums_in_request.append(word)
                t = Numer.text2numITER(word)
                nums_in_request.append(str(t))
                nums_in_request.append(str(Numer.num2roman(t)))
                
        splitted.extend(nums_in_request)
        splitted = rem_dup(splitted)
        
        f_request = [request]

        f_request.extend(nums_in_request)   # !!! MUST BE EDITTED !!!

        #   Synonyms
        f_words = []
        synonyms = []
        for word in splitted:
            s = Specific_Words.synonyms_searcher(word)
            if s is not None:  # Synonyms found
                syns = rem_dup(flat_list(s))
                synonyms.append(syns)
                f_words.append(syns)
            elif s is None:  # No synonyms found
                synonyms.append([word])
                f_words.append([word])

        #   1 word base split
        f_negz = f_words.copy()

        for i in range(0, len(f_words)):
            for j in range(0, len(f_words[i])):
                negz = negiz(f_words[i][j])
                f_negz[i][j] = negz

        #   2 word split    NOT WORKING NOW DUE SEARCH OPTIMIZATION
        ff_negz = []

        for lst in f_negz:  # base
            for word in lst:
                for i in range(f_negz.index(lst) + 1, len(f_negz)):
                    for j in range(0, len(f_negz[i])):
                        words = word + '  ' + f_negz[i][j]
                        ff_negz.append(words)

        for lst in synonyms:  # as in request
            for word in lst:
                for i in range(synonyms.index(lst) + 1, len(synonyms)):
                    for j in range(0, len(synonyms[i])):
                        words = word + '  ' + synonyms[i][j]
                        ff_negz.append(words)

        f_request.extend(flat_list(f_negz))
        f_request.extend(ff_negz)
        f_request = rem_dup(f_request)
        f_request = [word for word in f_request if word not in nums_in_request]
        final = []
        for word in f_request:
            words = word.split('  ')
            if words[0] in nums_in_request and words[1] in nums_in_request:
                pass
            else:
                final.append(word)
    
        return final
    else:
        return 0    


class Text:
    def __init__(self, _id, _title, _url):
        self.id = _id
        self.title = _title
        self.url = _url
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}:{self.title}"


def search(f_request):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='textcorpus',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    result = {}     # id: {'word': encount, 'word1': ...}
    with connection.cursor() as cur:
        cur.execute('SELECT * FROM qasym_kz')   # small table for testing

        rows = cur.fetchall()
        for row in rows:
            txt_obj = Text(row['ID'], row['Title'], row['URL'])
            slst = {}
            tokenized = tokenize(row['Text'])
            first = True  # 1st element is pure user request, won't be splitted
            for word in f_request:
                if first:
                    first = False
                    e = encount(word, row['Text'])
                else:
                    e = encount(word, tokenized)
                slst[word] = e
            
            for res in slst:    # Clean non related
                if slst[res] > 0:
                    result[txt_obj] = slst
                    break
            
        return result
    
    
def score(search_result, limit=10):     # Clean and show search results
    final = {}
    for text in search_result:
        sum = 0
        for word in search_result[text]:
            sum += search_result[text][word]
        final[text] = sum
    print({k: v for k, v in sorted(final.items(), key=lambda item: item[1])})

    result = []
    if len(final) >= limit:
        for i in range(0, limit):
            tx = max(final, key=final.get)
            final.pop(tx)
            result.append(tx)
    elif len(final) == 0:
        print('No result for this request')
        return 0
    else:
        for i in range(0, len(final)):
            tx = max(final, key=final.get)
            final.pop(tx)
            result.append(tx)
    r = ''
    print(result)
    for text in result:
        r += f'{text.title} - {text.url} \n'
    with open('SearchResult.txt', 'w', encoding='utf-8') as f:
        f.write(r)   


def find():
    request = input('Enter request: ')
    string = splitter(request)
    print(len(string), string)
    s = search(string)
    with open('LOG.txt', 'w', encoding='utf-8') as f:
        f.write(str(s))
    score(s)

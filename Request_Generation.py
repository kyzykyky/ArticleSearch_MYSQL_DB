from NumToTextKZ import Numer
from out2 import negiz
from SpecificWords import sozgebolu, Specific_Words
import pymysql.cursors
import operator
import time
import threading
import queue
from multiprocessing.pool import ThreadPool
from search import main_search, Text

'''
CURRENT SITUATION:
    SIMPLE SEARCH THAT CAN:
        1. FIND SYNONYMS OF REQUESTED WORDS AND ADD THEM TO REQUEST;
        2. FIND BASE OF REQUESTED WORDS AND ADD THEM TO REQUEST;
        3. FIND NUMBERS IN REQUEST (DIGITS, WORD AND ROMAN FORM) AND ADD THEM TO REQUEST;
        4. FIND ARTICLES IN MYSQL DB ONLY USING 'text' and 'keywords' FIELD.

REQUIRED TO ADD IN SYSTEM:
    1. TF-IDF INTEGRATION (FINDING WEIGHTS FOR WORDS);
    2. SEARCH TIME OPTIMIZATION (CREATE INDEXING SYSTEM, PARALLEL ALGORITHMS);
    3. OPTIMIZE NUMBER/DATE SEARCH, ADD VARIATIVITY OF USING DIGITS;
    4. SIMPLE USER INTERFACE;
    5. ADD SEARCH SUGGESTIONS.

    OPTIONAL:
        CREATE BASE OF BASIS OF THE WORD TO OPTIMIZE NEGIZ() FUNCTION.
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


def splitter(request):              # Creates subrequests
    request = request.strip()       # Check for empty request
    if request != '':

        nums_in_request = []
        date = ''
        check = False
        for word in request.split(' '):     # Add dates
            if Numer.is_date(word):
                nums_in_request.append(word)
                date = word
                check = True
        if check:
            request = request.replace(date, '')
            d = nums_in_request[0].split('.')
            nums_in_request.append(d[0])
            nums_in_request.append(Numer.num2month(d[1]))
            nums_in_request.append(d[2])

        request = ' '.join([word for word in sozgebolu(str.lower(request)) if word not in Specific_Words.stop_words_base])
        splitted = request.split()  # Removed stop words

        for word in splitted:
            if word.isdigit():
                nume = int(word)
                nums_in_request.append(word)
                if nume < 999999:   # Convert small numbers to alternative forms
                    nums_in_request.append(Numer.num2text(nume))
                    if nume < 9999:
                        nums_in_request.append(Numer.num2roman(nume))
            elif Numer.is_roman(str.upper(word)):   # Check if Roman number
                nums_in_request.append(word)
                t = Numer.roman2numITER(word)
                nums_in_request.append(str(t))
                nums_in_request.append(str(Numer.num2text(t)))
            elif word in Numer.units:   # Check if text form (only 0-9)
                nums_in_request.append(word)
                t = Numer.text2numITER(word)
                nums_in_request.append(str(t))
                nums_in_request.append(str(Numer.num2roman(t)))
                
        splitted = rem_dup(splitted)
        f_request = [request]  
        f_request += splitted

        #   Synonyms
        f_words = []
        synonyms = []
        for word in splitted:
            s = Specific_Words.synonyms_searcher(word)
            if s is not None:   # Synonyms found
                syns = rem_dup(flat_list(s))
                synonyms.append(syns)
                f_words.append(syns)
            elif s is None:     # No synonyms found
                synonyms.append([word])
                f_words.append([word])

        f_request.extend(flat_list(f_words))    # Add synonyms
        #   1 word base split
        f_negz = f_words.copy()

        for i in range(0, len(f_words)):
            for j in range(0, len(f_words[i])):
                negz = negiz(f_words[i][j])
                if negz is not None:
                    f_negz[i][j] = negz

        #   2 word split    NOT WORKING NOW DUE SEARCH OPTIMIZATION
        # ff_negz = []

        # for lst in f_negz:  # base
        #     for word in lst:
        #         for i in range(f_negz.index(lst) + 1, len(f_negz)):
        #             for j in range(0, len(f_negz[i])):
        #                 words = word + '  ' + f_negz[i][j]
        #                 ff_negz.append(words)

        # for lst in synonyms:  # as in request
        #     for word in lst:
        #         for i in range(synonyms.index(lst) + 1, len(synonyms)):
        #             for j in range(0, len(synonyms[i])):
        #                 words = word + '  ' + synonyms[i][j]
        #                 ff_negz.append(words)

        f_request.extend(flat_list(f_negz))
        # f_request.extend(ff_negz)
        f_request = rem_dup(f_request)
        f_request = [word for word in f_request if word not in nums_in_request]
        final = []
        for word in f_request:
            words = word.split('  ')
            if words[0] in nums_in_request and words[1] in nums_in_request:
                pass    # Removed double numbers
            else:
                final.append(word)

        final.extend(nums_in_request)   # Add numbers simply !!! MUST BE EDITTED !!!
        return final
    else:
        return 0    


def search(f_request):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='textdb',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    limit = 1200
    # thrds = 2
    # ch = int(limit/thrds)
    with connection.cursor() as cur:
        cur.execute(f'SELECT * FROM corpora LIMIT {limit}')     # Limited for now
        rows = cur.fetchall()
        return main_search(rows, f_request)
        # que = queue.Queue()   # Not working 
        # tasks = list()
        # for i in range(0, thrds):
        #     print(i*ch, (i+1)*ch)
        #     try:
        #         tasks[i] = threading.Thread(target=lambda q, arg1: q.put(main_search(rows[i*ch:(i+1)*ch], f_request)), args=(que, (rows[i*ch:(i+1)*ch], f_request)))
        #     except IndexError:
        #         pass
        # for t in tasks:
        #     t.start()     # Gets killed on start
        # for t in tasks:
        #     t.join()
        # return que.get()

    
def score(search_result, limit=10):     # Clean and show search results
    final = {}
    text_r, kw_r = search_result
    for text in text_r:             # 'text' search result
        sum = 0
        t = text_r[text]
        for word in t:
            sum += t[word]
        final[text] = sum
    for text in kw_r:               # 'keywords' search result
        sum = 0
        t = kw_r[text]
        for word in t:
            sum += t[word]
        if text in final:
            final[text] += sum
        else:
            final[text] = sum

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
        f.write(r.strip())   


def find():
    request = input('Enter request: ')
    start_time = time.time()
    string = splitter(request)
    print(len(string), string)
    s = search(string)
    score(s)
    print("--- %s seconds ---" % (time.time() - start_time))


def find_r(request):
    start_time = time.time()
    string = splitter(request)
    print(len(string), string)
    s = search(string)
    with open('LOG.txt', 'w', encoding='utf-8') as f:
        f.write(str(s))
    score(s)
    print("--- %s seconds ---" % (time.time() - start_time))
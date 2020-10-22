from SpecificWords import sozgebolu


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
    

class Text:
    def __init__(self, _id, _title, _url):
        self.id = _id
        self.title = _title
        self.url = _url
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}:{self.title}"


def main_search(rows, f_request):
    result = []
    result_t = {}
    result_kw = {}

    for row in rows:
        txt_obj = Text(row['id'], row['title'], row['url'])
            
        slst_t = text_search(row, f_request)     # Search in 'text'
            
        slst_kw = kw_search(row, f_request)      # Search in 'keywords'

        for res in slst_t:    # Clean non related (0 encounts)
            if slst_t[res] > 0:
                result_t[txt_obj] = slst_t
                break
        for res in slst_kw:    # Clean non related (0 encounts)
            if slst_kw[res] > 0:
                result_kw[txt_obj] = slst_kw
                break
        result = [result_t, result_kw]
    return result


def text_search(row, f_request):
    slst_t = {}
    tokenized = tokenize(row['text'])   # Search in 'text'
    first = True  # 1st element is pure user request, won't be splitted
    for word in f_request:
        if first:
            first = False
            e = encount(word, row['text'])
        else:
            e = encount(word, tokenized)
            slst_t[word] = e
    return slst_t

def kw_search(row, f_request):
    slst_kw = {}
    tokenized = tokenize(row['keywords'])
    first = True
    for word in f_request:
        if first:
            first = False
        else:
            e = encount(word, tokenized) * 10
            slst_kw['KW' + word] = e
    return slst_kw
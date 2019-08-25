def clean_text(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation,
    remove words containing numbers and remove consecutive multiple white spaces.'''
    text = text.lower()
    text = re.sub('\\[.*?}''"—{\\]', '', text)
#     text = re.sub('"*', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\\w*\\d\\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)
    return text
    
def remove_stop(doc_tokens):
    """removes stop words and returns list of all nonstop words that is lemmatized"""
    return [token.lemma_ for token in doc_tokens if not token.is_stop]

def open_books(directory):
    """iterates through file and opens each txt document
        creates dictionary with keys as document name and value as document text"""
    chapter_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            chapter_dict.update({filename : open(directory + '/' + filename, errors = 'ignore').read()})
    return chapter_dict

def join_list_of_str(list_):
    """joins list of strings as one long string"""
    space = ' '
    for i in range(len(list_)):
        return space.join(list_)
    
def clean_df(df):
    """for each row in df.text, applies clean_text function"""
    for i in df.text:
        clean_text(i)
    return i

def list_of_books(df):
    list_books = []
    for i in range(len(df.text)):
        list_books.append(df.text[i])
    return list_books

def show_wordcloud(data, title = None): 
    wordcloud = WordCloud(
        background_color='white',
        stopwords=set(STOPWORDS),
        max_words=150,
        max_font_size=50, 
        scale=4,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()
    
def compound_dict(dictionary):
    new_dict = {}
    analyzer = SentimentIntensityAnalyzer()
    for k,v in dictionary.items():
        vs = analyzer.polarity_scores(v)
        new_dict.update({k:vs['compound']})
    return new_dict

def tf_idf_dict(dict_):
    corpus = list(dict_.values())
    vectorizer = TfidfVectorizer(ngram_range = (1,2))
    X = vectorizer.fit_transform(corpus)
    idf = vectorizer.idf_
    return dict(zip(vectorizer.get_feature_names(), idf))
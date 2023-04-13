import nltk
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

with open('C:/Users/Gravity/Desktop/prism.pdf', 'rb') as f:
    # Create a PDF reader object
    reader = PyPDF2.PdfReader(f)

    # Extract text from each page and concatenate them
    text = ''
    for page in reader.pages:
        text += page.extract_text()


def summarize(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize each sentence into words, remove stop words and stem words
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    word_frequencies = {}
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word not in stop_words:
                stemmed_word = stemmer.stem(word)
                if stemmed_word in word_frequencies:
                    word_frequencies[stemmed_word] += 1
                else:
                    word_frequencies[stemmed_word] = 1
                    
    # Find weighted frequencies of each sentence
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency
    
    # Calculate score for each sentence and store in dictionary
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence)
        sentence_score = 0
        for word in sentence_words:
            stemmed_word = stemmer.stem(word)
            if stemmed_word in word_frequencies:
                sentence_score += word_frequencies[stemmed_word]
        sentence_scores[sentence] = sentence_score
    
    # Get top n sentences with highest scores
    n = int(input())
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]
    
    # Join top sentences to create summary
    summary = " ".join(top_sentences)
    return summary


summary = summarize(text)
print(summary)

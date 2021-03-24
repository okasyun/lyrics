# モジュールやライブラリのインポート
from gensim import corpora
from janome.tokenizer import Tokenizer
from gensim.models import word2vec
from wordcloud import WordCloud
import re
import requests
from bs4 import BeautifulSoup

# kashi_final_Radwimps.txtの読み込み
with open("kashi_final_Radwimps.txt", "r", encoding="utf-8") as f:
    kashi = f.read()

# 品詞を取り出し「名詞、動詞、形容詞、形容動詞」のリスト作成
def tokenize(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    word = []
    stop_word = create_stop_word()
    for token in tokens:
        part_of_speech = token.part_of_speech.split(",")[0]
        if part_of_speech == "名詞":
            if not token.surface in stop_word:
                word.append(token.surface)
        if part_of_speech == "動詞":
            if not token.base_form in stop_word:
                word.append(token.base_form)
        if part_of_speech == "形容詞":
            if not token.base_form in stop_word:
                word.append(token.base_form)
        if part_of_speech == "形容動詞":
            if not token.base_form in stop_word:
                word.append(token.base_form)

    # for wo in word:
    #     if not wo in counter: counter[wo] = 0
    #     counter[wo] += 1

    return word

# 取り除くword
my_stop_word = ['てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'これ', 'さん', 'して',
                'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う',
                'それ', 'ここ', 'ちゃん', 'くん', 'て', 'に', 'を', 'は', 'の', 'が', 'と', 'た', 'し', 'で',
                'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', 'ん', 'みたい', 'の', '私', '自分', 'たくさん',
                'ん', 'もの', 'こと']
# my_stop_word変数と頻出するstopwordのサイトを用いて邪魔なwordを取り除く関数を作成
def create_stop_word():
    target_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, "lxml")
    stop_word = str(soup).split()
    stop_word.extend(my_stop_word)
    return stop_word


# wordcloudを作成
sentence = [tokenize(kashi)]
word = tokenize(kashi)
word_cloud = ' '.join(word)
with open('kashi_final.txt', mode='w', encoding='utf-8') as fw:
    fw.write(word_cloud)
text_file = open('kashi_final.txt', encoding='utf-8')
text = text_file.read()
fpath = '/Users/shunokamoto/Library/Fonts/SourceHanCodeJP-Regular.otf'
wordcloud = WordCloud(background_color='white', font_path=fpath,
width=800, height=600, stopwords=set(my_stop_word)).generate(text)
wordcloud.to_file('./wordcloud_Radwimps.png')


model = word2vec.Word2Vec(sentence, size=200, min_count=4, window=4, iter=50)
print(model.wv.most_similar(positive=[u"世界"], negative=["愛"], topn=10))

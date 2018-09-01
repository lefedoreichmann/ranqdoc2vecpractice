# -*- coding: utf-8 -*-
import json
import MeCab
from gensim.models import doc2vec
import os
import sys


def load_json(target_game_name):
    # カード名とカードテキストの入力データ作成
    titles = []
    description = ""
    descriptions = []
    categories = []
    ids = []
    views =[]
    # Mecabの出力を分かち書きに指定
    mecab = MeCab.Tagger("-Owakati")

    json_path = target_game_name + "/" + target_game_name + ".json"

    # カードのテキストを形態素解析し、分かち書きしたものを改行区切りで一つのstringにする
    with open(json_path, "r") as file:
        article_dict = json.load(file)
        for article in article_dict:
            if article["title"] not in titles:
                titles.append(article["title"])
                categories.append(article["category"])
                ids.append(article["id"])
                views.append((article["view"]))
                mecab_result = mecab.parse(article["description"])
                if mecab_result is False:
                    description += "\n"
                    descriptions.append("")
                else:
                    description += mecab_result
                    descriptions.append(article["description"])


    with open(target_game_name + ".txt", "w") as file:
        file.write(description)

    return titles, descriptions,ids,categories,views


def generate_doc2vec_model(target_game_name):
    print("Training Start")
    # カードテキスト読み込み
    article_description = doc2vec.TaggedLineDocument(target_game_name + ".txt")
    # 学習
    model = doc2vec.Doc2Vec(article_description, size=300, window=8, min_count=1,
                            workers=4, iter=400, dbow_words=1, negative=5)

    # モデルの保存
    model.save(target_game_name + ".model")
    print("Training Finish")
    return model


if __name__ == '__main__':
    args = sys.argv

    TARGET_GAME_NAME = "ranq_learning"
    titles, descriptions ,ids,categories,views= load_json(TARGET_GAME_NAME)

    if os.path.isfile(TARGET_GAME_NAME + ".model") is True:
        model = doc2vec.Doc2Vec.load(TARGET_GAME_NAME + ".model")
    else:
        model = generate_doc2vec_model(TARGET_GAME_NAME)

     # 類似カードを求めたいカード名
    TARGET_article_NAME = args[1]
    article_index = titles.index(TARGET_article_NAME)

    # 類似カードと類似度のタプル（類似度上位10件）のリストを受け取る
    similar_docs = model.docvecs.most_similar(article_index)
    print("ID:"+ids[article_index]+"\nタイトル:"+titles[article_index]+"\nカテゴリ:"+categories[article_index]+"\nView:"+views[article_index])
    print("説明:")
    print("        "+descriptions[article_index][:100])
    print("--------------------is similar to--------------------")
    for similar_doc in similar_docs:
        print("ID:"+ids[similar_doc[0]])
        print(titles[similar_doc[0]] + " " + str(similar_doc[1]))
        print(views[similar_doc[0]])
        print("        "+descriptions[similar_doc[0]][:100], "\n")


from flask import Flask, request, render_template
import requests

app = Flask(__name__)


# ==================================
# 1. 建立中文、韓文題庫
# ==================================

zh_ko_dict = {
    "你好": "안녕하세요",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}


# ==================================
# 2. 建立中文、日文題庫
# ==================================

zh_ja_dict = {
    "你好": "こんにちは",
    "謝謝": "ありがとうございます",
    "對不起": "ごめんなさい",
    "早安": "おはようございます",
    "晚安": "おやすみなさい",
    "老師": "先生",
    "學生": "学生",
    "朋友": "友達",
    "家人": "家族",
    "愛": "愛"
}


# ==================================
# 3. 首頁
# ==================================

@app.route('/')
def index():
    return render_template('index.html')


# ==================================
# 4. 競賽
# ==================================

@app.route('/competition')
def competition():
    return render_template('competition.html')


# ==================================
# 5. Google 翻譯式語言選擇功能
# ==================================

@app.route('/translate', methods=['GET', 'POST'])
def translate():

    question = ""
    answer = ""

    source_lang = "zh-TW"
    target_lang = "ko"

    if request.method == 'POST':

        # 取得輸入文字
        question = request.form.get('question', '').strip()

        # 取得原文語言與目標語言
        source_lang = request.form.get('source_lang', 'zh-TW')
        target_lang = request.form.get('target_lang', 'ko')

        # 避免選擇相同語言
        if source_lang == target_lang:

            answer = "原文語言與翻譯語言不能相同。"

        # 中文翻譯韓文
        elif source_lang == "zh-TW" and target_lang == "ko":

            answer = zh_ko_dict.get(
                question,
                "抱歉，題庫中沒有這個韓文單字。"
            )

        # 中文翻譯日文
        elif source_lang == "zh-TW" and target_lang == "ja":

            answer = zh_ja_dict.get(
                question,
                "抱歉，題庫中沒有這個日文單字。"
            )

        # 韓文翻譯中文
        elif source_lang == "ko" and target_lang == "zh-TW":

            ko_zh_dict = {
                value: key
                for key, value in zh_ko_dict.items()
            }

            answer = ko_zh_dict.get(
                question,
                "抱歉，題庫中沒有這個中文單字。"
            )

        # 日文翻譯中文
        elif source_lang == "ja" and target_lang == "zh-TW":

            ja_zh_dict = {
                value: key
                for key, value in zh_ja_dict.items()
            }

            answer = ja_zh_dict.get(
                question,
                "抱歉，題庫中沒有這個中文單字。"
            )

        # 韓文翻譯日文
        elif source_lang == "ko" and target_lang == "ja":

            ko_zh_dict = {
                value: key
                for key, value in zh_ko_dict.items()
            }

            ja_zh_dict = {
                value: key
                for key, value in zh_ja_dict.items()
            }

            chinese = ko_zh_dict.get(question)

            if chinese:
                answer = zh_ja_dict.get(
                    chinese,
                    "找不到對應的日文翻譯。"
                )
            else:
                answer = "題庫中沒有這個韓文單字。"

        # 日文翻譯韓文
        elif source_lang == "ja" and target_lang == "ko":

            ja_zh_dict = {
                value: key
                for key, value in zh_ja_dict.items()
            }

            ko_zh_dict = {
                value: key
                for key, value in zh_ko_dict.items()
            }

            chinese = ja_zh_dict.get(question)

            if chinese:
                answer = zh_ko_dict.get(
                    chinese,
                    "找不到對應的韓文翻譯。"
                )
            else:
                answer = "題庫中沒有這個日文單字。"

        else:

            answer = "不支援這組語言。"

    return render_template(
        'translate.html',
        question=question,
        answer=answer,
        source_lang=source_lang,
        target_lang=target_lang
    )


# ==================================
# 6. 原本的互動活動
# ==================================

@app.route('/activities', methods=['GET', 'POST'])
def activities():

    if request.method == 'POST':

        question = request.form.get(
            'question', ''
        ).strip()

        answer = "抱歉，我目前沒有這個詞的韓文對應。"

        return render_template(
            'activities.html',
            question=question,
            answer=answer
        )

    return render_template(
        'activities.html',
        question="",
        answer=""
    )


# ==================================
# 7. 股票查詢功能
# ==================================

@app.route('/stock', methods=['GET', 'POST'])
def stock():

    question = ""
    answer = ""

    if request.method == 'POST':

        # 取得股票代號
        question = request.form.get(
            'question', ''
        ).strip()

        stock_no = question

        # 證交所 API
        url = (
            "https://www.twse.com.tw/exchangeReport/"
            f"STOCK_DAY?response=json&stockNo={stock_no}"
        )

        try:

            # 發送 API 請求
            res = requests.get(url, timeout=10)

            res.raise_for_status()

            data = res.json()

            # 判斷查詢是否成功
            if data.get("stat") == "OK" and data.get("data"):

                # 取得最新一筆資料的收盤價
                answer = data["data"][-1][6]

            else:

                answer = "查無資料，請確認股票代號。"

        except requests.RequestException:

            answer = "股票資料連線失敗，請稍後再試。"

        except (ValueError, KeyError, IndexError):

            answer = "股票資料格式錯誤，請稍後再試。"

        return render_template(
            'stock.html',
            question=question,
            answer=answer
        )

    return render_template(
        'stock.html',
        question="",
        answer=""
    )


# ==================================
# 8. 幹部介紹
# ==================================

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


# ==================================
# 9. 社團
# ==================================

@app.route('/club')
def club():
    return render_template('club.html')


# ==================================
# 10. 選修課程
# ==================================

@app.route('/electives')
def electives():
    return render_template('electives.html')


# ==================================
# 11. AI 頁面
# ==================================

@app.route('/ai')
def ai():
    return render_template('ai.html')


# ==================================
# 12. 67 頁面
# ==================================

@app.route('/67')
def page_67():
    return render_template('67.html')


# ==================================
# 13. 啟動 Flask
# ==================================

if __name__ == '__main__':

    app.run(debug=True)

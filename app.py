
# Google 翻譯式語言選擇功能

@app.route('/translate', methods=['GET', 'POST'])
def translate():

    question = ""
    answer = ""

    source_lang = "zh-TW"
    target_lang = "ko"

    if request.method == 'POST':

        # 取得使用者輸入的文字
        question = request.form.get('question', '').strip()

        # 取得使用者選擇的語言
        source_lang = request.form.get('source_lang', 'zh-TW')
        target_lang = request.form.get('target_lang', 'ko')

        # 中文翻譯韓文
        if source_lang == "zh-TW" and target_lang == "ko":
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
            answer = {
                value: key for key, value in zh_ko_dict.items()
            }.get(question, "抱歉，題庫中沒有這個中文單字。")

        # 日文翻譯中文
        elif source_lang == "ja" and target_lang == "zh-TW":
            answer = {
                value: key for key, value in zh_ja_dict.items()
            }.get(question, "抱歉，題庫中沒有這個中文單字。")

        else:
            answer = "目前尚未建立這組語言的翻譯題庫。"

    return render_template(
        'translate.html',
        question=question,
        answer=answer,
        source_lang=source_lang,
        target_lang=target_lang
    )

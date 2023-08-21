
import os
import openai
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")
eduKey = os.getenv("EDU_KEY")


def CallEduContent(keyWord): #回傳我要的資料
    url = f"https://pedia.cloud.edu.tw/api/v2/List?keyword={keyWord}&page=1&api_key={eduKey}"
    eduBack = requests.get(url)
    eduBackJson = eduBack.json()
    #檢查長度
    SelectedContent = []
    current_length = 0
    
    for item in eduBackJson:
        title = item["WordTitle"]
        desc = item["WordDesc"]
        title_length = len(title)
        desc_length = len(desc)
        
        # 檢查是否超過總長度限制
        if current_length + title_length + desc_length <= 800:
            SelectedContent.append({"WordTitle": title, "WordDesc": desc})
            current_length += title_length + desc_length
        else:
            break
    
    return SelectedContent


def generate_question(keyWord):
    formatted_text = "你是我的出題的小老師，學生有提問，請根據我提供的搜尋文本中，挑選其中與學生提問最相關的\"WordTitle\"設計題目，答題者並沒有看過文本，請你設計一則選擇題，共有四個選項，要選出當中錯誤敘述，並且在答案選項後面說明該選項錯誤的原因。\n\n回傳為以下json格式:\n{[question:{請你依據文字設計}],[option:[A:{請設計題目},B:{請設計題目},C:{請設計題目}D:{請設計題目}],[answer:{{選項}:{請說明該選項錯誤的原因並糾正}}]}\n範例:\n{\"question\": \"以下哪個選項錯誤？\", \"options\": {\"A\": \"目不交睫形容人辛勞或憂慮的沒有時間睡覺。\", \"B\": \"枕戈待旦形容時時警惕，準備作戰，不敢安睡。\", \"C\": \"花天酒地原指在美好的環境中飲酒作樂。\", \"D\": \"夙夜匪懈形容工作很勤奮。\"}, \"answer\": {\"D\": \"夙夜匪懈形容工作很勤奮。夙夜匪懈的意思是早晚都不懈怠，全心投入工作，而不是形容工作很勤奮。\"}}\n\n學生的問題為{{keyWord}}:\n請用以下文本設計:"
    trainCommand = formatted_text.replace("{{keyWord}}", keyWord) #為了可以將keyWord加入提示詞
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": trainCommand
            },
            {
                "role": "user",
                "content": f"{CallEduContent(keyWord)}" #呼叫擷取的Content
            },
        ],
        temperature=0.7,
        max_tokens=630,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response["choices"][0]["message"]["content"]

# # 使用示例
# keyWord = "蟑螂"
# response1 = generate_question(keyWord)
# print(response1["choices"][0]["message"]["content"])



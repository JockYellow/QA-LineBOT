from flask import Flask, request, render_template
#from func import generate_question
app = Flask(__name__)

T1Json = str({"question": "以下哪個選項錯誤？", "options": {"A": "貓的耳朵會向後貼，發出咆哮與「嘶」聲是表示忿怒或受驚。", "B": "貓的嗅覺比人類靈敏14倍。", "C": "貓失去了「甜」的味覺。", "D": "貓的聽力比人類高1個八度。"}, "answer": {"D": "貓的聽力比人類高1個八度。文本中提到貓的聽力可達64kHz，比人類要高1.6個八度音，而不是1個八度。"} })

@app.route('/')
def index():
    return render_template('index.html', question=None) 
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    question = keyword   
    #question = generate_question(keyword)  
    return render_template('index.html', question=question)  



if __name__ == '__main__':
    app.run(debug=True)


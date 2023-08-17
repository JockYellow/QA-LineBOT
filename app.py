from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')

    if keyword:
        # 在這裡執行你的搜尋邏輯，假設 search_result 是搜尋結果
        search_result = {
            'keyword': keyword,
            'results': ['result1', 'result2', 'result3']
        }
        return render_template('index.html', results=search_result['results'])
    else:
        return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)


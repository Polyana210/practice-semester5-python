from flask import Flask, render_template, request
from search import search_phrase
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def authorization():

   if request.method == 'POST':
       phrase = request.form.get('Phrase')
       search_stat = search_phrase(phrase)
       return '<div> Файл с исходными данными для поиска: {input_doc}. </div><div> Всего совпадений: {count}.</div><div> \n Результат поиска записан в файл: {output_doc}.</div>'.format(input_doc = search_stat["Input_document"], output_doc = search_stat["Output_document"],count = str(search_stat["Count"]))

   return '''
             <form method="POST">
                 <div><label>Введите фразу для поиска: <input type="text" name="Phrase"></label></div>
                 <input type="submit" value="Enter">
             </form>'''


if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, redirect
import urllib.parse
from checkers import thriftys, superstore, johns, quality_foods

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # When item is entered in search, get it and make it url friendly
        item = urllib.parse.quote(request.form['search'])
        # Check item price at each store
        thriftys_list = thriftys(item)
        sstore_list = superstore(item)
        johns_list = johns(item)
        qf_list = quality_foods(item)

        return render_template('index.html', thriftys = thriftys_list, sstore = sstore_list, johns = johns_list, qf = qf_list)

if __name__ == '__main__':
    app.run(debug = True)
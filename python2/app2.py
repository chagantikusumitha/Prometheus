from flask import Flask, render_template, request

app = Flask(__name__)

def fibonacci_series(n):
    n1, n2 = 0, 1
    fib_series = [n1]
    for _ in range(n - 1):
        n1, n2 = n2, n1 + n2
        fib_series.append(n1)
    return fib_series

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nterms = int(request.form['nterms'])
        fib_series = fibonacci_series(nterms)
        return render_template('index.html', fib_series=fib_series)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
pi
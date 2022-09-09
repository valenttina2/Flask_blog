from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/about')
@app.route('/home')
def about():
    return 'about us'

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'user page'+name+'-'+id



if __name__=='__main__':
    app.run(debug=True)
from flask import Flask
from flask import render_template,redirect,make_response,url_for
from flask import session, request, abort

import os

from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY','hello,world')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Contact')
def contact():
    return redirect('http://210.45.212.94')

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name',default='Human')
        response = f'hello,{name}'
        if 'logged_in' in session:
            response += '【Authenticated】'
        else:
            response += '【非法！】'

    return response

@app.route('/set/<name>')
def cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response

@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    else:
        return 'Welcome, my lord!'

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

@app.route('/post')
def show_post():
    post_body =generate_lorem_ipsum(n=2)
    return """
    <h1> A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load more</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function(){
        $('#load').click(function(){
            $.ajax({
                url:'/more',
                type:'get',
                success:function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>
    """ % post_body

@app.route('/more')
def more():
    return generate_lorem_ipsum(n=1)

if __name__ == '__main__':
    app.run()

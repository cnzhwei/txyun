from flask import Flask, flash
from flask import render_template,redirect,make_response,url_for
from flask import session, request, abort
import os
from forms import *
from jinja2.utils import generate_lorem_ipsum
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY','hello,world')
app.config['UPLOAD_PATH'] = os.path.join(app.root_path,'uploads')


@app.route('/')
@app.route('/index')
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

@app.route('/login_ok')
def login_ok():
    session['logged_in'] = True
    return redirect(url_for('hello'))

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash(f'Welcome,{username}')
        return redirect(url_for('index'))
    return render_template('login.html',form = form)

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
    <h1>A very long post</h1>
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

@app.route('/flash')
def just_flash():
    flash('寄托在腾讯云的网站txyun！')
    return redirect(url_for('index'))

import datetime
def datatime_filename(filename):
    ext = filename.split('.')[-1]
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return time+'.'+ext

@app.route('upload',methods=['GET','POST'])
def upload():
    form = AttachForm()
    if form.validate_on_submit():
        txt,img = form.textfile.data,form.imgfile.data
        txt_filename,img_filename = datatime_filename(txt.filename),datatime_filename(img.filename)
        txt.save(os.path.join(app.config['UPLOAD_PATH'],'txt', txt_filename))
        img.save(os.path.join(app.config['UPLOAD_PATH'], 'img', img_filename))

    return render_template('upload.html',form=form)

@app.route('/more')
def more():
    return generate_lorem_ipsum(n=1)

##异常处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404

@app.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'),500

if __name__ == '__main__':
    app.run()

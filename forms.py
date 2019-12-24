from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message='名字不能为空')])
    password = PasswordField('Password',validators=[DataRequired(message='密码不能为空'),Length(8,128,message='密码必须大于8位')])
    remember = BooleanField('Remberme')
    submit = SubmitField('Log in')

class AttachForm(FlaskForm):
    textfile = FileField('Upload Text File',validators=[FileAllowed(['fasta','txt','fa'],message='Fasta format only!')])
    imgfile = FileField('Upload Images',validators=[FileAllowed(['jpg','png','gif','jpeg'],message='Fasta format only!')])
    submit = SubmitField('Upload')
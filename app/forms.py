from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, FormField, IntegerField, SubmitField
from wtforms.validators import Required, Optional
from app.models import User

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    queryType = SelectField(choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    # print queryType

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        print self.queryType.data
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None: 
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class PopForm(Form):
    runOdom = BooleanField('Run Odom', default = False)
    days_in_field = IntegerField('Days in field', validators = [Required()])
    country_value = TextField('Country Value')

class InputForm(Form):
    queryType = SelectField(choices=[('vin_query', 'VinQuery'), ('sig_value_query', 'Signal Value Query'), ('pop_query', 'Population Query')], validators = [Required()])
    submit = SubmitField("Submit", validators = [Required()])
    params = FormField(PopForm)

'''
customer_carsTF = True, master_value = False, runOdom = False, runPack = False, 
    num_samples=None, days_in_field=None, region_value=None, subregion_value=None,
    country_value=None, state_value = None, min_warranty_date= None, filePath = None
'''
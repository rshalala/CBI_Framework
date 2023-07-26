from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from cbi_framework import authorized_emails

text_area_field_char_limit = 500


# custom validator to check if the email is authorized
def is_email_authorized(form, email_field):
    pass
    if email_field.data not in authorized_emails:
        raise ValidationError(f'{email_field.data} is not authorized')


# forms
class SubmitForm(FlaskForm):
    email_1 = StringField('Student 1 Email', validators=[DataRequired(), Email(), is_email_authorized])
    email_2 = StringField('Student 2 Email', validators=[Optional(), Email(), is_email_authorized])
    notebook_file = FileField('Jupyter Notebook File',
                              validators=[FileRequired(), FileAllowed(['ipynb', 'Jupyter Notebooks Only!'])])
    submit = SubmitField('Submit')


class FeedbackForm(FlaskForm):
    # Radio fields for implicit feedback questions for each feature (assuming max of 4 features) in each measure.
    # If failed the feature's test - present cases and ask regarding the measure's behaviour.
    feature1_cases = RadioField('', choices=[('case1', 'Case 1'), ('case2', 'Case 2'), ('none', 'None')],
                                validators=[Optional()])
    feature1_agree = RadioField('Do you agree with your measure\'s choice?',
                                choices=[('y', 'Yes'), ('n', 'No'), ('dn', 'Don\'t know')],
                                validators=[Optional()])
    feature2_cases = RadioField('', choices=[('case1', 'Case 1'), ('case2', 'Case 2'), ('none', 'None')],
                                validators=[Optional()])
    feature2_agree = RadioField('Do you agree with your measure\'s choice?',
                                choices=[('y', 'Yes'), ('n', 'No'), ('dn', 'Don\'t know')],
                                validators=[Optional()])
    feature3_cases = RadioField('', choices=[('case1', 'Case 1'), ('case2', 'Case 2'), ('none', 'None')],
                                validators=[Optional()])
    feature3_agree = RadioField('Do you agree with your measure\'s choice?',
                                choices=[('y', 'Yes'), ('n', 'No'), ('dn', 'Don\'t know')],
                                validators=[Optional()])

    # Feedback helpfulness ratings system
    rating_choice_list = [
        ('1', '1 - Not at all helpful'),
        ('2', '2'),
        ('3', '3 - Somewhat helpful'),
        ('4', '4'),
        ('5', '5 - Very helpful')
    ]
    rating = RadioField('How helpful was the feedback:', choices=rating_choice_list,
                        validators=[])
    comments = TextAreaField('Help us improve - please provide any comments regarding the feedback system:',
                             render_kw={'maxlength': text_area_field_char_limit})

    submit = SubmitField('Submit')

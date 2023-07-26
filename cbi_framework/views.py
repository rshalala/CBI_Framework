from flask import render_template, url_for, flash, redirect, request
import os
import random
from datetime import datetime

# Importing necessary modules from the cbi_framework package
import cbi_framework as cbi_framework
from cbi_framework import app, db, Feedback_type
from cbi_framework import users_dict
from cbi_framework.forms import SubmitForm, FeedbackForm
from cbi_framework.models import User, Submission
from cbi_framework import tools


# Route for running in analyzer mode - analyze all Jupyter notebooks provided in app.config['NOTEBOOKS_FOLDER'] 
@app.route('/analyze', methods=['GET', 'POST'])
def analyze_folder():
    # Clear the database prior to analysis
    tools.db_recreate_table(User)
    tools.db_recreate_table(Submission)

    # Analyze each notebook in the notebooks folder
    for notebook in os.listdir(app.config['NOTEBOOKS_FOLDER']):
        if not notebook.endswith('.ipynb'):
            continue
        # Analyze the notebook and retrieve solution features (the test cases results)
        solution_features = tools.analyze_notebook(cbi_framework.topic,
                                                   app.config['NOTEBOOKS_FOLDER'] + notebook.split('.')[0],
                                                   'temp' + notebook.split('.')[0], app.config['MODULES_FOLDER'])

        if isinstance(solution_features, Exception):
            # Handle cases where an exception occurred during analysis
            exception_type = type(solution_features).__name__
            print(f'notebook {notebook} threw Exception of type {exception_type}')
            continue
        if not solution_features:
            # Handle cases where the notebook returns an invalid value
            print('notebook ' + notebook + ' returns invalid value')
            continue
        
         # Create a user record and submission record in the database
        user_record = User(student_1_email=notebook.split('.')[0] + '@test.com')
        db.session.add(user_record)
        db.session.commit()

        submission_record = Submission(user_id=user_record.id, topic=cbi_framework.topic.name,
                                       num_of_features=len(solution_features)
                                       )
        # Store the solution features and their results in the submission record
        for f_idx in range(0, len(solution_features)):
            exec(f'submission_record.f{f_idx + 1}_success = '
                 f'solution_features.get(list(solution_features.keys())[f_idx])')
            exec(f'submission_record.f{f_idx + 1}_name = "{list(solution_features.keys())[f_idx]}"')
        db.session.add(submission_record)
        db.session.commit()

    return render_template('folder.html', title='Notebooks Analysis')


# Route for submitting solutions
@app.route('/', methods=['GET', 'POST'])
def submit():
    # Process the notebook submission form
    form = SubmitForm()

    id_1 = id_2 = ''
    if form.validate_on_submit():
        # Get users IDs
        id_1 = str(int(users_dict.get(form.email_1.data)))
        id_2 = users_dict.get(form.email_2.data)
        if id_2:
            id_2 = str(int(id_2))

        # Create user if it is a new user
        query_1_1 = User.query.filter_by(student_1_email=form.email_1.data).first()
        query_1_2 = User.query.filter_by(student_1_email=form.email_2.data).first()
        query_2_1 = User.query.filter_by(student_2_email=form.email_1.data).first()
        query_2_2 = User.query.filter_by(student_2_email=form.email_2.data).first()

        user_record = query_1_1  # just to avoid warning that it might be referenced before assignment
        if (query_1_1 and query_2_2) or (query_1_2 and query_2_1):
            new_user = False
            if query_1_1 and query_2_2:
                user_record = query_1_1
            elif query_1_2 and query_2_1:
                user_record = query_1_2
        else:
            new_user = True
            # create a new user record with feedback type sequence
            feedback_sequence = [0, 1, 2, random.randint(1, 2)]
            random.shuffle(feedback_sequence)
            user_record = User(student_1_email=form.email_1.data, student_2_email=form.email_2.data,
                               student_1_id=id_1, student_2_id=id_2,
                               fb_type_hypothesis=feedback_sequence[0],
                               fb_type_tvd=feedback_sequence[1],
                               fb_type_classification=feedback_sequence[2])

        # Add the new user record to the database
        if new_user:
            db.session.add(user_record)
            db.session.commit()

        # Rename and upload the file
        f = form.notebook_file.data
        if id_2:
            filename = id_1 + '_' + id_2 + '.ipynb'
        else:
            filename = id_1 + '.ipynb'

        save_to_path = os.path.join(app.config['UPLOAD_FOLDER'] + str.lower(cbi_framework.topic.name), filename)
        f.save(save_to_path)

        # Set arbitrary module name based on the first two letters on the email address
        module_name = form.email_1.data[:2] + form.email_2.data[:2]

        # Analyze the notebook and retrieve solution features - result should be a dictionary that represents the features and if each feature's test case was passed
        solution_features = tools.analyze_notebook(cbi_framework.topic, save_to_path, module_name,
                                                   app.config['MODULES_FOLDER'])

        # Set success default value to True
        success = True

        # Check if we got an exception and handle it
        if isinstance(solution_features, Exception):
            success = False
            if isinstance(solution_features, ImportError):
                try:
                    os.remove(app.config['MODULES_FOLDER'] + str(module_name) + '.py')
                except OSError as e:
                    pass
                flash(f'ImportError occurred, unable to import module named: {solution_features.name}', 'danger')
            elif isinstance(solution_features, TypeError):
                try:
                    os.remove(app.config['MODULES_FOLDER'] + str(module_name) + '.py')
                except OSError as e:
                    pass
                flash('Your method should return only a numerical value. Please fix it and re-submit', 'danger')
            else:
                exception_type = type(solution_features).__name__
                try:
                    os.remove(app.config['MODULES_FOLDER'] + str(module_name) + '.py')
                except OSError as e:
                    pass
                flash(f'Your submitted notebook produces a {exception_type}, please fix it and re-submit', 'danger')

        # Check case of no return value from the measure methods
        if not solution_features:
            success = False
            flash(f'Your measure calculation method does not return a numeric value, '
                  f'please verify that the "calculate_measure" method returns a value and re-submit', 'danger')

        # Set the feedback type according to the user record
        if success:
            feedback_type = -1
            if cbi_framework.topic is cbi_framework.Topic.HYPOTHESIS:
                feedback_type = user_record.fb_type_hypothesis
            elif cbi_framework.topic is cbi_framework.Topic.TVD:
                feedback_type = user_record.fb_type_tvd
            elif cbi_framework.topic is cbi_framework.Topic.CLASSIFICATION:
                feedback_type = user_record.fb_type_classification

            # Create the submission record and store it in the database
            submission_record = Submission(user_id=user_record.id, topic=cbi_framework.topic.name,
                                           file_path=save_to_path, feedback_type=feedback_type,
                                           num_of_features=len(solution_features)
                                           )
            for f_idx in range(0, len(solution_features)):
                exec(f'submission_record.f{f_idx + 1}_success = '
                     f'solution_features.get(list(solution_features.keys())[f_idx])')
                exec(f'submission_record.f{f_idx + 1}_name = "{list(solution_features.keys())[f_idx]}"')

            submission_record.time_submit = datetime.utcnow()
            db.session.add(submission_record)
            db.session.commit()

            flash('Submission successful!', 'success')  # message and bootstrap class of 'success'

            if feedback_type == 0:  # case of no feedback
                return render_template('completed.html', title='Task Completed')
            else:
                return redirect(url_for('feedback', id=submission_record.id, fbt=feedback_type, mod=module_name))

    # Render the submit.html template for displaying the notebook submission form
    return render_template('submit.html', title='Submission', form=form)


# Route for providing feedback to students
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    feedback_type = request.args.get('fbt')
    module_name = request.args.get('mod')
    submission_id = request.args.get('id')

    # Create the feedback form
    form = FeedbackForm()

    field_label = ''
    if cbi_framework.topic is cbi_framework.Topic.HYPOTHESIS:
        field_label = 'Which case will be considered as higher evidence for machine malfunction ' \
                      '(will get a higher score) by your measure?'
    elif cbi_framework.topic is cbi_framework.Topic.TVD:
        field_label = 'Which of the following cases will be considered as larger distance ' \
                      '(will get a higher score) by your measure?'
    elif cbi_framework.topic is cbi_framework.Topic.CLASSIFICATION:
        field_label = 'Which of the classification results will get a higher score by your measure?'

    # Set the field labels for the feedback form
    form.feature1_cases.label.text = form.feature2_cases.label.text = form.feature3_cases.label.text = field_label

    # Retrieve the submission record from the database
    submission_record = Submission.query.get(submission_id)

    # Handle implicit feedback case
    if int(feedback_type) == Feedback_type.IMPLICIT.value:
        print('they are equal')
        if submission_record.f1_success is False:
            form.feature1_cases.validators = []
            form.feature1_agree.validators = []
        if submission_record.f2_success is False:
            form.feature2_cases.validators = []
            form.feature2_agree.validators = []
        if submission_record.f3_success is False:
            form.feature3_cases.validators = []
            form.feature3_agree.validators = []

    if form.validate_on_submit():
        # Store the feedback provided by the student in the database
        submission_record.f1_cases = form.feature1_cases.data
        submission_record.f1_agree = form.feature1_agree.data
        submission_record.f2_cases = form.feature2_cases.data
        submission_record.f2_agree = form.feature2_agree.data
        submission_record.f3_cases = form.feature3_cases.data
        submission_record.f3_agree = form.feature3_agree.data
        submission_record.feedback_rating = form.rating.data
        submission_record.feedback_comments = form.comments.data
        submission_record.time_feedback = datetime.utcnow()
        submission_record.completed = True
        db.session.commit()

        return render_template('completed.html', title='Task Completed')

    # Analyze the notebook and retrieve solution features
    solution_features = tools.analyze_notebook(cbi_framework.topic, submission_record.file_path, module_name,
                                               app.config['MODULES_FOLDER'], convert=False)

    # Render the feedback template for the corresponding feedback type
    feedback_html = 'feedback_' + str.lower(cbi_framework.topic.name) + '.html'
    return render_template(feedback_html, title='Feedback', fb_type=feedback_type, features=solution_features,
                           form=form)
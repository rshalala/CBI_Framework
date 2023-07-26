from datetime import datetime
from cbi_framework import db


class User(db.Model):
    # Model for representing users
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    student_1_email = db.Column(db.String(50), nullable=False)
    student_2_email = db.Column(db.String(50))
    student_1_id = db.Column(db.String(10))
    student_2_id = db.Column(db.String(10))
    fb_type_hypothesis = db.Column(db.Integer)
    fb_type_tvd = db.Column(db.Integer)
    fb_type_classification = db.Column(db.Integer)
    submissions = db.relationship('Submission', backref='user', lazy=True)

    def __repr__(self):
        return f"User(ID: {self.id}, Email 1: {self.student_1_email}, Email 2: {self.student_2_email}, " \
               f"Hypothesis FB type: {self.fb_type_hypothesis}, TVD fb type: {self.fb_type_tvd}, " \
               f"Classification FB type: {self.fb_type_classification})\n"


class Submission(db.Model):
    # Model for representing user submissions

    # general - submit page
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String(20))
    feedback_type = db.Column(db.Integer)
    file_path = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

    # timestamps for evaluating time spent on feedback page
    time_submit = db.Column(db.DateTime)
    time_feedback = db.Column(db.DateTime)

    # features - submit page
    num_of_features = db.Column(db.Integer)
    f1_name = db.Column(db.String(30))
    f2_name = db.Column(db.String(30))
    f3_name = db.Column(db.String(30))

    # features test cases results - submit page
    f1_success = db.Column(db.Boolean)
    f2_success = db.Column(db.Boolean)
    f3_success = db.Column(db.Boolean)

    # feedback - feedback page
    feedback_rating = db.Column(db.Integer)
    feedback_comments = db.Column(db.String(500))

    # feedback responses for failed features - feedback page
    f1_cases = db.Column(db.String(10))
    f1_agree = db.Column(db.String(5))
    f2_cases = db.Column(db.String(10))
    f2_agree = db.Column(db.String(5))
    f3_cases = db.Column(db.String(10))
    f3_agree = db.Column(db.String(5))


    def __repr__(self):
        return f"Submission(ID: {self.id}, User ID: {self.user_id}, Topic: {self.topic}, " \
               f"FB type: {self.feedback_type}, Feedback rating: {self.feedback_rating}, " \
               f"\nFeatures: (1) {self.f1_name}: {self.f1_success}, (2) {self.f2_name}: {self.f2_success}, " \
               f"(3) {self.f3_name}: {self.f3_success}, Completed: {self.completed})\n"

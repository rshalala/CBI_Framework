# Code-Based Invention (CBI) Framework

The Code-Based Invention (CBI) Framework is a web application designed to facilitate code-based invention activities for educational and research purposes. It offers personalized feedback to students and assists in managing and analyzing activities at scale.

## Key Features

### Submission System

The CBI Framework's submission system incorporates two main features:

1. **Automated Solution Validation:** The framework automates the validation of submitted solutions, checking for code errors and ensuring that the invented method returns a valid numerical value. If validation fails, specific error prompts are provided to students to request resubmission.

2. **Personalized Feedback:** Personalized feedback is a central feature of the CBI Framework, serving to identify errors in students' solutions and summarize relevant knowledge for subsequent instructional phases. The feedback system employs test cases to evaluate specific features of the submitted solution and presents feedback in both explicit and implicit formats.

### Analyzer Mode

The analyzer mode of the CBI Framework is designed to assist in teaching and research purposes. It automates the process of analyzing a group of solutions (Jupyter notebooks) and generates data for comparison and insights. Instructors can gain valuable insights by comparing different groups of solutions and understanding student performance.

## How to Use the CBI Framework

1. **Clone the Repository:** Clone the CBI Framework repository from [GitHub Repository Link](insert_link).
2. **Install Dependencies:** Ensure you have Python and the required libraries installed. You can set up a virtual environment to isolate dependencies for this project. Run the following code to install all necessary dependencies for the CBI Framework application:
    ```bash
    pip install -r requirements.txt
    ```

3. **Initialize Database:** Initialize the database using the methods provided in `tools.py`. Example of usage:
    ```
    from cbi_framework import app, db, tools
    from cbi_framework.models import User, Submission

    with app.app_context():
        tools.db_init_user_table()
        tools.db_init_submission_table()
    ```

4. **Configure Settings:** Customize the CBI Framework by adjusting settings in the `__init__.py` file. You can specify various file paths and the active topic (e.g., classification).

5. **Run the Application:** Launch the CBI Framework web application using the command `python run.py`.

6. **To Add New Activity:** 
   - Create a Jupyter notebook containing the activity, you can refer to the sample activities provided in the `Testing notebooks` folder. Note that these also contain solutions as they are intended for illustarating the application.
   - Create a new Python file containing the implementation of the desired test in the `cbi_framework/analysis` folder, 
   - Create an HTML file in the `cbi_framework_templates` containing the feedback presentation based on the test cases yields. You can use the feedback files in the folder as templates.


## Source Code Overview

The application contains the following files:
- `__init__.py`: Initializes the Flask application and sets up the database.
- `views.py`: Contains the main views and routes for the web application.
- `tools.py`: Includes utility functions for analyzing Jupyter notebooks and managing the database.
- `forms.py`: Defines the WTForms used in the application for user input and feedback.
- `models.py`: Defines the database models (User and Submission) using SQLAlchemy.

## Contributing

Contributions to the CBI Framework are welcome! If you encounter any issues, have ideas for improvements, or would like to contribute new features, feel free to submit a pull request.

## License

The CBI Framework is licensed under the MIT License and is jointly owned by . You are free to use, modify, and distribute the software under the terms of this license. See the LICENSE file for more details.

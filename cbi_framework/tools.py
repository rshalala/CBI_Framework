from inspect import getmembers, isfunction, getsourcelines
import pandas as pd
import os
import sys
import importlib
from cbi_framework import Topic


def analyze_notebook(topic: Topic, notebook_path, module_name, module_path, convert=True):
    """
    Analyze a Jupyter notebook to extract solution features using the specified topic.

    :param topic: Enum representing the topic of analysis (e.g., Hypothesis, TVD, Classification).
    :param notebook_path: Path to the Jupyter notebook to analyze.
    :param module_name: Name of the module to create from the notebook.
    :param module_path: Path to the folder where the module will be saved.
    :param convert: Boolean flag to convert the notebook to a Python script (default=True).
    :return: Result of the analysis, or an Exception if an error occurs during analysis.
    """
    if convert:
        # Convert the notebook to a Python module
        command = f'jupyter nbconvert --output-dir="." --to script "{notebook_path}" --output ' \
                  f'{module_path}{module_name}'
        os.system(command)

    package_name = module_path.replace('/', '.')
    try:
        # Import the created module
        module = importlib.import_module(package_name + module_name)
        if package_name + module_name in sys.modules:
            module = importlib.reload(module)
    except Exception as err:
        return err

    # Get a list of functions in the module
    methods_list = [item[0] for item in getmembers(module) if isfunction(item[1])]
    if 'calculate_measure' not in methods_list:
        print(f"'calculate_measure' was not found in {methods_list}")
        return None
    
    analyzer = None  # just to avoid warning
    if topic is Topic.HYPOTHESIS:
        from cbi_framework.analysis import hypothesis as analyzer
    elif topic is Topic.TVD:
        from cbi_framework.analysis import tvd as analyzer
    elif topic is Topic.CLASSIFICATION:
        from cbi_framework.analysis import classification as analyzer
    elif topic is Topic.CLUSTERING:
        from cbi_framework.analysis import clustering as analyzer

    try:
        # Call the appropriate analyze_solution function based on the topic
        result = analyzer.analyze_solution('calculate_measure', module)
        return result
    except Exception as err:
        try:
            os.remove(module_path + module_name + '.py')
        except FileNotFoundError:
            print(f"{module_path + module_name} was not found. unable to delete")
        return err


def is_text_in_source_code(text: str, source_code: list) -> bool:
    """
    Check if the given text exists in the source code.

    :param text: Text to search for in the source code.
    :param source_code: List of strings representing the source code.
    :return: True if the text is found in the source code, False otherwise.
    """
    for line in source_code:
        if line.find(text) != -1:
            return True
    return False


def remove_used_methods(methods_names_list: list, module) -> list:
    """
    Remove methods (from the given methods_names_list) that are used by other methods in the given notebook.\n
    :param methods_names_list: List of methods names
    :param module: Notebook Python module
    :return: List containing only methods names that are not being used by other methods
    """
    relevant_methods = methods_names_list.copy()
    for method_name in methods_names_list:
        for to_import in methods_names_list:
            if method_name == to_import:
                continue
            imported = getattr(module, to_import)
            source_code_list = getsourcelines(imported)[0]
            if is_text_in_source_code(method_name, source_code_list):
                relevant_methods.remove(method_name)
                break

    return relevant_methods


def create_users_dictionary(csv_file):
    """
    Create a dictionary of authorized emails and their corresponding IDs from the provided CSV file.

    :param csv_file: Path to the CSV file containing email and ID columns.
    :return: Dictionary mapping authorized emails to their IDs.
    """
    df = pd.read_csv(csv_file)
    authorized_emails = df['email'].to_list()
    ids = df['id'].to_list()
    return dict(zip(authorized_emails, ids))


# def export_db_to_csv_files():
#     from cbi_framework import db
#     engine = db.get_engine()
#     # engine.table_names() to get the model names - should be just lowercase of the model names
#     connection = engine.connect()
#     df = pd.read_sql_table(model_name, connection)
#     return df


def db_recreate_table(table_model_obj):
    from cbi_framework import db
    engine = db.get_engine()
    table_model_obj.__table__.drop(engine)
    table_model_obj.__table__.create(engine)


def db_init_submission_table():
    from cbi_framework.models import Submission
    db_recreate_table(Submission)


def db_init_user_table():
    from cbi_framework.models import User
    db_recreate_table(User)
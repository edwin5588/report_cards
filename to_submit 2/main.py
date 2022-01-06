import sys
import pandas as pd
import numpy as np
import json
import os



def csv_to_pd(fp, csv_name):
    """
    converts CSV to a pandas dataframe object

    returns a dataframe object
    """

    df = pd.read_csv(fp)
    df = df.dropna()
    df.columns = [csv_name+ "_" +column for column in df.columns]
    return df

def validate_dataframes(df, kind):
    """
    validates dataframes and their datatypes based on different df.

    kinds = [courses, students, marks, tests]


    """

    if kind == 'marks':
        assert df[df['_mark'] < 0]["_mark"].sum() == 0, "Some scores are less than 0"
    elif kind == 'tests':
        assert df.tests_id.count() == len(df.tests_id.unique()), "Conflicting test ids"
    elif kind == 'courses':
        assert df.courses_id.count() == len(df.courses_id.unique()), "Conflicting course ids"
    elif kind == 'students':
        assert df.students_id.count() == len(df.students_id.unique()), "Conflicting student ids"



def check_test_weights(tests_pd):
    """
    checks the test weights
    weights must add up to 100, for each distinct course.

    returns true/false

    """

    for course_id in tests_pd.tests_course_id.unique():
        weights_sum = tests_pd[tests_pd['tests_course_id'] == course_id]['tests_weight'].sum()
        assert (weights_sum == 100), "Course weights do not add up to be 100!"
        if weights_sum != 100:
            return False
    return True



def get_test_weight(test_id, tests_pd):
    """
    get the test weight from a test_id

    """
    assert test_id in tests_pd.tests_id.unique(), ("Test ID: " + str(test_id) + " is not found in tests.csv!!")
    return tests_pd[tests_pd['tests_id'] == test_id]['tests_weight'].values[0]

def get_course_id(test_id, tests_pd):
    """
    get the corresponding course ID from a test_id

    """
    assert test_id in tests_pd.tests_id.unique(), ("Test ID: " + str(test_id) + " is not found in tests.csv!!")

    return tests_pd[tests_pd['tests_id'] == test_id]['tests_course_id'].values[0]

def add_info_to_marks(marks_pd, tests_pd):
    """
    adds weights, weighted_scores, and course_id to marks dataframe

    returns aggregated dataframe
    """

    marks_pd['weights'] = marks_pd['_test_id'].apply(lambda x: get_test_weight(x, tests_pd))
    marks_pd['weighted_scores'] = marks_pd['_mark']/100 * marks_pd['weights']/100
    marks_pd['course_id'] = marks_pd['_test_id'].apply(lambda x: get_course_id(x, tests_pd))
    return marks_pd

def json_builder(student_pd, courses_pd, additional_marks):
    """
    builds the json output file
    """
    student_tests = additional_marks.groupby("_student_id")
    unique_courses = courses_pd.courses_id.unique()

    # iterate through students
    json = {"students":[]}
    for student in student_pd.students_id.unique():
        studentName = student_pd[student_pd['students_id'] == student]["students_name"].values[0]
        totalAverage = 0
        course_counts = 0


        # iterate through the courses that this student took
        courses = []
        tests = student_tests.get_group(student)
        for course_id in tests.course_id.unique():
            assert course_id in unique_courses, ("Student " + str(studentName) + " took a non existing course: course ID : " + str(course_id))
            course = {}
            course_counts += 1
            courseAverage = round(tests[tests['course_id'] == course_id]["weighted_scores"].sum() * 100, 2)
            course_name = courses_pd[courses_pd['courses_id'] == course_id]['courses_name'].values[0]
            course_teacher = courses_pd[courses_pd['courses_id'] == course_id]['courses_teacher'].values[0]
            totalAverage += courseAverage

            course["id"] = int(course_id)
            course["name"] = course_name
            course["teacher"] = course_teacher
            course["courseAverage"] = courseAverage

            courses.append(course)

        json["students"].append({"id":int(student),
        "name":studentName,
        "totalAverage":round(totalAverage/course_counts, 2),
        "courses":courses})


    return json


if __name__ == "__main__":

    arguments = sys.argv
    courses_fp = arguments[1]
    students_fp = arguments[2]
    tests_fp = arguments[3]
    marks_fp = arguments[4]
    output_fp = arguments[5]

    tests_pd = csv_to_pd(tests_fp, 'tests')
    # FIRSTLY! check if course weights are valid:
    if check_test_weights(tests_pd) == False:
        dct = {"error": "Invalid course weights"}
        with open(output_fp, 'w') as fp:
            json.dump(dct, fp)
        fp.close()

        print("JSON outputted")
    else:
        # load dataframes to memory
        courses_pd = csv_to_pd(courses_fp, 'courses')
        student_pd = csv_to_pd(students_fp, 'students')
        marks_pd = csv_to_pd(marks_fp, '')

        validate_dataframes(courses_pd, 'courses')
        validate_dataframes(student_pd, 'students')
        validate_dataframes(marks_pd, 'marks')
        validate_dataframes(tests_pd, 'tests')

        # join marks and tests to calculate weighted averages
        added_info = add_info_to_marks(marks_pd, tests_pd)
        dct = json_builder(student_pd, courses_pd, added_info)
        with open(output_fp, 'w') as fp:
            json.dump(dct, fp)
        fp.close()
        print("JSON outputted")

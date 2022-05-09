import pandas as pd
import numpy as np
import plot_likert
import matplotlib as mpl

def get_dataframe():
    answers = []
    ignore = None
    for i in range(9):
        df = pd.read_excel("./data.xlsx", sheet_name=i, index_col=None)
        if i == 0:
            ignore = df.loc[df['Role and previous experience'].isin(['None of the above'])]['ID']
            print(ignore)
        df = df.loc[~df['ID'].isin(list(ignore))]
        
        answers.append(df)

    return answers

def get_likert_questions(df, question_indexes=None):
    if question_indexes is None:
        question_indexes = []

    likert_answers = df.copy(deep=True)
    columns = [
        "ID", 
        "Tidstämpel", 
        "Highest level of education", 
        "Experience of software development (in years)", 
        "Current occupation",
        "Role and previous experience",
        "Programming best practices",
        "What programming languages are you able to use proficiently?",
        "What programming languages do you use the most?",
        "Are you aware of the term clean code?",
        "Define what clean code is to you",
        "Do you have dyslexia or any other reading disorder?",
        "What naming style do you think is easiest to read? ",
        "Do you think giving constant variables SCREAMING_SNAKE_CASE names increases readability?",
        "What are the reasons for committing code that you are not fully satisfied with?",
        "What activities do/would help you write readable and clean code?",
    ]
    likert_answers.drop(columns, axis=1, inplace=True)
    
    columns = []
    for index in question_indexes:
        columns.append(likert_answers.columns[index])

    likert_answers.drop(columns, axis=1, inplace=True)

    return likert_answers

def plot_likert_data(data, size=(12,12), label_max_width=70):
    plot_likert.plot_likert(data, [1,2,3,4,5,6,7], 
        plot_percentage=True, 
        colors=plot_likert.colors.likert7,
        figsize=size,
        label_max_width=label_max_width
        )

def filter(df, columns, values_2d, negate_values=None):
    if negate_values is None or negate_values is False:
        negate_values = [False for i in range(len(columns))]
    elif negate_values is True:
        negate_values = [True for i in range(len(columns))]

    data = df.copy(deep=True)
    for column, values, neg in zip(columns, values_2d, negate_values):
        if not neg:
            data = data.loc[data[column].isin(values)]
        else:
            data = data.loc[~data[column].isin(values)]

    return data

    
def filter_on_values_from_sheet(df, sheet, columns, negate_values=None):
    if negate_values is None or negate_values is False:
        negate_values = [False for i in range(len(columns))]
    elif negate_values is True:
        negate_values = [True for i in range(len(columns))]

    data = df.copy(deep=True)
    sheet_data = sheet.copy(deep=True)
    for column, neg in zip(columns, negate_values):
        if not neg:
            sheet_data = sheet_data[sheet_data[column].notnull()]
        else:
            sheet_data = sheet_data[~sheet_data[column].notnull()]

    data = data.loc[data["ID"].isin(sheet_data['ID'])]

    return data
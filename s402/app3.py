import gradio

import numpy
import pandas

from matplotlib import pyplot
import seaborn

import re

students = pandas.read_csv("student_habits_performance.csv")

def controlador(edad, genero):
    pattern_male = re.compile(r"h", re.IGNORECASE)
    pattern_female = re.compile(r"m", re.IGNORECASE)

    if pattern_male.match(genero):
        genero = "Male"
    elif pattern_female.match(genero):
        genero = "Female"
    else:
        genero = "Other"

    students_group = students[
        (students["age"] == edad) &
        (students["gender"] == genero)
    ]

    exam_score_mean = students_group["exam_score"].mean()

    figure, axis = pyplot.subplots(2, 1)

    seaborn.boxplot(x=students_group["exam_score"], ax=axis[0])
    seaborn.kdeplot(x=students_group["exam_score"], ax=axis[1])

    return(exam_score_mean, figure, students_group)

vista = gradio.Interface(
    fn=controlador,
    inputs=[
        gradio.Slider(17, 25, step=1, label="Edad"),
        gradio.Textbox(label="Hombre / Mujer / Otro"),
    ],
    outputs=[
        gradio.Text(label="Calificacion promedio"),
        gradio.Plot(label="Grafica de las calificaciones en el segmento"),
        gradio.DataFrame(label="Calificaciones en el segmento"),
    ]
)

vista.launch()
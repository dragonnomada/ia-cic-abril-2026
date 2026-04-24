import gradio

from matplotlib import pyplot

# (Input 1 <- Textbox, Input 2 <- Number)
def controlador(nombre, edad):

    figure, axis = pyplot.subplots(1, 1)

    axis.plot([1, 2, 3], [4, 5, 6])

    # (Output 1 -> Text, Output 2 -> Plot)
    return (f"Hola {nombre}, tienes {edad} años", figure)

# Input
#   - Textbox
#   - Number
#   - Slicer
#   - Checkbox

# Output
#   - Text
#   - Label
#   - Plot
#   - DataFrame

vista = gradio.Interface(
    fn=controlador,
    inputs=[
        # Input 1
        gradio.Textbox(
            label="Nombre"
        ),
        # Input 2
        gradio.Number(
            label="Edad"
        ),
    ],
    outputs=[
        # Output 1
        gradio.Text(
            label="Saludo"
        ),
        # Output 2
        gradio.Plot(
            label="Grafica"
        ),
    ]
)

vista.launch()
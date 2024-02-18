import pandas as pd
from jinja2 import Template
import pyhtml as ph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import base64


class DataError(Exception):
    def __init__(self, message="Wrong Data"):
        self.message = message
        super().__init__(self.message)


def process_student_details(student_id):
    try:
        marks = pd.read_csv("data.csv")
        if student_id not in marks["Student id"].values:
            raise DataError("No such Student")
        s_marks = marks[marks["Student id"] == student_id]
        m_sum = sum(s_marks[" Marks"])

        pyhtml_rows = [
            ph.tr(ph.th("Student id"), ph.th("Course id"), ph.th("Marks")),
            *[
                ph.tr(
                    ph.td(str(row["Student id"])),
                    ph.td(str(row[" Course id"])),
                    ph.td(str(row[" Marks"])),
                )
                for _, row in s_marks.iterrows()
            ],
        ]

        template_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Student Data</title>
        </head>
        <body>
            <h1>Student Details</h1>
            <table border = "2" id = "student-details-table">
                {% for row in pyhtml_rows %}
                    {{ row }}
                {% endfor %}
                <tr>
                    <td colspan = "2" style="text-align:center">Total Marks:</td>
                    <td>{{ total_marks }}</td>
                </tr>
            </table>
            <br>
            <a href="http://127.0.0.1:5000/">Go Back</a>
        </body>
        </html>
        """

        template = Template(template_str)
        html_page = template.render(pyhtml_rows=pyhtml_rows, total_marks=m_sum)
        return html_page
    except DataError as e:
        return process_exception()


def process_course_details(course_id):
    try:
        marks = pd.read_csv("data.csv")

        if course_id not in marks[" Course id"].values:
            raise DataError("No such Course")

        c_marks = marks[marks[" Course id"] == course_id]
        c_max = c_marks[" Marks"].max()
        c_avg = c_marks[" Marks"].mean()

        fig = plt.Figure(figsize=(5, 4))
        canvas = FigureCanvasAgg(fig)

        ax = fig.add_subplot(111)
        ax.hist(c_marks[" Marks"], bins=10, edgecolor="black")
        ax.set_xlabel("Marks")
        ax.set_ylabel("Frequency")

        buf = io.BytesIO()
        fig.canvas.print_png(buf)

        img_data = base64.b64encode(buf.getvalue()).decode("utf-8")

        template_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Course Data</title>
        </head>
        <body>
            <h1>Course Details</h1>
            <table border = "2" id = "course-details-table">
                <tr>
                    <th>Average Marks</th>
                    <th>Maximum Marks</th>
                </tr>
                <tr>
                    <td>{{ average_marks }}</td>
                    <td>{{ max_marks }}</td>
                </tr>
            </table>
            <br>
            <img src= "data:image/png;base64,{{ image_data }}" alt="Histogram">
            <br>
            <a href="http://127.0.0.1:5000/">Go Back</a>
        </body>

        </html>
        """

        template = Template(template_str)
        html_page = template.render(
            average_marks=c_avg, max_marks=c_max, image_data=img_data
        )

        return html_page
    except DataError as e:
        return process_exception()


def process_exception():
    template_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Something Went Wrong</title>
    </head>
    <body>
        <h1>Wrong Inputs</h1>
        <br>
        Something went wrong
        <br>
        <a href="http://127.0.0.1:5000/">Go Back</a>
    </body>
    </html>
    """

    template = Template(template_str)
    html_page = template.render()

    return html_page


def generate(id_type, id_):
    if id_type == "student_id":
        try:
            html_content = process_student_details(id_)
        except Exception as e:
            html_content = process_exception()
    elif id_type == "course_id":
        try:
            html_content = process_course_details(id_)
        except Exception as e:
            html_content = process_exception()
    else:
        html_content = process_exception()
    return html_content

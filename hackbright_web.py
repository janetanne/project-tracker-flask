"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def get_homepage():
	"""Shows homepage with projects and students."""

	list_of_students = hackbright.get_all_students()

	list_of_projects = hackbright.get_all_projects()

	return render_template("homepage.html", projects=list_of_projects,
		students=list_of_students)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html", 
    						first=first,
    						last=last,
    						github=github,
    						student_grades=grades)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def show_add_student_form():
    """Show form for adding a student."""

    return render_template("student_add.html")

@app.route("/student-added", methods=['POST'])
def view_added_student():
	"""Handles data from add_student form."""

	first_name = request.form.get('firstname')
	last_name = request.form.get('lastname')
	github = request.form.get('github')

	hackbright.make_new_student(first_name, last_name, github)

	return render_template("student_added.html", github=github)

@app.route("/project-add")
def show_add_project_form():
    """Show form for adding a project."""

    return render_template("project_add.html")

@app.route("/project-added", methods=['POST'])
def view_added_project():
	"""Handles data from add_project form."""

	title = request.form.get('title')
	description = request.form.get('description')
	max_grade = request.form.get('max_grade')

	hackbright.make_new_project(title, description, max_grade)

	return render_template("project_added.html", title=title)

@app.route("/project")
def get_project_info():
	"""Shows data about project."""

	project_title = request.args.get('title')

	project = hackbright.get_project_by_title(project_title)

	students = hackbright.get_grades_by_title(project_title)

	return render_template("project.html", title=project[0],
							description=project[1],
							max_grade=project[2],
							all_project_grades=students)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "doood its a secret"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result/<id>')
def result(id):
    mysql = connectToMySQL("dojo_survey")
    id = int(id)
    print("*"*50)
    entry = mysql.query_db(f"SELECT * FROM dojo_survey_table WHERE id = {id};")
    return render_template("show.html", entry=entry)

@app.route('/create_result', methods=['POST'])
def create_result():
    print("*"* 50)
    if len(request.form['name']) < 1:
        flash("Please enter a first name")
    if len(request.form['location']) < 1:
    	flash("Please enter a location")
    if len(request.form['language']) < 2:
        flash("Please enter a language")
    if len(request.form['comment']) > 120:
        flash("Please enter a comment shorter than 120 characters")

    if not '_flashes' in session.keys():
        mysql = connectToMySQL("dojo_survey")
        query = "INSERT INTO dojo_survey_table (name, location, language, comment) VALUES (%(nm)s, %(lc)s, %(fl)s, %(cm)s);"
        data = {
            "nm": request.form['name'],
            "lc": request.form['location'],
            "fl": request.form['language'],
            "cm": request.form['comment']
        }
        id = mysql.query_db(query, data)
        return redirect("/result/"+str(id))
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
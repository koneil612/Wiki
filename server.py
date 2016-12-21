from flask import Flask,render_template,request,redirect
from index import *
import mysql.connector
import config

app = Flask("MyApp")

@app.route("/")
def home(methods=["GET"]):
    # list = Entry.getObjects()
    return render_template("layout.html", title="Wiki Pages")


@app.route("/<page_name>")
def placeholder(page_name):
    e = Entry(0,page_name)
    print e.content
    return render_template("placeholder.html", page=e)

# @app.route("/new_entry")
# def new_entry():
#     return render_template("edit.html", index=Entry())

@app.route("/<page_name>/edit", methods=["POST", "GET"])
def edit(page_name):
    id=request.form.get('id')
    entry=Entry()
    entry.title=request.form.get('title')
    entry.content=request.form.get('content')
    entry.save()
    return redirect("/savepage.html")

# @app.route("/{{page.title}}/update_entry",methods=["POST","GET"])
# def update_entry():
#     id=request.args.get('id')
#     entry = Entry(id)
#     return  render_template("edit.html",entry=entry)

if __name__=="__main__":
    app.run(debug=True)

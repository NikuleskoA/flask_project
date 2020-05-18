from flask import Flask
from flask import (
    request, flash, url_for, redirect, g, render_template)
from libs.postgres_db import get_db
from libs.ship import Ship

app = Flask(__name__)


@app.route('/add', methods=['POST', 'GET'])
def add_ship():
    if request.method == 'GET':
        countries = get_db().get_countries()
        return render_template('add_ship.html', countries=countries)
    else:
        temp_ship=Ship(name=request.form['name'], country_name=request.form['country'],description=request.form['description'],
                length=request.form['length'], width = request.form['width'],built_year=request.form['year'] , sid =None)
        get_db().insert_ship(temp_ship)
        return render_template('ships_table_form.html',ship_list=get_db().get_ships())


@app.route('/', methods=['POST', 'GET'])
def result():
    list1 = get_db().get_ships()
    if request.method == 'POST':
        result1 = request.form
        return render_template("ships_table_form.html", result=result1, ship_list=list1)
    else:
        return render_template("ships_table_form.html", result=None, ship_list=list1)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        if (not request.form['name'] or
                not request.form['country'] or
                not request.form['description']or
                not request.form['year'] or
                not request.form['length']or
                not request.form['width']):
            print("Ошибка")
        else:
            temp_ship = Ship(name=request.form['name'], built_year=request.form['year'],country_name=request.form['country'],
                 length=request.form['length'], description=request.form['description'], width=request.form['width'], sid=request.form['id'])
            print(temp_ship.make_dict())
            get_db().update_ship(temp_ship)
            return redirect(url_for("result"))
    else:
        ship_name = request.args.get('name')
        temp_ship = get_db().get_ship_by_name(ship_name)
        countries = get_db().get_countries()
        return render_template('edit.html', ship=temp_ship, countries=countries)


@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        ship_name = request.args.get('name')
        print(ship_name)
        get_db().del_ship(ship_name)
        return render_template("ships_table_form.html", result=None, ship_list=get_db().get_ships())

if __name__ == '__main__':
    app.run()

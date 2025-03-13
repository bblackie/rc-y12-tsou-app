from flask import Flask,g,render_template
import sqlite3 

app = Flask(__name__)

DATABASE = 'southeys_autoworld_database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/test")
def home():
    return render_template("test.html")



@app.route("/contents")
def contents():
    db = get_db()
    cursor = db.cursor()
    sql = """
        SELECT 
            Car_stock.stock_id,
            Car_manufacturer.manufacturer_name,
            Car_model.model_name,
            Car_stock.year,
            Car_bodystyle.bodystyle_name,
            Car_stock.car_price,
            Car_stock.distance
        FROM Car_stock
        JOIN Car_model ON Car_stock.model_id = Car_model.model_id
        JOIN Car_manufacturer ON Car_stock.manufacturer_id = Car_manufacturer.manufacturer_id
        JOIN Car_bodystyle ON Car_stock.bodystyle_id = Car_bodystyle.bodystyle_id
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return render_template("contents.html", results=results)
                                                                          

if __name__ == "__main__":
    app.run(debug=True)


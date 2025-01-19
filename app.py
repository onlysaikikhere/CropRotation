from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Crop rotation recommendations
CROP_ROTATION = {
    'corn': ['soybeans', 'wheat', 'clover'],
    'soybeans': ['corn', 'wheat', 'oats'],
    'wheat': ['clover', 'corn', 'soybeans'],
    'potatoes': ['beans', 'corn', 'peas'],
    'tomatoes': ['beans', 'lettuce', 'spinach'],
}

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            area REAL NOT NULL,
            current_crop TEXT NOT NULL,
            soil_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html', page='home')

@app.route('/fields')
def view_fields():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM fields')
    fields = c.fetchall()
    conn.close()
    return render_template('index.html', page='fields', fields=fields, recommendations=CROP_ROTATION)

@app.route('/add_field', methods=['GET', 'POST'])
def add_field():
    if request.method == 'POST':
        name = request.form['name']
        area = float(request.form['area'])
        current_crop = request.form['current_crop'].lower()
        soil_type = 'loamy'  # Always set soil type to 'loamy'
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO fields (name, area, current_crop, soil_type) VALUES (?, ?, ?, ?)', 
                  (name, area, current_crop, soil_type))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_fields'))
    return render_template('index.html', page='add_field')

@app.route('/delete_field/<int:field_id>', methods=['POST'])
def delete_field(field_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM fields WHERE id = ?', (field_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_fields'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
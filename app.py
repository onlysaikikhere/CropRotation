# app.py 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)  # This line is crucial

# Crop rotation recommendations
CROP_ROTATION = {
    'corn': ['soybeans', 'wheat', 'clover'],
    'soybeans': ['corn', 'wheat', 'oats'],
    'wheat': ['clover', 'corn', 'soybeans'],
    'potatoes': ['beans', 'corn', 'peas'],
    'tomatoes': ['beans', 'lettuce', 'spinach'],
}

# Store fields in memory
fields = []

@app.route('/')
def home():
    return render_template('index.html', page='home')  # passing page variable

@app.route('/fields')
def view_fields():
    return render_template('index.html', page='fields', fields=fields, recommendations=CROP_ROTATION)

@app.route('/add_field', methods=['GET', 'POST'])
def add_field():
    if request.method == 'POST':
        field = {
            'name': request.form['name'],
            'area': float(request.form['area']),
            'current_crop': request.form['current_crop'].lower(),
            'soil_type': 'loamy'  # Always set soil type to 'loamy'
        }
        fields.append(field)
        return redirect(url_for('view_fields'))
    return render_template('index.html', page='add_field')


if __name__ == '__main__':
    app.run(debug=True)
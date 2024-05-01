from app import app
from flask import render_template

# This is for rendering the home page
# Here's the basics for making any new route
# It's a good idea to use the same name/word, and same capitalization conventions
# Add a route name, function name, and html template name 
# (then go make that html template)
@app.route('/bart')
def bart():
    return render_template('bart.html')
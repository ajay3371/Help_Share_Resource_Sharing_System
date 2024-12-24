from flask import Flask, render_template, request, redirect, url_for,session
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Dummy data for users and food posts (replace with your database)
users = {
    'user1': {'password': 'password1', 'address': '123 Main St', 'village': 'Village1'},
    'user2': {'password': 'password2', 'address': '456 Elm St', 'village': 'Village2'}
}

food_posts = []

# Define a route for the homepage
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], food_posts=food_posts)
    else:
        return redirect(url_for('login'))
# Define a route for the login page
# Define a route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html', error=None)
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Define a route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username is already taken
        if username in users:
            error = 'Username is already taken. Please choose a different username.'
            return render_template('register.html', error=error)
        
        # If username is not taken, proceed with user registration
        
        users[username] = {'username': username, 'password': password}
        
        # Automatically log in the user after successful registration
        session['username'] = username
        
        # Redirect to homepage with a registration successful message
        return redirect(url_for('index', message='Registration successful'))
    
    return render_template('register.html')

food_posts = [
    {
        'username': 'user1',
        'food_name': 'Marriage Food',
        'address': '123 Main St, Village1',
        'details': 'Available for 50 members. Delicious dishes prepared for a wedding celebration.',
        'image_url': 'https://www.foodfood.com/blog/wp-content/uploads/2022/05/Latest-Indian-Wedding-Food-Menu-List.jpg'
    },
    {
        'username': 'user2',
        'food_name': 'Birthday Party Food',
        'address': '456 Elm St, Village2',
        'details': 'Leftover snacks and cake from a birthday party. Suitable for 20 guests.',
        'image_url': 'https://i.pinimg.com/originals/ac/2b/4e/ac2b4e120237348f501f62c415b125ea.jpg'
    },
    {
        'username': 'user3',
        'food_name': 'Community Potluck',
        'address': '789 Oak St, Village3',
        'details': 'Various dishes contributed by community members. Come and enjoy!',
        'image_url': 'https://5.imimg.com/data5/EP/OM/MY-12821574/catering_taj_wedding_services-500x500.jpg'
    },
    {
        'username': 'user4',
        'food_name': 'Office Lunch Buffet',
        'address': '101 Pine St, Village4',
        'details': 'Leftover buffet items from the office lunch. Take as much as you want!',
        'image_url': 'https://miro.medium.com/v2/resize:fit:720/1*A4A1_7qXyaof4UlaB3y-hw.jpeg'
    },
    {
        'username': 'user5',
        'food_name': 'Family Reunion Feast',
        'address': '202 Maple St, Village5',
        'details': 'Generous spread of homemade dishes. Bring your own containers!',
        'image_url': 'https://i.ytimg.com/vi/heKwu-6ZSKM/hqdefault.jpg'
    },
    # Add more sample food posts as needed
]


@app.route('/food')
def food():
    # Example data: list of available food items
    return render_template('food.html', food_posts=food_posts)
# Define a route for posting food
@app.route('/post_food', methods=['GET', 'POST'])
def post_food():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        food_name = request.form['food_name']
        address = request.form['address']
        details = request.form['details']
        image_url = request.form['image_url']
        image_file = request.files['image_file']

        # Save image if uploaded
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            image_url = url_for('static', filename='uploads/' + image_filename)

        new_food_post = {
            'username': session['username'],
            'food_name': food_name,
            'address': address,
            'details': details,
            'image_url': image_url
        }
        food_posts.append(new_food_post)
        return redirect(url_for('index'))

    return render_template('post_food.html')

@app.route('/claim_food', methods=['POST'])
def claim_food():
    if 'username' not in session:
        return redirect(url_for('login'))

    food_post_index = int(request.form['food_post_index'])
    if 0 <= food_post_index < len(food_posts):
        claimed_food = food_posts.pop(food_post_index)
        return render_template('claimed.html')  # Render the claimed food page
    else:
        return "Invalid food post index."
if __name__ == '__main__':
    app.run(debug=True)

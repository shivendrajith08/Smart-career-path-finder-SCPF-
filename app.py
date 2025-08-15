from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'spidey_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# DB Model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        existing = User.query.filter_by(email=email).first()
        if existing:
            error = '📛 Email already exists!'
        else:
            user = User(username=uname, email=email, password=pwd)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email, password=pwd).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/chat')
        else:
            error = '🛑 Invalid credentials!'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect('/login')
    messages = []
    if request.method == 'POST':
        user_input = request.form['message']
        bot_reply = ai_reply(user_input)
        messages.append({'type': 'user', 'text': user_input})
        messages.append({'type': 'bot', 'text': bot_reply})
    return render_template('chat.html', messages=messages, username=session.get('username'))

# AI Logic
def ai_reply(msg):
    msg = msg.lower()
    links = {
        "python": "https://roadmap.sh/python",
        "frontend": "https://roadmap.sh/frontend",
        "backend": "https://roadmap.sh/backend",
        "full stack": "https://roadmap.sh/full-stack",
        "data science": "https://roadmap.sh/data-science",
        "cybersecurity": "https://roadmap.sh/cyber-security",
        "ai": "https://roadmap.sh/ai",
        "devops": "https://roadmap.sh/devops",
        "cloud": "https://roadmap.sh/devops",
        "sql": "https://www.codecademy.com/learn/learn-sql",
        "ml": "https://roadmap.sh/ai",
        "react": "https://roadmap.sh/react",
        "android": "https://developer.android.com/courses",
    }

    for key in links:
        if key in msg:
            return f"""
                ✅ <b>{key.title()} Roadmap Ready!</b><br>
                🔗 <a href="{links[key]}" target="_blank">{links[key]}</a><br>
                🔥 Ungaluku {key.title()} path semma choice! Start pannunga bro! 💪
            """

    # Fallbacks
    if "job" in msg:
        return "💼 Job theduvingala? LinkedIn, Naukri la try pannunga. Resume update pannu."

    if "resume" in msg:
        return "📝 Resume la skills, projects highlight pannu. Canva, Novoresume use pannu."

    if "course" in msg or "learn" in msg:
        return "📚 Udemy, Coursera, FreeCodeCamp – free resources iruku bro!"

    # 💥 Default Roadmap Suggestion
    return """
        🤖 Naan ready da! Specific field sollunga na nalladhudhaan.<br>
        🔗 But unga career ku help aagura default roadmap link inga: <br>
        👉 <a href="https://roadmap.sh" target="_blank">https://roadmap.sh</a><br>
        🔥 Ellathayum browse panni unga interest choose pannunga! 😎
    """


    for key in links:
        if key in msg:
            return f"✅ <b>{key.title()} Roadmap Ready!</b><br>🔗 <a href='{links[key]}' target='_blank'>{links[key]}</a><br>🔥 Ungaluku {key.title()} path strong da! Kandippa try pannunga! 💪"

    if "job" in msg:
        return "💼 Job theduvingala? LinkedIn, Naukri, Indeed la try pannunga. Resume update pannunga bro!"

    if "resume" in msg:
        return "📝 Resume la highlight pannunga: skills, projects, certifications. Canva or Novoresume use pannu."

    if "course" in msg or "learn" in msg:
        return "📚 Udemy, Coursera, FreeCodeCamp – super resources iruku. Daily 1 hour practice pannu."

    return "🤖 Spidey ready da! Unga interest ennanu sollunga, naan roadmap kudukkaren superhero style la!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


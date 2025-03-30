from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

DATABASE = 'personal_site.db'

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So rows can be accessed like dictionaries
    return conn

# Blog route
@app.route("/blog")
def blog():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY created DESC").fetchall()
    conn.close()
    return render_template("blog.html", posts=posts)

# Route to initialize a post (for testing)
@app.route("/init_post")
def init_post():
    conn = get_db_connection()
    conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
                 ("My First Blog Post", "This is a sample blog post about my project."))
    conn.commit()
    conn.close()
    return "Initial post added."

# Route to create a new post
@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content:
            flash("Title and content are required!", "danger")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            flash("New post added successfully.", "success")
            return redirect(url_for('blog'))
    
    return render_template("new_post.html")


# Homepage route
@app.route("/")
def home():
    projects = [
        {"title": "Survey of Environmental Impacts of Plastic, Paper, and Cloth Bags",
         "desc": "In this project, I analyzed consumer buying behavior and assessed the environmental implications of various packaging solutions. I evaluated the trade-offs between plastic, paper, and cloth bags by considering their environmental impact and consumer preferences. Through quantitative analysis, I was able to provide valuable insights into the factors driving consumer choices and offer recommendations to promote sustainable packaging practices."},
        {"title": "Cost and Revenue Analysis of India’s Tourism Industry",
         "desc": "This project involved forecasting revenue trends for India’s tourism sector in a post-COVID scenario and identifying potential growth opportunities. Using data analysis and econometric techniques, I assessed the impact of policy measures and economic shifts on the sector’s future growth. The project’s findings provided strategic insights that could guide investment and policy decisions, showcasing my ability to apply data-driven methodologies to solve industry challenges."}
    ]

    experiences = [
        {"title": "Research Assistant | Ashoka University, Sonipat, Haryana",
         "desc": "As a Research Assistant at Ashoka University, I worked extensively with firm-level datasets, performing data cleaning and merging using Stata. I analyzed industry and sectoral trends by visualizing growth indicators through time-series graphs and applied econometric models to evaluate trade performance using panel data. This experience enhanced my ability to manage and analyze large datasets, improving my proficiency in econometric modeling and data-driven research."},
        {"title": "Digital & Analytics Intern | PGP Glass Pvt. Ltd., Vadodara, Gujarat",
         "desc": "During my internship at PGP Glass Pvt. Ltd., I processed and analyzed over 10,000 consumer records to derive actionable insights. I utilized Python libraries such as NumPy and pandas to clean and analyze the data, while Seaborn and Matplotlib were employed to create visualizations that revealed meaningful patterns and trends. The insights generated helped identify potential target markets for launching a health-focused product, demonstrating my ability to apply analytical tools to solve real-world business challenges."},
        {"title": "Teaching Assistant | Ahmedabad University, Ahmedabad, Gujarat",
         "desc": "As a Teaching Assistant at Ahmedabad University, I played an integral role in supporting 9 courses and guiding the academic progress of over 200 students. I was responsible for grading more than 300 assignments and exams, offering personalized feedback to enhance student performance. I also collaborated with faculty to develop lesson plans and instructional materials, incorporating interactive learning techniques to improve student engagement."},
        {"title": "Market Research Intern | Bonafide Research, Vadodara, Gujarat",
         "desc": "During my time at Bonafide Research, I conducted market research and consulting for 15+ clients, including Fortune 1000 companies and SMEs. I generated over 10 detailed market reports that influenced strategic decisions, leading to a 20% increase in client profitability. Through this experience, I honed my ability to translate data into actionable business insights and developed a strong foundation in market analysis and research methodologies."}
    ]

    return render_template("home.html", projects=projects, experiences=experiences)


# Contact form route
@app.route("/contact", methods=["POST"])
def contact():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Simulate form submission (In real apps, save to DB or send email)
    print(f"Received message from {name} ({email}): {message}")

    # Redirect back to home after submitting
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

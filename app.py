from flask import Flask, render_template, redirect, session, request
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', "avif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def top():
    session["before_page"] = "/"
    return render_template("top.html")

@app.route("/project_list")
def project_list():
    session["before_page"] = "/project_list"
    return render_template("project_list.html")

@app.route("/project")
def project():
    session["before_page"] = "/project"
    return render_template("project.html")

@app.route("/login", methods=["GET","POST"])
def login():
    
    
    if request.method == "POST":
        
        # form情報
        email = request.form.get("email")
        password = request.form.get("password")
        
        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crowdfundingsite"
            )
        
        cur = conn.cursor()
        
        cur.execute("""
                    SELECT id, user_name
                    FROM user
                    WHERE email = %s AND password = %s
                    """, (email, password))
        
        user_data = cur.fetchone()
        
        if user_data:
        
            session["id"] = user_data[0]
            session["user_name"] = user_data[1]
            
            return redirect(session["before_page"])
        
        else:
            error = "メールアドレスまたは、パスワードが間違えています"
            return render_template("login.html", error = error)
    
    return render_template("login.html")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    
    if request.method == "POST":
        print("post")
        # inputs = [value for key, value in request.form.items()]
        # print(inputs)
        
        
        # form情報
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
        
        cur = conn.cursor()
        try:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS user(
                            id INT AUTO_INCREMENT,
                            user_name VARCHAR(255),
                            email VARCHAR(255) ,
                            password VARCHAR(255),
                            PRIMARY KEY(id),
                            UNIQUE(email)
                        )
                        """)
            
            cur.execute("INSERT INTO user (user_name, email, password) VALUES(%s, %s, %s)",
                        (user_name, email, password))
            
            conn.commit()
        
        except:
            return render_template("sign_up.html", error = "このメールアドレスは既に登録されています。")
        
        
        
    return render_template("sign_up.html")

@app.route("/new_project", methods=["GET", "POST"])
def new_project():
    
    if request.method == "POST":
        project_name = request.form.get("project_name")
        goal = request.form.get("goal")
        end_date = request.form.get("end_date")
        top_file = request.files.get("top_file")  # 修正: request.form.get -> request.files.get
        sub_files = request.files.getlist("sub_file")  # 修正: request.form.getlist -> request.files.getlist
        project_detail = request.form.get("project_detail")
        
        print(project_name)
        print(goal)
        print(end_date)
        print(top_file)
        print(sub_files)
        
        
        app.config["UPLOAD_FOLDER"] = "static/images/project_img"
        
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
            
        file_save = {}
        
        if top_file and allowed_file(top_file.filename):
            filename = secure_filename(top_file.filename)
            file_save["top_file"] = filename
            top_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        sub_file_li = []
        for sub_file in sub_files:
            if sub_file and allowed_file(sub_file.filename):
                filename = secure_filename(sub_file.filename)
                sub_file_li.append(filename)
                sub_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                print(filename, "filename")
        
        file_save["sub_file"] = sub_file_li
        
        print(file_save)
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
        
        cur = conn.cursor()
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS project (
                        user_id INT,
                        project_name VARCHAR(255),
                        goal INT,
                        end_date DATE,
                        top_img VARCHAR(255),
                        sub_img1 VARCHAR(255),
                        sub_img2 VARCHAR(255),
                        sub_img3 VARCHAR(255),
                        sub_img4 VARCHAR(255),
                        project_detail VARCHAR(500)
                    )
                    """)
        
        cur.execute("INSERT INTO project (user_id,project_name,goal,end_date,top_img,sub_img1,sub_img2,sub_img3,sub_img4,project_detail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (1, project_name, goal, end_date, file_save["top_file"], file_save["sub_file"][0], file_save["sub_file"][1], file_save["sub_file"][2], file_save["sub_file"][3], project_detail))
        
        conn.commit()
        
    return render_template("new_project.html")


if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
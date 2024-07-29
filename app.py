from flask import Flask, render_template, redirect, session, request
import mysql.connector
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date

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
    
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
    
    cur = conn.cursor()
    
    cur.execute("""
                SELECT user_name, project_name, goal, top_img,fund_money, support, project_id
                FROM project
                INNER JOIN user ON user.id = project.user_id
                """)
    
    project_data = cur.fetchall()
    
    print(project_data)
    
    return render_template("project_list.html", project_data = project_data)

@app.route("/project/<int:number>")
def project(number):
    session["before_page"] = "/project"
    
    print(number)
    
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
    
    cur = conn.cursor()
    
    today = date.today()
    
    cur.execute("""
                SELECT *
                FROM project
                INNER JOIN user ON project.user_id = user.id
                WHERE project.project_id = %s
                """, (number,))
    
    project_data = cur.fetchone()
    
    time_limit = (project_data[4] - today).days
    
    cur.execute("""
                SELECT *
                FROM detail
                WHERE project_id = %s
                ORDER BY detail_order ASC
                """, (number,))
    
    detail_data = cur.fetchall()
    
    print(project_data)
    
    print(detail_data)
    
    return render_template("project.html", project_data = project_data, time_limit = time_limit, detail_data = detail_data)

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
        top_file = request.files.get("top_file")
        sub_files = request.files.getlist("sub_file")
        # project_detail = request.form.getlist("project_detail")

        print(project_name)
        print(goal)
        print(end_date)
        print(top_file)
        print(sub_files)
        # print(project_detail)
        
        
        
        
        
                    
        # print(project_details)

        
        app.config["UPLOAD_FOLDER"] = "static/images/project_img"

        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        
        
        # 初期値の設定
        top_file_default = "default_top.png"
        sub_file_defaults = ["default_sub1.png", "default_sub2.png", "default_sub3.png", "default_sub4.png"]
        
        file_save = {}

        # トップファイルの保存
        if top_file and allowed_file(top_file.filename):
            filename = secure_filename(top_file.filename)
            top_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_save["top_file"] = filename
            print("ほぞん")
        else:
            file_save["top_file"] = top_file_default

        # サブファイルの保存
        sub_file_li = []
        for i in range(4):
            if i < len(sub_files) and sub_files[i] and allowed_file(sub_files[i].filename):
                filename = secure_filename(sub_files[i].filename)
                sub_files[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                sub_file_li.append(filename)
            else:
                sub_file_li.append(sub_file_defaults[i])

        file_save["sub_file"] = sub_file_li
        
        # print(file_save)

        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
        
        cur = conn.cursor()
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS project (
                        project_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        project_name VARCHAR(255),
                        goal INT,
                        end_date DATE,
                        top_img VARCHAR(255),
                        sub_img1 VARCHAR(255),
                        sub_img2 VARCHAR(255),
                        sub_img3 VARCHAR(255),
                        sub_img4 VARCHAR(255),
                        fund_money INT DEFAULT 0,
                        support INT DEFAULT 0,
                        FOREIGN KEY (user_id) REFERENCES user(id)
                    )
                    """)
        
        cur.execute("""
                    INSERT INTO project 
                    (user_id, project_name, goal, end_date, top_img, sub_img1, sub_img2, sub_img3, sub_img4, fund_money) 
                    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, 
                    (1, project_name, goal, end_date, file_save["top_file"], 
                    file_save["sub_file"][0], file_save["sub_file"][1], 
                    file_save["sub_file"][2], file_save["sub_file"][3], 0))
        
        cur.execute("SELECT LAST_INSERT_ID()")
        last_insert_id = cur.fetchone()[0]
        
        cur.execute("""
                            CREATE TABLE IF NOT EXISTS detail(
                                detail_id INT AUTO_INCREMENT PRIMARY KEY,
                                project_id INT,
                                type CHAR(4),
                                value VARCHAR(500),
                                detail_order INT,
                                FOREIGN KEY(project_id) REFERENCES project(project_id)
                            )
                            """)
        
        
        
        
        # 詳細文
        form_data = request.form
        file_data = request.files
        
        for key, value in form_data.items():
            if "project_detail-" in key:
                print(f'Form data - {key}: {value}')
                cur.execute("INSERT INTO detail(project_id,type,value,detail_order) VALUES(%s,'text',%s,%s)",(last_insert_id,value,key.split("-")[1]))
        
        for key, file in file_data.items():
            if "project_detail-" in key:
                print(f'File data - {key}: {file.filename}')
            
                
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("INSERT INTO detail(project_id,type,value,detail_order) VALUES(%s,'img',%s,%s)",(last_insert_id,file.filename,key.split("-")[1]))
        
        
        conn.commit()
    return render_template("new_project.html")


@app.route("/support")
def support():
    
    return render_template("support.html")


if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
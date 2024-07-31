from flask import Flask, render_template, redirect, session, request
import mysql.connector
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date
from decimal import Decimal

app = Flask(__name__)

app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', "avif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)



@app.route("/")
def top():
    session["before_page"] = "/"
    
    if "id" in session:
        login_data = True
        print(session["id"])
    else:
        login_data = False
    
    today = date.today()
    
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
    
    cur = conn.cursor()
    
    data = (
    'user_name', 'project_name', 100, 'top_img', 1, Decimal('50'), 10, today
    )
    
    project_my_data = []
    
    if login_data:
        cur.execute("""
                SELECT user.user_name, project.project_name, project.goal, project.top_img, project.project_id, SUM(project_return.return_price), COUNT(DISTINCT support_user.user_id), project.end_date
                FROM project
                INNER JOIN support_user ON project.project_id = support_user.project_id
                INNER JOIN project_return ON support_user.return_number = project_return.id
                INNER JOIN user ON user.id = project.user_id
                WHERE user.id = %s
                ORDER BY COUNT(DISTINCT support_user.user_id) DESC
                LIMIT 4
                """, (session["id"],))
        
        project_my_data = cur.fetchall()
        
        if project_my_data and None not in project_my_data[0]:
            # 新しいリストを作成して、日付を日数に変換
            updated_my_project_data = []
            for data in project_my_data:
                end_date = data[7]
                days_left = (end_date - today).days
                # 新しいタプルを作成して、元のデータをコピーし、7番目の要素を日数に置き換えます
                percentage = float((data[5] / data[2]) * 100)
                updated_my_data = data[:7] + (days_left,) + (percentage,)
                updated_my_project_data.append(updated_my_data)

            # 新しいリストを出力
            for data in updated_my_project_data:
                print(data)
    
            # もし project_data を更新したい場合は、新しいリストで置き換えます
            project_my_data = updated_my_project_data
            
        else:
            project_my_data = []
        
    cur.execute("""
                SELECT user.user_name, project.project_name, project.goal, project.top_img, project.project_id, SUM(project_return.return_price), COUNT(DISTINCT support_user.user_id), project.end_date
                FROM project
                INNER JOIN support_user ON project.project_id = support_user.project_id
                INNER JOIN project_return ON support_user.return_number = project_return.id
                INNER JOIN user ON user.id = project.user_id
                ORDER BY COUNT(DISTINCT support_user.user_id) DESC
                LIMIT 4
                """)
    
    project_data = cur.fetchall()

    print(project_data)

    if project_data and None not in project_data[0]:
        # 新しいリストを作成して、日付を日数に変換
        updated_project_data = []
        for data in project_data:
            end_date = data[7]
            days_left = (end_date - today).days
            # 新しいタプルを作成して、元のデータをコピーし、7番目の要素を日数に置き換えます
            percentage = float((data[5] / data[2]) * 100)
            updated_data = data[:7] + (days_left,) + (percentage,)
            updated_project_data.append(updated_data)

        # 新しいリストを出力
        for data in updated_project_data:
            print(data)
    
        # もし project_data を更新したい場合は、新しいリストで置き換えます
        project_data = updated_project_data
        
    else:
        project_data = []

    return render_template("top.html", login_data=login_data, project_data=project_data, project_my_data=project_my_data)

@app.route("/project_list")
def project_list():
    session["before_page"] = "/project_list"
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
    today = date.today()
    
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
    
    data = (
    'user_name', 'project_name', 100, 'top_img', 1, Decimal('50'), 10, today
    )
    
    cur = conn.cursor()
    
    print(request.args)
    
    where = ""
    
    if "search" in request.args:
        print("s")
    
        search_data = request.args.get("search").split()
        print(search_data)
    
        for i in range(len(search_data)):
            if i == 0:
                where = f"WHERE project.project_name LIKE '%{search_data[i]}%'"
            else:
                where = f" AND project.project_name LIKE '%{search_data[i]}%'"
        
    cur.execute(f"""
                SELECT user.user_name, project.project_name, project.goal, project.top_img, project.project_id, SUM(project_return.return_price), COUNT(DISTINCT support_user.user_id), project.end_date
                FROM project
                INNER JOIN support_user ON project.project_id = support_user.project_id
                INNER JOIN project_return ON support_user.return_number = project_return.id
                INNER JOIN user ON user.id = project.user_id
                {where}
                """)
    
    project_data = cur.fetchall()

    print(project_data)

    if None not in project_data[0]:
        # 新しいリストを作成して、日付を日数に変換
        updated_project_data = []
        for data in project_data:
            end_date = data[7]
            days_left = (end_date - today).days
            # 新しいタプルを作成して、元のデータをコピーし、7番目の要素を日数に置き換えます
            percentage = float((data[5] / data[2]) * 100)
            updated_data = data[:7] + (days_left,) + (percentage,)
            updated_project_data.append(updated_data)

        # 新しいリストを出力
        for data in updated_project_data:
            print(data)
    

        # もし project_data を更新したい場合は、新しいリストで置き換えます
        project_data = updated_project_data
        
    else:
        project_data = None
        

    return render_template("project_list.html", project_data = project_data, login_data =login_data)

@app.route("/project/<int:number>")
def project(number):
    session["before_page"] = f"/project/{number}"
    
    print(number)
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
    
    cur = conn.cursor()
    
    today = date.today()
    
    cur.execute("""
                SELECT 
                    project.project_id, 
                    project.project_name,
                    project.goal,
                    project.end_date,
                    project.top_img,
                    project.sub_img1,
                    project.sub_img2,
                    project.sub_img3,
                    project.sub_img4,
                    user.user_name,
                    SUM(project_return.return_price) AS total_support_amount,
                    COUNT(DISTINCT support_user.user_id) AS support_user_count
                FROM 
                    project
                INNER JOIN 
                    user ON project.user_id = user.id
                INNER JOIN 
                    support_user ON project.project_id = support_user.project_id
                INNER JOIN 
                    project_return ON support_user.return_number = project_return.id
                WHERE 
                    project.project_id = %s
                GROUP BY 
                    project.project_id;

                """, (number,))
    
    project_data = cur.fetchone()
    
    time_limit = (project_data[3] - today).days
    
    cur.execute("""
                SELECT *
                FROM detail
                WHERE project_id = %s
                ORDER BY detail_order ASC
                """, (number,))
    
    detail_data = cur.fetchall()
    
    print(project_data)
    
    print(detail_data)
    
    return render_template("project.html", project_data = project_data, time_limit = time_limit, detail_data = detail_data, login_data =login_data)

@app.route("/login", methods=["GET","POST"])
def login():
    
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
    
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
            
            if "before_page" in session:
            
                return redirect(session["before_page"])
            
            else:
                return redirect("/")
        
        else:
            error = "メールアドレスまたは、パスワードが間違えています"
            return render_template("login.html", error = error)
    
    return render_template("login.html", login_data =login_data)

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
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
        
        
        
    return render_template("sign_up.html", login_data =login_data)

@app.route("/new_project", methods=["GET", "POST"])
def new_project():
    
    session["before_page"] = "/new_project"
    
    
    
    if "id" not in session:
        return redirect("/login")
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
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
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS project_return(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        project_id INT,
                        return_price INT,
                        return_detail VARCHAR(500),
                        return_img VARCHAR(255),
                        FOREIGN KEY (project_id) REFERENCES project(project_id)
                    )
                    """)
        
        print(form_data)
        return_num = None
        for key, value in form_data.items():
            
            # print(key, value)
            
            if "return_price-" in key:
                return_num = key.split("-")[1]
                return_price = value
                # print(return_num)
            
            if return_num:
            
                if f"return_textarea-{return_num}" == key:
                    return_text = value
                    # print("text")
                    
                    for file_key, file in file_data.items():
                        
                        if f"return_img-{return_num}" == file_key:
                            # return_img = file

                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            
                            print(return_num ,return_price, return_text, file.filename)
                            
                            cur.execute("INSERT INTO project_return(project_id,return_price,return_detail,return_img) VALUES (%s,%s,%s,%s)",
                                        (last_insert_id, return_price, return_text, file.filename))
                            
                            return_num = None
                            
                
                
            else:
                print("error")
                
            
            
            
            
        
        conn.commit()
    return render_template("new_project.html", login_data =login_data)


@app.route("/return_select/<int:number>", methods=["GET", "POST"])
def support(number):
    session["before_page"] = f"/return_select/{number}"
    print(number)
    if "id" not in session:
        return redirect("/login")
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
    print(session)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crowdfundingsite"
    )

    cur = conn.cursor(session)

    if request.method == "POST":
        form_data = request.form.getlist("return_check")
        print(form_data, "request.form")
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS support_user(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        project_id INT,
                        return_number INT,
                        FOREIGN KEY (user_id) REFERENCES user(id),
                        FOREIGN KEY (project_id) REFERENCES project(project_id),
                        FOREIGN KEY (return_number) REFERENCES project_return(id)
                    )
                    """)
        
        for select in form_data:
            cur.execute("INSERT INTO support_user(user_id,project_id,return_number) VALUES(%s,%s,%s)",
                        (session["id"],number, select ))
            
        conn.commit()
        
        
        # データベースに保存するなどの処理をここに追加

    cur.execute("""
                SELECT * 
                FROM project_return
                WHERE project_id = %s
                ORDER BY return_price ASC
                """, (number,))
    
    return_data = cur.fetchall()
    # print(return_data)

    cur.close()
    conn.close()

    return render_template("return.html", number=number, return_data=return_data, login_data =login_data)

@app.route("/my_project_list")
def my_project():
    session["before_page"] = "/project_list"
    
    if "id" in session:
        login_data = True
    else:
        login_data = False
    
    today = date.today()
    
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )
    
    cur = conn.cursor()
    
    
    
    
    cur.execute(f"""
                SELECT user.user_name, project.project_name, project.goal, project.top_img, project.project_id, SUM(project_return.return_price), COUNT(DISTINCT support_user.user_id), project.end_date
                FROM project
                INNER JOIN support_user ON project.project_id = support_user.project_id
                INNER JOIN project_return ON support_user.return_number = project_return.id
                INNER JOIN user ON user.id = project.user_id
                WHERE user.id = %s
                """, (session["id"],))
    
    project_data = cur.fetchall()

    print(project_data)

    if None not in project_data[0]:
        # 新しいリストを作成して、日付を日数に変換
        updated_project_data = []
        for data in project_data:
            end_date = data[7]
            days_left = (end_date - today).days
            # 新しいタプルを作成して、元のデータをコピーし、7番目の要素を日数に置き換えます
            updated_data = data[:7] + (days_left,)
            updated_project_data.append(updated_data)

        # 新しいリストを出力
        for data in updated_project_data:
            print(data)
    

        # もし project_data を更新したい場合は、新しいリストで置き換えます
        project_data = updated_project_data
        
    else:
        project_data = None

    return render_template("my_project_list.html", project_data = project_data, login_data =login_data)


if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)
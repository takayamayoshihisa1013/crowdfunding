import mysql.connector


conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crowdfundingsite"
        )

cur = conn.cursor()

cur.execute("""
            
            """)
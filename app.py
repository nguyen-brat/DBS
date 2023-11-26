from flask import Flask, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database="postgres",
    user = "postgres", 
    host= 'database-1.cxrip2pysplk.ap-southeast-2.rds.amazonaws.com',
    password = "123456789",
    port = 5432
)
cur = conn.cursor()

@app.route('/', methods=['POST', 'GET'])
def default():
    return "Hello world"

# @app.route('/retrieve_title', methods=['POST', 'GET'])
# def retrieve_title():

#     sql_query = '''
#     from 
# '''
#     cur.execute(sql_query)
#     conn.commit()
#     cur.close()

# @app.route('/retrieve_session', methods=['POST', 'GET'])
# def retrieve_session():
#     sql_query = '''

# '''

# @app.route('/retrieve_ssn', methods=['POST', 'GET'])
# def retrieve_ssn():
#     sql_query = '''
#     from 
# '''
#     cur.execute(sql_query)
#     conn.commit()
#     cur.close()

# @app.route('/retrieve_total_cost', methods=['POST', 'GET'])
# def retrieve_total_cost():
#     sql_query = '''
#     from 
# '''
#     cur.execute(sql_query)
#     conn.commit()
#     cur.close()

# @app.route('/retrieve_client_name', methods=['POST', 'GET'])
# def retrieve_client_name():
#     sql_query = '''
#     from 
# '''
#     cur.execute(sql_query)
#     conn.commit()
#     cur.close()

@app.route('/add_client', methods=['POST', 'GET'])
def add_client():
    ssn = request.args.get('ssn')
    fname = request.args.get('fname')
    mname = request.args.get('mname')
    lname = request.args.get('lname')
    email = request.args.get('email')
    phone_number = request.args.get('phone_number')
    home_address = request.args.get('home_address')
    sql_query = f'''INSERT INTO person (ssn, fname, mname, lname, email, phone_number, home_address) VALUES
    {ssn, fname, mname, lname, email, phone_number, home_address};
    '''
    cur.execute(sql_query)
    conn.commit()
    return f"sucess full add client to db"

@app.route('/remove_client', methods=['POST', 'GET'])
def remove_client():
    ssn = request.args.get('ssn')
    sql_query = f'''DELETE FROM person
    WHERE ssn LIKE '%{ssn}%';
    '''
    cur.execute(sql_query)
    conn.commit()
    #cur.close()

    return f"success full remove client has ssn {ssn} out of db"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='6868', debug=True)
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

@app.route('/borrow_book', methods=['POST', 'GET'])
def borrow_book():
    pass

@app.route('/pay_book', method=['POST', 'GET'])
def pay_book():
    pass

@app.route('/retrieve_title', methods=['POST', 'GET'])
def retrieve_title():
    '''
    This function retrieve the titles of all materials that was provided by a
    specific organization name and published in a specific year
    '''
    publication_year = request.args.get('publication_year')
    organization = request.args.get('organization')
    sql_query = f'''
    SELECT title FROM item
    INNER JOIN organization ON organization.providerid = item.providerid
    WHERE item.publication_date >= '%{publication_year}-1-1%'::date
    AND item.publication_date <= '%{publication_year}-12-31%'::date
    AND organization.name LIKE '%{organization}%'
'''
    cur.execute(sql_query)
    output = cur.fetchall()
    conn.commit()
    #cur.close()
    return output

@app.route('/retrieve_session', methods=['POST', 'GET'])
def retrieve_session():
    '''
    find session_id of a session has data < given date
    and chossen payment method
    '''
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')
    payment_method = request.args.get('payment_method')
    sql_query = f'''
    SELECT sessionid FROM session
    WHERE payment_method LIKE '%{payment_method}%'
    AND day < {day}
    AND month <= {month}
    AND year <= {year}
'''
    cur.execute(sql_query)
    output = cur.fetchall()
    conn.commit()
    return output

# @app.route('/retrieve_ssn', methods=['POST', 'GET'])
# def retrieve_ssn():
#     sql_query = '''
#     from 
# '''
#     cur.execute(sql_query)
#     conn.commit()
#     cur.close()

@app.route('/retrieve_total_cost', methods=['POST', 'GET'])
def retrieve_total_cost():
    clientid = request.args.get('clientid')
    month = request.args.get('month')
    sql_query = f'''
    SELECT SUM(cost)
    FROM session
    WHERE session.clientid LIKE '%{clientid}%'
    AND session.month = {month}
'''
    cur.execute(sql_query)
    conn.commit()
    output = cur.fetchall()
    #cur.close()
    return output

@app.route('/retrieve_client_name', methods=['POST', 'GET'])
def retrieve_client_name():
    '''
    Retrieve name of all client that make more than
    10 session in a specific year
    '''
    year = request.args.get('year')
    sql_query = f'''
    SELECT person.fname, person.lname
    FROM session
    INNER JOIN member ON member.memberid = session.clientid
    INNER JOIN person ON person.ssn = member.ssn
    WHERE session.year = {year}
    GROUP BY session.clientid
    HAVING COUNT(*) > 10
'''
    cur.execute(sql_query)
    conn.commit()
    output = cur.fetchall()
    #cur.close()
    return output

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
    #cur.close()
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
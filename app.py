from flask import Flask, request, jsonify
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

# @app.route('/borrow_book', methods=['POST', 'GET'])
# def borrow_book():
#     pass

# @app.route('/pay_book', method=['POST', 'GET'])
# def pay_book():
#     pass

@app.route('/retrieve_title', methods=['POST', 'GET'])
def retrieve_title():
    '''
    This function retrieve the titles of all materials that was provided by a
    specific organization name and published in a specific year
    '''
    #cur = conn.cursor()
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
    outputs = cur.fetchall()
    outputs = [{'title':output} for output in outputs]
    conn.commit()
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/retrieve_session', methods=['POST', 'GET'])
def retrieve_session():
    '''
    find session_id of a session has data < given date
    and chossen payment method
    '''
    #cur = conn.cursor()
    date = request.args.get('date')
    payment_method = request.args.get('payment_method')
    sql_query = f'''
    SELECT sessionid FROM session
    INNER JOIN member ON session.clientid = member.memberid
    INNER JOIN client ON member.memberid = client.memberid
    WHERE payment_method LIKE '%{payment_method}%'
    AND client.registerdate < '%{date}%'::date;
'''
    cur.execute(sql_query)
    outputs = cur.fetchall()
    outputs = [{'sessionid':output} for output in outputs]
    conn.commit()
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/retrieve_magazine_expensivest', methods=['POST', 'GET'])
def retrieve_magazine_highest_price():
    #cur = conn.cursor()
    authorid = request.args.get('authorid')
    sql_query = f'''
    SELECT
        item.issn_isbn
    FROM
        item
    INNER JOIN write ON item.issn_isbn = write.issn_isbn
    WHERE
        item.price = (
        SELECT
            MAX(price)
        FROM
            item
        INNER JOIN write ON item.issn_isbn = write.issn_isbn
        WHERE
            itemtype LIKE '%Magazine%'
        AND write.authorid = {authorid}
    )
    AND
        write.authorid = {authorid}
    AND
        item.itemtype LIKE '%Magazine%';
'''
    cur.execute(sql_query)
    conn.commit()
    outputs = cur.fetchall()
    outputs = [{'issn_isbn':output} for output in outputs]
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/retrieve_total_cost', methods=['POST', 'GET'])
def retrieve_total_cost():
    #cur = conn.cursor()
    clientid = request.args.get('clientid')
    month = request.args.get('month')
    sql_query = f'''
    SELECT SUM(cost)
    FROM session
    WHERE session.clientid LIKE '%{clientid}%'
    AND session.month = {month}
    AND session.year = 2022
'''
    cur.execute(sql_query)
    conn.commit()
    output = cur.fetchall()
    output = [{'result':output}]
    #cur.close()
    return jsonify({'result':output})

@app.route('/retrieve_client_name', methods=['POST', 'GET'])
def retrieve_client_name():
    '''
    Retrieve name of all client that make more than
    10 session in a specific year
    '''
    #cur = conn.cursor()
    year = request.args.get('year')
    sql_query = f'''
    SELECT
        session.clientid, fname, lname
    FROM
        session
    INNER JOIN member ON member.memberid = session.clientid
    INNER JOIN person ON person.ssn = member.ssn
    WHERE
        session.year = {year}
    GROUP BY
        session.clientid, fname, lname
    HAVING
        COUNT(session.clientid) >= 10
'''
    cur.execute(sql_query)
    conn.commit()
    outputs = cur.fetchall()
    outputs = [{'cliendid':output[0], 'fname':output[1], 'lname':output[2]} for output in outputs]
    #cur.close()
    return jsonify({'result':outputs})

@app.route('/add_client', methods=['POST', 'GET'])
def add_client():
    #cur = conn.cursor()
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
    #cur = conn.cursor()
    ssn = request.args.get('ssn')
    sql_query = f'''DELETE FROM person
    WHERE ssn LIKE '%{ssn}%';
    '''
    cur.execute(sql_query)
    conn.commit()
    #cur.close()

    return f"success full remove client has ssn {ssn} out of db"

@app.route('/borrow_book', methods=['POST', 'GET'])
def borrow_book():
    attri = request.get_json()
    '''
    date_session DATE,
	clientid int,
    payment_method VARCHAR(255),
	cost_borrow numeric,
	managerid VARCHAR(255),
	wkey VARCHAR(255),
	
	publisher VARCHAR(255),
	num_pages int,
	issn_isbn VARCHAR(255), 
	borrow_date DATE,
	return_date DATE
    '''
    sql_query = f'''
    call borrow_book({attri['date_session']}, {attri['clientid']}, {attri['payment_method']}, {attri['cost_borrow']}, {attri['managerid']}, {attri['wkey']}, {attri['publisher']}, {attri['num_pages']}, {attri['issn_isbn']}, {attri['borrow_date']}, {attri['borrow_date']}) 
'''
    cur.execute(sql_query)
    conn.commit()
    #cur.close()
    return 'successfully add borrow book data'

@app.route('/pay_book', method=['POST', 'GET'])
def pay_book():
    issn_isbn = request.args.get('issn_isbn')
    sql_query = f'''UPDATE physical_copy SET count = count + 1;
    '''
    cur.execute(sql_query)
    conn.commit()

    return_date = request.args.get('return_date')
    sql_query = f'''UPDATE borrow SET return_date = {return_date};
    '''
    cur.execute(sql_query)
    conn.commit()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port='6868', debug=True)
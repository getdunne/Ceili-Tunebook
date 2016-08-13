import psycopg2
import json

def create(conn, book_name, set_name, wrap, wrap_to, tune_list):
    cur = conn.cursor()
    cur.execute('insert into sets (book_name, set_name, wrap, wrap_to, tune_list) values (%s, %s, %s, %s, %s) returning id', (book_name, set_name, wrap, wrap_to, json.dumps(tune_list)))
    set_id = cur.fetchone()[0]
    conn.commit()
    return set_id


def retrieve(conn, set_id):
    cur = conn.cursor()
    cur.execute('select book_name, set_name, wrap, wrap_to, tune_list from sets where id=%s', (set_id,))
    book_name, set_name, wrap, wrap_to, tune_list = cur.fetchone()
    return book_name, set_name, wrap, wrap_to, json.loads(tune_list)


def update(conn, set_id, book_name, set_name, wrap, wrap_to, tune_list):
    cur = conn.cursor()
    cur.execute('update sets set book_name=%s, set_name=%s, wrap=%s, wrap_to=%s, tune_list=%s where id=%s', (book_name, set_name, wrap, wrap_to, json.dumps(tune_list), set_id))
    conn.commit()


def delete(conn, set_id):
    cur = conn.cursor()
    cur.execute('delete from sets where id=%s', (set_id,))
    conn.commit()


def search (conn, book_name, set_name):
    if book_name is None or book_name == '':
        book_name = '%'
    else:
        book_name = '%' + book_name + '%'
    if set_name is None or set_name == '':
        set_name = '%'
    else:
        set_name = '%' + set_name + '%'
    cur = conn.cursor()
    cur.execute('select id, book_name, set_name from sets where lower(book_name) like lower(%s) and lower(set_name) like lower(%s) order by book_name, set_name', (book_name, set_name))
    return cur.fetchall()
    

if __name__ == '__main__':
    import secrets
    conn = psycopg2.connect(secrets.getDBConnectString())
    
    # Create
    tune_list = [(5, '(2A,2B)x2'),(6, '(2A,2B)x2'),(7, '(2A,2B)x2'),(8, '(2A,2B)x2')]
    set_id = create(conn, 'Ceili Band Big Book', 'Reel Set 2', True, 0, tune_list)
    print 'Create: set_id =', set_id
    
    # Update
    tune_list = [(1, '(2A,2B)x2'),(2, '(2A,2B)x2'),(3, '(2A,2B)x2'),(4, '(2A,2B)x2')]
    update(conn, set_id, 'Ceili Band Bigger Book', 'Reel Set 1', False, 0, tune_list)
    
    # Retrieve
    book_name, set_name, wrap, tune_list = retrieve(conn, set_id)
    print book_name
    print set_name
    print wrap
    print tune_list
    
    # Delete
    delete(conn, set_id)
    
    # Search
    print search(conn, None, 're')
    


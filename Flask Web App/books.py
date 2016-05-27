import psycopg2
import json

def create(conn, name):
    cur = conn.cursor()
    cur.execute('insert into books (name, url, content) values (%s, %s, %s) returning id', (name, None, json.dumps([])))
    book_id = cur.fetchone()[0]
    conn.commit()
    return book_id


def retrieve(conn, book_id):
    cur = conn.cursor()
    cur.execute('select name, url, content from books where id=%s', (book_id,))
    name, url, content = cur.fetchone()
    return name, url, json.loads(content)


def update(conn, book_id, name, url, content):
    cur = conn.cursor()
    cur.execute('update books set name=%s, url=%s, content=%s where id=%s', (name, url, json.dumps(content), book_id))
    conn.commit()


def delete(conn, book_id):
    cur = conn.cursor()
    cur.execute('delete from books where id=%s', (book_id,))
    conn.commit()


def search (conn, name):
    if name is None or name == '':
        name = '%'
    else:
        name = '%' + name + '%'
    cur = conn.cursor()
    cur.execute('select id, name, url from books where lower(name) like lower(%s) order by name', (name,))
    return cur.fetchall()
    

if __name__ == '__main__':
    import secrets
    conn = psycopg2.connect(secrets.getDBConnectString())
    
    # Create
    book_id = create(conn, 'Ceili Band Big Book')
    print 'Create: book_id =', book_id
    
    # Update
    name = 'KCB Big Book'
    url = 'http://barf.com/img001.jpg'
    content = [['Ceili Dance', []], ['Set Dance', []]];
    update(conn, book_id, name, url, content)
    
    # Retrieve
    name, url, content = retrieve(conn, book_id)
    print name
    print url
    print content
    
    # Search
    print "Search 'big':",
    print search(conn, 'big')
    print "Search 'dung':",
    print search(conn, 'dung')
    
    # Delete
    delete(conn, book_id)
    


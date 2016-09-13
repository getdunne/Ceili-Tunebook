import psycopg2

def create(conn, title, composer, tune_type, timesig, key, file_ext, url, abc):
    cur = conn.cursor()
    cur.execute('insert into tunes (title, composer, tune_type, timesig, key, file_ext, url, abc) values (%s, %s, %s, %s, %s, %s, %s, %s) returning id', (title, composer, tune_type, timesig, key, file_ext, url, abc))
    tune_id = cur.fetchone()[0]
    conn.commit()
    return tune_id


def retrieve(conn, tune_id):

    cur = conn.cursor()
    cur.execute('select title, composer, tune_type, timesig, key, file_ext, url, abc from tunes where id=%s', (tune_id,))
    title, composer, tune_type, timesig, key, file_ext, url, abc = cur.fetchone()
    image_path = '/static/img/%d.%s' % (tune_id, file_ext)
    return image_path, title, composer, tune_type, timesig, key, file_ext, url, abc


def update(conn, tune_id, title, composer, tune_type, timesig, key, file_ext, url, abc):
    cur = conn.cursor()
    cur.execute('update tunes set title=%s, composer=%s, tune_type=%s, timesig=%s, key=%s, file_ext=%s, url=%s, abc=%s where id=%s', (title, composer, tune_type, timesig, key, file_ext, url, abc, tune_id))
    conn.commit()


def delete(conn, tune_id):
    cur = conn.cursor()
    cur.execute('delete from tunes where id=%s', (tune_id,))


def search (conn, title, tune_type, key):
    if title is None or title=='':
        title = '%'
    else:
        title = '%' + title + '%'
    if key is None or key=='':
        key = '%'
    else:
        key = key + '%'
    cur = conn.cursor()
    if tune_type is None or tune_type=='':
        cur.execute('select id, title, tune_type, timesig, key, file_ext from tunes where lower(title) like lower(%s) and lower(key) like lower(%s) order by lower(title)', (title, key))
    elif tune_type == 'song':
        cur.execute('select id, title, tune_type, timesig, key, file_ext from tunes where lower(title) like lower(%s) and lower(key) like lower(%s) and tune_type is null order by lower(title)', (title, key))
    else:
        cur.execute('select id, title, tune_type, timesig, key, file_ext from tunes where lower(title) like lower(%s) and lower(key) like lower(%s) and tune_type=%s order by lower(title)', (title, key, tune_type))
    tuneList = list()
    for tune_id, title, tune_type, timesig, key, file_ext in cur.fetchall():
        image_path = '/static/img/%d.%s' % (tune_id, file_ext)
        timesig = '' if timesig is None else str(timesig / 10) + '/' + str(timesig % 10)
        if tune_type is None: tune_type = 'song'
        tuneList.append((tune_id, title, tune_type, timesig, key, image_path));
    return tuneList


if __name__ == '__main__':
    import secrets
    conn = psycopg2.connect(secrets.getDBConnectString())
    
    # Create
    url = 'https://thesession.org/tunes/441/abc/1'
    abc = """X: 1
T: John Ryan's
R: polka
M: 2/4
L: 1/8
K: Dmaj
dd B/c/d/B/ | AF ED | dd B/c/d/B/ | AF E2 |
dd B/c/d/B/ | AF Ad | fd ec | d2 d2 ||
fd de/f/ | gf ed | fd de/f/ | gf a2 |
fd de/f/ | gf ed | fd ec | d2 d2 ||"""
    tune_id = create(conn, "John Ryan's", 'Trad.', 'polka', 44, 'D Major', 'png', url, abc)
    print 'Create: tune_id =', tune_id
    
    # Update
    tune_list = [(1, '(2A,2B)x2'),(2, '(2A,2B)x2'),(3, '(2A,2B)x2'),(4, '(2A,2B)x2')]
    update(conn, tune_id, "John Ryan's", 'Trad.', 'polka', 44, 'D Major', 'jpg', url, abc)
    
    # Retrieve
    image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = retrieve(conn, tune_id)
    print image_path
    print title
    print composer
    print tune_type
    print timesig
    print key
    print file_ext
    print url
    print abc
    
    # Delete
    delete(conn, tune_id)
    
    # Search
    tuneList = search(conn, None, 'polka', 'D')
    print 'Search result:'
    print tuneList
    


import psycopg2
import secrets
conn = psycopg2.connect(secrets.getDBConnectString())

import random
import json
import subprocess
import base64
import tunes, sets, books

from flask import Flask, session, render_template, redirect, url_for, request, escape

app = Flask(__name__)

@app.route('/new_tune_abc', methods=['GET', 'POST'])
def new_tune_abc():
    if 'username' not in session: return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('abc_tune_form.html')
    else:
        title = request.form['title']
        tune_type = request.form['type']
        timesig = request.form['timesig']
        if timesig is not None and timesig != '':
            s = timesig.split('/')
            ts = int(s[0])*10 + int(s[1])
        key = request.form['key']
        abc = request.form['abc']
        if abc == '': return "ABC field must be filled"
        idata = request.form['imgdata'].decode("utf-8")
        idata = idata.replace('data:image/png;base64,', '')
        idata = idata.replace(' ', '+')
        idata = base64.b64decode(idata)
        tune_id = tunes.create(conn, title, None, tune_type, ts, key, 'png', None, abc)
        f = open('static/img/%d.png' % tune_id, 'wb')
        f.write(idata)
        f.close()
        return redirect(url_for('edit_tune_abc', tune_id=tune_id))

@app.route('/edit_tune_abc/<tune_id>', methods=['GET', 'POST'])
def edit_tune_abc(tune_id):
    if 'username' not in session: return redirect(url_for('login'))
    if request.method == 'GET':
        image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, int(tune_id))
        if title is None: title = ''
        if tune_type is None: tune_type = ''
        timesig = '' if timesig is None else str(timesig / 10) + '/' + str(timesig % 10)
        if key is None: key = ''
        if abc is None: abc = ''
    else:
        title = request.form['title']
        tune_type = request.form['type']
        timesig = request.form['timesig']
        if timesig is not None and timesig != '':
            s = timesig.split('/')
            its = int(s[0])*10 + int(s[1])
        key = request.form['key']
        abc = request.form['abc']
        if abc == '': return "ABC field must be filled"
        idata = request.form['imgdata'].decode("utf-8")
        idata = idata.replace('data:image/png;base64,', '')
        idata = idata.replace(' ', '+')
        idata = base64.b64decode(idata)
        tunes.update(conn, tune_id, title, None, tune_type, its, key, 'png', '', abc)
        f = open('static/img/' + tune_id + '.png', 'wb')
        f.write(idata)
        f.close()
    return render_template('edit_tune_abc.html',
        title=title,
        tune_type=tune_type,
        timesig=timesig,
        key=key,
        abc=abc,
        tune_id=tune_id)

@app.route('/new_tune_img', methods=['GET', 'POST'])
def new_tune_img():
    if 'username' not in session: return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('new_tune_form.html')
    else:
        f = request.files['img']
        t = f.content_type
        file_ext = None
        if (t == 'image/jpeg'): file_ext = 'jpg'
        elif (t == 'image/png'): file_ext = 'png'
        title = request.form['title']
        tune_type = request.form['type']
        timesig = request.form['timesig']
        if timesig is not None and timesig != '':
            s = timesig.split('/')
            timesig = int(s[0])*10 + int(s[1])
        key = request.form['key']
        url = request.form['url']
        if url == '': url = None
        abc = request.form['abc']
        if abc == '': abc = None
        if file_ext is not None:
            # user has uploaded a specific image for this tune
            tune_id = tunes.create(conn, title, None, tune_type, timesig, key, file_ext, url, abc)
            f.save('static/img/%d.%s' % (tune_id, file_ext))
            return render_template('new_tune_result.html',
                title=title,
                url=url,
                abc=abc,
                file_ext=file_ext,
                tune_id=tune_id)
        else:
        #    # no user-supplied image; create one based on ABC
        #    file_ext = 'png'
        #    tune_id = tunes.create(conn, title, None, tune_type, timesig, key, file_ext, url, abc)
        #    scriptName = 'tune_image.bat' if platform.system() == 'Windows' else './tune_image.sh'
        #    subprocess.Popen([scriptName, str(tune_id), 'static/img'])
            return redirect(request.referrer)

#@app.route('/tune_img/<tune_id>')
#def generateTuneImage(tune_id):
#    tune_id = int(tune_id)
#    image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
#    if abc is None: abc = ''
#    return render_template('tune_img.html', abc=abc)

@app.route('/edit_tune/<tune_id>', methods=['GET', 'POST'])
def editSpecificTune(tune_id):
    if 'username' not in session: return redirect(url_for('login'))
    tune_id = int(tune_id)
    if request.method == 'GET':
        image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
        if title is None: title = ''
        if tune_type is None: tune_type = ''
        timesig = '' if timesig is None else str(timesig / 10) + '/' + str(timesig % 10)
        if key is None: key = ''
        if url is None: url = ''
        if abc is None: abc = ''
        return render_template('edit_tune.html',
            tune_id=tune_id,
            title=title,
            tune_type=tune_type,
            timesig=timesig,
            key=key,
            url=url,
            abc=abc,
            image_path=image_path,
            ur=str(random.randint(1,999)))
    else:
        f = request.files['img']
        t = f.content_type
        file_ext = None
        fileUploaded = True
        if (t == 'image/jpeg'): file_ext = 'jpg'
        elif (t == 'image/png'): file_ext = 'png'
        else:
            fileUploaded = False
            tune_id = int(tune_id)
            image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
        title = request.form['title']
        if title == '': title = None
        tune_type = request.form['type']
        if tune_type == '': tune_type = None
        timesig = request.form['timesig']
        if timesig is not None and timesig != '':
            s = timesig.split('/')
            timesig = int(s[0])*10 + int(s[1])
        else:
            timesig = None
        key = request.form['key']
        if key == '': key = None
        url = request.form['url']
        if url == '': url = None
        new_abc = request.form['abc']
        if new_abc == '': new_abc = None
        if fileUploaded:
            # user uploaded a new image for this tune; replace any old one
            tunes.update(conn, tune_id, title, None, tune_type, timesig, key, file_ext, url, new_abc)
            f.save('static/img/%d.%s' % (tune_id, file_ext))
        #elif new_abc != abc:
        #    # user did not upload a new tune image, but edited ABC; create new image
        #    file_ext = 'png'
        #    tunes.update(conn, tune_id, title, None, tune_type, timesig, key, file_ext, url, new_abc)
        #    scriptName = 'tune_image.bat' if platform.system() == 'Windows' else './tune_image.sh'
        #    subprocess.Popen([scriptName, str(tune_id), 'static/img'])
            
        return redirect(request.referrer)

@app.route('/search_tune', methods=['GET', 'POST'])
def search_tune():
    if request.method == 'GET':
        return render_template('tune_search_form.html')
    else:
        title = request.form['title']
        tune_type = request.form['type']
        key = request.form['key']
        tuneList = tunes.search(conn, title, tune_type, key)
        limit = 6
        if len(tuneList) <= limit:
            return render_template('tune_search_result_detailed.html', tunes=tuneList)
        else:
            return render_template('tune_search_result_compact.html', tunes=tuneList)

@app.route('/set/<set_number>')
def preview_set(set_number):
    book_name, set_name, wrap, wrap_to, tune_list = sets.retrieve(conn, set_number)
    tuneList = list()
    for (tune_id, repeats) in tune_list:
        image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
        tuneList.append((image_path, title, repeats))
    return render_template('set_preview.html', book_name=book_name, set_name=set_name, wrap=wrap, wrap_to=wrap_to, tune_list=tuneList)

@app.route('/showset/<set_number>')
def show_set(set_number):
    book_name, set_name, wrap, wrap_to, tune_list = sets.retrieve(conn, set_number)
    tuneList = list()
    # once through the tune list
    for (tune_id, repeats) in tune_list:
        image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
        tuneList.append((image_path, title, repeats))
    if wrap:
        wrap_title = tuneList[wrap_to][1]
        tune_count = len(tuneList)
        for i in xrange(29):
            # 30 more times through the repeated portion
            for j in xrange(wrap_to, tune_count):
                image_path, title, repeats = tuneList[j]
                tuneList.append((image_path, title, repeats))
    return render_template('set_show.html', set_name=set_name, tune_list=tuneList, wrap=wrap, wrap_title=wrap_title)

@app.route('/json/<set_number>')
def json_set(set_number):
    book_name, set_name, wrap, wrap_to, tune_list = sets.retrieve(conn, set_number)
    tuneList = list()
    for (tune_id, repeats) in tune_list:
        image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
        tuneList.append((image_path, title, repeats))
    return json.dumps([book_name, set_name, wrap, wrap_to, tuneList])

@app.route('/new_set', methods=['GET', 'POST'])
def new_set():
    if 'username' not in session: return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('newset_form.html')
    else:
        book_name = request.form['book_name']
        set_name = request.form['set_name']
        if 'wrap' in request.form:
            wrap = True
            wrap_to = int(request.form['wrap_to'])
        else:
            wrap = False
            wrap_to = 0
        tune_list = list()
        for i in [1,2,3,4,5,6]:
            tune_id = request.form['tune_id_%d' % i]
            repeats = request.form['repeats_%d' % i]
            if tune_id is None or tune_id == '': break
            tune_list.append((int(tune_id), repeats))
        set_id = sets.create(conn, book_name, set_name, wrap, wrap_to, tune_list)
        return redirect(url_for('preview_set', set_number=set_id))

@app.route('/edit_set/<set_number>', methods=['GET', 'POST'])
def edit_set(set_number):
    if 'username' not in session: return redirect(url_for('login'))
    set_id = int(set_number)
    book_name, set_name, wrap, wrap_to, tune_list = sets.retrieve(conn, set_id)
    if request.method == 'GET':
        return render_template('edit_set.html', set_id=set_id, book_name=book_name, set_name=set_name, wrap=wrap, wrap_to=wrap_to, tune_count=len(tune_list), tune_list=tune_list)
    else:
        book_name = request.form['book_name']
        set_name = request.form['set_name']
        if 'wrap' in request.form:
            wrap_to = int(request.form['wrap_to'])
            wrap = True
        else:
            wrap = False
            wrap_to = 0
        tune_list = list()
        for i in [1,2,3,4,5,6]:
            tune_id = request.form['tune_id_%d' % i]
            repeats = request.form['repeats_%d' % i]
            if tune_id is None or tune_id == '': break
            tune_list.append((int(tune_id), repeats))
        sets.update(conn, set_id, book_name, set_name, wrap, wrap_to, tune_list)
        return redirect(request.referrer)

@app.route('/search_set', methods=['GET', 'POST'])
def search_set():
    if request.method == 'GET':
        return render_template('set_search_form.html')
    else:
        book_name = request.form['book_name']
        set_name = request.form['set_name']
        setlist = sets.search(conn, book_name, set_name)
        return render_template('set_search_result.html', setlist=setlist)

@app.route('/new_book')
def new_book():
    if 'username' not in session: return redirect(url_for('login'))
    book_id = books.create(conn, 'New Tune Book')
    return redirect(url_for('edit_book', book_number=book_id))
    
@app.route('/book/<book_number>')
def show_book(book_number):
    book_id = int(book_number)
    name, url, content = books.retrieve(conn, book_id)
    print json.dumps(content)
    print
    name2, content2 = expand_setnames([name, content])
    print json.dumps(content2)
    return render_template('show_book.html', book_name=name, content=json.dumps(content2))

@app.route('/edit_book/<book_number>', methods=['GET', 'POST'])
def edit_book(book_number):
    if 'username' not in session: return redirect(url_for('login'))
    book_id = int(book_number)
    name, url, content = books.retrieve(conn, book_id)
    if request.method == 'GET':
        return render_template('edit_book.html', book_id=book_id, book_name=name, url=url, content=json.dumps(content))
    else:
        f = request.files['img']
        t = f.content_type
        file_ext = None
        fileUploaded = True
        if (t == 'image/jpeg'): file_ext = 'jpg'
        elif (t == 'image/png'): file_ext = 'png'
        else: fileUploaded = False
        
        name = request.form['book_name']
        content = json.loads(request.form['content'])
        if fileUploaded:
            path = 'static/img/book%d.%s' % (book_id, file_ext)
            f.save(path)
            url = '/' + path
        books.update(conn, book_id, name, url, content)
        
        return redirect(request.referrer)

@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    if request.method == 'GET':
        return render_template('book_search_form.html')
    else:
        book_name = request.form['book_name']
        booklist = books.search(conn, book_name)
        return render_template('book_search_result.html', booklist=booklist)

def expand_setnames(book):
    if type(book) is list:
        name, chapters = book
        expandedChapters = list()
        for chapter in chapters:
            expandedChapters.append(expand_setnames(chapter))
        return [name, expandedChapters]
    else:
        set_id = int(book)
        book_name, set_name, wrap, wrap_to, tune_list = sets.retrieve(conn, set_id)
        return [set_id, set_name]

def expand_sets(book):
    if type(book) is list:
        name, chapters = book
        expandedChapters = list()
        for chapter in chapters:
            expandedChapters.append(expand_sets(chapter))
        return [name, expandedChapters]
    else:
        set_id = int(book)
        book_name, set_name, wrap, wrap_to, tune_list = sets.retrieve(conn, set_id)
        tuneList = list()
        for (tune_id, repeats) in tune_list:
            image_path, title, composer, tune_type, timesig, key, file_ext, url, abc = tunes.retrieve(conn, tune_id)
            tuneList.append([image_path, title, repeats])
        return [set_name, wrap, wrap_to, tuneList]

@app.route('/book_json/<book_id>')
def book_json(book_id):
    name, url, content = books.retrieve(conn, int(book_id))
    book = [name, content]
    return json.dumps(expand_sets(book))

@app.route('/edit_abc')
def abcedit():
    return render_template('abc_edit.html')
    
@app.route('/save_abc')
def abcsave():
    return render_template('abc_save.html')
    
@app.route('/')
def home():
    privileged = loggedin = 'username' in session
    return render_template('home.html', loggedin=loggedin, privileged=privileged)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if secrets.checkUserPass(username, password):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return '''
        <form action="" method="post">
            <p>Username: <input type=text name=username>
            <p>Password: <input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

import platform

if __name__ == '__main__':
    random.seed()
    app.secret_key = secrets.getSecretKey()
    app.debug = platform.system() == 'Windows'
    app.run(host='0.0.0.0')


import re

def chopro2html(song):
    # escape <, >, and & characters
    song = song.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # delete CR in CR/LF, if present
    song = song.replace('\r', '')
    
    html = ''
    mode = 0
    
    lClasses = [ 'lyrics', 'lyrics_chorus', 'lyrics_tab', 'lyrics_chorus_tab' ]
    cClasses = [ 'chords', 'chords_chorus', 'chords_tab', 'chords_chorus_tab' ]
    
    for line in song.split('\n'):
        if len(line) == 0:
            # empty line
            html += '<br>\n'
        elif line[0] == '#':
            # comment line, starts with pound symbol
            html += '<!--' + line[1:] + '-->\n'
        elif line[0] == '{':
            # command
            colonPos = line.find(':')
            closeBracePos = line.find('}')
            cmd = line[1:colonPos]
            text = line[colonPos+1:closeBracePos]
            if cmd == 'title' or cmd == 't':
                html += '<h1>' + text + '</h1>\n'
            elif cmd == 'subtitle' or cmd == 'st':
                html += '<h2>' + text + '</h2>\n'
            elif cmd == 'start_of_chorus' or cmd == 'soc':
                mode |= 1
            elif cmd == 'end_of_chorus' or cmd == 'eoc':
                mode &= ~1
            elif cmd == 'comment' or cmd == 'c':
                html += '<p class="comment">' + text + '</p>\n'
            elif cmd == 'comment_italic' or cmd == 'ci':
                html += '<p class="comment_italic">' + text + '</p>\n'
            elif cmd == 'comment_box' or cmd == 'cb':
                html += '<p class="comment_box">' + text + '</p>\n'
            elif cmd == 'start_of_tab' or cmd == 'sot':
                mode |= 2
            elif cmd == 'end_of_tab' or cmd == 'eot':
                mode &= ~2
            else:
                html += '<!--Unsupported command: ' + cmd + '-->\n'
        else:
            # line with chords and lyrics
            line = line.replace(' ', '&nbsp;')
            chords = re.findall('\[.*?\]', line)
            lyrics = re.split('\[.*?]', line)
            if lyrics[0] == '': del lyrics[0]   # line began with a chord
            
            if len(lyrics) == 1 and len(chords) == 0:
                # line without chords
                html += '<div class="' + lClasses[mode] + '">' + lyrics[0] + '</div>\n'
            else:
                html += '<table cellpadding=0 cellspacing=0>\n<tr>\n'
                for chord in chords:
                    html += '<td class="' + cClasses[mode] + '">' + chord[1:-1] + '</td>'
                html += '</tr>\n<tr>'
                for lyric in lyrics:
                    while lyric.startswith('&nbsp;'): lyric = lyric[6:]
                    html += '<td class="' + lClasses[mode] + '">' + lyric + '</td>'
                html += '</tr></table>\n'
                
    return html

import gevent
from gevent import monkey; monkey.patch_socket()
import urllib2
import yajl
import os, socket
from multiprocessing import Process, Queue, Value, Array

sock_file = '/tmp/dbfm.sock'

def down_mp3(url, ssid):
    fu = urllib2.urlopen(url)
    data = fu.read()
    with open('/tmp/%s.mp3'%ssid, 'wb') as f:
        f.write(data)

def mplay_mp3(ssid):
    os.system('mplayer /tmp/%s.mp3 >/dev/null 2>&1'%ssid)

def down_playlist():
    pl_url = "http://douban.fm/j/mine/playlist?type=n&h=|432599:p&channel=1&from=mainsite&r=ecc38a4d94"
    pl_f = urllib2.urlopen(pl_url)
    data = pl_f.read()
    pl = yajl.loads(data)
    pl_f.close()
    return pl['song']

def bind_socket(status=None):
    current_status = 'init'
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(sock_file)
        s.listen(3)
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            if data == 'get':
                conn.sendall(current_status.encode('utf-8'))
            elif data.startswith('set'):
                current_status = data.split(':')[1]
        conn.close
    finally:
        os.unlink(sock_file)

def play_muc(status=None):
    while True:
        pl = down_playlist()
        for song in pl:
            try:
                s_url, s_ssid, s_title = song['url'], song['ssid'], song['title']
                down_mp3(s_url, s_ssid)
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect(sock_file)
                s.sendall("set:%s"%s_title)
                s.close()
                mplay_mp3(s_ssid)
                #print s_url, s_ssid, s_title
            except BaseException as e:
                continue

def cli_socket():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(sock_file)
    s.sendall("get")
    data = s.recv(1024)
    s.close()
    print data

def main():
    if os.path.exists(sock_file):
        cli_socket()
        return 'Tks God'
    pid = os.fork()
    if pid:
        return 'init'

    pid2 = os.fork()
    if pid2:
        bind_socket()
    play_muc()
 
#    g2 = gevent.spawn(play_muc)
#    g1 = gevent.spawn(bind_socket)
#    gevent.joinall([g1, g2])

if __name__ == '__main__':
    main()
    


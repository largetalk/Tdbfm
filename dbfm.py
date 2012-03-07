import gevent
import urllib2
import yajl
import os

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


def main():
    pl = down_playlist()
    for song in pl:
        try:
            s_url, s_ssid = song['url'], song['ssid']
            print s_url, s_ssid
        except BaseException as e:
            continue
        down_mp3(s_url, s_ssid)
        mplay_mp3(s_ssid)

if __name__ == '__main__':
    main()
    


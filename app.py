from flask import Flask, render_template, redirect
import rethinkdb as r

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('main.html')

@app.route('/<user>')
def bio(user):
    rconn = r.connect('localhost')
    useri = r.db('bittybio').table('users').get(user).run(rconn)
    rconn.close()
    if useri == None:
        return 'Sorry! We couldn\'t find '+user+'.'
    else:
        return render_template('bio.html', **useri)

@app.route('/<user>/bb')
def touser(user):
    return redirect(user)

@app.route('/<user>/<net>')
def usersnet(user, net):
    rconn = r.connect('localhost')
    userdata = r.db('bittybio').table('users').get(user).run(rconn)
    netdata = r.db('bittybio').table('nets').get(net).run(rconn)
    if userdata == None or netdata == None:
        return 'User or network undefined!'
    goto_name = None
    try:
        goto_name = userdata['sns'][net]
    except KeyError:
        return 'User doesn\'t appear to be in the given network.'
    try:
        url = netdata['user_url']
    except KeyError:
        url = netdata['url']
    if netdata['prefix']:
        return redirect('http://'+goto_name+'.'+url)
    else:
        return redirect('http://'+url+goto_name)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)

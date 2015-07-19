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

@app.route('/<user>/edit')
def editbio(user):
    rconn = r.connect('localhost')
    useri = r.db('bittybio').table('users').get(user).run(rconn)
    rconn.close()
    if useri == None:
        return 'Sorry! We couldn\'t find '+user+'.'
    else:
        return render_template('edit.html', **useri)


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
    goto_name = []
    for dnet in userdata['nets']:
        if dnet['net'] == net:
            goto_name.append(dnet['url'])
    try:
        url = netdata['user_url']
    except KeyError:
        url = netdata['url']
    if len(goto_name) > 1:
        return "Multiple potential URLs found."
    elif netdata['prefix']:
        return redirect('http://'+goto_name[0]+'.'+url)
    else:
        return redirect('http://'+url+goto_name[0])

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)

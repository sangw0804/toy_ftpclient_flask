from flask import Flask, render_template, request, redirect
import ftplib

app = Flask(__name__)
client = None

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
  global client
  if request.method == 'POST':
    form = request.form
    client = ftplib.FTP(form['host'], form['user'], form['password'])

    return redirect('/main')
  else:
    return render_template('login.html')

@app.route('/main', methods=['GET'])
def main():
  pwd = client.pwd()
  ls = ['d back to parent dir ..']
  client.dir(ls.append)
  ls = map(lambda l: l.split(), ls)

  new_ls = []
  for l in ls:
    new_l = {}
    new_l['is_d'] = (l[0][0] == 'd')
    new_l['desc'] = ' '.join(l[0:-1])
    new_l['name'] = l[-1]
    new_ls.append(new_l)

  return render_template('main.html', pwd=pwd, ls=new_ls)

@app.route('/command', methods=['GET'])
def command():
  arg = request.args['arg']
  cmd = request.args['cmd']

  if cmd == 'cwd':
    client.cwd(arg)
  elif cmd == 'rmdir':
    client.rmd(arg)
  elif cmd == 'rm':
    client.delete(arg)

  return redirect('/main')
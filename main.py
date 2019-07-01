from flask import Flask, render_template, request, redirect, flash
import ftplib
from pathlib import Path
from helpers.index import ls_trim

app = Flask(__name__)
app.secret_key = '1234'
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

  new_ls = ls_trim(ls)

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
  elif cmd == 'get':
    with open(f'{Path.home()}/Downloads/{arg}', 'wb') as f:
      client.retrbinary(f'RETR {arg}', f.write)
    flash(f'successfully get {arg} at ~/Downloads/')

  return redirect('/main')
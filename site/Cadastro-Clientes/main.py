import os
from flask import Flask, render_template, request
from flask_cors import CORS
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder='templates')
CORS(app)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mudar123'
app.config['MYSQL_DATABASE_DB'] = 'acimpacta'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
  try:
      return render_template('index.html')
  except Exception as e:
      return str(e)

@app.route('/gravar', methods=['POST'])
def gravar():
  try:
      coon = mysql.connect()
      cursor = coon.cursor()
      json = request.get_json()
      email = json['email']
      nome = json['first_name']
      sobrenome = json['last_name']
      senha = json['password']
      if email and nome and sobrenome and senha:
        cursor.execute('insert into login (email, nome, sobrenome, senha) VALUES (%s, %s, %s, %s)', (email, nome, sobrenome, senha))
        coon.commit()
      return render_template('index.html')
  except Exception as e:
        return ({'error': str(e)})


@app.route('/listar', methods=['GET'])
def listar():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('select email, nome, sobrenome, senha from login')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
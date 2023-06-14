from flask import Flask, render_template
import .l 
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")



@app.route("//")
def hello_world():
    return render_template("index.html")




'''
Executa o servidor
'''
def run(name, address, port):
    
    app.run(host=address,port=port)



from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

HOST = "147.139.179.33"
USER = "root"
PASSWORD = "Vjr#1234"

def run_ssh(command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASSWORD)

        stdin, stdout, stderr = ssh.exec_command(command)

        if command.startswith("sudo"):
            stdin.write(PASSWORD + "\n")
            stdin.flush()

        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        if error:
            return "ERROR:\n" + error
        return output

    except Exception as e:
        return f"Connection Failed: {e}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    result = run_ssh("sudo systemctl status vjr")
    return render_template("index.html", tab="status", result=result)


@app.route("/restart", methods=["POST"])
def restart():
    result = run_ssh("sudo systemctl restart vjr")
    result += "\n\n" + run_ssh("sudo systemctl status vjr")
    return render_template("index.html", tab="restart", result=result)


if __name__ == "__main__":
    app.run(debug=True, port=5005, host='0.0.0.0')

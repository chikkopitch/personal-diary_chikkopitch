from flask import Flask, redirect, render_template, request

from database import add_message, get_all_messages, init_db


app = Flask(__name__)
init_db()


@app.route('/')
def index():
    """Главная страница: показывает все сообщения."""
    messages = get_all_messages()
    return render_template('index.html', messages=messages)


@app.route('/add', methods=['POST'])
def add():
    """Обрабатывает отправку нового сообщения."""
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if name and message:
        add_message(name, message)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

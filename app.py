from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / 'entries.json'
app = Flask(__name__, template_folder='templates', static_folder='static')


def load_entries():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_entries(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    entries = load_entries()
    return render_template('index.html', entries=entries)


@app.route('/entry/<int:idx>')
def detail(idx):
    entries = load_entries()
    if 0 <= idx < len(entries):
        entry = entries[idx]
        return render_template('detail.html', entry=entry, idx=idx)
    return "Not found", 404


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        entries = load_entries()
        title = request.form.get('title')
        content = request.form.get('content')
        entries.append({'title': title, 'content': content})
        save_entries(entries)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:idx>', methods=['GET', 'POST'])
def edit(idx):
    entries = load_entries()
    if not (0 <= idx < len(entries)):
        return "Not found", 404
    if request.method == 'POST':
        entries[idx]['title'] = request.form.get('title')
        entries[idx]['content'] = request.form.get('content')
        save_entries(entries)
        return redirect(url_for('detail', idx=idx))
    return render_template('edit.html', entry=entries[idx], idx=idx)


@app.route('/delete/<int:idx>', methods=['POST'])
def delete(idx):
    entries = load_entries()
    if 0 <= idx < len(entries):
        entries.pop(idx)
        save_entries(entries)
        return redirect(url_for('index'))
    return "Not found", 404

# ==========================================
# ПРАКТИЧЕСКАЯ РАБОТА №7: Поиск
# ==========================================
@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_tasks = [task for task in tasks if query in task['text'].lower()]
    else:
        filtered_tasks = tasks
    return render_template('index.html', tasks=filtered_tasks, search_query=query)

# ==========================================
# ПРАКТИЧЕСКАЯ РАБОТА №8: Сортировка
# ==========================================

# Сортировка по дате (новые сверху)
@app.route('/sort/date')
def sort_by_date(): 
    sorted_tasks = sorted(tasks, key=lambda t: t.get('date', ''), reverse=True)
    return render_template('index.html', tasks=sorted_tasks)

# Сортировка по статусу (сначала активные)
@app.route('/sort/status')
def sort_by_status():
    sorted_tasks = sorted(tasks, key=lambda t: t.get('done', False))
    return render_template('index.html', tasks=sorted_tasks)

# Сортировка по приоритету (высокий → средний → низкий)
@app.route('/sort/priority')
def sort_by_priority():
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.get('priority', 'средний'), 2)
    )
    return render_template('index.html', tasks=sorted_tasks)

# Сортировка по алфавиту (А → Я)
@app.route('/sort/alpha')
def sort_by_alpha():
    sorted_tasks = sorted(tasks, key=lambda t: t.get('text', '').lower())
    return render_template('index.html', tasks=sorted_tasks)

if __name__ == '__main__':
    app.run(debug=True)

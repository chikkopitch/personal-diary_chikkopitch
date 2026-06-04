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
    # Присваиваем каждой записи её оригинальный номер из JSON
    for i, entry in enumerate(entries):
        entry['id'] = i
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
        # Пока дата не добавляется из формы, но если добавишь, сортировка по дате заработает
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
    entries = load_entries()
    
    # Присваиваем оригинальные ID перед фильтрацией
    for i, entry in enumerate(entries):
        entry['id'] = i
        
    if query:
        # Ищем совпадения и в заголовке, и в тексте дневника
        filtered_entries = [e for e in entries if query in e.get('title', '').lower() or query in e.get('content', '').lower()]
    else:
        filtered_entries = entries
        
    return render_template('index.html', entries=filtered_entries, search_query=query)

# ==========================================
# ПРАКТИЧЕСКАЯ РАБОТА №8: Сортировка
# ==========================================

# Сортировка по дате
@app.route('/sort/date')
def sort_by_date(): 
    entries = load_entries()
    for i, entry in enumerate(entries): entry['id'] = i
    sorted_entries = sorted(entries, key=lambda e: e.get('date', ''), reverse=True)
    return render_template('index.html', entries=sorted_entries)

# Сортировка по статусу (в дневнике этого поля нет, но код не упадет)
@app.route('/sort/status')
def sort_by_status():
    entries = load_entries()
    for i, entry in enumerate(entries): entry['id'] = i
    sorted_entries = sorted(entries, key=lambda e: e.get('done', False))
    return render_template('index.html', entries=sorted_entries)

# Сортировка по приоритету (в дневнике этого поля нет, но код не упадет)
@app.route('/sort/priority')
def sort_by_priority():
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}
    entries = load_entries()
    for i, entry in enumerate(entries): entry['id'] = i
    sorted_entries = sorted(entries, key=lambda e: priority_order.get(e.get('priority', 'средний'), 2))
    return render_template('index.html', entries=sorted_entries)

# Сортировка по алфавиту (по заголовку записи)
@app.route('/sort/alpha')
def sort_by_alpha():
    entries = load_entries()
    for i, entry in enumerate(entries): entry['id'] = i
    sorted_entries = sorted(entries, key=lambda e: e.get('title', '').lower())
    return render_template('index.html', entries=sorted_entries)

if __name__ == '__main__':
    app.run(debug=True)
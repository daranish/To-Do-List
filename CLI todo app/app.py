from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_tasks():
    try:
        with open('./todo.txt') as f:
            content = f.readlines()
        latest_id = int(content[0].strip())
        tasks = {line.split('```')[0]: line.split('```')[1].strip() for line in content[1:]}
        return latest_id, tasks
    except FileNotFoundError:
        with open('./todo.txt', 'w') as f:
            f.write('0\n')
        return 0, {}
    except IndexError:
        return 0, {}

def save_tasks(latest_id, tasks):
    curr_ind = [str(latest_id)]
    task_lines = [str(i) + '```' + t for i, t in tasks.items()]
    with open('./todo.txt', 'w') as f:
        f.writelines('\n'.join(curr_ind + task_lines))

@app.route('/')
def index():
    latest_id, tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        latest_id, tasks = load_tasks()
        new_id = latest_id + 1
        tasks[str(new_id)] = task
        save_tasks(new_id, tasks)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/done/<task_id>')
def done_task(task_id):
    latest_id, tasks = load_tasks()
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(latest_id, tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

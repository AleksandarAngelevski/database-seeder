import json
import os

PROGRESS_FILE = "seed_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}
    return {}

def save_progress(step, value: bool | int | str = True):
    progress = load_progress()
    progress[step] = value
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def get_progress(step, default=0):
    return load_progress().get(step, default)

def is_done(step):
    return load_progress().get(step) == True


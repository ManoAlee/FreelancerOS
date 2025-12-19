
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: System, Files & OS Tools (50+ Tools)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import shutil
import platform
import datetime
import glob
import sys

def get_os_name(): return platform.system()
def get_os_release(): return platform.release()
def get_python_version(): return sys.version
def get_current_dir(): return os.getcwd()
def list_files(path="."): return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
def list_folders(path="."): return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
def count_files(path="."): return len(list_files(path))
def file_exists(path): return os.path.exists(path)
def dir_exists(path): return os.path.isdir(path)
def create_dir(path): os.makedirs(path, exist_ok=True); return f"Created {path}"
def delete_file(path): os.remove(path); return f"Deleted {path}"
def delete_dir(path): shutil.rmtree(path); return f"Deleted {path}"
def rename_file(old, new): os.rename(old, new); return f"Renamed {old} to {new}"
def copy_file(src, dst): shutil.copy2(src, dst); return f"Copied {src} to {dst}"
def move_file(src, dst): shutil.move(src, dst); return f"Moved {src} to {dst}"
def get_file_size(path): return os.path.getsize(path)
def get_file_created_time(path): return datetime.datetime.fromtimestamp(os.path.getctime(path)).isoformat()
def get_file_modified_time(path): return datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
def read_text_file(path): 
    with open(path, 'r', encoding='utf-8') as f: return f.read()
def write_text_file(path, content): 
    with open(path, 'w', encoding='utf-8') as f: f.write(content); return "Written"
def append_text_file(path, content): 
    with open(path, 'a', encoding='utf-8') as f: f.write(content); return "Appended"
def get_env_var(var): return os.environ.get(var)
def set_env_var(var, val): os.environ[var] = val; return "Set"
def get_user_home(): return os.path.expanduser("~")
def join_paths(*args): return os.path.join(*args)
def split_path(path): return os.path.split(path)
def get_absolute_path(path): return os.path.abspath(path)
def is_hidden(path): return os.path.basename(path).startswith(".")
def search_files(pattern, path="."): return glob.glob(os.path.join(path, pattern))
def make_archive(base_name, format, root_dir): return shutil.make_archive(base_name, format, root_dir)
def unpack_archive(filename, extract_dir): shutil.unpack_archive(filename, extract_dir)
def get_disk_usage(path="."): return shutil.disk_usage(path)
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')
def open_file_default(path): 
    if platform.system() == "Windows": os.startfile(path)
    else: os.system(f"open {path}") # Mac/Linux simplified
def get_cpu_count(): return os.cpu_count()
def exit_program(): sys.exit()
def sleep_seconds(sec): import time; time.sleep(sec)
def get_date_today(): return str(datetime.date.today())
def get_time_now(): return str(datetime.datetime.now().time())
def get_timestamp(): return datetime.datetime.now().timestamp()
def timestamp_to_date(ts): return str(datetime.datetime.fromtimestamp(ts))
def days_between(d1, d2): 
    # Assumes d1, d2 are date strings YYYY-MM-DD
    dt1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    dt2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((dt2 - dt1).days)
def add_days(date_str, days):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return str((dt + datetime.timedelta(days=days)).date())
def is_leap_year(year): return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
def get_week_number(date_str): return datetime.datetime.strptime(date_str, "%Y-%m-%d").isocalendar()[1]
def get_weekday(date_str): return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
def touch_file(path): open(path, 'a').close()
def sanitize_filename(name): return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).strip()
def folder_is_empty(path): return not os.listdir(path)

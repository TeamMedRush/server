from os import listdir
from os.path import isfile

def load_routes():
  base_dir = __file__.replace("/__init__.py", "")
  file_queue = [base_dir]
  import_set = {*()}

  while file_queue:
    curr_path = file_queue.pop(0)

    for file in listdir(curr_path):
      full_path = curr_path + "/" + file

      if isfile(full_path):
        if file != __file__:
          import_set.add(full_path)
      else:
        if file != "__pycache__":
          file_queue.append(full_path)

  for file in import_set:
    relative_path = file.replace(base_dir + "/", "")
    module_name = relative_path.replace("/", ".").replace(".py", "")
    __import__(f"mrs.route.{module_name}")


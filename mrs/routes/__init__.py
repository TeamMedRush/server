import os

def load_routes():
  base_dir = os.path.dirname(__file__)
  file_queue = [base_dir]
  import_set = {*()}

  while file_queue:
    curr_path = file_queue.pop(0)

    for file in os.listdir(curr_path):
      full_path = os.path.join(curr_path, file)

      if os.path.isfile(full_path):
        if file.endswith(".py") and not file.startswith("__"):
          import_set.add(full_path)
      else:
        if file != "__pycache__":
          file_queue.append(full_path)

  for file_path in import_set:
    relative_path = os.path.relpath(file_path, base_dir)
    module_name = relative_path.replace(os.sep, ".").replace(".py", "")
    __import__(f"mrs.routes.{module_name}")


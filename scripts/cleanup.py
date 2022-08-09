import json
import glob
import os
import argparse

def is_directory(path):
  if (os.path.isdir(path)):
    return True
  else: 
    return False

def read_files_path(files_path):
  path_list = []
  
  if (is_directory(files_path)):
    for path in glob.iglob(files_path + '/**/*.json', recursive=True):
      path_list.append(path)
    return path_list
  else:
    path_list.append(files_path)
    return path_list

def read_json(path):
  f = open(path, 'r')
  return json.loads(f.read())

def write_json(file_path, data):
  with open(file_path, 'w', encoding='utf-8') as json_file:
    return json.dump(data, json_file, indent=2, ensure_ascii=False)

def delete_image_data(data_path):
  json_files = read_files_path(data_path)

  for file in json_files:
    data = read_json(file)

    if 'imageData' in data:
      del data['imageData']
      write_json(file, data)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--input', type=str, help='File that consists of a list of prediction, label pair')

  args = parser.parse_args()

  if args.input is None:
    raise AssertionError("You need to provide a file for evaluation. Use --help for getting more info.")

  delete_image_data(args.input)

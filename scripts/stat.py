import os
import json
import re
import glob
import argparse
      
def strip_line(words):
  return re.sub(r"[\s\n\t'\\t'\s]*", "", words)
      
def split_line(words):
  iterate_words = iter(list(words))
  result = [i if i != '្' else i + next(iterate_words) for i in iterate_words]
  return result

def count_characters(words):
  words = strip_line(words)
  words = split_line(words)
    
  number_of_alphabets = {}

  for word in words:
    if (word):
      if word in number_of_alphabets:
        number_of_alphabets[word] += 1
      else:
        number_of_alphabets[word] = 1
        
  return number_of_alphabets

def read_files_path(files_path):
  path_list = []
  
  if (os.path.isdir(files_path)):
    for path in glob.iglob(os.path.join(files_path, "**/*.json"), recursive=True):
      path_list.append(path)
    return path_list
  else:
    path_list.append(files_path)
    return path_list
    
def read_json(path):
  f = open(path, 'r')
  return json.loads(f.read())

def get_labels_from_json(data):
  return [key['label'] for key in data['shapes']]

def stat(input):
  files_path = read_files_path(input)
  number_of_text_boxes = 0
  number_of_alphabet = {}
  
  for file in files_path:
    json = read_json(file)
    number_of_text_boxes += len(get_labels_from_json(json))
    word_lists = get_labels_from_json(json)
    
    for word in word_lists:
      line = split_line(strip_line(word))
      
      for word in line:
        if (word):
          if word in number_of_alphabet:
            number_of_alphabet[word] += 1
          else:
            number_of_alphabet[word] = 1
  
  return {'number_of_text_boxes': number_of_text_boxes, 'number_of_each_character': number_of_alphabet}

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input', type=str, required=True, help='Pathname that consists of images and corresponding labels in JSON format.')
  args = parser.parse_args()
  
  if args.input is None:
    raise AssertionError("You need to provide a pathname to perform the stat. Use --help for getting more info.")
  
  print(stat(args.input))

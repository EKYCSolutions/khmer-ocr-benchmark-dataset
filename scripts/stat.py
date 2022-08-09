import os
import json
import re
import glob
import argparse

def is_directory(path):
  if (os.path.isdir(path)):
    return True
  else: 
    return False
      
def strip_words(words):
  return re.sub(r"[\s\n\t'\\t'\s]*", "", words)
      
def split_words(words):
  iterate_words = iter(list(words))
  result = [i if i != '្' else i + next(iterate_words) for i in iterate_words]
  return result

def count_characters(words):
  words = strip_words(words)
  words = split_words(words)
    
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

def get_labels_from_json(data):
  return [key['label'] for key in data['shapes']]

def count_number_of_text_boxes(input):
  files_path = read_files_path(input)
  number_of_text_boxes = 0
  
  for file in files_path:
    json = read_json(file)
    number_of_text_boxes += len(get_labels_from_json(json))
  
  return number_of_text_boxes

def count_characters_from_json(input):
  files_path = read_files_path(input)
  number_of_alphabet = {}
  
  for file in files_path:
    json = read_json(file)
    word_lists = get_labels_from_json(json)
    
    for word in word_lists:
      strip_word = strip_words(word)
      split_word = split_words(strip_word)
      
      for word in split_word:
        if (word):
          if word in number_of_alphabet:
            number_of_alphabet[word] += 1
          else:
            number_of_alphabet[word] = 1
    
  return number_of_alphabet

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input', type=str, required=True, help='File that consists of a list of prediction, label pair')
  args = parser.parse_args()
  
  if args.input is None:
    raise AssertionError("You need to provide a file for evaluation. Use --help for getting more info.")
  
  print('There are %s boxes.' %count_number_of_text_boxes(args.input))
  print(count_characters_from_json(args.input))

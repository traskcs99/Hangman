import string
import pprint
import re
import random
pp = pprint.PrettyPrinter(indent=4)


def create_wordlist(fileName, length):
  f = open(fileName)
  wordlist = []
  for word in f:
    word = word.strip().upper()
    if word.isalpha() and len(word) == length: 
      wordlist.append(word)
  return wordlist

def create_analysis_dict():
    out = {'letters': {}, 'count': 0}
    for l in string.ascii_uppercase:
        out['letters'][l] = {
            'positions': {},
            'count': 0,
            'listSizeEV': None,
            'probability': 0
        }
    return out


def generate_unique_letter_keys(word):
    uniqueLetters = set(word)
    out = []
    for letter in uniqueLetters:
        key = ''
        for char in word:
            if char == letter:
                key += char
            else:
                key += "_"
        out.append((letter, key))
    return out


def process_word_in_analysis_dict(letterKeyList, analysis_dict):
    analysis_dict['count'] += 1
    for i in letterKeyList:
        letter, key = i
        count = analysis_dict['letters'][letter]['positions'].get(key, 0)
        analysis_dict['letters'][letter]['positions'][key] = count + 1
        analysis_dict['letters'][letter]['count'] += 1


def calculate_remaining_list_sizeEV(analysis_dict):
    totalSize = analysis_dict['count']
    delete = []
    for letter, info in analysis_dict['letters'].items():
        if info['count'] == 0:
          delete.append(letter)
          continue
        ev = 0
        info['probability'] = info['count'] / totalSize
        for key, count in info['positions'].items():
          ev += count * count / totalSize
          '''false ev'''
        ev += (totalSize - info['count']) * (totalSize - info['count']) / totalSize
        info['listSizeEV'] = ev
    for key in delete: del analysis_dict['letters'][key]
        

def find_min_list_sizeEV(analysis_dict):
    letters = analysis_dict['letters']
    key_min = min(letters.keys(), key=(lambda k: letters[k]['listSizeEV']))
    minList = [
        x for x in list(letters.keys())
        if letters[x]['listSizeEV'] == letters[key_min]['listSizeEV']
    ]
    return minList


def find_max_letter_probability(analysis_dict):
    letters = analysis_dict['letters']
    key_max = max(letters.keys(), key=(lambda k: letters[k]['probability']))
    maxList = [
        x for x in list(letters.keys())
        if letters[x]['probability'] == letters[key_max]['probability']
    ]
    return maxList


def find_max_letter_count(analysis_dict):
    letters = analysis_dict['letters']
    key_max = max(letters.keys(), key=(lambda k: letters[k]['count']))
    maxList = [
        x for x in list(letters.keys())
        if letters[x]['count'] == letters[key_max]['count']
    ]
    return maxList


def get_ranked_letter_list(wordlist, alreadyPicked = []):
  d = create_analysis_dict()
  for word in wordlist:
    u = generate_unique_letter_keys(word.upper())
    process_word_in_analysis_dict(u, d)
  for x in alreadyPicked:
      d['letters'].pop(x,None)
  calculate_remaining_list_sizeEV(d)
  letterList = [(letter, value['listSizeEV']) for letter, value in d['letters'].items()]
  letterList.sort(key = lambda x: x[1])
  return letterList

def calc_percent_diff(num1, num2):
  return abs(((num1-num2)/num1))

def pick_letter(wordlist, guessed_letters, rnd):
  l = get_ranked_letter_list(wordlist, guessed_letters)
  if rnd:
    top_10_percent = [t for t in l if l[0][1] * 1.025 > t[1]]
    l = random.choice(top_10_percent)
    l=l[0]
  else: 
    l = l[0][0]
  return l

def format_display_word(displayWord, secretWord, letter):
  outlist = []
  for i in range(len(secretWord)):
    if secretWord[i] == letter:
      displayWord = displayWord[:i] + letter + displayWord[i+1:]
      outlist.append((letter, i))
  return (displayWord, outlist)

def shrink_word_list(wordlist, rightLettersWithIndex, wrong_letters):
  outList =[]
  for word in wordlist:
    if any([l in word for l in wrong_letters]):
        continue
    elif all([ l == word[i] for (l,i) in rightLettersWithIndex ]):
      outList.append(word)
  return outList

def start_game(secretWord, rnd = False):
  secretWord = secretWord.upper()
  wordlist = create_wordlist('masterwordlist.txt', len(secretWord))
  guessed_letters = []
  displayWord = '-' * len(secretWord)
  right_letters = []
  wrong_letters = []
  right = len(right_letters)
  wrong = len(wrong_letters)
  rightLettersWithIndex = []
  while (displayWord != secretWord):
    l = pick_letter(wordlist, guessed_letters, rnd) 
    guessed_letters.append(l)

    if l in secretWord:
      right_letters.append(l)
      right += 1
      displayWord, ol = format_display_word(displayWord, secretWord, l)
      rightLettersWithIndex += ol
    else:
      wrong_letters.append(l)
      wrong += 1
    wordlist = shrink_word_list(wordlist, rightLettersWithIndex, wrong_letters)
    print(f'Right: {right}, Wrong: {wrong}, Display: {displayWord}, Guessed Wrong: {wrong_letters}')



""" 
start_game('bookworm'.upper())
"""
'''   
wordlist = create_wordlist('masterwordlist.txt', len(secretWord))

d = create_analysis_dict()
for word in wordlist:
  u = generate_unique_letter_keys(word.upper())
  process_word_in_analysis_dict(u, d)
calculate_remaining_list_sizeEV(d)






#print(find_min_list_sizeEV(d))
#print(find_max_letter_probability(d))
#print(find_max_letter_count(d))
#pp.pprint(d)
print("++++========++++++")
print(wordlist)
print(pick_letter(wordlist, [], False))
wordlist = shrink_word_list(wordlist, [('A',1), ('T',3), ('T',2)],['D'])
print(wordlist)
print("++++========++++++")
#print(pick_letter(wordlist, ["D"], False))

secretWord = "CARL"
wordlist = create_wordlist('masterwordlist.txt', len(secretWord))
#wordlist = ["CARL", "PAUL", "ALEX", "DOUG", "MATT"]
guessed_letters = []
displayWord = '-' * len(secretWord)
right_letters = []
wrong_letters = []
right = len(right_letters)
wrong = len(wrong_letters)
rightLettersWithIndex = []
print(len(wordlist))
print(secretWord in wordlist)

l = pick_letter(wordlist, guessed_letters, False) 
print(f'Picked: {l}')
guessed_letters.append(l)
if l in secretWord:
  right_letters.append(l)
  right += 1
  displayWord, ol = format_display_word(displayWord, secretWord, l)
  rightLettersWithIndex += ol
else:
  wrong_letters.append(l)
  wrong += 1
  wordlist = shrink_word_list(wordlist, rightLettersWithIndex, wrong_letters)
  print(len(wordlist))
  print(f'Right: {right}, Wrong: {wrong}, Display: {displayWord}')
'''
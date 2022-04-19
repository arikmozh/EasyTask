from Easy import *

# set of string options
yes = {'yes','y', 'ye', ''} 
no = {'no','n'}

def start():
  is_running_another_round = True
  while(is_running_another_round):
    print('\nStarting test...\n')
    key_word = input('Please tell me what you want to find next to you?\n')
    test = Easy(key_word)
    test.run()
    choice = input('Are you having fun?\nDo you want to continue?\n\n[Y/n]?\nPlease respond with "yes" or "no"\n')
    if choice in yes:
      pass
    elif choice in no:
      is_running_another_round = False
  print('\nThe test is done.')

start()


'''actual_word = 'flame'
import pyautogui
import time
import random
import json 

with open('wordles.json', 'r') as f:
    wordles = json.load(f)
with open('nonwordles.json', 'r') as f:
    nonwordles = json.load(f)

cur_wordles = wordles

while True:
    feedback = []
    print(f"len: {len(cur_wordles)}")
    guess = random.choice(cur_wordles)
    for i in range(5):
        if guess[i] == actual_word[i]:
            feedback.append('0')
        elif guess[i] in actual_word:
            feedback.append('1')
        else:
            feedback.append('2')
    feedback_str = ''.join(feedback)
    print(f"guess: {guess}, feedback: {feedback_str}")
    if feedback_str == '00000': 
        print("you win!")
        break
    cur_wordles = [word for word in cur_wordles if all((feedback[i] == '0' and word[i] == guess[i]) or (feedback[i] == '1' and guess[i] in word and word[i] != guess[i]) or (feedback[i] == '2' and guess[i] not in word) for i in range(5))]'''

import pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01
import time
import random
import json 

with open('wordles.json', 'r') as f:
    wordles = json.load(f)

cur_wordles = wordles

# coords
row_col_coords = [
    (610, 220),
    (675, 219),
    (737, 218),
    (801, 219),
    (867, 219),

    (610, 289),
    (673, 285),
    (739, 289),
    (805, 290),
    (867, 291),

    (610, 356),
    (674, 355),
    (738, 351),
    (803, 353),
    (866, 351),

    (613, 418),
    (672, 418),
    (737, 418),
    (805, 418),
    (866, 417),

    (610, 482),
    (673, 482),
    (738, 481),
    (802, 480),
    (867, 481),

    (610, 546),
    (673, 545),
    (736, 543),
    (803, 543),
    (868, 545),
]

play_button_coords = (641, 635) 

def play_again():
    global play_button_coords
    pyautogui.moveTo(play_button_coords[0], play_button_coords[1], duration=0.01)
    pyautogui.click()

print("screen size:", pyautogui.size())
shot = pyautogui.screenshot()
shot_size = shot.size
print("screenshot size:", shot_size)

# Failed code to try to make it work with diff window sizes 

#row_col_coords = [(round(shot_size[0]/1470 * coord[0]), round(shot_size[1]/956 * coord[1])) for coord in row_col_coords]
#play_button_coords = (round(shot_size[0]/1470 * play_button_coords[0]), round(shot_size[1]/956 * play_button_coords[1]))
print(row_col_coords)

def get_feedback(round):
    global row_col_coords
    feedback = []
    for i in range(5):
        coord = row_col_coords[round*5 + i]

        shot = pyautogui.screenshot(region=(0, 0, pyautogui.size()[0], pyautogui.size()[1]))

        shot.save("debug.png")
        pixel = shot.getpixel((coord[0], coord[1]))
        #print(f"col: {i}, pixel: {pixel}")
        if abs(pixel[0] - 121) < 10 and abs(pixel[1] - 168) < 10 and abs(pixel[2] - 107) < 10: # green
            feedback.append(0)
        elif abs(pixel[0] - 197) < 10 and abs(pixel[1] - 181) < 10 and abs(pixel[2] - 102) < 10: # yellow
            feedback.append(1)
        elif abs(pixel[0] - 121) < 10 and abs(pixel[1] - 124) < 10 and abs(pixel[2] - 126) < 10: # gray 
            feedback.append(2)
        else:
            feedback.append(3)  

    return feedback

def input_guess(guess):
    #global row_col_coords
    for i in range(5):
        #coord = row_col_coords[round*5 + i]
        #pyautogui.moveTo(coord[0], coord[1], duration=0.1)
        #pyautogui.click()
        pyautogui.typewrite(guess[i], interval=0.001)

    #pyautogui.moveTo(coord[0]+100, coord[1], duration=0.1) 
    pyautogui.press('enter')

# Add a function to calculate expected feedback for each possible secret word. 
def calculate_feedback(word, guess):
    # Start with saying nothing was found, then update it as you go along.
    # The reason we have to do this is because of duplicate letters in words, and yellow letters.
    feedback = [2]*5
    word_list = list(word)
    for i in range(5):
        if guess[i] == word_list[i]:
            feedback[i] = 0
            word_list[i] = None
    for i in range(5):
        if feedback[i] == 2 and guess[i] in word_list:
            feedback[i] = 1
            word_list[word_list.index(guess[i])] = None
    return feedback 

print("starting...")
time.sleep(1.5)
round = 0

wins = 0
losses = 0 
num_games = 6

while wins + losses < num_games:
    feedback = []
    print(f"len: {len(cur_wordles)}")
    guess = random.choice(cur_wordles)
    input_guess(guess)
    time.sleep(1)
    feedback = get_feedback(round)
    feedback_str = ''.join([str(x) for x in feedback])
    print(f"guess: {guess}, feedback: {feedback_str}")
    if feedback_str == '00000':
        round = 0 
        wins += 1 
        cur_wordles = wordles
        print(f"you win! total wins: {wins}, total losses: {losses}")
        time.sleep(2.5)
        play_again()
        time.sleep(0.75)
        continue 
    if round == 5:
        print(f"you lost one! rip. total wins: {wins}, total losses: {losses}")
        round = 0 
        losses += 1 
        cur_wordles = wordles
        time.sleep(2.5)
        play_again()
        time.sleep(0.75)
        continue
    cur_wordles = [word for word in cur_wordles if calculate_feedback(word, guess) == feedback]
    round += 1

print(f"final wins: {wins}, final losses: {losses}")



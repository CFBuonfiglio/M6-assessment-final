#!/usr/bin/env python
# coding: utf-8

# # Word + Hint JSON Creation

# In[ ]:


import json

wordlist = [
    {
        'word':'MISSISSIPPI',
        'hint':'Known for the river'
    },
    {
        'word':'RUSTLE',
        'hint':'Done with cattle and newspapers'
    },
    {
        'word':'WIZARDRY',
        'hint':'The arcane arts'
    },
    {
        'word':'TORNADOES',
        'hint':'Enemy of Dorothy'
    },
    {
        'word':'FRACTURE',
        'hint':'A break'
    },
    {
        'word':'INTERPRETED',
        'hint':'Not compiled'
    }
]

with open("words.json", "w") as outfile:
    json.dump(wordlist, outfile)


# # Functions

# In[ ]:


def ask_buy_vowel(): #Verifies response
    r = input("\nWould you like to buy a vowel for $250? Y/N ")
    while r not in ["Y", "y", "N", "n"]:
        r = input("Please select Y or N. ")
    return r

def ask_consonant(): #Ensures that the guess is non-numeric and either a consonant or a word
    g = input("Guess a consonant, or guess the word! ").upper()
    while g.isalpha() is False: #Checking for alphabetical character
        g = input("Please enter a consonant or guess the word. ")
    while g in ["A", "E", "I", "O", "U"]: #Checking for consonant
        g = input("Please enter a consonant or guess the word. ")
    return g

def ask_vowel(): #Ensures that the guess is a vowel
    g = input("Guess a vowel. ").upper()
    while g not in ["A", "E", "I", "O", "U"]: #Checking for consonant
        g = input("Please enter a vowel. ").upper()
    return g


# # Game

# In[ ]:


#Import JSON word file
file = open('words.json') 
words = file.read() 
wordlist = json.loads(words) 

#Select random word & its hint
import random
randomness = random.randint(0, len(wordlist) - 1)

target = wordlist[randomness]["word"]
hint = wordlist[randomness]["hint"]

#Build the word's "board"
blank = [] 

for ltr in target: 
    blank.append('_') 

#Create the wheel
wheel = list(range(100, 1000, 50))
wheel.append(1500)
wheel.append(2000)
wheel.append(3000)
wheel.append("BANKRUPT")
wheel.append("LOSE A TURN")
wheel.append("MYSTERY")

#Game controls
landed_on = 0 
activeplayer = 0 
currentround = 1 #Change to 3 to test final round

wallet = [0, 0, 0] 

guess = ''
finalguesses = ['', '', '', '', ''] 
finalreveal = ["R", "S", "T", "L", "N", "E"]

buyavowel = False 

response = ''

gameover = False 


### Game Begins ###
print("Welcome to...\nWheel! Of! Fortune!")

while gameover is False:
    while currentround != 3:
        print("\n===================================")
        print(f"Round {currentround}")
        print(f"Player {activeplayer + 1}'s turn")
        print(f"Player {activeplayer + 1}'s total winnings: ${wallet[activeplayer]}\n")
        print(f"Hint: {hint}")
        print(' '.join(blank))
        print("\nSpinning the wheel...")
        landedon = random.choice(wheel)
        
        #Check if player landed on BANKRUPT / LOSE A TURN / MYSTERY
        if landedon == "BANKRUPT" or landedon == "LOSE A TURN" or landedon == "MYSTERY":
            print(f"You landed on {landedon}!")
            if landedon == "MYSTERY":
                landedon = random.choice(["BANKRUPT", 1000])
            if landedon == "BANKRUPT": #Player landed on BANKRUPT
                wallet[activeplayer] = 0
                print("Oh no! Your total winnings have returned to zero, and your turn is over.")
                if activeplayer == 2:
                    print("On to the next round...")
                    currentround += 1
                    activeplayer = 0
                else:
                    activeplayer += 1
            elif landedon == "LOSE A TURN": 
                print("Oh no! Your turn is over.")
                if activeplayer == 2:
                    print("On to the next round...")
                    currentround += 1
                    activeplayer = 0
                else:
                    activeplayer += 1
            else: #Player won $1000 from MYSTERY
                print("You win an extra $1000!")
                wallet[activeplayer] += 1000
        
        else: #Player landed on a cash value
            print(f"You landed on ${landedon}!\n")
            guess = ask_consonant()
            if len(guess) == 1:
                if guess in target:
                    for index, ltr in enumerate(target):
                        if ltr == guess:
                            blank[index] = guess
                    print(f"Good guess! You added ${landedon} to your total winnings!\n")
                    wallet[activeplayer] += landedon
                    
                    print(f"{' '.join(blank)}\n")
                    
                    buyavowel = True

                    while buyavowel is True:
                        response = ask_buy_vowel()
                        if response in ["Y", "y"]:
                            guess = ask_vowel()
                            if guess in target:
                                for index, ltr in enumerate(target):
                                    if ltr == guess:
                                        blank[index] = guess
                                print("\nGood guess!\n")
                                print(f"Hint: {hint}")
                                print(' '.join(blank))
                                print(f'Cash remaining: {wallet[activeplayer]}')
                            else: 
                                print(f"Sorry, no {guess}!")
                        else: #Response is N/n
                            buyavowel = False
                else:
                    print(f"Sorry, no {guess}!")
                    if activeplayer == 2:
                        print("Too bad! On to the next round.")
                        currentround += 1
                        activeplayer = 0
                    else:
                        print(f"Pass the keyboard to player {activeplayer + 2}!")
                        activeplayer += 1
            else:
                if guess == target:
                    print(f"\nThe word was {target}!")
                    print(f"Player {activeplayer + 1} wins!")
                    wallet[activeplayer] += 50000
                    print(f"Your total winnings are: ${wallet[activeplayer]}")
                    print("\nSee you next time on...\nWheel! Of! Fortune!")
                    gameover = True
                    break
                else: #Guessed the word incorrectly
                    print("\nSorry, that wasn't the word!")
                    if activeplayer == 2:
                        print("On to the next round!")
                        currentround += 1
                        activeplayer = 0
                    else:
                        print(f"Pass the keyboard to Player {activeplayer + 2}")
                        activeplayer += 1
    else:
        if wallet[0] == wallet[1]:
            if wallet[1] == wallet[2]:
                activeplayer = random.randint(0, 2) #If all players have the same winnings, pick at random
        else:
            activeplayer = wallet.index(max(wallet))
        print("\n===================================")
        print(f"Welcome to the final round, Player {activeplayer + 1}!")
        print("If you win this bonus round, you'll win an additional $50,000 on top of your current winnings.\n")
        
        for index, ltr in enumerate(target):
            if ltr in finalreveal:
                blank[index] = target[index]
        print(" ".join(blank))
        print()
        print("Guess four consonants and one vowel.")
        
        for i in range(len(finalguesses) - 1):
            finalguesses[i] = input(f"Consonant {i + 1}: ").upper()
            while finalguesses[i].isalpha() is False: #Checking for alphabetical character
                finalguesses[i] = input("Please enter a consonant. ").upper()
            while finalguesses[i] in ["A", "E", "I", "O", "U"]:
                finalguesses[i] = input("Please enter a consonant. ").upper()
        
        finalguesses[4] = input("Vowel: ").upper()
        
        while finalguesses[4].isalpha() is False: #Checking for alphabetical character
            finalguesses[4] = input("Please enter a vowel. ").upper()
        while finalguesses[4] not in ["A", "E", "I", "O", "U"]:
            finalguesses[4] = input("Please enter a vowel. ").upper()
        
        for item in finalguesses:
            for index, ltr in enumerate(target):
                if ltr == item:
                    blank[index] = item
                    
        print()
        print(" ".join(blank))
        
        validguess = False
        
        guess = input("You've got one shot to guess the word for $50,000! ").upper()

        while guess.isalpha() is False:
            guess = input("Please enter alphabetical text only! ").upper()

        while validguess is False:
            if len(guess) == 1: #Checking for full word
                guess = input("Please enter a word! ").upper()
            else:
                validguess = True

        if guess == target:
            print("Congratulations! You win!")
            wallet[activeplayer] += 50000
            print(f"Your total winnings are: ${wallet[activeplayer]}")
            print("\nSee you next time on...\nWheel! Of! Fortune!")
            gameover = True
            break
        else: #Guess was incorrect
            print("Sorry, but that's not the right word!")
            print(f"The word was: {target}")
            print(f"You're still taking home ${wallet[activeplayer]}!")
            print("\nSee you next time on...\nWheel! Of! Fortune!")
            gameover = True
            break


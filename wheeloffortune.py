
import random

def welcome(winning, emptyPhrase, category):
    print("Welcome to Wheel of Fortune!")
    print("The Phrase Is: ")
    print(" ".join(emptyPhrase))
    print("The Category is: " +category)
    print("Your winning is: $ " + str(winning))

def generate_phrase(phraseNum):
    phraseBank = open('phrasebank.txt').read().splitlines()
    phrase = phraseBank[phraseNum]
    return phrase

def generate_cat(num):
    if num <20:
        return "Before and After"
    elif num >=20 and num <40:
        return "Song Lyrics"
    elif num >=40 and num <60:
        return "Around the House"
    elif num >=60 and num <80:
        return "Food and Drink"
    else:
        return "Same Name"

def generate_empty(phrase):
    length = len(phrase)
    emptyPhrase = []
    for index in phrase:
        if index.isalpha():
            emptyPhrase += "_"
        else:
            emptyPhrase += index
    return emptyPhrase

def user_input(winning, phrase, consonants, vowels):
    print("Would you like to Spin the Wheel (type ‘spin’), Buy A Vowel (type ‘vowel’), or Solve the Puzzle (type ‘solve’)? ")
    userInput = input("Type your action: ")
    done = False
    guess = ""
    solved = False
    while done == False:
        if userInput.lower() == "spin":
            done = True
            result = spin(winning, phrase, consonants)
            winning = result[0]
            guess = result[1]

        elif userInput.lower() == "vowel":
            done = True
            if credit_check(winning) == True:
                guess = vowel(vowels)
                check_phrase(guess, phrase)
                winning -= 250
            else:
                print("Sorry, you don’t have enough winnings to buy a vowel!")
        elif userInput.lower() == "solve":
            done = True
            solved = solve(phrase)
            if solved:
                print("That’s correct - you solved the puzzle!")
            else:
                print("Sorry, that guess is incorrect! All your winnings are gone :(")
                if winning > 0:
                    winning = 0
        else:
            userInput = input("Invalid input, please type a command of 'spin', 'vowel', or 'solve': ")
    return winning, guess, solved

def spin(winning, phrase, consonants):
    outcome = [50, 100, 100, 100, 100, 100, 100, 200, 200, 200, 200, 250, 250, 250, 500, 500, 750, 750, 1000, 2000, 5000, 10000, "Bankrupt","Bankrupt"]
    roll = random.randint(0,23)
    consonant = ""
    if roll <22:
        spinVal = outcome[roll]
        print("You spun: $" + str(spinVal))
        consonant = guess_consonant(consonants)
        multiple = check_phrase(consonant, phrase)
        winning = change_point(winning, spinVal, multiple)
    else:
        print("Uh oh, you’ve spun a Bankrupt! Your winnings will go down to $0.")
        winning = 0
    return winning, consonant

def guess_consonant(consonants):
    done = False
    repeat = False
    consonant = input("Guess a consonant: ").upper()

    while done == False:
        for letter in consonants:
            if consonant == letter:
                repeat = True

        if consonant.isalpha() and len(consonant)==1 and is_consonant(consonant)==True and repeat == False:
            done = True
            return consonant
        else:
            repeat = False
            consonant = input("Invalid input, please enter a non-repeating consonant: ")

def change_point(winning, spinVal, multiple):
    winLoss = spinVal*multiple
    if winLoss <0:
        print("$"+ str(winLoss*-1)+ " will be deducted from your balance")
    elif winLoss >0:
        print("$" + str(winLoss)+ " will be added to your balance")
    else:
        print("No change to your balance")
    winning +=winLoss
    return winning

def check_phrase(guess, phrase):
    multiple = 0
    for index in phrase:
        if guess.upper() == index.upper():
            multiple +=1
    if multiple == 0:
        print("Sorry, there are no " + guess + " in the puzzle")
        multiple = -1
    else:
        print("Great job, "+ guess +" appear in the puzzle "+ str(multiple) +" times!")
    return multiple

def is_consonant(letter):
    vowels = "AEIOU"
    isConsonant = True
    for index in vowels:
        if letter.upper() == index:
            isConsonant= False
    return isConsonant

def credit_check(winning):
    if winning >= 250:
        return True
    else:
        return False

def vowel(vowels):
    repeat = False
    done = False
    vowel = input("Ok! $250 will be deducted from your winnings. Which vowel would you like to buy (A, E, I, O, U)?: ").upper()
    while done == False:
        for letter in vowels:
            if vowel == letter:
                repeat = True
        if vowel.isalpha() and len(vowel)==1 and is_consonant(vowel)==False and repeat == False:
            done = True
            return vowel.upper()
        else:
            repeat = False
            vowel = input("Invalid input, please enter a non-repeating vowel: ").upper()

def solve(phrase):
    solve = input("What’s your best guess (be sure to enter your guess with single spaces!)?: " ).upper()
    if solve == phrase:
        return True
    else:
        return False

    return

def replace_empty(guess, phrase, emptyPhrase):
    length = len(phrase)
    indexList = []
    index = 0
    while index <length:
        if guess == phrase[index]:
            emptyPhrase[index] = guess
        index +=1
    return emptyPhrase

def announce(winning, emptyPhrase, consonants, vowels):
    print("")
    print("The phrase is: ")
    print(" ".join(emptyPhrase))
    print("Your guessed vowels: ", end = " ")
    for word in vowels:
        print(word, end = " ")
    print("")
    print("Your guessed consonants: ", end = " ")
    for word in consonants:
        print(word, end = " ")
    print("")
    print("Your remaining balance: $" + str(winning))

def main():
    winning = 0
    ranNum = random.randint(0,99)
    done = False
    consonants = []
    vowels = []

    phrase = generate_phrase(ranNum)
    emptyPhrase = generate_empty(phrase)
    category = generate_cat(ranNum)
    welcome(winning, emptyPhrase, category)

    while done == False:
        result = user_input(winning, phrase, consonants, vowels)
        winning = result[0]
        guess = result[1].upper()
        done = result[2]
        if is_consonant(guess):
            consonants +=guess
        else:
            vowels +=guess
        if done == False:
            emptyPhrase = replace_empty(guess, phrase, emptyPhrase)
            announce(winning ,emptyPhrase,consonants,vowels)
    if winning <0:
        winning = 0
    print("Congratulations, you’ve won the game! Your winnings are $" + str(winning) + "! Thank you for playing the Wheel of Fortune!")

if __name__ == '__main__':
    main()

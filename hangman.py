# -*- coding: utf-8 -*-
"""
Created on 14 Feb 2019

@author: Fbasham
"""

from random import randint

again = True
while again:

    start = input('press "y" to choose the test-case word: ')
    if start == "y":
        word = 'hangman'
        
    elif start == 'f':
        word = 'frank basham is fucking awesome'
        
    else:
        with open(r'H:\FBasham\Python (do not delete code please)\sampleFICT.txt', 'r') as word_list:
            words = word_list.read().split(' ')
            word = (words[randint(0,1000)] + ' ' + words[randint(0,1000)] + ' ' + words[randint(0,1000)])
    
    
    for l in word.lower():
        if l != ' ':
            print('_', end = ' ')
        else:
            print(' ', end = ' ')
    print('')
    
    sketch = [
    [(''), (''), (' |_________ '), (' |       |  '), (' |	 O     '),(' |          '),(' |          '),(' |          '),(' |          ')],
    [(''), (''), (' |_________ '), (' |       |  '), (' |	 O     '),(' |       |  '),(' |          '),(' |          '),(' |          ')],
    [(''), (''), (' |_________ '), (' |       |  '), (' |	 O     '),(' |      /|  '),(' |          '),(' |          '),(' |          ')],
    [(''), (''), (' |_________ '), (' |       |  '), (' |	 O     '),(' |      /|\ '),(' |          '),(' |          '),(' |          ')],
    [(''), (''), (' |_________ '), (' |       |  '), (' |	 O     '),(' |      /|\ '),(' |      /   '),(' |          '),(' |          ')],
    [(''), (''), (' |_________ '), (' |       |  '), (' |	 O     '),(' |      /|\ '),(' |      / \ '),(' |          '),(' |          ')]]


    

    match = []
    guesses = []
    wrong = 0  
    while wrong < 6:
        guess = input('guess a letter: ')
        guesses.append(guess)
        print('you\'ve guessed: ')
        for g in sorted(set(guesses)):
            print(g, end = ', ')
    
        if guess in word:
            print('')
            print('match!')
            match.append(guess)
    
        else:
            print('')
            print('not a match')
            wrong += 1
            for i in (sketch[wrong-1]):
                print(i)
    
        for m in word:
            if m in match:
                print(m, end = ' ')
                
            elif m != ' ':
                print('_', end = ' ')
                
            else:
                print(' ', end = ' ')
        
        if set(word.replace(' ','')) == set(match):
            print('')
            print('you win!')
            break
    
        
        if wrong == 6:        
            print('')
            print('sorry, you lose')
            print('the word you were trying to guess was: ' + word)
    
    play = input('press "y" to play again: ')
    if play != "y":
        print('goodbye world!')
        again = False



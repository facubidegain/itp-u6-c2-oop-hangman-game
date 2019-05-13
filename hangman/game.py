from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self,char,hit=None,miss=None):
        self.char = char
        if hit is not None and miss is not None:
            raise InvalidGuessAttempt()
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit == True:
            return True
        return False
    
    def is_miss(self):
        if self.miss == True:
            return True
        return False


class GuessWord(object):
    def __init__(self,word):
        if not word:
            raise InvalidWordException()
        self.answer = word
        self.masked = self._mask_word()
        
    def _mask_word(self):
        return '*'*len(self.answer)
    
    def perform_attempt(self,guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException()
        if guess.lower() in self.answer.lower():
            attempt = GuessAttempt(guess,hit=True)
            for index,char in enumerate(self.answer):
                if char.lower() == guess.lower():
                    self.masked = self.masked[:index] + char.lower() + self.masked[index+1:]
        else:
            attempt = GuessAttempt(guess,miss=True)
        return attempt
        


class HangmanGame(object):
    WORD_LIST = ['rmotr','python','awesome']
    
    @classmethod
    def select_random_word(cls,list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
    
    def __init__(self,word=WORD_LIST,number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word))

    
    def guess(self,guess):
        if self.is_finished():
            raise GameFinishedException()
        attempt = self.word.perform_attempt(guess)
        self.previous_guesses.append(guess.lower())
        if attempt.is_hit():
            if self.is_won():
                raise GameWonException()
        else:
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
        return attempt
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
            
    
    
    
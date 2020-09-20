from random import *
from itertools import *
import string                       
class password_generator():  
   def __init__(self,final_output,special_nproduction,final_specp): #creating the local variables
       self.final_output = final_output
       self.special_nproduction = special_nproduction
       self.final_specp = final_specp
      
      
   def alpha_rand_func(self): #for randomly selecting alphabets
       alpha = string.ascii_letters
       for i in range(4):
           self.final_output += choice(alpha)
        
   def symbol_rand_func(self): #for randomly selecting symbols
      symbol = " ';>?<,./|}{][]}_+=-!@#$%^&*()~`"
      for i in range(3):
         self.special_nproduction += choice(symbol)
             
   def int_rand_func(self): #for randomly selecting integers
      integer = string.digits
      for i in range(2):
         self.special_nproduction += choice(integer)
        
   def special_number_production(self): #for concatenating the integers and symbols
          self.special_nproduction = list(self.special_nproduction)
          init_perm = list(permutations((self.special_nproduction),5))
          selected_comb_init_list = choice(init_perm) #selecting a permutation of integers and symbols randomly
          mod_selected_comb_init = "" #for storing the permutation in the form of a variable
          for i in selected_comb_init_list: #iterating through the selected_comb_init_list
             mod_selected_comb_init += i 
          self.final_output += mod_selected_comb_init  # adding the integer-symbol combination to final output
   def final_output_production(self): #for concatenating all the characters, selecting a combination of it randommly and returning it as output
           return self.final_output #returns the final output
####################################          

####################################
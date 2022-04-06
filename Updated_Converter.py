#!/usr/bin/env python
# coding: utf-8

# In[29]:



# Basic imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn


# our key value pairs to be converted
conversion = {
    "iy_B" : "AI",    
    "iy_E" : "AI",
    "iy_I" : "AI",
    "iy_S" : "AI",
    "b_B" : "MBP",
    "b_E" : "MBP",
    "b_I" : "MBP",
    "b_S" : "MBP",
    "d_B" : "L",
    "d_E" : "L",
    "d_I" : "L",
    "d_S" : "L",
    "f_B" : "FV",
    "f_E" : "FV",
    "f_I" : "FV",
    "f_S" : "FV",
    "g_B" : "E",
    "g_E" : "E",
    "g_I" : "E",
    "g_S" : "E",
    "k_B" : "etc",
    "k_E" : "etc",
    "k_I" : "etc",
    "k_S" : "etc",
    "sh_B" : "U",
    "sh_E" : "U",
    "sh_I" : "U",
    "sh_S" : "U",
    "l_B" : "L",
    "l_E" : "L",
    "l_I" : "L",
    "l_S" : "L",
    "m_B" : "MBP",
    "m_E" : "MBP",
    "m_I" : "MBP",
    "m_S" : "MBP",
    "n_B" : "L",
    "n_E" : "L",
    "n_I" : "L",
    "n_S" : "L",
    "ow_B" : "O",
    "ow_E" : "O",
    "ow_I" : "O",
    "ow_S" : "O",
    "aa_B" : "AI",
    "aa_E" : "AI",
    "aa_I" : "AI",
    "aa_S" : "AI",
    "th_B" : "L",
    "th_E" : "L",
    "th_I" : "L",
    "th_S" : "L",
    "p_B" : "MBP",
    "p_E" : "MBP",
    "p_I" : "MBP",
    "p_S" : "MBP",
    "oy_B" : "O",
    "oy_E" : "O",
    "oy_I" : "O",
    "oy_S" : "O",
    "r_B" : "etc",
    "r_E" : "etc",
    "r_I" : "etc",
    "r_S" : "etc",
    "uh_B" : "E",
    "uh_E" : "E",
    "uh_I" : "E",
    "uh_S" : "E",
    "ae_B" : "AI",
    "ae_E" : "AI",
    "ae_I" : "AI",
    "ae_S" : "AI",
    "s_B" : "etc",
    "s_E" : "etc",
    "s_I" : "etc",
    "s_S" : "etc",
    "t_B" : "etc",
    "t_E" : "etc",
    "t_I" : "etc",
    "t_S" : "etc",
    "ah_B" : "AI",
    "ah_E" : "AI",
    "ah_I" : "AI",
    "ah_S" : "AI",
    "v_B" : "FV",
    "v_E" : "FV",
    "v_I" : "FV",
    "v_S" : "FV",
    "w_B" : "WQ",
    "w_E" : "WQ",
    "w_I" : "WQ",
    "w_S" : "WQ",
    "y_B" : "E",
    "y_E" : "E",
    "y_I" : "E",
    "y_S" : "E",
    "z_B" : "etc",
    "z_E" : "etc",
    "z_I" : "etc",
    "z_S" : "etc",
    "ch_B" : "U",
    "ch_E" : "U",
    "ch_I" : "U",
    "ch_S" : "U",
    "ao_B" : "AI",
    "ao_E" : "AI",
    "ao_I" : "AI",
    "ao_S" : "AI",
    "dh_B" : "etc",
    "dh_E" : "etc",
    "dh_I" : "etc",
    "dh_S" : "etc",
    "uw_B" : "WQ",
    "uw_E" : "WQ",
    "uw_I" : "WQ",
    "uw_S" : "WQ",
    "zh_B" : "etc",
    "zh_E" : "etc",
    "zh_I" : "etc",
    "zh_S" : "etc",
    "eh_B" : "E",
    "eh_E" : "E",
    "eh_I" : "E",
    "eh_S" : "E",
    "aw_B" : "O",
    "aw_E" : "O",
    "aw_I" : "O",
    "aw_S" : "O",
    "ax_B" : "etc",
    "ax_E" : "etc",
    "ax_I" : "etc",
    "ax_S" : "etc",
    "el_B" : "L",
    "el_E" : "L",
    "el_I" : "L",
    "el_S" : "L",
    "ay_B" : "AI",
    "ay_E" : "AI",
    "ay_I" : "AI",
    "ay_S" : "AI",
    "en_B" : "etc",
    "en_E" : "etc",
    "en_I" : "etc",
    "en_S" : "etc",
    "hh_B" : "etc",
    "hh_E" : "etc",
    "hh_I" : "etc",
    "hh_S" : "etc",
    "er_B" : "E",
    "er_E" : "E",
    "er_I" : "E",
    "er_S" : "E",
    "ih_B" : "AI",
    "ih_E" : "AI",
    "ih_I" : "AI",
    "ih_S" : "AI",
    "jh_B" : "etc",
    "jh_E" : "etc",
    "jh_I" : "etc",
    "Jh_S" : "etc",
    "ey_B" : "E",
    "ey_E" : "E",
    "ey_I" : "E",
    "ey_S" : "E",
    "ng_B" : "etc",
    "ng_E" : "etc",
    "ng_I" : "etc",
    "ng_S" : "etc",
    "oov_S" : "rest"
}

# Taking input from user i.e: the file contain's only name
user_inp = input("Hello Sir, wish you a happy day \nPlease enter the filename without (.json): \n")

# open the json file 
with open(user_inp+".json", "r") as file:
    
    # Load Json into a variable
    my_inp = json.load(file)
    
    # print some successful message 
    print("your file is loaded successfully \nWe are working on it")
    
    # Let's find the list of words from this json
    words = my_inp["words"]
    
    # find the first iteration from words dict to get the name
    first_dict = words[0]
    
    # find the word that will apear at the first line of our .dat file
    name = first_dict["word"]
        
        
    # now let's open a txt file with same filename that can stores the info temporarily
    with open(user_inp+".txt", "w") as txt:
        """"
        In this text file we will write the data that we need in .dat file
        this file is worked as a temporary storage
        we will convert this txt file to dat file below once done with writing
        """
        
        # first entry should be the name of very first dictionay of words in dat file
        txt.write(name)
        
        # a space and new line
        txt.write(" \n")
        
        # a temprary storage variable we will use later in this code
        temp = 0
        
        # loop through the words list to find out phone and duration
        for itr in words:
            
            # finding the start for each dict to multiply this vith duration and then write to file
            # round function will automatically round the number in this cases
            start = round(itr["start"]*24)
            
            # Now loop through this phones dictionaries and store the data into opened file
            for phn in itr["phones"]:
          
                # store the value of duration in a variable by multiplying 24
                duration = round(phn["duration"]*24)
                
                # update the start
                start = start+duration
                
                # write duration as string into file
                txt.write(str(start))
                
                # write a space
                txt.write(" ")
                
                # find the phone name by checking the conversion dictionary
                sample = conversion[phn["phone"]]
                
                # write this converted name into file
                txt.write(sample)

                # then go to next line after each iteration
                txt.write("\n")
                
        # close the txt file once found all the iterations
        txt.close()
        
        # print out a message
        print("We have done with finding phones and durations\n")
    
    # now close the json file from where the data is being searched
    file.close()

# load the txt file
my_txt = pd.read_csv(user_inp+".txt", delimiter="\t", header=None)

# convert this into .dat file
my_txt.to_csv(user_inp+".dat", header=None, index=None, sep='|')

print(f"Please check the directory you have a file with name {user_inp}.dat\n")


# In[ ]:





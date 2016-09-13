#author chee,stbf
#version 1.0
#Python 3.4
#written for zhaw

'''
<module documentation>
'''

import os
import sys
#---------
from IO import prefile_analyzer
from IO import word_catcher
from utils import progressbar
from utils import logger

def filterOutCorrectFiles(directory,extens=".txt",encoding="UTF-8"):
    '''
    Filters out files with the .txt extension.
    '''
    files = []
    for name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, name)):
            if(prefile_analyzer.isFileInOrder(os.path.join(directory, name))[0]):
                if(extens in name):
                    files.append(name)
    return files


def import_directory(directory,startindex=-1,endWord = "#End",sep=";",extens=".txt"):
    '''
    Imports words from all files in directory
    '''
    files = filterOutCorrectFiles(directory)
    print("Found ",len(files)," files to import")
    rootWordList = import_words(directory+"\\"+files[0])
    for i in range(1,len(files)):
        rootWordList.extend(import_words(str(directory+"\\"+files[i]),startindex,endWord,sep))
    return rootWordList
    

def import_words(filename,startindex = -1,endWord = "#END",sep=";",extens=".txt",ignorfstate=False):
    '''
    Imports words from file
    First checks if file is in Order
    Then it checks line for line if it
    has the right pattern
    '''
    words = []
    logger.writeToLog(filename,status="[file]")
    if(ignorfstate==False):
        report = prefile_analyzer.isFileInOrder(filename)
    else:report = [True,""]
    #If is dir
    if(os.path.isdir(filename)):
        return import_directory(filename,startindex,endWord,sep,extens)
    #if is file
    if(report[0]):
        count = 1
        with open(filename, "r",encoding='utf-8-sig', errors='ignore') as file:
            for line in file:
                if(count>startindex):
                    line = line.strip()
                    if(line.lower() == endWord.lower()):break
                    if(sep in line):
                        #Also has phonetic
                        logger.writeToLog("Found Phonetics")
                        #   --  Should be substring --
                        word = line[0:line.index(sep)]
                        word = word.lower()
                        phonetic = line[line.index(sep):len(line)]
                        if("," in word):
                            wordt = word.split(",")
                            w = ""
                            for i in wordt:
                                if(word_catcher.isGermanWord(str(i.strip()))[0]==True):
                                    w+=i
                            words.append([w,phonetic])
                        else:
                            ret = word_catcher.isGermanWord(str(word))
                            if(ret[0]==True):words.append([word,phonetic])
                    else:
                        #normal import
                        line = line.lower()
                        if("," in line):
                            worte = line.split(",")
                            wt = ""
                            for i in worte:
                                if(word_catcher.isGermanWord(str(i))[0]):
                                    wt+= i + ","
                            words.append(wt[:-1])
                        else:
                            ret = word_catcher.isGermanWord(str(line))
                            if(ret[0]==True):words.append(line)
                            else:
                                try:
                                    logger.writeToLog(str(count) +"{"+str(line)+"}" + str(ret[1]),status="[Line]>")
                                except:
                                    logger.writeToLog("Could not log line "+str(count))
                count+=1
    else:
        logger.writeToLog(report)
    print("imported ", len(words)," from file [",filename,"]")
    return words

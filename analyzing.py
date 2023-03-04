import random
'''
    Class for an Analyze object.
    This object analyzes a song to gather all of the necessary words (a noun, verb, adjective from the song as well as 
    a word describing the song's key) required by the spotify.py.
    Additionally, percentages of the happy, sad, and angry words in the song are collected. (Used in spotify.py)
'''
class Analyze:

    # class attributes:

    # used for file names
    song_choice = ""
    file_name_for_key_words = ""

    # array of all of the lyrics in the song_choice file
    lyric_array = []

    # percentages of the various emotions in the song (song in song_choice file)
    percent_sad = 0
    percent_happy = 0
    percent_angry = 0

    # verb, noun, and adjective found in the song
    verb = ""
    adjective = ""
    noun = ""

    # string describing the key of the song
    key_string = ""

    # array containing words found in the song that have the respective emotion
    sad_words_in_song = []
    happy_words_in_song = []
    angry_words_in_song = []

    # initialize object
    def __init__(self, songchoice):
        self.song_choice = songchoice       # set song choice to string passed in from user
        self.setup_lyric_array()            # call function to setup the lyric array
        self.begin_analysis()               # analyze the song which sets all of the class attributes

    # puts song lyrics in an array, lyric_array
    def setup_lyric_array(self):
        file_loc = "songlyrics/" + self.song_choice             # get location of file
        music_file = open(file_loc, "r")                        # open the file

        # music_data is a list containing each line in the file as a list item
        music_data = music_file.readlines()                     # read lines into music_data.

        # go through each line in music_data
        for line in music_data:
            # split the line by the space bars
            words_on_line = line.split(" ")

            # go through each word on the line
            for word in words_on_line:
                word = word.lower()               # lower the word - provide consistency when comparing strings

                # remove any punctuation or spaces so only the word itself is added to the lyric array
                if (word.endswith("\n")):
                    self.lyric_array.append(word.removesuffix("\n"))
                elif(word.endswith(",")):
                    self.lyric_array.append(word.removesuffix(","))
                elif (word.endswith("!")):
                    self.lyric_array.append(word.removesuffix("!"))
                elif (word.endswith("?")):
                    self.lyric_array.append(word.removesuffix("?"))
                elif (word.endswith(".")):
                    self.lyric_array.append(word.removesuffix("."))
                elif ((word.__contains__("\""))):
                    self.lyric_array.append(word.replace("\"", ""))
                else:
                    self.lyric_array.append(word)

        music_file.close()          # close the file - done reading

    # Sets all of the percent (of the various emotions) and word (key string, verb, noun, adjective) class
    # attributes
    # Notes:
    # Calls helpers to get the sad, happy, and angry percents.
    # Calls helper to set the class words (key string, verb, noun, and adjective)
    def begin_analysis(self):

        # sets up sad percent, happy percent, and angry percent
        self.emotion("sadwords")
        self.emotion("happywords")
        self.emotion("angrywords")

        # calls helper to set respective class attribute (file_name_for_key_words) to the name of the file
        # containing words describing the key of the song
        self.set_key_file_name()

        # calls set class words
        self.set_class_words()

    # sets the class words (key string, verb, noun, and adjective)
    def set_class_words(self):

        # grab a word/phrase (randomly) that describes the song's key
        random_num = int(random.random() * len(self.file_name_for_key_words))

        file_loc = "tempoinfo/" + self.file_name_for_key_words
        key_file = open(file_loc, "r")
        content = key_file.readlines()
        self.key_string = content[random_num]
        key_file.close()

        #find a random verb in song
        self.verb = self.findword("adj,noun.verb/verbs")

        # find a random adjective in song
        self.adjective = self.findword("adj,noun.verb/adjectives")

        # find a random noun in song
        self.noun = self.findword("adj,noun.verb/nouns")

    # find percent of words (corresponding to one emotion - either happy,sad, or mad) in lyrics
    def emotion(self, file_name):
        # create array for emotion words
        emotion_words_array = []

        # get location of file
        file_loc = "emotionwords/" + file_name

        # open emotion words file
        swords = open(file_loc, "r")

        # put the words in an array
        for line in swords:
            emotion_words_array.append(line.replace("\n", ""))

        # get total number of words in song
        total_words = len(self.lyric_array)

        num_emotion = 0     # used to keep track of number of words in song associated with the given emotion

        # go through lyrics looking for the respective emotion words
        for index in range(len(self.lyric_array)):

            word = self.lyric_array[index]

            # try to find word (from lyrics) in emotion word array. if so, increment num_emotion counter
            try:
                num_emotion += 1
                emotion_words_array.index(word)
                self.sad_words_in_song.append(word)
            except Exception:
                num_emotion -= 1

        # set the percent of emotion words in song
        if file_name == "sadwords":
            self.percent_sad = float(num_emotion / total_words) * 100
        elif file_name == "angrywords":
            self.percent_angry = float(num_emotion / total_words) * 100
        else:
            self.percent_happy = float(num_emotion / total_words) * 100

    # return the filename listing words that describe the key of the song

    # sets the class attribute, file_name_for_key_words with the location of the file containing key words
    def set_key_file_name(self):

        # get name of file for specific song containing the key
        keyfile = self.song_choice + "beats"

        # get key and node of song
        file_loc = "songbeats/" + keyfile       # location of file containing key information
        music_file = open(file_loc, "r")        # open file
        key = music_file.readline().removesuffix("\n")      # get key
        node = music_file.readline().removesuffix("\n")     # get node
        music_file.close()                      # close file
        self.file_name_for_key_words = str(key) + str(node)     # set class attribute

    # Find a word from the filename (either file of adjectives, nouns, or verbs) that is also found in the lyrics
    def findword(self, filename):
        word_type = []
        possiblewords = []

        # open file and put words from filename in array, word_type
        # EX: could be putting verbs or nouns or adjectives in array word_type
        word_file = open(filename, "r")
        for line in word_file:
            word_type.append(line.replace("\n", ""))
        word_file.close()               # close file
        file_loc = "songlyrics/" + self.song_choice

        print("all possible " + filename)
        # traverse over array word_type
        for word in word_type:
            # if the word can be found in the lyrics of the song, add the word to the possible_words array
            if word in open(file_loc).read():
                print(word)
                possiblewords.append(word.lower())

        # if no words of word type were found in the lyrics, then raise exception
        if len(possiblewords) == 0:
            raise Exception("No word type ( from " + filename + ") in lyrics")
        return possiblewords[int(random.random() * len(possiblewords))].removeprefix(" ")
import random
from graphics import *
from pygame import mixer
from analyzing import Analyze


# function that displays the graphics for a song analysis
def musicandgraphics():

    # set up window
    window_height = 750
    window_width = 1000
    win = GraphWin('Swift Analysis', window_width, window_height)
    win.setBackground("springgreen")

    # plays song
    mixer.init()
    mixer.music.load("songmp3/readyforit.mp3")
    mixer.music.play()

    message_location = window_height/(100/7)        # used for location of text
    message_inc_val = window_height/(100/7)         # used to adjust location of text

    # save colors based on emotion
    sad_color = "midnightblue"
    angry_color = "crimson"
    happy_color = "magenta"

    # array to keep track of text throughout the program
    messages_array = []

    initial_texts = ['Hello! We are going to analyze a Taylor Swift Song',
                     'Here are your options (please type exactly as you see <3)',
                     'Please click the screen when done', '1.champagne problems   2.mad woman   3.mirrorball',
                     '4.bad blood   5.better than revenge   6.picture to burn',
                     '7.bejeweled   8.lavender haze   9.fearless   10.lover ']

    size_message_text = int(window_height / 30)     # size of message text

    # set up message, instructions, and options
    for index in range(len(initial_texts)):
        text = initial_texts[index]
        message = Text(Point(window_width / 2, message_location), text)
        message_location += message_inc_val  # adjust location for next text
        messages_array.append(message)

        if index == 3:
            message.setTextColor("yellow")
        elif index == 4:
            message.setTextColor("blueviolet")
        elif index == 5:
            message.setTextColor("magenta")
        else:
            message.setTextColor("orange")
        message.setStyle("bold")
        message.setSize(size_message_text)
        message.draw(win)

    # set up user input box
    text_entry = Entry(Point(window_width/2, window_height/2), 100)
    text_entry.draw(win)
    messages_array.append(text_entry)

    # wait for mouse to move on before proceeding
    win.getMouse()

    # stop playing music
    mixer.stop()

    # call analyze using user input
    val = text_entry.getText()
    try:
        val = val.replace(" ", "").lower()
        song_analysis = Analyze(val)
    except Exception:
        # if there is an exception - there was an invalid input from the user
        # tell the user and then re-run the program
        for message in messages_array:
            message.undraw()
        final_message = Text(Point(window_width/2, window_height/2), 'Invalid Input : Will re-run program in just a moment')
        final_message.setSize(30)
        final_message.setTextColor("black")
        final_message.draw(win)
        time.sleep(3)
        win.close()
        mixer.stop()
        musicandgraphics()
        exit()

    color_for_rest = ""
    colorforsentences_page2 = ""

    # set colors for the remaining texts and background based off of percentages and/or key
    # this is explained more in the README
    if song_analysis.file_name_for_key_words == "bmajor":       # sad song
        color_for_rest = angry_color
        colorforsentences_page2 = "blue"
    elif song_analysis.percent_angry > 7:       # angry song
        difference_angry_sad = abs(song_analysis.percent_angry - song_analysis.percent_sad)
        if (song_analysis.percent_sad > 6) & (difference_angry_sad < 5):    # angry and sad song
            color_for_rest = "maroon"
            colorforsentences_page2 = "lightgray"
        else:           # angry song
            color_for_rest = angry_color
            colorforsentences_page2 = "blue"
    elif song_analysis.percent_sad > song_analysis.percent_happy:   # sad song
        color_for_rest = sad_color
        colorforsentences_page2 = "yellow"
    elif song_analysis.percent_happy > song_analysis.percent_sad:       # happy song
        color_for_rest = happy_color
        colorforsentences_page2 = "indigo"

    song_verb = song_analysis.verb
    song_adjective = song_analysis.adjective
    song_noun = song_analysis.noun
    song_key_word = song_analysis.key_string

    line1 = "This song will " + song_verb + " with you"
    line2 = "If this song were a person, it would be " + song_adjective
    line3 = "If this song were a thing, it would be a " + song_noun
    if song_noun.startswith("a"):
        line3 = "If this song were a thing, it would be an " + song_noun
    line4 = "Most importantly, it's giving " + song_key_word
    sentences = [line1, line2, line3, line4]

    # set numbers for adjusting text placement
    message_inc_val = window_height/10
    message_location = window_height/2 + message_inc_val

    # display the sentences created
    for sentence in sentences:
        display_line = Text(Point(win.getWidth() / 2, message_location), sentence)
        messages_array.append(display_line)
        message_location += message_inc_val
        display_line.setTextColor(color_for_rest)
        display_line.setSize(size_message_text)
        display_line.setStyle("bold")
        display_line.draw(win)

    # sleep for 5 seconds to allow user to read sentences
    time.sleep(5)
    # stop the music
    mixer.music.stop()
    # set background according to the emotion of the song
    win.setBackground(color_for_rest)

    # undraw the message and instructions and message
    for message in messages_array:
        message.undraw()

    print("angry " + str(song_analysis.percent_angry))
    print("sad " + str(song_analysis.percent_sad))
    print("happy " + str(song_analysis.percent_happy))


    # plays song (from user input)
    musictitle = val + '.mp3'
    mixer.music.load("songmp3/" + musictitle)
    mixer.music.play()


    # set x, y, and change value for the circles
    circle_size = 0.02 * window_width
    # calculations are designed to display the circles in the center of the screen
    x = 0.15 * window_width - circle_size
    change_val = (window_width-(2 * x))/15
    y = window_height/2

    # if circles would not fit in the y-direction, then adjust x and change_val
    if change_val*15 > (window_height - circle_size*6):
        change_val = (window_height - (6 * circle_size)) / 15
        x = (window_width - 15 * change_val) / 2 - circle_size

    # array to keep track of circle - later change the color of circles
    circles = []

    color_for_circles = color_rgb(100, 75, 200)         # initial color for circles

    # circles appear from middle left to middle bottom to middle right to top middle to middle left
    for counter in range(32):
        # create circle, set color, draw, add to list...
        if counter < 8:         # middle left to middle bottom
            circle1 = Circle(Point(x, y), circle_size)
            x += change_val
            y += change_val
        elif counter < 16:      # middle bottom to middle right
            circle1 = Circle(Point(x, y), circle_size)
            x += change_val
            y -= change_val
        elif counter < 25:      # middle right to top middle
            circle1 = Circle(Point(x, y), circle_size)
            x -= change_val
            y -= change_val
        else:                   # top middle to middle left
            if counter == 25:
                y += change_val * 2
            circle1 = Circle(Point(x, y), circle_size)
            x -= change_val
            y += change_val
        circle1.setFill(color_for_circles)
        circle1.setOutline("white")
        circle1.draw(win)
        circles.append(circle1)
        counter += 1

    messages_array.clear()

    # size of the small text in the top of the diamond
    message_size = int(win.getWidth()/110)
    # small text in the top of the diamond
    top_diamond_words = ['Are you ready for it?', '(TS Reference lol)']

    # display text on graphics
    for i in range(2):
        words = top_diamond_words[i]
        if i == 0:
            y = window_height/2 - message_inc_val*3.25
        else:
            y = window_height/2 - message_inc_val*3
        message = Text(Point(window_width/2, y), words)
        message.setTextColor("white")
        message.setStyle("bold")
        message.setSize(message_size)
        message.draw(win)

    # used for location of sentences (contain verb, noun, adjective, key word)
    difference_from_x_edge = window_width / 4
    difference_from_y_edge = 0.05 * window_height

    message_size = int(message_size * 1.2)

    # display the sentences in the four corners of the window
    for i in range(4):
        if i == 0:           # first sentence - verb
            sentence = Text(Point(difference_from_x_edge, difference_from_y_edge), line1)
        elif i == 1:        # second sentence - adjective
            sentence = Text(Point(difference_from_x_edge, window_height - difference_from_y_edge), line2)
        elif i == 2:        # third sentence - noun
            sentence = Text(Point(window_width - difference_from_x_edge, difference_from_y_edge), line3)
        else:       # fourth sentence - goofy (from key)
            sentence = Text(Point(window_width - difference_from_x_edge, window_height - difference_from_y_edge), line4)
        sentence.setTextColor(colorforsentences_page2)
        sentence.setSize(message_size)
        sentence.setStyle("bold")
        sentence.draw(win)

    # array of colors
    colors = ["yellow", "blue", "indigo", "midnightblue", "crimson", "magenta", "red", "lime", "hotpink",
              "plum", "orangered", "seagreen", "teal", "aqua", "blueviolet", "white", "maroon"]
    colors.remove(color_for_rest)     # remove the background color from the array

    # get correct image
    image_title = "songgifs/" + val + ".gif"

    # change the circles (in order - left to right, right to left..) color (to a random color)
    for counter in range(14):
        # select a random color to change circles to
        ran = int(random.random()*len(colors))
        color = colors[ran]

        # remove color from colors so it cannot be repeated
        colors.remove(color)

        # change all of the circles to that color
        for c in circles:
            c.setFill(color)
            time.sleep(0.05)        # so user can actually see the change
            if counter == 5:         # once counter gets to five, display image
                my_image = Image(Point(window_width/2, window_height/2), image_title)
                my_image.draw(win)
        time.sleep(0.3)  # wait for 0.3 seconds until loop again

    # display exit message
    exitmessage = Text(Point(window_width/2, window_height/2 + message_inc_val*2.3), 'Please press any key to exit')
    exitmessage.setTextColor("lime")
    exitmessage.setStyle("bold")
    exitmessage.setSize(int(message_size*1.2))
    exitmessage.draw(win)

    # wait for a key from usr
    win.getKey()
    # stop the music
    mixer.music.stop()
    # close the window
    win.close()


musicandgraphics()

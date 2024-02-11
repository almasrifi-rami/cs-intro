# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import re
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description,
                 link, pubdate):
        """
        Class containing information about a news story

        Arguments:
            guid (str) -- string denoting a globally unique identifier of the story
            title (str) -- string denoting the title of the story
            description (str) -- string describing the story
            link (str) -- web link to the story
            pubdate (datetime) -- the date of publishing the story

        Returns:
            None
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        # setting the timezone to EST for comparison later on
        self.pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))

    def get_guid(self):
        """
        method for accessing guid of story

        Returns:
            str -- GUID of the story
        """
        return self.guid
    
    def get_title(self):
        """
        method for accessing the title of the story

        Returns:
            str -- title of the story
        """
        return self.title
    
    def get_description(self):
        """
        method for accessing the story description

        Returns:
            str -- description of the story
        """
        return self.description
    
    def get_link(self):
        """
        method for accessing the link to the story

        Returns:
            str -- link to the website of the story
        """
        return self.link
    
    def get_pubdate(self):
        """
        method for accessing the publication date of the story

        Returns:
            datetime -- date of the publication of the story
        """
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        a phrase trigger based on Trigger class

        Arguments:
            phrase (str) -- phrase to trigger when encountered

        Returns:
            None
        """
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        """
        take in a string phrase as an argument and returns True if 
        the whole phrase is present in text and False otherwise
        """
        # regular expression pattern that matches any non-letter character
        pattern = r"[^\w']"
        # split the text to get all available words
        word_list = re.split(pattern, text)
        # make sure all words are lower case
        word_list = [word.lower() for word in word_list if word != '']
        
        # split the phrase in case it has multiple words
        phrase_list = re.split(pattern, self.phrase)
        phrase_list = [word for word in phrase_list if word != '']

        # use try and except in case any errors happen
        # ValueError when word_list.index() doesn't find the word in the list
        # IndexError for when the later words in trigger are before the first word
        try:
            # check for the first word from phrase in the word list
            idx = word_list.index(phrase_list[0])
            # loop over all the words in the phrase after the first
            for i, word in enumerate(phrase_list[1: ]):
                # check if each of these word are following the first (in the same order)
                if word_list[idx + i + 1] == word:
                    continue
                # if not return False
                else:
                    return False
            # if the loop is executed properly return True
            return True
        # if any word is not found then the function will return False
        # or their order is incorrect return False
        except:
            return False
        
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return super().evaluate(story)


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        a subclass of PhraseTrigger that will trigger if the phrase
        is in the title of the news story

        Arguments:
            phrase (str) -- string denoting the trigger phrase 
        """
        super().__init__(phrase)

    def is_phrase_in(self, text):
        return super().is_phrase_in(text)
    
    def evaluate(self, story):
        text = story.get_title()
        return self.is_phrase_in(text)

    
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        a subclass of PhraseTrigger that will trigger if the phrase
        is in the description of the news story

        Arguments:
            phrase (str) -- string denoting the trigger phrase 
        """
        super().__init__(phrase)

    def is_phrase_in(self, text):
        return super().is_phrase_in(text)
    
    def evaluate(self, story):
        text = story.get_description()
        return self.is_phrase_in(text)
    

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        """
        A trigger class based on the publication date and time of a news story

        Arguments:
            time (str) -- string of datetime in EST with format "3 Oct 2016 17:00:10"
        
        Returns:
            None
        """
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S") \
                            .replace(tzinfo=pytz.timezone("EST"))

    def evaluate(self, story):
        return super().evaluate(story)
    

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        """
        Trigger class that will trigger for news stories published before a certain datetime
        """
        super().__init__(time)

    def evaluate(self, story):
        pubdate = story.get_pubdate()
        return pubdate < self.time
    
class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        """
        Trigger class that will trigger for news stories published after a certain datetime
        """
        super().__init__(time)

    def evaluate(self, story):
        pubdate = story.get_pubdate()
        return pubdate > self.time

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, Trigger):
        """
        A trigger class that returns the opposite evaluation of the trigger it is given
        """
        self.Trigger = Trigger

    def evaluate(self, story):
        return not self.Trigger.evaluate(story)
    
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, Trigger_1, Trigger_2):
        """
        A trigger class that takes two triggers and evaluates to 
        True if both triggers evaluate to True else False
        """
        self.Trigger_1 = Trigger_1
        self.Trigger_2 = Trigger_2

    def evaluate(self, story):
        return (self.Trigger_1.evaluate(story) and self.Trigger_2.evaluate(story))
    
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, Trigger_1, Trigger_2):
        """
        A trigger class that takes two triggers and evaluates to True
        if any of the triggers evaluate to True
        """
        self.Trigger_1 = Trigger_1
        self.Trigger_2 = Trigger_2

    def evaluate(self, story):
        return (self.Trigger_1.evaluate(story) or self.Trigger_2.evaluate(story))
    

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    # initiate a list to store relevant stories
    relevant_stories = []

    # loop over all stories and check whether any trigger fires for them
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                # append the story to the list
                relevant_stories.append(story)

    return relevant_stories




#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    # adding a mapping to the trigger types and their classes
    trigger_types = {
        'TITLE': TitleTrigger,
        'DESCRIPTION': DescriptionTrigger,
        'AFTER': AfterTrigger,
        'BEFORE': BeforeTrigger,
        'NOT': NotTrigger,
        'AND': AndTrigger,
        'OR': OrTrigger
    }
    # defining two groups of triggers
    # group1 takes a phrase or time as an argument
    # group2 takes two triggers as an argument
    trigger_group_1 = ['TITLE', 'DESCRIPTION', 'AFTER', 'BEFORE']

    # initiate a trigger map to store all triggers,
    # and list to store only triggers to use
    triggers_map = {}
    triggers_list = []

    # loop over the lines and split the keywords
    for line in lines:
        kws = line.split(',')
        # check second word
        # if it is a trigger type (then the line doesn't start with "ADD")
        # add the trigger to the map based on its type
        if kws[1] in trigger_group_1:
            triggers_map[kws[0]] = trigger_types[kws[1]](kws[2])
        elif kws[1] == 'NOT':
            triggers_map[kws[0]] = trigger_types[kws[1]](
                triggers_map.get(kws[2])
            )
        elif kws[1] in ['AND', 'OR']:
            triggers_map[kws[0]] = trigger_types[kws[1]](
                triggers_map.get(kws[2]),
                triggers_map.get(kws[3])
            )
        # if the line starts with "ADD"
        # find the triggers from the map
        if kws[0] == 'ADD':
            for trigger in kws[1: ]:
                triggers_list.append(triggers_map.get(trigger))
        
    return triggers_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Trump")
        t2 = DescriptionTrigger("Russia")
        t3 = DescriptionTrigger("Ukraine")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('src/ps5/triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories in RSS news feed of Yahoo do not contain a description
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


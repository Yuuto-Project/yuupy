import markovify


# https://github.com/jsvine/markovify
class CampBuddyMakov(markovify.Text):
    def sentence_split(self, text):
        # simpler split case that fits our needs
        return text.strip().split('\n')

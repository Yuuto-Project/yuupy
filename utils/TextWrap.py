# This code is kindly stolen from StackOverlow. 
# Parts of it have been updated to better suit our needs
# https://stackoverflow.com/a/49719319

from PIL import ImageFont, ImageDraw, Image

class TextWrapper(object):
    """ Helper class to wrap text in lines, based on given text, font and max allowed line width."""

    def __init__(self, text, font, max_width):
        self.text = text
        self.text_lines = [
            ' '.join([w.strip() for w in l.split(' ') if w])
            for l in text.split('\n')
            if l
        ]
        self.font = font
        self.max_width = max_width

        self.draw = ImageDraw.Draw(
            Image.new(
                mode='RGB',
                size=(100, 100)
            )
        )

        self.space_width = self.draw.textsize(
            text=' ',
            font=self.font
        )[0]

    def get_text_width(self, text):
        return self.draw.textsize(
            text=text,
            font=self.font
        )[0]

    def wrapped_text(self):
        wrapped_lines = []
        buf = []
        buf_width = 0

        for line in self.text_lines:
            # Go through every word in the text (seperated by ' ')
            for word in line.split(' '):
                word_width = self.get_text_width(word)

                # Determine the expected width of the text with the next word added to it
                if not buf:
                    # If this is the first word, simply add the word itself
                    expected_width = word_width 
                else:
                    # Not the first word, add to existing lenght, including the length of the space
                    expected_width = buf_width + self.space_width + word_width

                if expected_width <= self.max_width:
                    # Word fits in line
                    buf_width = expected_width
                    buf.append(word)
                else:
                    # Word doesn't fit in line
                    if buf:
                        # Append line to the output array
                        wrapped_lines.append(' '.join(buf))
                    
                    # Clear buffer array and buffer width
                    buf = [word]
                    buf_width = word_width

            # If there is any leftower, add it to the output array and cler the buffer
            if buf:
                wrapped_lines.append(' '.join(buf))
                buf = []
                buf_width = 0

        return '\n'.join(wrapped_lines)
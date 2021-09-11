from collections.abc import Sequence
import re


def get_emoji_list(ctx):
    emojis = {}
    for emoji in ctx.guild.emojis:
        emojis[emoji.name]=emoji.id
    return emojis

def get_formated_emoji(emoji, emoji_list):
    formatted_emoji = ""
    print(str(emoji_list))
    try:
        emoji_id = emoji_list[emoji]
        formatted_emoji = "<{name}:{id}>".format(name=emoji, id=emoji_id)
    except:
        print("Exception!!")
    finally:
        return formatted_emoji

def extract_emoji(formatted_emoji):
    EMOJI_REGEX = "^<:(.*):[0-9]+>$"
    match = re.search(EMOJI_REGEX, formatted_emoji)
    return match.group(1)


def list_to_str(list):
    final_string = ""
    for item in list:
        final_string += item + "\n"
    return final_string

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)

    def check(message):
        if message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content
        if content and actual_content not in content:
            return False
        return True
    return check

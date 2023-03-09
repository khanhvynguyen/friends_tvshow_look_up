import os
import re
from typing import List


def read_file(path: str) -> List[str]:
    """

    :param path: e.g., "datasets/season1/episode1.srt"
    :return:  ["CAR HORNS HONKING",
            "There's nothing to tell. It's just some guy I work with.", ....]
    """
    # Open the file in read mode
    with open(path, 'r', encoding="latin-1") as file:
        # Read the contents of the file
        content = file.read()

    # Print the contents of the file
    content = content.split("\n\n")  # split content into paragraphs
    content = [x[2:] for x in content]  # remove the first number in each
    pattern = r'(?<=[a-zA-Z,])\n'  # combine into a sentence if not been a sentence yet
    for i in range(len(content)):
        content[i] = re.sub(pattern, ' ', content[i])

    return content


def process_text(text: str):
    clean_text = text.lower()
    remove_characters = [",", "?", "!", ".", "-", "_"]  # remove these from the text
    replacements = {
        "don't": "do not",
        "I'd": "I would",
        "we'd": "we would",
        "it's": "it is",
        "'ve": "have",
        "there's": "there is",
        "we're": "we were",
        "i'm": "i am",
        "won't": "will not",
        "can't": "cannot",
        "'s": " is",
        "how's it going": "how is it going",
        "'re": " are",
        "how you doin": "how you doing",
        "how're you doin": "how are you doing"
    }
    for contraction, expanded in replacements.items():
        clean_text = clean_text.replace(contraction, expanded)

    for c in remove_characters:
        clean_text = clean_text.replace(c, "")
    return clean_text


def find_text_in_file(query: str, text_file: List[str]) -> str:
    query = process_text(query)
    for text in text_file:
        text = process_text(text)  # e.g., i don't want her to go through what i went through with carl.
        if query in text:
            return True
    return False


def get_all_file_paths(folder_path: str) -> List[str]:
    """

    :param folder_path: "datasets"
    :return: ["datasets/season1/friends.s01e01.720p.bluray.x264--sujaidr.srt",
            "datasets/season1/friends.s01e02.720p.bluray.x264--sujaidr.srt",
            ....
            "datasets/season2/friends.s02e01.720p.bluray.x264--sujaidr.srt",
            ...
            "datasets/season10/friends.s10e01.720p.bluray.x264--sujaidr.srt"]
    """

    file_path_list = []
    # Walk through the folder and its subdirectories using os.walk()
    for root, dirs, files in os.walk(folder_path):
        # Iterate through all files in the current directory
        for filename in files:
            # Join the root path and filename to get the full file path
            file_path = os.path.join(root, filename)
            # if ".srt" in file_path:
            file_path_list.append(file_path)
    return file_path_list

if __name__ == '__main__':
    content = read_file("datasets/Season_1/Friends - [1x03] - The One with the Thumb.srt")
    print(content)
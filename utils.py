import os
import re
from typing import List


def read_file_srt(path: str) -> List[str]:
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
    res = []
    for i in range(len(content)):
        tmp = re.sub(pattern, ' ', content[i]).split("\n")

        if len(tmp) >= 2:
            if len(tmp[0]) < 5:
                del tmp[0]
            time, *text_content = tmp
            text_content = " ".join(text_content)
            if "-->" in time:
                time_start, time_end = time.split("-->")
                hour_min_sec_start, mil_sec_start = time_start.split(",")
                h, min_start, sec = hour_min_sec_start.split(":")
            elif "," in time:
                time_start, time_end = time.split(",")
                hour_min_sec_start, mil_sec_start = time_start.split(".")
                h, min_start, sec = hour_min_sec_start.split(":")
            else:
                continue
            text_content = re.sub(r"(^')|('$)|(^\")|(\"$)", "", text_content)
            text = f"{min_start}m:{sec}s, {text_content}"
            res.append(text)
    return res


def read_file_sub(path: str) -> List[str]:
    """
        :param path: e.g., "datasets/season2/episode6.sub"
        :return:  ["CAR HORNS HONKING",
                "There's nothing to tell. It's just some guy I work with.", ....]
        """
    # Open the file in read mode
    with open(path, 'r', encoding="latin-1") as file:
        # Read the contents of the file
        lines = file.readlines()

    # Print the contents of the file
    frames_per_sec = 25  # assume 25 frames per second
    res = []
    for line in lines:  # e.g of line: {1}{45}Ripped with SubRip 1.17 and Verified by CdinT|cdint@hotmail.com
        # format of sub file: https://clideo.com/resources/subtitle-file-formats-overview
        line = re.sub(r'[{\n|\"]', '', line)
        try:
            frame_start, frame_end, *content = line.split("}")
            sec_start, sec_end = int(frame_start) // frames_per_sec, int(frame_end) // frames_per_sec
            min_start = sec_start // 60
            sec = sec_start % 60
            content = " ".join(content)
            content = re.sub(r"(^')|('$)|(^\")|(\"$)", "", content)
            text = f"{min_start}m:{sec}s, {content}"
            res.append(text)
        except:
            print(line)
            continue
    return res


def read_file(path: str):
    if path.endswith(".sub"):
        return read_file_sub(path)
    elif path.endswith(".srt"):
        return read_file_srt(path)
    else:
        NotImplementedError()


def process_text(text: str):
    clean_text = text.lower()
    remove_characters = [",", "?", "!", ".", "-", "_", "[", "]", " "]  # remove these from the text
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
    clean_query = process_text(query)
    for raw_text in text_file:
        clean_text = process_text(raw_text)  # e.g., i don't want her to go through what i went through with carl.
        if clean_query in clean_text:
            return raw_text
    return ""


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
            if file_path.endswith(".srt") or file_path.endswith(".sub"):
                file_path_list.append(file_path)
    return file_path_list


if __name__ == '__main__':
    my_string = "'maybe it was' justreally clear that day.'"
    new_string = re.sub(r"(^')|('$)", "", my_string)
    print(new_string)

    ## BUG: test with "really white" failed.

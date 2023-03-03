import os
import re
from typing import List

import streamlit as st
import pandas as pd


def read_file(path: str) -> List[str]:
    """

    :param path: e.g., "datasets/season1/episode1.srt"
    :return:  ["CAR HORNS HONKING",
            "There's nothing to tell. It's just some guy I work with.", ....]
    """
    # Open the file in read mode
    with open(path, 'r', encoding='Latin-1') as file:
        # Read the contents of the file
        content = file.read()

    # Print the contents of the file
    content = re.split("^\n$", content)
    return content


def process_text(text: str):
    clean_text = text.lower()
    return clean_text


def find_text_in_file(query: str, text_file: List[str]) -> bool:
    query = process_text(query)
    for text in text_file:
        text = process_text(text)  # e.g., i don't want her to go through what i went through with carl. Oh.
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
            if ".srt" in file_path:
                file_path_list.append(file_path)
    return file_path_list


def look_up_episode(query: str) -> List[str]:
    folder_path = "datasets"
    res = []
    file_path_list = get_all_file_paths(folder_path)
    for file_path in file_path_list:
        text_file = read_file(file_path)
        is_found = find_text_in_file(query, text_file)
        if is_found:
            res.append(file_path)
    return res


st.write(
    """
    # Friends Episode Lookup
    Hello *world!*
    """
)

query = st.text_input("Enter the text to look up, for example 'really white'", "")
if query != "":
    res = look_up_episode(query)
    st.write(res)




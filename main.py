from typing import Tuple, Dict

import streamlit as st
from utils import *


def look_up_episode(query: str, folder_path: str) -> List[Dict]:
    """
    :param query:
    :param folder_path:
    :return:
    """
    searching_res = []
    file_path_list = get_all_file_paths(folder_path)
    for file_path in file_path_list:
        text_list = read_file(file_path)  # all contents in an episode
        text_found = find_text_in_file(query, text_list)
        if text_found != "":
            season, episode, clean_title = format_title(file_path)
            searching_res.append((season, episode, clean_title, text_found))

    searching_res = sorted(searching_res)
    res_list = []
    for x in searching_res:
        res = {
            "title": x[-2],
            "text_found": x[-1]
        }
        res_list.append(res)
    return res_list


def format_title(result: str) -> Tuple:
    """
    :param result: a file path
    :return: list of results, which include which season and episode
    """
    remove_left_bracket = result.replace("[", "")
    remove_right_bracket = remove_left_bracket.replace("]", "")
    split_result = remove_right_bracket.split("/")
    split_result = split_result[2].split("-")
    season, episode = split_result[1].strip().split("x")
    episode_title = split_result[-1].replace(".srt", "").replace(".en", "").replace(".sub", "")
    clean_title = f"Season {season}, Episode {episode}, Title:{episode_title}"

    return int(season), int(episode), clean_title


def run_web(folder_path: str):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.write(
        "<h2>Friends TV Show - Episode Lookup </h2>", unsafe_allow_html=True)
    st.image("img/friends_cover.jpeg", width=900)

    query = st.text_input('Enter the text to look up, for example "how\'re you doing?"', "")
    # st.selectbox("who spoke?", ["Joe", "Chandler", "Monica"], )
    if query != "":
        res_list = look_up_episode(query, folder_path)
        for res in res_list:
            st.write(
                f"""<p style="font-size:26px; color: rgb(17, 134, 145);"><i>{res["title"]}</i></p>{res["text_found"]}
                     <br> </br>
                     """,
                unsafe_allow_html=True)


if __name__ == '__main__':
    run_web(folder_path="datasets")

    # Debug
    # look_up_episode("really white", folder_path="datasets")

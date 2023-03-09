import streamlit as st
from utils import *


def look_up_episode(query: str, folder_path: str) -> List[str]:
    """

    :param query:
    :param folder_path:
    :return:
    """
    res = []
    file_path_list = get_all_file_paths(folder_path)
    for file_path in file_path_list:
        text_list = read_file(file_path)  # all contents in an episode
        found_text = find_text_in_file(query, text_list)
        if found_text != "":
            cleaned_result = format_result(file_path)
            res.append(cleaned_result + ": " +found_text)
    return res


def format_result(result: str) -> List[str]:
    """

    :param result: a file path
    :return: list of results, which include which season and episode
    """
    remove_left_bracket = result.replace("[", "")
    remove_right_bracket = remove_left_bracket.replace("]", "")
    split_result = remove_right_bracket.split("/")
    split_result = split_result[2].split("-")
    season_episode = split_result[1].strip().split("x")
    episode_title = split_result[-1].replace(".srt","").replace(".en","")
    final_result = f"Season {season_episode[0]}, Episode {season_episode[1]}, Title:{episode_title}"

    return final_result



def run_web(folder_path: str):
    st.write(
        """
        # Friends TV Show Episode Lookup
        """
    )
    st.image("img/friends_cover.jpeg", width=900)

    query = st.text_input('Enter the text to look up, for example "how\'re you doing?"', "")
    # st.selectbox("who spoke?", ["Joe", "Chandler", "Monica"], )
    if query != "":
        res = look_up_episode(query, folder_path)
        for r in res:
            st.write(r)


if __name__ == '__main__':
    run_web(folder_path="datasets")

    res = "datasets/Season_10/Friends - [10x11] - The One Where the Stripper Cries.srt"
    season_name = format_result(res)
    print(season_name)

global url
import requests
import subprocess

url = "https://api-aniwatch.onrender.com"
s = requests.Session()

def anime_search():
    title = input("Search Anime : ")
    page = 1
    anime_count = 0
    search_result = []

    result = s.get(url=f'{url}/anime/search?q={title}&page={page}')
    if result.status_code == 200:
        data = result.json()
        animes = data.get('animes', [])
        if not animes:
            print("No Anime Found with that Name. ")
            
        else:
            for anime in animes:
                anime_count += 1
                print(f"{anime_count}. Name : {anime['name']}")
                search_result.append({'Title' : anime['name'], 'ID': anime['id']})
    return search_result

def select_anime(search_results=anime_search()):
    try:
        selected_index = int(input("Select Your Anime: "))
        if 1 <= selected_index <= len(search_results):
            selected_anime  = search_results[selected_index - 1]
            anime_id = selected_anime['ID']
            return anime_id
        else:
            print("Invalid Selection.")
    except ValueError:
        print("Invalid Input. please enter a valid number. ")
    
def anime_info(anime_id = select_anime()):
    if anime_id:
        episode_url = f'{url}/anime/episodes/{anime_id}'
        result = s.get(episode_url)
        # print(result.json())
        if result.status_code == 200:
            data = result.json()
            episodes = data.get('episodes', [])
            print(f"Total Number of Episode : {data.get('totalEpisodes')}")
            print(f"Episodes for selected anime: {anime_id}: ")
            
        else:
            print("Error fetching episode data from the API. ")
    return episodes

def selected_episode(episodes = anime_info()):
    if episodes:
        for episode in episodes:
            print(f"Episode: {episode['number']} Name: {episode['title']}")
    episode_no = int(input("Choose Episode : "))
    episode_info = episodes[episode_no-1]
    
    if episode_no == int(episode_info['number']):
        # print(episode_info)
        return episode_info['episodeId']
    else:
        print("No Episode found for the selected anime. ")
        


def get_episode_link(episodeid=None,url=url):
    
    if episodeid is None:
        episodeid = selected_episode()
    category = input('What You Prefer Sub or Dub ? (sub/dub)')
    res = s.get(url=f"{url}/anime/episode-srcs?id={episodeid}&category={category}")
    
    if res.status_code == 200:
        link_data = res.json()
        links = link_data.get('sources', [])
        url = links[0]['url']
    else:
        print("Failed to retrieve episode links.")
        return None  
    
    subs = res.json().get('subtitles')
    for i, sub in enumerate(subs):
        print(f"{i + 1}. {sub['lang']}")
    
    selected_url = None
    while selected_url is None:
        try:
            selected_index = int(input("Select a subtitle language (enter the number): "))
            if 1 <= selected_index <= len(subs):
                selected_subtitle = subs[selected_index - 1]
                selected_url = selected_subtitle['url']
                print(f"Selected subtitle language: {selected_subtitle['lang']}")
                # print(f"Subtitle URL: {selected_url}")
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    return url, selected_url

def main():
    m3u8 ,subtitle_url= get_episode_link()
    mpv_command = [".\\mpv\\mpv.com", m3u8, f'--sub-file={subtitle_url}', '--fs']
    subprocess.Popen(mpv_command)
    print('Loading Playerrr....')
if __name__ == "__main__":
    main()
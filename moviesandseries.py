import requests
import html
import re
import json


class MoviesAndSeries:

    def __init__(self):
        #list of tuples
        self.list_title = list()
        self.list_episodes = list()
    
    def __str__(self):
        _str = ''
        for i, title in enumerate(self.list_title):
            _str += f'{i:>2}) '+title[0]+'\n'
        return _str[:-1]
    
    def __len__(self):
        return len(self.list_title)

    def getTitleList(self, query):
        self.list_title = list()
        query = query.lower()
        r = requests.get(f'https://altadefinizione.mx/?s={query.replace(" ", "+")}')
        content_no_css = re.sub(r'(<style[^<]+|style=(\"|\')[^\"\']+(\"|\'))', '', r.text)
        urls = re.findall(r'(https:\/\/altadefinizione\.\w+\/\w+\/[^\"]+)\"\s*data-url', content_no_css)
        titles = re.findall(f'-title">([^<]+)', content_no_css)
        # print(urls, len(titles))
        for i, title in enumerate(titles):
            if query in title.lower():
                self.list_title.append((html.unescape(title).title(), urls[i]))
        
        return self.list_title

    def getEpisodeList(self, indexTitle=0):
        if len(self.list_title) == 1:
            indexTitle = 0
        contentPageShow = self._contentFromUrl(self.list_title[indexTitle][1])
        episodeLinks = re.findall(r'https:\/\/vcrypt.pw\/akv\/\w+', contentPageShow)
        if len(episodeLinks) > 0:
            titles = [title.strip() for title in re.findall(r'<td><b>([\w\s]+)', contentPageShow)]
            self.list_episodes = list(zip(titles, episodeLinks))
        else:
            # sometimes there is not any "vcrypt.pw/akv" link
            episodeLinks = re.findall(r'https:\/\/altadefinizione.mx\/film_in_streaming\/\w+\/\w+', contentPageShow)
            if len(episodeLinks) > 0:
                # print([(self.list_title[indexTitle][0], re.sub('\/0$', '/1', episodeLinks[0]))])
                self.list_episodes = [(self.list_title[indexTitle][0], re.sub('\/0$', '/1', episodeLinks[0]))]
        return self.list_episodes
        

    def getShowUrl(self, episode_number=0):
        if int(episode_number) > (len(self.list_episodes) - 1):
            episode_number = 0
        pagePre1Episode = self._contentFromUrl(self.list_episodes[episode_number][1])
        out2Link = re.findall(r"\/out2\/\w+", pagePre1Episode)
        if len(out2Link) > 0:
            actionKey = re.findall(r'\w{10,}', out2Link[0])[0]
            r = requests.post('https://4snip.pw'+re.sub(r'\/out2\/', '/outlink/', out2Link[0]), data={'url': actionKey})
            urlVideo = 'https://akvideo.stream' + re.findall(r'action=\'([\/\w\.]+)\'', r.text)[0]
            r = requests.get(urlVideo, allow_redirects=True)
            return urlVideo
        else:
            return self.list_episodes[episode_number][1]

    def printEpisodes(self):
        for i, ep in enumerate(self.list_episodes):
            print(f'{i:>3}) {ep[0]}')

    def _contentFromUrl(self, link=False, filename=''):
            content = ''
            if link:
                page = requests.get(link)
                content = page.text
            # remove any kind of style in order to reduce text
            content = re.sub(r'(<style[^<]+|style=(\"|\')[^\"\']+(\"|\'))', '', content)
            if filename != '':
                with open(filename, 'w') as f:
                    f.write(content)
            return content

    # def _do_you_wish_to_continue(self):
    #     # do_you_wish_to_continue = input("\nDo you wish to continue (y/yes/ok) or [num] or (list/l): ")
    #     do_you_wish_to_continue = input("\nDo you wish to continue (y/yes/ok): ")
    #     if do_you_wish_to_continue in ['y', 'yes', 'ok']:
    #         return False
    #     elif do_you_wish_to_continue.isnumeric():
    #         return do_you_wish_to_continue
    #     elif do_you_wish_to_continue in ['list', 'l']:
    #         return True
    #     return False
import requests
import json

from moviesandseries import MoviesAndSeries

mes = MoviesAndSeries()

def runBot(mes):
    tryAgain = 'or run another search'
    selectInputSentence = 'Select a {} by its index from the list (number) {}: '
    continueCondition = True
    selectAnotherEpisode = False
    query = ''
    while continueCondition:
        if not selectAnotherEpisode:
            query = input('\nSearch for your show: ') if not query else query
            if query:
                mes.getTitleList(query)
        
        if len(mes.list_title) > 0:
            if not selectAnotherEpisode:
                print(mes)
                titleIndex = input(selectInputSentence.format('title', tryAgain))
            if not selectAnotherEpisode:
                episodeindex = '0'
            if str(titleIndex).isnumeric():
              if '/serie' in mes.list_title[int(titleIndex)][1]:
                if not selectAnotherEpisode:
                    titleIndex = int(titleIndex)
                    mes.getEpisodeList(titleIndex if titleIndex < len(mes.list_title) else 0)
                    mes.printEpisodes()
                if len(mes.list_episodes) > 1:
                    episodeindex = input(selectInputSentence.format('episode', tryAgain)) if not selectAnotherEpisode else episodeindex
                    if episodeindex.isnumeric():
                        index = int(episodeindex)
                        print(mes.getShowUrl(index if index < len(mes.list_episodes) else 0))
                        episodeindex = input('Do you wish to select another episode (number)?: ')
                        if episodeindex and episodeindex.isnumeric:
                            selectAnotherEpisode = True
                        else:
                            selectAnotherEpisode = False
                    else:
                        # here episodeindex is another query search
                        query = episodeindex
                else:
                    print(mes.getShowUrl(int(episodeindex)))
              else:
                print(mes.list_title[int(titleIndex)][1])
            else:
                # here titleIndex is another query search
                query = titleIndex
        else:
            print('No results were found')
            query = ''

runBot(mes)
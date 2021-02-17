# Reference: https://docs.scrapy.org/en/latest/intro/tutorial.html
import scrapy
import pandas as pd

class MultitracksSpider(scrapy.Spider):
    name = 'multitracks' # Identifies the Spider. It must be unique within a project

    start_urls = [
        'https://www.cambridge-mt.com/ms/mtk/',
    ]

    # Based in the html
    ROOT = 'c-mtk'
    GENRE = '__genre'
    ARTIST = '__artist'

    def parse(self, response): # A method that will be called to handle the response downloaded for each of the requests made.

        # Dictionaries based on 'multitracks/models.py' (https://github.com/ignacio-nava/Multitrack_Downloader) 
        # that will later be used to create the DataFrames
        genre = {
            'name':[]
        }

        artist = {
            'name':[],
            'contact': [],
        }

        multitrack =  {
            'title': [],
            'file_zip': [],
            'file_size': [],
            'number_channels': [],
            'preview': [],
            'genre': [],
            'artist': []
        }

        # Scrape the data from the URL (html) and save it on the dictionaries
        g, a = -1, -1
        for genre_selector in response.css(f'.{self.ROOT} .{self.ROOT+self.GENRE}'):
            genre['name'].append(genre_selector.css('h3 span::text').get())
            g += 1
            for artist_selector in genre_selector.css(f'.{self.ROOT+self.ARTIST}'):
                artist['name'].append(artist_selector.css('div h4 span::text').get())
                artist['contact'].append(artist_selector.css('.m-container__header span a::attr(href)').get())
                a += 1
                for mtk_selector in artist_selector.css('div.m-container ul li.m-mtk-track'):
                    mtk_data = mtk_selector.css('.m-mtk-track__downloads li')[-2]
                    multitrack['title'].append(mtk_selector.css('.m-mtk-track__name::text').get().replace('\n','')[1:-1])
                    multitrack['file_zip'].append(mtk_data.css('.m-mtk-download__links a::attr(href)').get())
                    multitrack['file_size'].append(mtk_data.css('.m-mtk-download__links span::text').get())
                    multitrack['number_channels'].append(int(mtk_data.css('.m-mtk-download__count::text').get().split(' ')[0]))
                    multitrack['preview'].append(mtk_data.css('.m-mtk-download__preview span::attr(data-src)').get())
                    multitrack['genre'].append(g)
                    multitrack['artist'].append(a)
                    
        # Write three CSV file with the data scraped
        models = [genre, artist, multitrack]
        models_name = ['genre', 'artist', 'multitrack']
            
        for model in models:
            dfs = [ pd.DataFrame(data=model) for model in models ]

        # if an Excel file is needed
        # with pd.ExcelWriter(f'models.xlsx') as writer:
        #     for i in range(len(dfs)):
        #         dfs[i].to_excel(writer,sheet_name=models_name[i])

        # CSV files
        for i in range(len(dfs)):
            dfs[i].to_csv(f'models_files/{models_name[i]}.csv', index=False, header=True)

# Run in the project's root:
# {user}$ mkdir models_files (if you didn't before)
# {user}$ scrapy crawl multitracks 
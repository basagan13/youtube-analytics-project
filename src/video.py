import os
from googleapiclient.discovery import build


class Video:
    @classmethod
    def get_service(cls):
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('YT_API_KEY')
        # создать специальный объект для работы с API
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def video_response(self):
        youtube = Video.get_service()
        return youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                     id=self.video_id).execute()

    def __init__(self, video_id: str):
        self.video_id = video_id

        video_response = self.video_response
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.video_id}")'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

        video_response = self.video_response
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

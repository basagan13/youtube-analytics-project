import json, os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    @classmethod
    def get_service(cls):
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('YT_API_KEY')
        # создать специальный объект для работы с API
        return build('youtube', 'v3', developerKey=api_key)

    youtube = Channel.get_service()

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.descr = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        channel_attr = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'descr': self.descr,
            'url': self.url,
            'subscribers': self.subscriber_count,
            'videos': self.video_count,
            'views': self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dumps(channel_attr, indent=2, ensure_ascii=False)

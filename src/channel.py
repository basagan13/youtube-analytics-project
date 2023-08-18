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

    @property
    def channel(self):
        youtube = Channel.get_service()
        return youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.channel
        self.title = channel['items'][0]['snippet']['title']
        self.descr = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self):
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        channel_attr = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.descr,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(channel_attr, f, indent=2, ensure_ascii=False)

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Not the same type')
        return int(self.subscriber_count) == int(other.subscriber_count)

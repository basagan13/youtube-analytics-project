from src.channel import Channel


class Video:
    @property
    def video_response(self):
        youtube = Channel.get_service()
        return youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                     id=self.__video_id).execute()

    def __init__(self, video_id: str):
        self.__video_id = video_id

        video_response = self.video_response
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    @property
    def video_id(self):
        return self.__video_id

    @property
    def video_url(self):
        return f'https://youtu.be/{self.__video_id}'

    def __str__(self):
        return self.video_title

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.__video_id}")'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

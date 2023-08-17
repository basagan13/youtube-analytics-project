from datetime import timedelta
import isodate
from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def youtube(self):
        return Channel.get_service()

    @property
    def title(self):
        playlist_list = self.youtube.playlists().list(part='snippet', id=self.playlist_id,
                                                      maxResults=1).execute()
        return playlist_list['items'][0]['snippet']['title']

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def playlist_videos(self):
        return self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                 part='contentDetails').execute()

    @property
    def video_response(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video
                                in self.playlist_videos()['items']]

        return self.youtube.videos().list(part='snippet,contentDetails,statistics',
                                          id=','.join(video_ids)).execute()

    @property
    def total_duration(self):
        tm = timedelta(hours=0, minutes=0)
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            tm += duration
        return tm

    def show_best_video(self):
        max_like_count = 0
        max_like_video_id = ''
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                max_like_video_id = video['id']

        return f"https://youtu.be/{max_like_video_id}"

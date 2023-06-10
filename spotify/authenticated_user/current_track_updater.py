from item.track import Track

class currentTrackUpdater:
    def __init__(self, spotify):
        self.sp = spotify.sp
        self.current_state = self.sp.current_playback()
        
    def pause(self):
        if self.sp.current_playback() is not None:
            self.sp.pause_playback()
        
    
    def resume(self):
        if self.current_state is not None:
            self.sp.start_playback()
    
    def skip(self):
        if self.current_state is not None:
           self.sp.next_track()

    def shuffle(self):
        if self.current_state is not None:
            shuffle_state = self.current_state['shuffle_state']
            if shuffle_state == False:
                self.sp.shuffle(True)
            else:
                self.sp.shuffle(False)
        
    def repeat(self):
        if self.current_state is not None:
            repeat_state = self.current_state['repeat_state']
            if repeat_state == 'off':
                self.sp.repeat('context')
            elif repeat_state == 'context':
                self.sp.repeat('track')
            else:
                self.sp.repeat('off')
        
    def volume(self, volume):
        if self.current_state is not None:
            if 0 <= volume <=100:
                self.sp.volume(volume)
            else:
                raise ValueError("Volume input must be between 0-100")

    def previous_track(self):
        if self.current_state is not None:
            self.sp.previous_track()
    
    def play_track(self, track_name, track_artist = ""):
        if self.current_state is not None:
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.sp.search(q=query, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if len(items) != 0:
                self.sp.start_playback(uris=[Track(items[0]).uri])
            else:
                raise ValueError("Could not find a song")
    
    def add_track_to_queue(self, track_name, track_artist = ""):
        if self.current_state is not None:
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.sp.search(q=query, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if len(items) != 0:
                self.sp.add_to_queue(uri=Track(items[0]).uri)
            else:
                raise ValueError("Could not find a song")
       
    
    def play_playlist(self, playlist_name="", playlist_uri="", playlist_link=""):
        if self.current_state is not None and any([playlist_name, playlist_uri, playlist_link]):
            print(1)
                # Handle playing the playlist based on the provided inputs
            if playlist_uri:
                self.sp.start_playback(context_uri=playlist_uri)
            elif playlist_link:
                playlist_id = playlist_link.split('/')[-1]
                self.sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
            else:
                playlists = self.sp.current_user_playlists()
                for playlist in playlists['items']:
                    if playlist['name'].strip().lower() == playlist_name.strip().lower():
                        self.sp.start_playback(context_uri=playlist['uri'])

    



    
        
    

    
    
    
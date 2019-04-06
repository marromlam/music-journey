# music-journey

This is a **python3** script to download Spotify playlists that were stored as CSV files.
In order to get this CSV playlists you should use the link on first Usage step, because the script uses this columns format.

This is only for _demo purposes_, I encourage not to use this package to ilegally download copyright contents.

## Packages
_music-journey_ doesn't rely on any external package, but eyed3. So basically you simply install _eyed3_, and you are done.

By the other hand, it's not a package, you should install _youtube-dl_. This is a well-known package to download YouTube videos in different formats. You can find it at: https://ytdl-org.github.io/youtube-dl/download.html

## Usage
This is really easy: 
1. We go to https://rawgit.com/watsonbox/exportify/master/exportify.html, we sign in with our Spotify credentials and we download our file. Let's say we give it a creative name: /Downloads/playlist.csv.
2. We launch our favourite terminal app, and we run (there is no need o add the ".csv" extension, script will handle this stuff): 
```
python3 musicjourney.py --list /Downloads/playlist.csv
```
3. Wait while magic runs. Enjoy your _music-journey_!


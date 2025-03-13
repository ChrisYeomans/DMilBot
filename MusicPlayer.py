from __future__ import annotations
import asyncio
from random import randint
from typing import List
import discord
from typing import TYPE_CHECKING

import yt_dlp as youtube_dl

if TYPE_CHECKING:
    from Bot import Bot

#
# TODO: ADD BOONIFIER
#

ytdl_format_options = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
        }
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = ""

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicPlayer:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.playlist: List[YTDLSource] = []
        self.current_song_title: str = ""

    def get_active_voice_clients(self) -> List[discord.VoiceClient]:
        return [e for e in self.bot.client.voice_clients if e]

    def is_connected(self) -> bool:
        return len(self.get_active_voice_clients()) > 0
    
    def get_active_voice_client(self) -> discord.VoiceClient:
        return self.get_active_voice_clients()[0]
    
    def play_next(self):
        if len(self.playlist) == 0:
            return
        player = self.playlist.pop(0)
        self.current_song_title = player.title
        voice_client = self.get_active_voice_client()
        voice_client.play(player, after=lambda e: self.play_next() if len(self.playlist) > 0 else None)

    async def play(self, interaction: discord.interactions, url: str):
        await interaction.response.defer()
        voice_client: discord.VoiceClient = None
        if self.is_connected():
            voice_client = self.get_active_voice_client()
        elif interaction.user.voice is not None:
            voice_client = await interaction.user.voice.channel.connect()
        else:
            await interaction.followup.send("You must be in a voice channel to play music.")
            return
        
        if voice_client is None:
            await interaction.followup.send("The bot is not connected to a voice channel.")
            return
        
        boon_rand = randint(1, self.bot.constants.boon_rand_odds[1] * 10)
        print(f"BoonRand: {boon_rand}")
        if boon_rand > (self.bot.constants.boon_rand_odds[1] - self.bot.constants.boon_rand_odds[0]) * 10:
            await interaction.followup.send("Boonified!")
            url = "https://www.youtube.com/watch?v=prYbXj3zPfs&ab"
        player = await YTDLSource.from_url(url, stream=True)
        
        self.playlist.append(player)
        if not voice_client.is_playing():
            await interaction.followup.send('**Now playing:** {}'.format(player.title))
            self.play_next()
        else:
            await interaction.followup.send('**Added to queue:** {}'.format(player.title))
            

    async def stop(self, interaction: discord.interactions):
        if self.is_connected():
            voice_client = self.get_active_voice_client()
            voice_client.stop()
            self.playlist = []
            await voice_client.disconnect()
            await interaction.response.send_message("Music stopped.")
        else:
            await interaction.response.send_message("The bot is not connected to a voice channel.")

    async def skip(self, interaction: discord.interactions):
        if self.is_connected():
            voice_client = self.get_active_voice_client()
            voice_client.stop()
            self.play_next()
            await interaction.response.send_message("Song skipped.")
        else:
            await interaction.response.send_message("The bot is not connected to a voice channel.")

    async def queue(self, interaction: discord.interactions):
        await interaction.response.send_message("Queue: \n" + f"Current Song: {self.current_song_title}\n" + "\n".join([f"{i+1}: {e.title}" for i, e in enumerate(self.playlist)]))

    async def playing(self, interaction: discord.interactions):
        await interaction.response.send_message(f"Currently playing: {self.current_song_title}")


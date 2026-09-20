# from crewai_tools import YoutubeChannelSearchTool
#
# yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@krishnaik06')
from crewai.tools import BaseTool
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import re


class YouTubeTool(BaseTool):
    name: str = "YouTube Search and Transcript Tool"
    description: str = (
        "Search for YouTube videos from the Krishnaik06 channel "
        "and retrieve their transcripts."
    )

    def _run(self, query: str) -> str:
        # Search YouTube
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "playlistend": 5
        }

        search_query = f"ytsearch5:{query} Krishnaik06"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(search_query, download=False)

        videos = results.get("entries", [])

        if not videos:
            return "No YouTube videos found."

        output = []

        for video in videos:
            video_id = video.get("id")
            title = video.get("title")

            if not video_id:
                continue

            try:
                api = YouTubeTranscriptApi()
                transcript = api.fetch(video_id)

                text = " ".join(
                    snippet.text for snippet in transcript
                )

                output.append(
                    f"VIDEO: {title}\n"
                    f"URL: https://www.youtube.com/watch?v={video_id}\n"
                    f"TRANSCRIPT:\n{text[:10000]}\n"
                )

            except Exception:
                output.append(
                    f"VIDEO: {title}\n"
                    f"URL: https://www.youtube.com/watch?v={video_id}\n"
                    f"Transcript unavailable.\n"
                )

        return "\n\n".join(output)


yt_tool = YouTubeTool()
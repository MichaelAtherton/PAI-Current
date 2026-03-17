"""YouTube channel and playlist scraper using yt-dlp."""

import json
import re
import subprocess
from datetime import datetime
from typing import Iterator, Optional

from ..config import get_settings
from ..models import VideoMetadata


def detect_youtube_source_type(url: str) -> str:
    """Detect whether a YouTube URL is a channel, playlist, video, or unknown.

    Args:
        url: YouTube URL to classify.

    Returns:
        "channel", "playlist", "video", or "unknown".
    """
    if re.search(r"youtube\.com/playlist\?list=", url):
        return "playlist"
    if re.search(r"youtube\.com/watch\?", url) or re.search(r"youtu\.be/", url):
        return "video"
    if re.search(
        r"youtube\.com/(@[\w-]+|channel/[\w-]+|c/[\w-]+|user/[\w-]+)",
        url,
    ):
        return "channel"
    return "unknown"


class YouTubeScraper:
    """Extract video metadata from a YouTube channel or playlist using yt-dlp."""

    def __init__(self, source_url: str):
        """Initialize scraper with a YouTube channel or playlist URL.

        Args:
            source_url: YouTube channel URL (e.g., https://www.youtube.com/@username)
                        or playlist URL (e.g., https://www.youtube.com/playlist?list=PLxxx)
        """
        self.source_url = source_url
        self.source_type = detect_youtube_source_type(source_url)
        self.settings = get_settings()

    def get_video_urls(self, limit: Optional[int] = None) -> Iterator[VideoMetadata]:
        """Stream video metadata from channel or playlist.

        Args:
            limit: Maximum number of videos to fetch. None for all.

        Yields:
            VideoMetadata for each video found.
        """
        url = self.source_url
        if self.source_type == "channel":
            # Normalize channel URLs to /videos tab for consistent listing.
            # Strip any existing tab suffix (/shorts, /streams, /playlists, etc.)
            # so yt-dlp gets the full video catalogue.
            url = re.sub(r"/(videos|shorts|streams|playlists|community|about)/?$", "", url.rstrip("/"))
            url += "/videos"

        cmd = [
            self.settings.get_yt_dlp_path(),
            "--flat-playlist",
            "--dump-json",
            url,
        ]
        if limit:
            cmd.extend(["--playlist-items", f"1:{limit}"])

        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
                yield self._parse_metadata(data)
            except json.JSONDecodeError:
                continue

        proc.wait()

    def get_single_video_metadata(self, video_url: str) -> VideoMetadata:
        """Get metadata for a single YouTube video.

        Args:
            video_url: Direct URL to a YouTube video.

        Returns:
            VideoMetadata for the video.
        """
        cmd = [
            self.settings.get_yt_dlp_path(),
            "--dump-json",
            "--no-download",
            video_url,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return self._parse_metadata(data)

    def _parse_metadata(self, data: dict) -> VideoMetadata:
        """Parse yt-dlp JSON output into VideoMetadata.

        Args:
            data: JSON data from yt-dlp.

        Returns:
            Parsed VideoMetadata.
        """
        timestamp = None
        if data.get("timestamp"):
            try:
                timestamp = datetime.fromtimestamp(data["timestamp"])
            except (ValueError, OSError):
                pass

        return VideoMetadata(
            id=data.get("id", ""),
            url=data.get("webpage_url") or data.get("url", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            duration=data.get("duration", 0) or 0,
            timestamp=timestamp,
            view_count=data.get("view_count", 0) or 0,
            like_count=data.get("like_count", 0) or 0,
        )

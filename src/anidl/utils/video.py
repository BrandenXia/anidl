import asyncio
import subprocess
from pathlib import Path

VIDEO_SUFFIXS = [".mp4", ".mkv", ".avi", ".webm", ".flv"]


def ensure_ffmpeg_installed():
    """Check if ffmpeg is installed on the system."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        raise RuntimeError("ffmpeg not found")


async def check_video_integrity(video_path: Path) -> bool:
    """Check if the video file is valid and not corrupted."""
    p = await asyncio.create_subprocess_exec(
        "ffprobe",
        "-v",
        "error",
        video_path.expanduser().absolute(),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    await p.wait()
    assert p.stderr is not None, "stderr should not be None"
    return not await p.stderr.readline()

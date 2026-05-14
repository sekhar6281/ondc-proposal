"""
make_video.py
Records AP Commerce Stack presentation using Playwright's live browser recording.
- Real CSS animations captured as they play
- Each slide shown for exact duration of its audio
- UI elements hidden (voice btn, lang toggle, progress bar)
- Auto-advance timer disabled (no slide repeats)
- Font sizes boosted ~30% for readability
- Full 1920x1080 scale
- Audio merged via ffmpeg
"""

import asyncio, subprocess, sys
from pathlib import Path
from mutagen.mp3 import MP3
from playwright.async_api import async_playwright
import imageio_ffmpeg

FFMPEG    = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR  = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"
OUT_DIR   = BASE_DIR / "video_output"
OUT_DIR.mkdir(exist_ok=True)

SLIDES = 13
URL    = "http://localhost:3333"
WIDTH  = 1920
HEIGHT = 1080

# CSS injected into the page before recording — only hide UI controls
INJECT_CSS = """
.voice-btn, .lang-toggle, #prog-bar {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
"""


def get_duration(mp3_path: Path) -> float:
    return MP3(str(mp3_path)).info.length


async def record_visual(lang: str) -> Path:
    """Live-record the presentation browser with animations playing."""
    print(f"\n[Recording browser] {lang.upper()} ...")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT},
            record_video_dir=str(OUT_DIR),
            record_video_size={"width": WIDTH, "height": HEIGHT},
        )
        page = await context.new_page()
        await page.goto(URL, wait_until="networkidle")

        # Inject CSS: hide UI controls + boost font sizes
        await page.evaluate(f"""
            (function() {{
                var s = document.createElement('style');
                s.textContent = {repr(INJECT_CSS)};
                document.head.appendChild(s);
            }})();
        """)

        # Fill 1920x1080 fully — remove the 1.2 cap, use full viewport scale
        await page.evaluate("""
            (function() {
                var stage = document.getElementById('stage');
                var bw = 960, bh = 580;
                var scale = Math.min(window.innerWidth / bw, window.innerHeight / bh);
                stage.style.transform = 'scale(' + scale + ')';
                stage.style.transformOrigin = 'top left';
                stage.style.left = ((window.innerWidth  - bw * scale) / 2) + 'px';
                stage.style.top  = ((window.innerHeight - bh * scale) / 2) + 'px';
                stage.style.margin = '0';
            })();
        """)

        # Set language, then IMMEDIATELY pause auto-advance timer
        await page.evaluate(f"setLang('{lang}')")
        await page.evaluate("pauseProgress()")

        # Reset to slide 1 with animations
        await page.evaluate("""
            (function() {
                document.getElementById('s' + cur).classList.remove('active');
                cur = 1;
                var slide = document.getElementById('s1');
                slide.querySelectorAll('*').forEach(function(el) {
                    el.style.animation = 'none';
                    void el.offsetHeight;
                    el.style.animation = '';
                });
                slide.classList.add('active');
            })();
        """)

        # Wait for slide 1 audio duration
        dur1 = get_duration(AUDIO_DIR / f"{lang}_01.mp3")
        print(f"  slide 01  ({dur1:.1f}s)")
        await page.wait_for_timeout(int(dur1 * 1000))

        # Slides 2-13
        for i in range(2, SLIDES + 1):
            dur = get_duration(AUDIO_DIR / f"{lang}_{i:02d}.mp3")
            await page.evaluate(f"""
                (function() {{
                    document.getElementById('s' + cur).classList.remove('active');
                    cur = {i};
                    var slide = document.getElementById('s{i}');
                    slide.querySelectorAll('*').forEach(function(el) {{
                        el.style.animation = 'none';
                        void el.offsetHeight;
                        el.style.animation = '';
                    }});
                    slide.classList.add('active');
                    pauseProgress();
                }})();
            """)
            print(f"  slide {i:02d}  ({dur:.1f}s)")
            await page.wait_for_timeout(int(dur * 1000))

        # Save video path before closing
        raw_video = Path(await page.video.path())
        await context.close()
        await browser.close()

    print(f"  Raw recording: {raw_video.name}")
    return raw_video


def build_audio_track(lang: str) -> Path:
    """Concatenate all slide MP3s into one AAC audio track."""
    print(f"\n[Audio track] {lang.upper()} ...")
    list_file = OUT_DIR / f"audio_list_{lang}.txt"
    with open(list_file, "w") as f:
        for i in range(1, SLIDES + 1):
            f.write(f"file '{(AUDIO_DIR / f'{lang}_{i:02d}.mp3').as_posix()}'\n")

    out = OUT_DIR / f"combined_{lang}.aac"
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:a", "aac", "-b:a", "192k",
        str(out),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Audio concat failed:\n{result.stderr.decode()}")
    list_file.unlink()
    total = sum(get_duration(AUDIO_DIR / f"{lang}_{i:02d}.mp3") for i in range(1, SLIDES + 1))
    print(f"  Audio track: {total:.1f}s total")
    return out


def merge_video_audio(video: Path, audio: Path, out: Path):
    """Merge WebM video + AAC audio -> final MP4."""
    print(f"\n[Merge] video + audio ...")
    cmd = [
        FFMPEG, "-y",
        "-i", str(video),
        "-i", str(audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-shortest",
        str(out),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Merge failed:\n{result.stderr.decode()}")


async def make_video(lang: str):
    print(f"\n{'='*52}")
    print(f"  AP Commerce Stack  {lang.upper()} video  {SLIDES} slides")
    print(f"{'='*52}")

    raw_video  = await record_visual(lang)
    audio_file = build_audio_track(lang)

    final = BASE_DIR / f"AP_Commerce_Stack_{lang.upper()}.mp4"
    merge_video_audio(raw_video, audio_file, final)

    # cleanup
    raw_video.unlink(missing_ok=True)
    audio_file.unlink(missing_ok=True)

    size_mb = final.stat().st_size / (1024 * 1024)
    total_s = sum(get_duration(AUDIO_DIR / f"{lang}_{i:02d}.mp3") for i in range(1, SLIDES + 1))
    print(f"\n[Done]  {final.name}  ({size_mb:.1f} MB  |  {total_s/60:.1f} min)")
    return final


async def main():
    langs = sys.argv[1:] if sys.argv[1:] else ["en"]
    for lang in langs:
        await make_video(lang)
    print("\n[All done]")


if __name__ == "__main__":
    asyncio.run(main())

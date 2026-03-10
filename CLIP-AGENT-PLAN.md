# Short-Form Clip Agent — Architecture

Automated pipeline: Long-form YouTube → Short clips → TikTok + Instagram Reels

---

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  YouTube     │────▶│  Transcript  │────▶│  Claude AI   │────▶│  FFmpeg      │
│  Video (MP4) │     │  + Timestamps│     │  Pick Clips  │     │  Cut + Format│
└─────────────┘     └──────────────┘     └─────────────┘     └──────┬───────┘
                                                                     │
                                                              ┌──────▼───────┐
                                                              │  Post to     │
                                                              │  TikTok +    │
                                                              │  Reels       │
                                                              └──────────────┘
```

---

## Step-by-Step Pipeline

### Step 1: Download + Transcribe

**Tools:** `yt-dlp` (download) + `whisper` (transcribe with timestamps)

```bash
# Download the video
yt-dlp -f "bestvideo[height<=1080]+bestaudio" -o "episode.mp4" "$YOUTUBE_URL"

# Transcribe with word-level timestamps
whisper episode.mp4 --model medium --output_format json --word_timestamps True
```

**Output:** A JSON transcript with every word timestamped — this is how the agent knows *where* to cut.

### Step 2: Claude Picks the Clips

Feed the transcript to Claude and ask it to find clip-worthy moments.

```python
import anthropic
import json

client = anthropic.Anthropic()

with open("episode.json") as f:
    transcript = json.load(f)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    system="""You are a short-form video editor for a Claude Code tutorial channel.

Your job: find 3-5 clip-worthy moments from this transcript that would work as
30-90 second TikTok/Reels clips.

Good clips have:
- A clear "hook" in the first 3 seconds (surprising statement, bold claim, cool demo moment)
- A self-contained idea (doesn't require watching the full video to understand)
- High energy or "aha moment" energy
- Practical value (a tip, trick, or insight viewers can use immediately)

For each clip, return:
1. start_time (seconds)
2. end_time (seconds)
3. hook (the first sentence — this becomes the on-screen text)
4. caption (for TikTok/Reels post — include hashtags)
5. title (short, punchy)

Return as JSON array.""",
    messages=[{
        "role": "user",
        "content": f"Here's the transcript for my Claude Code tutorial. Find the best clips:\n\n{json.dumps(transcript)}"
    }]
)

clips = json.loads(response.content[0].text)
```

**Example output from Claude:**
```json
[
  {
    "title": "The One Setting Everyone Misses",
    "start_time": 234.5,
    "end_time": 289.2,
    "hook": "Most people skip this setting and it costs them hours",
    "caption": "This one Claude Code setting changed everything 🤯 #claudecode #ai #coding #devtools"
  }
]
```

### Step 3: FFmpeg Cuts + Formats the Clips

```python
import subprocess

for i, clip in enumerate(clips):
    start = clip["start_time"]
    duration = clip["end_time"] - clip["start_time"]

    # Cut the clip and convert to 9:16 vertical (1080x1920)
    subprocess.run([
        "ffmpeg", "-ss", str(start), "-i", "episode.mp4",
        "-t", str(duration),
        "-vf", "crop=ih*9/16:ih,scale=1080:1920",  # Center crop to vertical
        "-c:v", "libx264", "-c:a", "aac",
        f"clip_{i}_{clip['title'].replace(' ', '_')}.mp4"
    ])
```

**Key detail:** The `crop=ih*9/16:ih` filter center-crops your 16:9 Loom recording into 9:16 vertical. Since your content is a desktop screencast, you may want to crop to the most important region (terminal area) instead of dead center. More on that below.

### Step 4: Add Captions (Subtitles Burned In)

Short-form videos with captions get ~40% more watch time. Use the Whisper timestamps to burn them in:

```python
# Generate .srt subtitle file for each clip
def make_srt(transcript_words, start_time, end_time):
    # Filter words in the clip's time range
    clip_words = [w for w in transcript_words
                  if start_time <= w["start"] <= end_time]

    # Group into 4-6 word chunks for readable captions
    chunks = []
    for i in range(0, len(clip_words), 5):
        group = clip_words[i:i+5]
        chunks.append({
            "start": group[0]["start"] - start_time,
            "end": group[-1]["end"] - start_time,
            "text": " ".join(w["word"] for w in group)
        })

    # Write SRT
    srt = ""
    for j, chunk in enumerate(chunks):
        srt += f"{j+1}\n"
        srt += f"{format_ts(chunk['start'])} --> {format_ts(chunk['end'])}\n"
        srt += f"{chunk['text']}\n\n"
    return srt

# Burn captions into video with FFmpeg
subprocess.run([
    "ffmpeg", "-i", f"clip_{i}.mp4",
    "-vf", f"subtitles=clip_{i}.srt:force_style='FontSize=24,Bold=1,Alignment=10,MarginV=40'",
    f"clip_{i}_captioned.mp4"
])
```

### Step 5: Post to TikTok + Reels

**TikTok:** Use the [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started/)
```python
# TikTok requires OAuth + Creator API access
# Upload flow: init upload → upload video → publish
import requests

# Initialize upload
resp = requests.post("https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size
        },
        "post_info": {
            "title": clip["caption"],
            "privacy_level": "PUBLIC_TO_EVERYONE"
        }
    }
)
upload_url = resp.json()["data"]["upload_url"]
# Then PUT the video file to upload_url
```

**Instagram Reels:** Use the [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/guides/content-publishing/)
```python
# Step 1: Create media container
resp = requests.post(
    f"https://graph.facebook.com/v19.0/{ig_user_id}/media",
    data={
        "media_type": "REELS",
        "video_url": public_video_url,  # Must be publicly accessible
        "caption": clip["caption"],
        "access_token": ig_access_token
    }
)
container_id = resp.json()["id"]

# Step 2: Publish
requests.post(
    f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish",
    data={"creation_id": container_id, "access_token": ig_access_token}
)
```

---

## Smart Cropping for Screen Recordings

Since your videos are Loom desktop recordings (16:9), naive center-crop to 9:16 will cut off the sides. Better approach:

**Option A — Dynamic region of interest (recommended):**
Claude analyzes the transcript and tells FFmpeg which screen region matters for each clip:
```python
# If the clip is about terminal commands, crop to the terminal area
# If the clip is about UI, crop to the browser area
crop_regions = {
    "terminal": "crop=608:1080:656:0",    # Right side where terminal is
    "browser":  "crop=608:1080:280:0",     # Left-center where browser is
    "full":     "crop=1080:1080:420:0,scale=1080:1920"  # Square center + pad
}
```

**Option B — Picture-in-picture layout:**
Keep full desktop at top, zoom into the key area at bottom:
```
┌──────────────────┐
│  Full desktop     │  ← small, provides context
│  (scaled down)    │
├──────────────────┤
│                  │
│  Zoomed-in area  │  ← large, readable
│  (terminal/code) │
│                  │
└──────────────────┘
```

---

## Running It as a Claude Code Agent

Wrap the whole pipeline in a Claude Code skill:

**File: `~/.claude/commands/clip-it.md`**
```markdown
# /clip-it — Generate short-form clips from a YouTube video

Given a YouTube URL, this skill:
1. Downloads the video with yt-dlp
2. Transcribes it with Whisper (word-level timestamps)
3. Uses Claude to identify 3-5 clip-worthy moments
4. Cuts clips with FFmpeg (9:16 vertical, burned-in captions)
5. Optionally posts to TikTok and Instagram Reels

## Usage
User provides: YouTube URL
Agent does everything else.
```

Then from Claude Code: `/clip-it https://youtube.com/watch?v=xxxxx`

---

## Prerequisites to Install

```bash
# Video download
pip install yt-dlp

# Transcription
pip install openai-whisper

# Video processing (likely already installed)
brew install ffmpeg

# Python SDK
pip install anthropic requests
```

---

## API Access Needed

| Platform | What you need | How to get it |
|----------|--------------|---------------|
| **TikTok** | Creator API access + OAuth app | Apply at developers.tiktok.com |
| **Instagram** | Facebook Developer App + IG Business Account | developers.facebook.com |
| **Claude** | API key (you already have this) | console.anthropic.com |

**Note:** TikTok's Content Posting API requires app review (~1-2 weeks). Instagram requires a Business or Creator account linked to a Facebook Page. Both are free.

---

## Realistic v1 vs v2

### v1 (build this weekend)
- Download + transcribe + Claude picks clips + FFmpeg cuts them
- Output: folder of ready-to-post vertical clips with captions
- **You manually upload to TikTok/Reels** (drag and drop, paste the caption Claude wrote)
- This alone saves 90% of the work

### v2 (build when you have API access)
- Auto-post to TikTok + Reels
- Schedule posts (spread clips across the week)
- A/B test different hooks for the same clip
- Analytics feedback loop (which clips perform → refine Claude's selection prompt)

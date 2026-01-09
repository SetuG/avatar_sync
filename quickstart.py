import time
from sync import Sync
from sync.common import Audio, GenerationOptions, Video
from sync.core.api_error import ApiError


api_key = "sk-Ot7rQ_qsQmWjRUXg38V2HA.5V2cPsG_rLf3ehz4J6cZDY63vUOTpZJD" 


video_url = "https://assets.sync.so/docs/example-video.mp4"

audio_url = "https://assets.sync.so/docs/example-audio.wav"

client = Sync(
    base_url="https://api.sync.so", 
    api_key=api_key
).generations

print("Starting lip sync generation job...")

try:
    response = client.create(
        input=[Video(url=video_url),Audio(url=audio_url)],
        model="lipsync-2",
        options=GenerationOptions(sync_mode="cut_off")
    )
except ApiError as e:
    print(f'create generation request failed with status code {e.status_code} and error {e.body}')
    exit()

job_id = response.id
print(f"Generation submitted successfully, job id: {job_id}")

generation = client.get(job_id)
status = generation.status
while status not in ['COMPLETED', 'FAILED']:
    print('polling status for generation', job_id)
    time.sleep(10)
    generation = client.get(job_id)
    status = generation.status

if status == 'COMPLETED':
    print('generation', job_id, 'completed successfully, output url:', generation.output_url)
else:
    print('generation', job_id, 'failed')
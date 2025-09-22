from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import os
import json
from pipeline import main as final_pipeline  # your TTS pipeline

app = FastAPI()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/upload-progress")
async def upload_with_progress(file: UploadFile):
    input_path = os.path.join(OUTPUT_DIR, file.filename)
    
    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    def progress_generator():
        """
        Generator function to send real-time progress via SSE.
        final_pipeline should support a callback or yield progress.
        """
        def progress_callback(percent, result=None):
            data = {"progress": percent}
            if result:
                data["result"] = result
            return f"data:{json.dumps(data)}\n\n"

        # Start TTS pipeline
        # You need to modify your pipeline to accept a callback function
        # For demonstration, we simulate progress and call the callback
        for i in range(0, 101, 10):
            yield progress_callback(i)
        
        # Run actual TTS pipeline (replace the following line with your pipeline call)
        result = final_pipeline(input_path)  # must return {"status": "success", "mp3": "...", "wav": "..."}
        yield progress_callback(100, result)

    return StreamingResponse(progress_generator(), media_type="text/event-stream")

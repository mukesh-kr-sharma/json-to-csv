from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse
import json
import csv
from io import StringIO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        request=request, name="index2.html"
    )


@app.post("/", response_class=StreamingResponse)
def json_to_csv(json_file: UploadFile):
    json_obj = json.loads(json_file.file.read().decode('utf-8'))

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    header = json_obj[0].keys()
    csv_writer.writerow(header)

    for item in json_obj:
        csv_writer.writerow(item.values())

    csv_data = csv_buffer.getvalue()
    csv_buffer.close()

    return StreamingResponse(
        iter([csv_data]),
        media_type='text/csv',
        headers={
            "Content-Disposition": f"attachment;filename={json_file.filename.rsplit('.')[0]}.csv"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        # host="0.0.0.0", 
        # port=5000, 
        log_level="info"
    )
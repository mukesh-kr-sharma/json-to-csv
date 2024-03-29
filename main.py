from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse
import json
import csv
from io import StringIO
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def homepage():
    content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utility: JSON To CSV Converter</title>
    <!-- Tailwind CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="max-w-md mx-auto mt-8 p-6 bg-white shadow-md rounded-md">
        <h1 class="text-2xl font-bold mb-4">Upload a JSON File</h1>
        <form action="/json-to-csv" method="POST" enctype="multipart/form-data">
            <div class="mb-4">
                <label for="json_file" class="block text-gray-700 font-bold mb-2">Choose a file:</label>
                <input type="file" id="json_file" name="json_file" class="w-full py-2 px-3 border border-gray-300 rounded-md">
            </div>
            <div class="mt-4">
                <button type="submit" class="w-full py-2 px-4 bg-blue-500 text-white font-semibold rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600">Convert JSON to CSV</button>
            </div>
        </form>
    </div>
</body>
</html>
    """
    return HTMLResponse(content)


@app.post("/json-to-csv", response_class=StreamingResponse)
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
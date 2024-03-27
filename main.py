from fastapi_cors import CORS
from fastapi import FastAPI, UploadFile
import pandas as pd
from fastapi.responses import StreamingResponse, HTMLResponse

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORS,
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
async def json_to_csv(json_file: UploadFile):
    df = pd.read_json(json_file.file)
    csv_text = df.to_csv(index=False)
    csv_bytes = csv_text.encode('utf-8')
    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment;filename={json_file.filename.rsplit('.')[0]}.csv"}
    )

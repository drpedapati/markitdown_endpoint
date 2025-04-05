from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import markitdown

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def homepage():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Markitdown Converter</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background: linear-gradient(to right, #ece9e6, #ffffff);
          margin: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }
        .container {
          background: #fff;
          padding: 2rem 3rem;
          border-radius: 8px;
          box-shadow: 0 4px 8px rgba(0,0,0,0.1);
          text-align: center;
        }
        h1 {
          margin-bottom: 1rem;
          color: #333;
        }
        input[type="file"] {
          margin: 1rem 0;
        }
        button {
          padding: 0.5rem 1rem;
          background-color: #4CAF50;
          color: #fff;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        button:hover {
          background-color: #45a049;
        }
        #result {
          margin-top: 1.5rem;
          text-align: left;
          background: #f7f7f7;
          padding: 1rem;
          border-radius: 4px;
          white-space: pre-wrap;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Markitdown Converter</h1>
        <form id="uploadForm">
          <input type="file" id="fileInput" name="file" required>
          <br>
          <button type="submit">Convert</button>
        </form>
        <div id="result"></div>
      </div>
      <script>
        document.getElementById("uploadForm").addEventListener("submit", async function(event) {
          event.preventDefault();
          const fileInput = document.getElementById("fileInput");
          const formData = new FormData();
          formData.append("file", fileInput.files[0]);
          const response = await fetch("/convert", { method: "POST", body: formData });
          const data = await response.json();
          document.getElementById("result").textContent = data.markdown;
        });
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/convert")
async def convert_to_markdown(file: UploadFile = File(...)):
    content = await file.read()
    markdown_text = markitdown.convert(content.decode("utf-8"))
    return {"markdown": markdown_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

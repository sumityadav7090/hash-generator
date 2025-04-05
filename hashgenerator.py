from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import hashlib
import uvicorn

app = FastAPI()

# Function to generate hashes
def generate_hashes(text):
    return {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA-1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA-256": hashlib.sha256(text.encode()).hexdigest(),
        "SHA-512": hashlib.sha512(text.encode()).hexdigest(),
        "BLAKE2": hashlib.blake2b(text.encode()).hexdigest()
    }

# Main Page
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hash Generator</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; }
            .container { width: 50%; margin: auto; background: white; padding: 20px; margin-top: 50px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            h1 { color: #333; }
            input { width: 80%; padding: 10px; margin: 10px; border: 1px solid #ccc; border-radius: 5px; }
            button { width: 85%; padding: 10px; margin: 10px; background-color: #007BFF; color: white; border: none; cursor: pointer; font-size: 16px; border-radius: 5px; }
            button:hover { background-color: #0056b3; }
            #results { margin-top: 20px; text-align: left; padding: 10px; background: #f9f9f9; border-radius: 5px; box-shadow: 0 0 5px rgba(0, 0, 0, 0.1); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Hash Generator</h1>
            <form action="/generate" method="post">
                <input type="text" name="inputText" placeholder="Enter text to hash..." required>
                <button type="submit">Generate Hash</button>
            </form>
        </div>
    </body>
    </html>
    """

# Hash Generator API
@app.post("/generate", response_class=HTMLResponse)
async def generate(inputText: str = Form(...)):
    hashes = generate_hashes(inputText)
    result_html = f"""
    <div id="results">
        <h2>Generated Hashes:</h2>
        <p><strong>MD5:</strong> {hashes['MD5']}</p>
        <p><strong>SHA-1:</strong> {hashes['SHA-1']}</p>
        <p><strong>SHA-256:</strong> {hashes['SHA-256']}</p>
        <p><strong>SHA-512:</strong> {hashes['SHA-512']}</p>
        <p><strong>BLAKE2:</strong> {hashes['BLAKE2']}</p>
    </div>
    <a href="/">🔙 Go Back</a>
    """
    return result_html

# Run Locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

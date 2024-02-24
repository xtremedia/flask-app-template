import json
import logging

from flask import Flask, render_template, request
from openai import AzureOpenAI

from config import config


# creating the 404 page (Optional)
def page_not_found(e):
    return render_template("404.html"), 404


# Initialise the Flask app
app = Flask(__name__)
app.config.from_object(config["development"])
app.register_error_handler(404, page_not_found)

api_key = app.config["API_KEY"]
# Initialise the OPENAI library with the key saved in the CONFIG file
client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint="https://dalleai3.openai.azure.com/",
    api_key=api_key,
)


# ----------START FUNCTIONS------
def createImageFromPrompt(prompt):
    try:
        response = client.images.generate(
            prompt=prompt, n=1, size="1024x1024", quality="standard", model="Dalle3"
        )
        json_response = json.loads(response.model_dump_json())
        return json_response["data"]
    except Exception as e:
        logging.error(e)
        return []


"""             # Save the image to disk
            with open(image_path, "wb") as image_file:
                image_file.write(generated_image)

            images.append(image_path)

        return images
    except Exception as e:
        logging.error(e)
        return [] """
# image_url = json.loads(result.model_dump_json())['data'][0]['url']

# ----------END FUNCTIONS-----------------


# View Functions
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        images = []
        prompt = request.form["prompt"]
        res = createImageFromPrompt(prompt)

        if len(res) > 0:
            for img in res:
                images.append(img["url"])

    return render_template("index.html", **locals())


# Run Flask
if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8000", debug=False)

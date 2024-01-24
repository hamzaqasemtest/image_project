import openai
import json
import os

client = openai.AzureOpenAI(
    api_version= os.getenv("api_version"),
    azure_endpoint= os.getenv("azure_endpoint"),
    api_key= os.getenv("api_key"),
)


result = client.images.generate(
    model="dalle_images_lookup",
    prompt="you know the carton tom and gerry generate image of tom smoking a ciggarette ridding a classic car  and make it look like a gangster ",
    n=1
)


image_url = json.loads(result.model_dump_json())['data'][0]['url']

print(image_url)
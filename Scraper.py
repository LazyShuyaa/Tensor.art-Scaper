import time
import requests

url = "https://api.tensor.art/works/v1/works/task"
headers = {"authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjcyMzY0NzM1NzY2NDYzNTYwNywiZGV2aWNlSWQiOiIiLCJyZWZyZXNoVG9rZW4iOiIiLCJleHBpcmVUaW1lIjoyNTkyMDAwLCJleHAiOjE3MTc1MjExODh9.DHgfdI7JFzW9KMQOKcSgRCYymd0ooBi4ukPO7WEW16A"}
payload = {"params": {"baseModel": {"modelId": "639919414063618803","modelFileId": "639920449149693501"},"sdxl": {"refiner": False},"models": [],"embeddingModels": [],"sdVae": "Automatic","prompt": "Naruto","negativePrompt": "EasyNegative","height": 768,"width": 512,"imageCount": 1,"steps": 20,"samplerName": "Euler a","images": [],"cfgScale": 7,"seed": "-1","clipSkip": 2,"etaNoiseSeedDelta": 31337,"v1Clip": False},"credits": 0.8,"taskType": "TXT2IMG","isRemix": False,"captchaType": "CLOUDFLARE_TURNSTILE"}
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    task_id = response.json()['data']['task']['taskId']
    print("Task Created with id", task_id)
else:
    print("Error:", response.status_code)

image_url = None

while True:
    if image_url:
        break
    
    time.sleep(10)

    url = "https://api.tensor.art/works/v1/works/tasks?size=20&cursor=0&returnAllTask=true"
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' in data and 'tasks' in data['data']:
        for task in data['data']['tasks']:
            if task['taskId'] == task_id and task['status'] == "FINISH":
                image_url = task['items'][0]['url']
                print(image_url)
                break
    else:
        print("No tasks available.")

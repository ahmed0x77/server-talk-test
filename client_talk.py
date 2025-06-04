# client.py
import requests

API_URL = "https://p84k48o0044os0owoogkcggg.nextspacey.com/execute/python"

def send_code(code):
    try:
        response = requests.post(API_URL, json={"code": code})
        result = response.json()
        if result.get("stdout"):
            print(result["stdout"].strip())
        if result.get("stderr"):
            print(result["stderr"].strip())
    except Exception as e:
        print(f"Error: {e}")






# code_to_send = """
# import requests
# import platform


# IS_LINUX = platform.system()
# print(f"Is the system Linux? {IS_LINUX}")
# """


# get the python code from the file `temp_2.py`
with open('temp_2.py', 'r', encoding='utf-8') as file:
    code_to_send = file.read()


send_code(code_to_send)





















# print("Enter Python code (type 'exit' to quit):")
# while True:
#     try:
#         line = input(">>> ")
#         if line.strip().lower() == 'exit':
#             break
#         send_code(line)
#     except KeyboardInterrupt:
#         print("\nExiting...")
#         break

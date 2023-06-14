# ngrok config add-authtoken 2OGf3aO2kxoNO1vp9HUNpqADi1e_3enMiHrmmoLy8tcLRp7aV
# ngrok http 80

import subprocess

result1 = subprocess.Popen(["python", "manage.py", "runserver"])
print(result1)  # Natija haqida ma'lumotni ko'rish (returncode, stdout, stderr)

# result2 = subprocess.run(["ngrok", "config", "add-authtoken", "2OGf3aO2kxoNO1vp9HUNpqADi1e_3enMiHrmmoLy8tcLRp7aV"])
# print(result2)

output1 = subprocess.Popen(["python", "bot.py"])
print(output1)  # Chiqishni ko'rish

# output2 = subprocess.Popen(["ngrok", "http", "8000"], shell=True)
# print(output2)
import time

for i in range(10):
    print(f"\rProgress: {i}% ", end="", flush=True)
    time.sleep(0.5)

with open('C:\\Users\\adity\\OneDrive\\Pictures\\Camera Roll\\WIN_20221228_16_38_34_Pro.jpg', 'rb') as f:
    data = f.read()

with open('output.jpg', 'wb') as f_output:
    f_output.write(b"hello") 

with open('output.jpg', 'rb') as file:
    message = file.read()

print("Retrieved message:", str(message,'utf-8'))

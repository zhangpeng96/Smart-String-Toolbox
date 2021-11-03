import base64
from io import BytesIO
from PIL import Image, ImageGrab

# 则img = Image.open(image_path).convert('RGB')
def image_to_base64():
    # img = Image.open(image_path)
    img = ImageGrab.grabclipboard()
    try:
        img = img.convert('L')
    except Exception as e:
        # raise "剪贴板格式错误"
        return b''
    # img.show()
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

# print(image_to_base64())
print('data:image/png;base64,' + image_to_base64().decode('utf-8'))
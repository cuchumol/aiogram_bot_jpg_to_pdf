from PIL import Image
from config import BASE_DIR 
import os


output_pdf = "output.pdf"


def join_pdf(buffer_list, user_id):
    '''images = []
    for photo in list_images:
        image = Image.open(photo)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        images.append(image)

    if images:
        images[0].save(f"{BASE_DIR}/{user_id}_{output_pdf}", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

    return f"{BASE_DIR}/{user_id}_{output_pdf}"'''

    images = []
    for buffer in buffer_list:
        image = Image.open(buffer)
        
        # for pdf
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        images.append(image)

    if images:
        images[0].save(f"{BASE_DIR}/{user_id}_{output_pdf}", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

    return f"{BASE_DIR}/{user_id}_{output_pdf}"



def delete_pdf(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
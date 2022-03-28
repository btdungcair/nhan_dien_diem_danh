import locale
import io
import re
import os
import controller
import pandas as pd
from PIL import Image
from shutil import copyfile

def getName(s):
    s = s.split()
    lname = s[0]
    fname = s[-1]
    return (lname, fname)
    
def compare(name):
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    lname = getName(name)[0]
    fname = getName(name)[1]
    return locale.strxfrm(fname), locale.strxfrm(lname)

def sort_by_name(student_list):
    """
    Sort students list by name in Vietnamese alphabet
    """
    student_list.sort(key=lambda x: compare(x[1]))
    return student_list

def image_to_octet_string(image_path):
    """
    Convert image to octet string
    """
    with open(image_path, "rb") as image_file:
        return image_file.read()

def octet_string_to_image(octet_string):
    """
    Convert octet string to image
    """
    img = Image.open(io.BytesIO(octet_string))
    return img

def validate_student_id(student_id):
    """
    Validate student id: must be 8 digits and doesn't exist in database
    """
    id_list = controller.get_id_list()
    regex = r'^\d{8}$'
    if re.match(regex, student_id) and int(student_id) not in id_list:
        return True
    else:
        return False

def validate_date(date_string):
    """
    Validate date: must be in format dd/mm/yyyy
    """
    regex = r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$'
    if re.match(regex, date_string):
        return True
    else:
        return False

def copy_student_image_to_ImagesStudent_dir(student_id, original_image_path):
    """
    Copy image of student to ImagesStudent directory
    """
    destination = os.getcwd() + '/ImagesStudent/'
    if original_image_path.endswith('.jpg'):
        copyfile(original_image_path, destination + student_id + '.jpg')
    elif original_image_path.endswith('.png'):
        copyfile(original_image_path, destination + student_id + '.png')

def update_student_image_in_ImagesStudent_dir(old_id, new_id, new_image_path):
    """
    Update image of student in ImagesStudent directory
    """
    old_id = str(old_id)
    destination = os.getcwd() + '/ImagesStudent/'
    if new_image_path == "":
        if os.path.exists(destination + old_id + '.jpg'):
            os.rename(destination + old_id + '.jpg', destination + new_id + '.jpg')
        elif os.path.exists(destination + old_id + '.png'):
            os.rename(destination + old_id + '.png', destination + new_id + '.png')
    else:
        if os.path.exists(destination + old_id + '.jpg'):
            os.remove(destination + old_id + '.jpg')
        elif os.path.exists(destination + old_id + '.png'):
            os.remove(destination + old_id + '.png')
        if new_image_path.endswith('.jpg'):
            copyfile(new_image_path, destination + new_id + '.jpg')
        elif new_image_path.endswith('.png'):
            copyfile(new_image_path, destination + new_id + '.png')

def export_csv_file(file_path, data, columns_list):
    """
    Export data to csv file
    """
    df = pd.DataFrame(data, columns=columns_list)
    df.to_csv(file_path, index=False, header=True)

def export_xlsx_file(file_path, data, columns_list):
    """
    Export data to xlsx file
    """
    df = pd.DataFrame(data, columns=columns_list)
    df.to_excel(file_path, index=False, header=True)

def remove_image_student_from_ImagesStudent_dir(student_id):
    """
    Remove image of student from ImagesStudent directory
    """
    destination = os.getcwd() + '/ImagesStudent/'
    if os.path.exists(destination + student_id + '.jpg'):
        os.remove(destination + student_id + '.jpg')
    elif os.path.exists(destination + student_id + '.png'):
        os.remove(destination + student_id + '.png')
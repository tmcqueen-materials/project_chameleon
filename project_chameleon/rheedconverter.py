import os
import numpy as np 
import matplotlib.pyplot as plt
import sys
import argparse

def get_image_dimensions(input_file):
    file_size = os.path.getsize(input_file)
    with open(input_file,"rb") as f:
        f.seek(39)
        data = f.read(6)
        signature = data.decode('utf-8')
        f.seek(49)
        data = f.read(2)
        width = int.from_bytes(data, byteorder='big') 
        f.seek(321)
        data = f.read(2)
        height = int.from_bytes(data, byteorder='big')
    f.close()
    header_size = file_size - 2*(width*height)
    if file_size > 3*(width*height):
        if signature == 'KSA00F':
            header_size = 640
        else:
            header_size = 685

    return height, width, header_size

def rheedconverter(file_name, output_file):
    """
    ``rheedconverter()`` is a function to allow RHEED users to convert 16 bpp .img images into 8 bpp more easily readable .png images

    :args: This function has two inputs: ``file_name`` and ``output_file``. ``file_name`` should be a rheed .img file. This function has been designed to handle images with dimensions of 1024x1024 as that is the standard size for RHEED images used for developing this function. ``output_file`` is a string which will be the name of the final output file. 

    :return: this function does not return anything. The output is saved as an image file.

    :exception: will throw an exception if the input file is not a .img file, or if the input file is not the correct size.
    """

    #Make sure input is a .img file
    if not file_name.endswith('.img'):
        raise ValueError("ERROR: bad input. Expected .img file")
    if not str(output_file).endswith('.png'):
        raise ValueError("ERROR: please make your output file a .png file")
    if os.path.getsize(file_name) < 615040:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too small.")
    if os.path.getsize(file_name) > 1049216:
        raise ValueError("ERROR: This size of file cannot be handled by this function. File too large.")
    
    file_height, file_width, header_bytes = get_image_dimensions(file_name)
    
    #Open file as unknown type. Skip header bytes and adjust to a height X width image. 
    with open(file_name,"r") as f:
        f.seek(header_bytes)
        laue = np.fromfile(f,dtype="<u2",count=file_width*file_height).reshape((file_height,file_width))
    
    #Operate to adjust from 16bpp to 8 bpp so the image can be displayed easier
    im_temp = laue - laue.min()
    im_temp = im_temp / im_temp.max()
    im_temp = im_temp * 255
   
    #Adjust to unsigned integers and save as a jpeg
    im_uint8_scaled = im_temp.astype(np.uint8)
    plt.axis('off')
    plt.imshow(im_uint8_scaled)
    plt.savefig(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    args = parser.parse_args()
    rheedconverter(args.input, args.output)
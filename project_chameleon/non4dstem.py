import hyperspy.api as hs
from glob import glob
import matplotlib.pyplot as plt
import os
import argparse

def non4dstem(data_folder = None, outputs_folder = None, data_file = None, output_file = None):
    """
    ``non4dstem`` is a function that takes an input folder or file containing 2D and 3D STEM images and converts those files into plots that are saved either as an output folder or as a single output file. This function was tested on .dm4 files, .ser files, and .emd files, but can handle any filetypes that can be parserd by the hyperspy 'load' function. This file can only take inputs in specific pairings. ``data_file`` can be paired with ``output_file`` and ``outputs_folder``. ``data_folder`` may only be paired with ``outputs_folder``.
 
    :args: This function has four inputs: ``data_folder``, ``data_file``, ``outputs_folder``, ``output_file``. ``data_folder`` should be a folder holding all non 4D files that are being processed. ``data_file`` should be a file containing a single non 4D stem file. ``outputs_folder`` is a string which will be the name out the folder that holds all the processed images. ``output_file`` is a string which will be the name of the single file output. 

    :return: this function does not return anything. It saves converted files as .png images in the folder labeled ``output_folder``.

    :exceptions: will throw an exception if the ``data_folder`` is not a folder.
    """
    if data_folder and os.path.isdir(data_folder) is False:
        raise ValueError("ERROR: bad input. Expected folder")
    if outputs_folder and '.' in str(outputs_folder):
        raise ValueError("ERROR: Output Folder should not contain '.'")
    if data_folder and os.listdir(data_folder) == 0:
        raise ValueError("ERROR: bad input. Data folder should contain files")
    if data_folder and data_file:
        raise ValueError("ERROR: Too many inputs. Can only have one of data_folder and data_file")
    if data_folder and output_file:
        raise ValueError("ERROR: Incorrect inputs. data_folder in not compatible with output_file")
    if data_folder and not outputs_folder:
        raise ValueError("ERROR: Incorrect inputs. data_folder must have an outputs_folder")
    if outputs_folder and output_file:
        raise ValueError("ERROR: Too many inputs. Can only have one of outputs_folder and output_file")
    
    if data_folder:
        #Create outputs folder and read in files from data folder
        count = 0
        os.makedirs(outputs_folder)
        for file in glob(data_folder + "/*"):
            data = hs.load(file)

        #For each file that gets read in, plot and save as a figure
        print(data)
        for obj in data:
            count = count + 1
            obj.plot()
            plt.savefig(f"{outputs_folder}/{os.path.splitext(os.path.split(file)[-1])[0]}_{obj.metadata.Signal.signal_type}{count}.png")
            plt.close()

    elif data_file and output_file:
        data = hs.load(data_file)
        data.plot()
        plt.savefig(output_file)
        plt.close()

    elif data_file and outputs_folder:
        os.makedirs(outputs_folder)
        data = hs.load(data_file)
        data.plot()
        plt.savefig(f"{outputs_folder}/{os.path.splitext(os.path.split(data_file)[-1])[0]}_{data.metadata.Signal.signal_type}.png")
        plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input folder")
    parser.add_argument("output", help="the output folder")
    args = parser.parse_args()
    non4dstem(data_folder = args.input, output_folder = args.output)

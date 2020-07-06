# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 10:50:07 2018
# Conversion tool for https://github.com/carpedm20/multi-speaker-tacotron-tensorflow
This prepares LJ-Dataset (available at https://keithito.com/LJ-Speech-Dataset/) to json and wav format
that can be processed into .npz file using datasets.generate_data. 

@author: engiecat (github)
"""
import os
from utils import load_json, write_json, backup_file, str2bool
import argparse

base_dir = os.path.dirname(os.path.realpath(__file__))
work_dir = os.getcwd()
class Data(object):
    def __init__(
            self, audio_name, audio_transcript,audio_normalized_transcript,audio_path='ERR'):
        self.audio_name = audio_name
        self.audio_transcript = audio_transcript
        self.audio_normalized_transcript=audio_normalized_transcript
        self.audio_path = audio_path

def read_csv(path,fn_encoding='UTF8'):
    # reads csv file into audio snippet name and its transcript
    with open(path, encoding=fn_encoding) as f:
        data = []
        temp='' # for storing non-normalized
        for line in f:
            audio_name, audio_transcript,audio_normalized_transcript = line.split('|')
            audio_transcript=audio_transcript.strip()
            audio_normalized_transcript=audio_normalized_transcript.strip()
            data.append(Data(audio_name, audio_transcript,audio_normalized_transcript))
        return data

def convert_name_to_path(name, audio_dir, audio_format):
    # converts audio snippet name to audio snippet path
    abs_audio_dir=os.path.abspath(os.path.join(base_dir,audio_dir))
    # the audio directory is respective to dataset folder(base_dir)
    # while the working directory is at the root directory (work_dir)
    result= os.path.join('./',os.path.relpath(abs_audio_dir,work_dir), name+'.'+audio_format )
    return result

def convert_to_json_format(data, is_normalized):
    # converts into json format
    if is_normalized:
        result={data.audio_path:[data.audio_normalized_transcript]}
    else:
        result={data.audio_path:[data.audio_transcript]}
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata', default="metadata.csv")
    parser.add_argument('--metadata_enconding', default="UTF8")
    parser.add_argument('--audio_dir', default="wavs")
    parser.add_argument('--audio_format', default='wav')
    parser.add_argument('--alignment_filename', default="alignment.json")
    parser.add_argument('--use_normalize', default=True, type=str2bool)
    config = parser.parse_args()
    
    print(' [*] Reading metadata file - '+config.metadata)
    data = read_csv(os.path.join(base_dir, config.metadata))
    print(' [*] Converting to audio_path...')
    results={}
    for d in data:
        d.audio_path=convert_name_to_path(d.audio_name,config.audio_dir,config.audio_format) 
        results.update(convert_to_json_format(d, config.use_normalize))
    print(' [*] Saving to json...')
    alignment_path = \
        os.path.join(base_dir, config.alignment_filename)
    if os.path.exists(alignment_path):
        backup_file(alignment_path)
    write_json(alignment_path, results)
    print(' [!] All Done!')
    print(work_dir)
    

#!flask/bin/python
# -*- coding: utf-8 -*-
import os, traceback
import hashlib
import argparse
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify, \
        send_from_directory, make_response, send_file

from hparams import hparams
from audio import load_audio, combine_audio
from synthesizer import Synthesizer
from utils import str2bool, prepare_dirs, makedirs, add_postfix

import socket
from myipcheck import change_IP_in_HTML
from aboutAudio import mix_audio_withPATH, combine_audio_pydub, create_alarm, create_briefing, create_birthday
from aboutText import combine_alarm_text, combine_briefing_text, combine_birthday_text
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

member_id = 1
method_id = 0

ROOT_PATH = "web"
AUDIO_DIR = "audio"
AUDIO_PATH = os.path.join(ROOT_PATH, AUDIO_DIR)

base_path = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(base_path, 'web\\static')

global_config = None
synthesizer = Synthesizer()
app = Flask(__name__, root_path=ROOT_PATH, static_url_path='')
CORS(app)

###########################################################################################

def slice_text(input_text):
    MaxLen = 50
    MinLen = 10
    # . 단위로 자르기
    textList = input_text.split('.')
    #del(textList[-1])

    sliced_textList = []
    for text in textList.copy():
        if len(text) > MaxLen:
            # ,가 있는지 확인하기
            idx = text.find(',', 0, len(text))
            while idx != -1:
                # , 단위로 자르기
                nextIdx = text.find(',', idx + 1, len(text))

                # 자른부분 넣기
                if nextIdx == -1:
                    # 잘랐는데도 길이가 긴 것에 대해서 처리, 50 이상이면 2등분, 100이상이면 3등분 이런 식으로 자르기
                    if len(text[idx + 1:len(text)]) > MaxLen:
                        copytext = text[idx + 1:len(text)]
                        div = len(copytext)/(len(copytext)/MaxLen)
                        prefix_idx = 0
                        for idx in range(len(copytext)):
                            # N등분 한 것에서 공백을 발견하면 자르기
                            if copytext[idx] == ' ' and (idx - prefix_idx > div or idx == len(copytext) - 1):
                                sliced_textList.append(copytext[prefix_idx:idx])
                                prefix_idx = idx + 1
                    else:
                        sliced_textList.append(text[idx + 1:len(text)])
                else:
                    if len(text[idx+1: nextIdx]) > MaxLen:
                        copytext = text[idx+1: nextIdx]
                        div = len(copytext) / (len(copytext) / MaxLen)
                        prefix_idx = 0
                        for idx in range(len(copytext)):
                            if copytext[idx] == ' ' and (idx - prefix_idx > div or idx == len(copytext) - 1):
                                sliced_textList.append(copytext[prefix_idx:idx])
                                prefix_idx = idx + 1
                    else:
                        sliced_textList.append(text[idx+1: nextIdx])

                # Idx 갱신
                idx = nextIdx
        else:
            sliced_textList.append(text)


    while '' in sliced_textList:
        sliced_textList.remove('')
    while '.' in sliced_textList:
        sliced_textList.remove('.')
    while ' ' in sliced_textList:
        sliced_textList.remove(' ')

    return sliced_textList

def audio_clear():
    for model_name in ['손석희', '유인나', '코퍼스','김난희', '이주형']:
        CUR_PATH = os.getcwd()
        relative_dir_path = os.path.join(AUDIO_DIR, model_name)
        
        real_path = os.path.join(CUR_PATH, ROOT_PATH)
        real_path = os.path.join(real_path, relative_dir_path)
        files = os.listdir(real_path)
        for f in files:
            DEL_PATH = os.path.join(real_path,f)
            os.remove(DEL_PATH)

###########################################################################################

def match_target_amplitude(sound, target_dBFS):
   change_in_dBFS = target_dBFS - sound.dBFS
   return sound.apply_gain(change_in_dBFS)

def amplify(path, keep_silence=300):
    sound = AudioSegment.from_file(path)

    nonsilent_ranges = pydub.silence.detect_nonsilent(
            sound, silence_thresh=-50, min_silence_len=300)

    new_sound = None
    for idx, (start_i, end_i) in enumerate(nonsilent_ranges):
        if idx == len(nonsilent_ranges) - 1:
            end_i = None

        amplified_sound = \
                match_target_amplitude(sound[start_i:end_i], -20.0)

        if idx == 0:
            new_sound = amplified_sound
        else:
            new_sound = new_sound.append(amplified_sound)

        if idx < len(nonsilent_ranges) - 1:
            new_sound = new_sound.append(sound[end_i:nonsilent_ranges[idx+1][0]])

    return new_sound.export("out.mp3", format="mp3")

def generate_audio_response(textList, speaker_id, alarm_id):
    #global global_config
    #model_name = os.path.basename(global_config.load_path)
    #iskorean=global_config.is_korean
    audio_clear()

    global member_id, method_id
    if member_id != speaker_id:
        
        if speaker_id == 0:
            if not (member_id==0):
                if member_id != -1:
                    synthesizer.close()
                synthesizer.load('logs/backup_log/son+yuinna', 2)
        elif speaker_id == 3:
            if not (member_id==3):
                if member_id != -1:
                    synthesizer.close()
                synthesizer.load('logs/backup_log/new_inna+kss+leejh+nandong2',4)
        else:
            if not (member_id==1 or member_id==2 or member_id==4):
                if member_id != -1:
                    synthesizer.close()
                synthesizer.load('logs/backup_log/new_inna+kss+leejh', 3)
       
        member_id = speaker_id      

    if speaker_id==0:
        model_name='손석희'
        #speaker_id=0        
    elif speaker_id==1:
        model_name='유인나'
        speaker_id=0
    elif speaker_id==2:
        model_name='코퍼스' #한국어 코퍼스
        speaker_id=1
    elif speaker_id==3:
        model_name='김난희'
        #speaker_id=3
    else:
        model_name='이주형'
        speaker_id=2

    ###########################################################################################
    # 이 부분 반목문 돌림

    textcnt = 0 # 몇번째 텍스트인지 확인 용도
    audio_list = [] #체크 용도
    print(textList)
    for text in textList:
        # hashed_text = hashlib.md5(text.encode('utf-8')).hexdigest() # 텍스트 
        hashed_text = "{}".format(str(textcnt))
        
        # 이 부분을 반복문
        # 이 부분이 경로 생성 하는 부분
        relative_dir_path = os.path.join(AUDIO_DIR, model_name)
        relative_audio_path = os.path.join(
                relative_dir_path, "{}.{}.wav".format(hashed_text, speaker_id))
        real_path = os.path.join(ROOT_PATH, relative_audio_path)
        
        makedirs(os.path.dirname(real_path))
        
        if not os.path.exists(add_postfix(real_path, 0)):
            try:
                #audio는 파일명임
                audio = synthesizer.synthesize(
                        [text], paths=[real_path], speaker_ids=[speaker_id],
                        attention_trim=True)[0]
                audio_list.append(audio)
            except:
                return jsonify(success=False), 400
            
        
        textcnt +=1
    
    ###########################################################################################

    # 음성 합치기
    # 합친 음성 이름은 'output.wav'
    CUR_PATH = os.getcwd()
    #print(CUR_PATH) # audio 이름 체크용
    FILE_PATH = os.path.join(AUDIO_PATH, model_name)
    #print(FILE_PATH) # audio 이름 체크용
    print("method {} 실행중".format(method_id))
    alarm_type = 0
    alarm_id -= 1

    if (method_id == 1) or (method_id == 2):  # basic
        combine_audio(os.path.join(CUR_PATH, FILE_PATH))
    elif method_id == 3:  # morning_call
        combine_audio(os.path.join(CUR_PATH, FILE_PATH))  # web\audio\model_name\output.wav
        if alarm_id == 0 or alarm_id == 1 or alarm_id == 2 or alarm_id == 3:
            alarm_type = 0
        else:
            alarm_id = (alarm_id - 4)
            alarm_type = 1
        create_alarm(alarm_id, model_name, alarm_type) # bgm_select, model_name, type
    elif method_id == 4:  # briefing
        combine_audio(os.path.join(CUR_PATH, FILE_PATH))  # web\audio\model_name\output.wav
        create_briefing(alarm_id, model_name) # bgm_select, model_name, #0 1 2 3
    elif method_id == 5:  # birthday
        combine_audio(os.path.join(CUR_PATH, FILE_PATH))  # web\audio\model_name\output.wav
        create_birthday(0, model_name) # bgm_select, model_name, #0 1 2 3

    #print(os.path.join(CUR_PATH, FILE_PATH))
    #print(TEST_PATH)

    ###########################################################################################

       return send_file(
        os.path.join('audio', model_name, 'output.wav'),
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename=hashed_text + ".wav")

    ###########################################################################################

    # 합친 파일 불러와서 audio에 넣기
    response = make_response(os.path.join('web', 'audio', model_name, 'output.wav'))
    response.headers['Content-Type'] = 'audio/wav'
    response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
    return response


@app.route('/')
def menu():
    audio_clear()
    return render_template('index_greatness.html')

@app.route('/basics')
def index():
    global method_id
    method_id = 1
    text = request.args.get('text') or "듣고 싶은 문장을 입력해 주세요."
    return render_template('index2.html', text=text)

@app.route('/lettering')
def lettering():
    global method_id
    method_id = 2
    text = request.args.get('text') or " "
    return render_template('lettering.html', text=text)

@app.route('/alarm')
def alarm():
    return render_template('alarm.html')

@app.route('/alarm_morningcall')
def alarm_mo():
    global method_id
    method_id = 3
    text = request.args.get('text') or "노래 번호 + 시간 + 내가 듣고 싶은 말 을 입력해 보세요"
    return render_template('alarm_morningcall.html', text=text)

@app.route('/alarm_brief')
def alarm_br():
    global method_id
    method_id = 4
    text = request.args.get('text') or "노래 번호 + 시간 + 오늘 일정 을 입력해 보세요"
    return render_template('alarm_brief.html', text=text)

@app.route('/alarm_birthday')
def alarm_bi():
    global method_id
    method_id = 5
    text = request.args.get('text') or "이름을 등록해주세요"
    return render_template('alarm_birthday.html', text=text)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/generate')
def view_method():
    global method_id, alarm_id 

    text = request.args.get('text')
    
    #1:basic, 2:lettering, 3:morning, 4:briefing, 5:alarm
    alarm_id = 0
    if method_id == 3:
        text, alarm_id = combine_alarm_text(text)
    elif method_id == 4:
        text, alarm_id = combine_briefing_text(text)
    elif method_id == 5:
        text = combine_birthday_text(text)
    
    textList = slice_text(text)
    
    speaker_id = int(request.args.get('speaker_id'))

    if text:
        return generate_audio_response(textList, speaker_id, alarm_id)
    else:
        return {}

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(
            os.path.join(static_path, 'js'), path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(
            os.path.join(static_path, 'css'), path)

@app.route('/audio/<path:path>')
def send_audio(path):
    return send_from_directory(
            os.path.join(static_path, 'audio'), path)


@app.route('/download/<path:path>')
def send_download(path):
    return send_from_directory(
            os.path.join(static_path, 'download'), path)

@app.route('/basic_source/<path:path>')
def send_basic_source(path):
    return send_from_directory(
            os.path.join(static_path, 'basic_source'), path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory(
            os.path.join(static_path, 'images'), path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_path',required=False)
    parser.add_argument('--checkpoint_step', default=None, type=int)
    parser.add_argument('--num_speakers', default=5, type=int)
    parser.add_argument('--port', default=51000, type=int)
    parser.add_argument('--debug', default=False, type=str2bool)
    parser.add_argument('--is_korean', default=True, type=str2bool)
    config = parser.parse_args()

    #if os.path.exists(config.load_path):
    #    prepare_dirs(config, hparams)

    #    global_config = config
    #    synthesizer.load(config.load_path, config.num_speakers, config.checkpoint_step)
    #else:
    #   print(" [!] load_path not found: {}".format(config.load_path))
    
    MY_IP = socket.gethostbyname(socket.gethostname())
    change_IP_in_HTML() #main.js는 따로 바꿔주기
    synthesizer.load('logs/backup_log/new_inna+kss+leejh', 3)
    app.run(host=MY_IP, port=8888)  # debug=True debug=config.debug 하면 수정사항이 실시간으로 반영됨

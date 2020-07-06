## librosa 사용하기
## 현재는 librosa 사용하면 .wav파일만 불러올 수 있음
## 불러오기 : librosa.load()
## 합치기(join) : librosa.append()
import librosa
import numpy as np
from pydub import AudioSegment
import os

###################################################################
############################# librosa #############################
###################################################################
# speaker_id : 0 - 손석희, 1 - 유인나, 2 - 코퍼스, 3 - 난희, 4 - 주형
# 받을 때 번호 필요 없음
def combine_audio_librosa(INPUT_PATH):
    CUR_PATH = os.getcwd()
    AUDIO_DIR_PATH = os.path.join(CUR_PATH, INPUT_PATH)

    # 경로에 파일이 없으면 실행 안함
    if os.path.exists(AUDIO_DIR_PATH):
        FILE_PATHS = os.listdir(AUDIO_DIR_PATH)     # audio 폴더안에 있는 파일/폴더 이름 불러오기
        WAVE_PATHS = []                             # .wav 파일만 남기기
        waves = []                                  # 불러온 .wav 파일들

        # .wav 파일만 남기고 제거
        for paths in FILE_PATHS:
            if paths.find('.wav') != -1:
                WAVE_PATHS.append(paths)

        # .wav 파일 불러오기
        for paths in WAVE_PATHS:
                waves.append(librosa.load(AUDIO_DIR_PATH + "\\" + paths))

        # .wav 파일 합치기
        # 첫번째 파일에다가 계속 append 하는 형식으로 함
        z, sr = waves[0]

        for i in range(1, len(waves)):
            z = np.append(z, waves[i][0])

        # 파일 출력
        OUTPUT_WAVE_PATH = os.path.join(AUDIO_DIR_PATH, "output.wav")
        librosa.output.write_wav(OUTPUT_WAVE_PATH, z, sr)

    else:
        print("파일이 없습니다.")

###################################################################


# 짧은 음원 길이에 맞추기
def modulate_length(sound1, sound2):
    len1 = len(sound1)
    len2 = len(sound2)
    print("len1 : {}".format(len1))
    print("len2 : {}".format(len2))
    if len1 > len2:
        return sound1[:len2], sound2
    else:
        return sound1, sound2[:len1]

# 음원 볼륨 조절
def modulate_volume(sound, dB):
    return sound + dB

def join_audio(sound1, sound2):
    return sound1 + sound2

# 음원 볼륨
def mix_audio_withSound(sound1, sound2, mod_vol1, mod_vol2):
    # AudioSegment.ffmpeg = "/"
    # sound1, sound2 = modulate_length(sound1, sound2)

    sound1 = modulate_volume(sound1, mod_vol1)
    sound2 = modulate_volume(sound2, mod_vol2)

    mix_sound = AudioSegment.overlay(sound1, sound2)
    return mix_sound
    # mix_wav.export(os.path.join(DIR_PATH, 'mix_result_-3dB.wav'), format='wav')

def mix_audio_withPATH(DIR_PATH, WAV_NAME1, WAV_NAME2, mod_vol1, mod_vol2):
    # AudioSegment.ffmpeg = "/"
    sound1_path = os.path.join(DIR_PATH, WAV_NAME1)
    wav2_path = os.path.join(DIR_PATH, WAV_NAME2)
    wav1 = AudioSegment.from_wav(sound1_path)
    wav2 = AudioSegment.from_wav(wav2_path)

    wav1, wav2 = modulate_length(wav1, wav2)
    wav1 = modulate_volume(wav1, mod_vol1)
    wav2 = modulate_volume(wav2, mod_vol2)

    mix_wav = AudioSegment.overlay(wav1, wav2)
    # return mix_wav
    mix_wav.export(os.path.join(DIR_PATH, 'mix_result_-3dB.wav'), format='wav')

def create_alarm(bgm_select, model_name, alarm_type):
    # 음성 파일-> web/output.py
    # CUR_PATH = os.getcwd()
    AUDIO_PATH = os.path.join('web', 'audio', model_name,'output.wav')
    print('AUDIO_PATH: ', AUDIO_PATH)
    BGM_BASE_PATH = os.path.join('web', 'static', 'basic_source', 'alarm')
    print('BGM_BASE_PATH: ', BGM_BASE_PATH)
    OUTPUT_PATH = os.path.join('web', 'static', 'download', 'morning_call')
    print('OUTPUT: ', OUTPUT_PATH)

    base_sound = AudioSegment.from_wav(AUDIO_PATH)
    base_sound += 10
    result = base_sound
    # 기본 알람음 + 음성
    if alarm_type == 0:
        BGM_BASE_PATH = os.path.join(BGM_BASE_PATH, 'type0')
        if bgm_select >= 0 or bgm_select < 4:
            alarm_bgm = AudioSegment.from_wav(os.path.join(BGM_BASE_PATH, 'alarm{}.wav'.format(bgm_select)))
            if bgm_select == 3:
                alarm_bgm += 10
            else:
                alarm_bgm -= 10

            result = (alarm_bgm + base_sound) + (alarm_bgm + base_sound)
        else:
            print('해당 알람음이 없습니다.')
    # 배경 알람음 + 음성
    elif alarm_type == 1:
        BGM_BASE_PATH = os.path.join(BGM_BASE_PATH, 'type1')
        if (bgm_select >= 0) and (bgm_select < 3):
            alarm_bgm = AudioSegment.from_wav(os.path.join(BGM_BASE_PATH, 'alarm{}.wav'.format(bgm_select)))
            if bgm_select == 0:
                alarm_bgm += 10
                result = alarm_bgm[:30000]
            elif bgm_select == 1:
                result = alarm_bgm[:30000]
            elif bgm_select == 2:
                result = alarm_bgm[:30000]

            for i in range(len(alarm_bgm) // 10000):
                result = AudioSegment.overlay(result, base_sound, position=i*10000)

        else:
            print('해당 알람음이 없습니다.')

    result.export(os.path.join(OUTPUT_PATH, 'created_alarm.wav'), format='wav')
    result.export(AUDIO_PATH, format='wav')

    return result

def create_briefing(bgm_select, model_name):
    AUDIO_PATH = os.path.join('web', 'audio', model_name, 'output.wav')
    print('AUDIO_PATH: ', AUDIO_PATH)
    BGM_BASE_PATH = os.path.join('web', 'static', 'basic_source', 'briefing')
    print('BGM_BASE_PATH: ', BGM_BASE_PATH)
    OUTPUT_PATH = os.path.join('web', 'static', 'download', 'briefing')
    print('OUTPUT: ', OUTPUT_PATH)

    base_sound = AudioSegment.from_wav(AUDIO_PATH)
    base_sound += 10
    result = base_sound
    if (bgm_select >= 0) and (bgm_select < 4):
        briefing_bgm = AudioSegment.from_wav(os.path.join(BGM_BASE_PATH, 'briefing{}.wav'.format(bgm_select)))
        briefing_bgm = briefing_bgm[:30000]
        result = AudioSegment.overlay(briefing_bgm, base_sound, position=3000)
    else:
        print('해당 알람음이 없습니다.')

    result.export(os.path.join(OUTPUT_PATH, 'created_alarm.wav'), format='wav')
    result.export(AUDIO_PATH, format='wav')
    return result

def create_birthday(bgm_select, model_name):
    AUDIO_PATH = os.path.join('web', 'audio', model_name, 'output.wav')
    print('AUDIO_PATH: ', AUDIO_PATH)
    BGM_BASE_PATH = os.path.join('web', 'static', 'basic_source', 'birthday')
    print('BGM_BASE_PATH: ', BGM_BASE_PATH)
    OUTPUT_PATH = os.path.join('web', 'static', 'download', 'birthday')
    print('OUTPUT: ', OUTPUT_PATH)

    base_sound = AudioSegment.from_wav(AUDIO_PATH)
    base_sound += 10
    result = base_sound
    if (bgm_select >= 0) and (bgm_select < 3):
        birthday_bgm = AudioSegment.from_wav(os.path.join(BGM_BASE_PATH, 'birthday{}.wav'.format(bgm_select)))
        birthday_bgm -= 15
        # briefing_bgm = briefing_bgm[:30000]
        result = AudioSegment.overlay(birthday_bgm, base_sound, position=3000)
        result = AudioSegment.overlay(result, base_sound, position=35000)
    else:
        print('해당 알람음이 없습니다.')

    result.export(os.path.join(OUTPUT_PATH, 'created_alarm.wav'), format='wav')
    result.export(AUDIO_PATH, format='wav')
    return result

def combine_audio_pydub(DIR_PATH):
    if os.path.exists(DIR_PATH):
        FILE_PATHS = os.listdir(DIR_PATH)  # audio 폴더안에 있는 파일/폴더 이름 불러오기
        WAVE_PATHS = []  # .wav 파일만 남기기
        waves = []  # 불러온 .wav 파일들

        # .wav 파일만 남기고 제거
        for paths in FILE_PATHS:
            if paths.find('.wav') != -1:
                WAVE_PATHS.append(paths)

        # .wav 파일 불러오기
        for paths in WAVE_PATHS:
            waves.append(AudioSegment.from_wav(os.path.join(DIR_PATH, paths)))

        # .wav 파일 합치기
        # 첫번째 파일에다가 계속 append 하는 형식으로 함
        sound = waves[0]

        if len(waves) > 1:
            for i in range(1, len(waves)):
                sound += sound[i]

        # 파일 출력
        OUTPUT_WAVE_PATH = os.path.join(DIR_PATH, "output.wav")
        sound.export(OUTPUT_WAVE_PATH, format='wav')
    else:
        print("파일이 없습니다.")


# combine_audio("audio")
# mix_audio('audio', '0.wav', '1.wav')
# create_alarm(2, '코퍼스', 1)  # bgm , model, type


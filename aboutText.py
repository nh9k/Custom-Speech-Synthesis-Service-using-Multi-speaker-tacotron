# -*- coding: UTF-8 -*-
def sliceText(inputText):
    # inputText = "파티장에 들어서자마자 나는 주인을 찾으려 했다. 한두 사람 붙잡고 그의 소재를 물었지만, 놀란 얼굴로 나를 보면서 그의 소재에 대해 아는 바가 없다고 하도 격렬하게 부인하기에 하는 수 없이 칵테일 테이블 쪽으로 슬금슬금 자리를 옮겨갈 수밖에 없었는데, 그곳은 외톨이가 혼자임을 들키거나 할 일 없어 보이지도 않으면서 얼쩡거릴 수 있는 유일한 장소였다. 한잔 마시고 확 취해서 어색함을 날려버리려던 참에 조던 베이커가 나타났다. 그녀는 저택에서 나와 대리석 계단 꼭대기에 서서 몸을 약간 뒤로 젖힌 채, 경멸과 흥미가 뒤섞인 눈초리로 정원을 내려다보고 있었다. 환영을 받든 아니든, 지나가는 사람한테 말 한마디라도 건네려면 일단 누군가와 함께 있어야 한다는 생각이 들었다."
    MaxLen = 50
    MinLen = 10

    # 먼저 '.' 단위로 자르기
    textList = inputText.split('.')
    # del(textList[-1])

    sliced = []
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
                            if copytext[idx] == ' ' and (idx - prefix_idx > div or idx == len(copytext) - 1):
                                sliced.append(copytext[prefix_idx:idx])
                                prefix_idx = idx + 1
                    else:
                        sliced.append(text[idx + 1:len(text)])
                else:
                    if len(text[idx+1: nextIdx]) > MaxLen:
                        copytext = text[idx+1: nextIdx]
                        div = len(copytext) / (len(copytext) / MaxLen)
                        prefix_idx = 0
                        for idx in range(len(copytext)):
                            if copytext[idx] == ' ' and (idx - prefix_idx > div or idx == len(copytext) - 1):
                                sliced.append(copytext[prefix_idx:idx])
                                prefix_idx = idx + 1
                    else:
                        sliced.append(text[idx+1: nextIdx])

                # Idx 갱신
                idx = nextIdx
        else:
            sliced.append(text)


    # 체크용 구문
    print('\n\n')
    for text in textList:
        print(text, "\n길이 : ", len(text))
    print('\n\n')
    for text in sliced:
        print(text, "\n길이 : ", len(text))

    return sliced

def alarm_text_slice(input_text):
    # [알람 기입 양식]
    # xx시 xx분 알람내용
    idx = input_text.find('번')
    select_num = input_text[idx-1]

    idx = input_text.find('시')
    hour = input_text[idx - 2:idx]
    idx = input_text.find('분')
    minute = input_text[idx - 2:idx]
    idx = input_text.find(' ', idx)
    contents = input_text[idx + 1:]

    int_hour = int(hour)
    int_minute = int(minute)
    if (int_hour >= 0) and (int_hour < 12):
        hour = '오전 {}'.format(int_hour)
    elif int_hour > 12:
        hour = '오후 {}'.format(int_hour - 12)

    slice_list = [hour, minute, contents]
    return slice_list, int(select_num)

def combine_briefing_text(input_text):
    info_list, alarm_id = alarm_text_slice(input_text)
    #print("[유인나버전]")
    text = '안녕하세요 기분 좋은 날이에요. 오늘 오후는 13도로 아주 맑은 날씨에요. ' \
           '오늘은 {}시 {}분에 {}가 있어요 잊지마세요. ' \
           '이상으로 오늘의 브리핑을 마칠게요.'.format(info_list[0], info_list[1], info_list[2])
    return text, alarm_id

def combine_alarm_text(input_text):
    info_list, alarm_id = alarm_text_slice(input_text)
    text = '{}시 {}분 입니다. {}.'.format(info_list[0], info_list[1], info_list[2])
    return text, alarm_id

def combine_birthday_text(input_text):
    text = '축하합니다. 오늘은 당신이 태어난 날이에요. {}님 생일 축하합니다.'.format(input_text)
    return text

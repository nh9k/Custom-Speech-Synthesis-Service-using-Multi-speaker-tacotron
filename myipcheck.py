# -*- coding: utf-8 -*-
import socket
import os

def change_IP_in_HTML():
    # input: INPUT_DIR_PATH
    # IP 주소 구하기, IP 주소는 str형태로 되어 있음
    # Local IP, gethostname() 이랑 getfqdn() 같음
    local_IP = socket.gethostbyname(socket.gethostname())

    # WLAN IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    WLAN_IP = s.getsockname()[0]
    print("Local IP : " + local_IP)
    print("WLAN IP : " + WLAN_IP)

    # ----------------------------------------------------------------
    # html 파일 경로 잡기
    # ----------------------------------------------------------------
    # INPUT_DIR_PATH ==> ex) web\\templates
    # DIR_PATH = os.path.join('web','templates') 도 가능
    # ----------------------------------------------------------------
    # DIR_PATH = os.path.join(os.getcwd(), INPUT_DIR_PATH)

    DIR_PATH = os.path.join('web','templates')
    FILE_DIR_NAMES = os.listdir(DIR_PATH)  # audio 폴더안에 있는 파일/폴더 이름 불러오기
    HTML_NAMES = []                        # HTML 파일 이름만 저장할 리스트
    for paths in FILE_DIR_NAMES:
        if paths.find('.html') != -1:
            HTML_NAMES.append(paths)

    print("[바꾼 html 파일 리스트]")
    for html in HTML_NAMES:
        print(os.path.join(DIR_PATH, html))
        with open(os.path.join(DIR_PATH, html), 'r', encoding='UTF-8') as html_file:
            lines = html_file.readlines()

            for i in range(len(lines)):
                ip_pos = lines[i].find('<a href="http://1')
                if ip_pos != -1:
                    ip_pos += 16
                    end_pos = lines[i].find(':', ip_pos)
                    left_substr = lines[i][:ip_pos]
                    right_substr = lines[i][end_pos:]
                    lines[i] = left_substr + WLAN_IP + right_substr  # Local_IP 와 WLAN_IP 중 선택해서 사용

        with open(os.path.join(DIR_PATH, html), 'w', encoding='UTF-8') as html_file:
            # print(lines)
            html_file.writelines(lines)
    
    ##main.js의 ip 수정
    #print(os.path.join('web\static\js', 'main.js'))
    #with open(os.path.join('web\static\js', 'main.js'), 'r', encoding='UTF-8') as js_file:
    #        lines = js_file.readlines()

    #        for i in range(len(lines)):
    #            ip_pos = lines[i].find('var myipcheck')
    #            if ip_pos != -1:
    #                ip_pos += 17
    #                end_pos = lines[i].find("'", ip_pos)
    #                end_pos = lines[i].find("'", end_pos)
    #                left_substr = lines[i][:ip_pos]
    #                right_substr = lines[i][end_pos:]
    #                lines[i] = left_substr + WLAN_IP + right_substr  # Local_IP 와 WLAN_IP 중 선택해서 사용

    #with open(os.path.join('web\\static\\js', 'main.js'), 'w', encoding='UTF-8') as js_file:
    #        # print(lines)
    #        js_file.writelines(lines)


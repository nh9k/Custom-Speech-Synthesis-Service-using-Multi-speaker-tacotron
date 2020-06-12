# Custom-Speech-Synthesis-Service-using-Multi-speaker-tacotron

Develop Custom Speech Synthesis Service using Deep learning (April 2019 – Sep 2019)  
We won an overwhelming first place in the competition (Electronic Engineering Creative Research Convergence Design), and won the grand prize (Sep, 2019)

<br/>  

## Additional Implementation from our team (Custom-Speech-Synthesis Service)

- Learning with data that includes Seok-Hee Son (News anchor), In-Na Yoo (Actress), Korean corpus, Ju-Hyung Lee (Team member), and Nan-Hee Kim (Team member)  

- Created web services([Demo video](https://nh9k.github.io/ml/Custom-Service.html)) using `flask` on the basis of [carpedm20/Multi-Speaker Tacotron in TensorFlow](https://github.com/carpedm20/multi-speaker-tacotron-tensorflow) through good model learning results, and its contents are `basic synthesizer`, `letter writing`, `briefing`, `alarm service` 

- Called up `learned log(.ckpt)` with a `good speaker combination` and performed speech synthesis by `switching model` during the service

- The `learning` was done on the `Linux server`, and the `demonstration`([Demo video](https://nh9k.github.io/ml/Custom-Service.html)) was done on the `Windows server`

- To use for service, created phrase and composed BGM with synthesized voice using `librosa`

- This is the [source code](https://github.com/nh9k/Custom-Speech-Synthesis-Service-using-Multi-speaker-tacotron) of the computer that I demonstrated (`Windows system`)

<br/>  

## Helpful command

### Preparing datasets

#### Slice audio file with silence  

```
python3 -m audio.silence --audio_pattern "./datasets/yuinna/audio/*.wav" --method=pydub`
```
- Cuted into silent sections and learned with matched lines for voice file.

#### Create a file : numpy, npz  

```
python3 -m datasets.generate_data ./datasets/son/alignment.json
```
- alignment is lines

#### Concatenate WAV file (Method: SoX v14.4.1)  
 
```
sox input1.wav input2.wav input3.wav output.wav
```
- you can also combine wav files using `FFMPEG`.

#### Remove noise (Method: SoX v14.4.1)  

```
sox input.wav -n noiseprof noise.prof
sox input.wav output.wav noisered noise.prof 0.21
```

<br/>  

### Training

#### Train a model  

```
python3 train.py --data_path ./datasets/yuinna,./datasets/kss,./datasets/nandong
```

#### Tensorboard  

```
tensorboard --logdir=logs\son+yuinna
```

<br/>  

### Synthesis audio & Demo sites

#### Synthesis  

```
python synthesizer.py --load_path logs/son+yuinna --text "반갑습니다" --num_speakers 2 --speaker_id 0
```
- id 0 is Seok-Hee Son.
- id 1 is In-Na Yoo.

#### APP (Demo Web page)  

```
python app.py --load_path logs/son+yuinna --num_speakers=2
```  



<br/>  

## some issues
#### Librosa version problem
- Learning (Linux server, Librosa 0.6.2, 0.6.3)
```
#librosa 0.6.2, 0.6.3
def save_audio(audio, path, sample_rate=None):
    #audio *= 32767 / max(0.01, np.max(np.abs(audio)))
    librosa.output.write_wav(path, audio, #.astype(np.int16)
            hparams.sample_rate if sample_rate is None else sample_rate)

    print(" [*] Audio saved: {}".format(path))
```

- Demo (Window server, Librosa 0.5.1)
```
#librosa 0.5.1
def save_audio(audio, path, sample_rate=None):
    audio *= 32767 / max(0.01, np.max(np.abs(audio)))
    librosa.output.write_wav(path, audio.astype(np.int16),
            hparams.sample_rate if sample_rate is None else sample_rate)

    print(" [*] Audio saved: {}".format(path))
```

<br/> 

#### Good combination of speaker  

- Model name (speaker)
    - son (Seok-Hee Son)  
    - yuinna (In-Na Yoo)  
    - new_inna (In-Na Yoo, version2) 
    - nandong (Nan-Hee Kim, team member) 
    - nandong2 (Nan-Hee Kim, team member, version 2)  
    - LEEJH (Ju-Hyung Lee, team member)  
    - kss (Korean corpus)  
    - hozzi (Ho-Yeon Kim, team member)
    
- About speaker
    - version2 is the results We've gone through more screening about lines with speech.
    - hozzi was unable to use because of poor learning results.
    - Son is the datasets of Newroom
        - 43700 lines / 11 hours
        - using `Google Cloud STT API` + handmade
    - new_inna is the datasets of audiobook
        - 3670 lines / 5 hours
        - handmade
    - kss is the provided datasets 
        - 12800 lines / 3 hours
    - LEEJH & nandong2
        - 2930 lines / 3 hours
        - recorded `The Old Man and the Sea` in a quiet environment  
        - handmade
    - hozzi
        - 550 lines / an hour
        - handmade

- Experiments
    - son + yuinna
    - son + yuinna + hozzi
    - son + hozzi
    - yuinna + kss
    - new_inna + kss + LEEJH
    - new_inna + kss + LEEJH + nandong
    - new_inna + kss + nandong2
    - new_inna + kss + LEEJH + nandong2  
    
- Best combination  
    - son + yuinna
        - son was the best result.
        - yuinna was the worst result
    - new_inna + kss + LEEJH
        - new_inna, kss, LEEJH were the best results.
    - new_inna + kss + LEEJH + nandong2
        - nandong2 were the best results.

<br/>  

## Prerequisites

There is a difference from [the original model github version](https://github.com/carpedm20/multi-speaker-tacotron-tensorflow/blob/master/requirements.txt).  
You can refer to [our version](#).

<br/>  

## Model

If you want to model-learning, you can refer to [our source code(Custom-Speech-Synthesis Service)](https://github.com/nh9k/Custom-Speech-Synthesis-Service-using-Multi-speaker-tacotron) or source code here.  

- [Multi-speaker-tacotron model](https://github.com/carpedm20/multi-speaker-tacotron-tensorflow)     

<br/>  

## Project demo & Presentation
[My blog demo video & PPT](https://nh9k.github.io/ml/Custom-Service.html)

<br/>  

## Real demo web page & Source Code
coming soon!

<br/>  

## References
Thank you so much,  
- [Multi-speaker-tacotron-tensorflow](https://github.com/carpedm20/multi-speaker-tacotron-tensorflow) / carpedm20      
- [딥러닝 음성합성 multi-speaker-tacotron(tacotron+deepvoice)설치 및 사용법](http://nblog.syszone.co.kr/archives/9416) / 서진우 님    
- [인공지능 deep voice를 이용한 TTS(음성합성) 구현하기 _ 손석희 앵커](http://melonicedlatte.com/machinelearning/2018/07/02/215933.html) / melonicedlatte     
- Older friend Hyun Kim from [Power Supply Robot Club](https://nh9k.github.io/control/PowerSupply-Robot-Club.html)   

<br/>  

## Team member
We've been through the whole process together, but main role is...   
[Nanhee Kim](https://github.com/nh9k): Learning and Making Web Service, Provided main idea.  
[Hoyeon Kim](https://github.com/mozzihozzi): To use for service, created phrase and composed BGM with synthesized voice, team learder   
[Juhyung Lee](https://github.com/darpa776): Got a good custom datasets, and selection     
  
<br/>  

## Author
Nanhee Kim / [@nh9k](https://github.com/nh9k) / [nh9k blog](https://blog.naver.com/kimnanhee97)
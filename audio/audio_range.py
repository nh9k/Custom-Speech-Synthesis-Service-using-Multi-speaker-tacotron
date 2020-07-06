import os
import argparse
import tqdm

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.py':
                    print(full_filename)
    except PermissionError:
        pass


def audio_range(_load_path, _min, _max):
    base_dir = _load_path

    for (path, dir, files) in os.walk(base_dir):
        for filename in tqdm.tqdm(files):
            print(filename)
            each_size = os.path.getsize(path + '/' + filename)
            print(filename, '  /   size is == ', each_size)

            ext = os.path.splitext(filename)[-1]
            if not ext == '.wav':
                print('This folder contains not audio file!! In audio folder, they must have only wav file!!')
                return

            print(os.getcwd())

            # 규정 사이즈 이상은 제거
            if not (_min <= each_size and each_size <= _max) :
                print(path + '/' + filename, ' is removed!!')
                os.remove( path + '/' + filename )



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_path', required=True)
    parser.add_argument('--min', default= 300000)
    parser.add_argument('--max', default=1600000)
    config = parser.parse_args()

    if not os.path.exists(config.load_path):
        print("wrong path!!")

    print (config.load_path)

    if config.load_path in 'kim_anchor':
        print("wrong path!! path must have kim_anchor")

    else :
        audio_range(config.load_path, config.min, config.max)

    # 텍스트에 아무 것도 없는 내용 제거 
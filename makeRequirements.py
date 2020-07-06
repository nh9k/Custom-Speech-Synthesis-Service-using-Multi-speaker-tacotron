package_name = []
package_ver = []

with open('requirements_.txt','r') as f:
    for line in f:
        for i, Word in enumerate(line.split()):
           if i==0:
               package_name.append(Word)
           elif i==1:
               package_ver.append(Word)
        print(package_name[-1], package_ver[-1])
f.close()

with open('requirements_ours.txt', 'w') as f:
    for size in range(len(package_name)):
        data = package_name[size] + "==" + package_ver[size] + "\n"
        f.write(data)
f.close()


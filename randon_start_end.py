import random
from numpy import zeros as npzeros
import matplotlib.pyplot as plt
import os
import re
#------------------------
from main import just_go

class area:
    def __init__(self,lb:list,ru:list) -> None:
        self.lb=lb
        self.ru=ru

    def generate_random_point(self, num):
        self.points = npzeros((num, 2))
        for i in range(num):
            x = random.uniform(self.lb[0], self.ru[0])
            y = random.uniform(self.lb[1], self.ru[1])
            self.points[i] = (x, y)
    
    def __len__(self):
        return len(self.points)

def test_and_save(area_list:list,radius,file_name,num):
    file_name_pure=file_name[:-4]
    step_list=[]

    for item in area_list:
        item.generate_random_point(num)


    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path_succ = os.path.join(script_dir, f'test_result\\{file_name_pure}\\success')
    folder_path_fail = os.path.join(script_dir, f'test_result\\{file_name_pure}\\fail')
    folder_path_result = os.path.join(script_dir, f'test_result\\{file_name_pure}')

    if not os.path.exists(folder_path_succ):
        os.makedirs(folder_path_succ)
    if not os.path.exists(folder_path_fail):
        os.makedirs(folder_path_fail)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot()
    
    i=0
    success=0
    for i in range(len(area_list[0])):

        a, b = random.sample(area_list, 2)
        start=a.points[i]
        end=b.points[i]

        result=just_go(start, end, radius, file=file_name,save=True,ax=ax, fig=fig,savename=str(i),folder_name=file_name_pure,rtn_step=True)
        ax.clear()
        i+=1
        if(result[0]):
            success+=1
        
        step_list.append(result[1])

    ax.clear()
    plt.plot(range(0,num),step_list,color="orange")
    ax.text(0.9, 0.9, f"success_rate:{success/num}", transform=ax.transAxes, ha='right', va='top', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round'))
    fig.savefig(f"{folder_path_result}\\summary.png")
    
    return success/num


def read(file_name, path_type='relative'):
        
        if(path_type == 'relative'):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            path = script_dir+"\\test_sets\\"+file_name

        print(path)

        f = open(path, mode='r', encoding="utf-8")
        if f == None:
            raise IOError
        
        target_name=f.readline()[:-1]
        area_list=[]

        while (1):
            line = f.readline()
            if(line == ""):
                break

            if "radius" in line:
                s = line.replace("radius:", "")
                radius=float(s)

            elif "num" in line:
                s = line.replace("num:", "")
                num=int(s)

            elif "(" in line:
                matches = re.findall(r'[-+]?\d*\.\d+|\d+',line)
                for i in range(len(matches)):
                    matches[i]=float(matches[i])

                if(len(matches)==4):
                    temp=area([*matches[:2]],[*matches[2:]])
                    area_list.append(temp)

            else:
                print("read_test_sets_warning")

        f.close()

        return test_and_save(area_list,radius,target_name,num)


print(read("7_shape_trap_test.txt")) #input_test_set_file here
pass

            
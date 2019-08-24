import os
import tkinter
from tkinter import filedialog
import binvox_rw
import draw



def selectFile():
    path_ = filedialog.askopenfilename(title='选择STL文件', filetypes=[('STL模型文件', '*.stl'), ('All Files', '*')])
    filepath.set(path_)
    select.set("file")
    
def selectPath():
    path_ = filedialog.askopenfilename(title='选择binvox文件', filetypes=[('binvox模型文件', '*.binvox'), ('All Files', '*')])
    path.set(path_)
    select.set("path")
    
def copyfile(filename):
    newfilename = os.getcwd() + "\\" + filename.split("/")[-1]
    print("copying file: " + filename)
    print("          to: " + newfilename)
    try:
        file = open(filename, "rb")
        new_file = open(newfilename, "wb")
    except:
        return False
    while True:
        content = file.read(1024)
        if len(content) == 0:
            break 
        new_file.write(content)
    file.close()
    new_file.close()
    return newfilename

def delfile(filename):
    if filename == False:
        pass
    else:
        print("del file: " + filename)
        os.remove(filename)
    
def startConvert():
    fileList = []
    if select.get() == "file":
        filename = copyfile(filepath.get())
        if filename != False:
            os.system(command.format(size = size.get(), filename = filename))
            delfile(filename)
            fileList.append(filename.lower().replace("stl", "binvox"))
    elif select.get() == "path":
        fileList.append(path.get().lower().replace("stl", "binvox"))
    return fileList

def readBinvodFile(filename):
    with open(filename, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)
    return model
    
def modelIng():
    filename = startConvert()
    model = readBinvodFile(filename[0])
    if drawTypr.get() == 'normal':
        import draw
        draw.viewer(model)
    elif drawTypr.get() == 'central':
        import drawCentral
        drawCentral.viewer(model)
    elif drawTypr.get() == 'random':
        import drawRandom
        drawRandom.viewer(model)
    



command = "binvox.exe -d {size} {filename}"

window = tkinter.Tk()
window.title('stl文件素体化')

filepath = tkinter.StringVar()
path = tkinter.StringVar()
select = tkinter.StringVar()
select.set("file")
size = tkinter.StringVar()
size.set(128)

drawTypr = tkinter.StringVar()
drawTypr.set("normal")

tkinter.Radiobutton(window, variable = select, value = "file").grid(row = 0, column = 0)
tkinter.Label(window, text = "文件地址").grid(row = 0, column = 1)
tkinter.Entry(window, textvariable = filepath, width = 50).grid(row = 0, column = 2)
tkinter.Button(window, text = "选择文件路径", command = selectFile).grid(row = 0, column = 3)
tkinter.Label(window, text = "或者：").grid(row = 1, column = 2)

tkinter.Radiobutton(window, variable = select, value = "path").grid(row = 2, column = 0)
tkinter.Label(window, text = "binvox文件").grid(row = 2, column = 1)
tkinter.Entry(window, textvariable = path, width = 50).grid(row = 2, column = 2)
tkinter.Button(window, text = "选择路径", command = selectPath).grid(row = 2, column = 3)


tkinter.Label(window, text = "分辨率").grid(row = 3, column = 1)
tkinter.Entry(window, textvariable = size, width = 4).grid(row = 3, column = 3)
tkinter.Scale(window, from_ = 0, to = 1024, orient = tkinter.HORIZONTAL, resolution = 32, length = 300, variable = size).grid(row = 3, column = 2)

tkinter.Radiobutton(window, text = "默认渲染（上红下绿）", variable = drawTypr, value = "normal").grid(row = 4, column = 2)
tkinter.Radiobutton(window, text = "中心渲染（上红下绿）", variable = drawTypr, value = "central").grid(row = 5, column = 2)
tkinter.Radiobutton(window, text = "随机渲染（上红下绿）", variable = drawTypr, value = "random").grid(row = 6, column = 2)

tkinter.Button(window, text = "开始", command = modelIng, width = 10).grid(row = 7, column = 2)


window.mainloop()
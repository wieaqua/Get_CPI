import json
import requests
import tkinter as tk
from tkinter import messagebox

def get_clink():
    '''
    clion download link
    '''
    with open('info.json', 'r', encoding='utf-8') as fp:
        content = json.load(fp)
        clon = content['CL']
        info = clon[0]

        version_id = info['version']
        build_id = info['build']

        for key in info.keys():
            if key == 'downloads':
                dl = info[key]
        
        for key in dl.keys():
            if key == 'windows':
                win = dl[key]
        link = win['link']

        return version_id, build_id, link 

def get_plink():
    '''
    pycharm link
    '''
    with open('info.json', 'r', encoding='utf-8') as fp:
        content = json.load(fp) # 得到一个字典
        pyp = content['PCP'] # 得到一个列表
        lastRelease = pyp[0] # 得到一个字典

        version_id = lastRelease['version'] # 版本号
        build_id = lastRelease['build']
    for key in lastRelease.keys():
        if key == 'downloads':
            download_links = lastRelease[key]
    
    for key in download_links.keys():
        if key == 'windows':
            win_d = download_links[key]

    for key in win_d.keys():
        if key == 'link':
            link = win_d[key]
    
    return version_id, build_id, link

def get_ilink():
    '''
    IDEA link
    '''
    with open('info.json', 'r', encoding='utf-8') as fp:
        content = json.load(fp) # 是一个字典
        iu = content['IIU'] # 得到一个列表
        info = iu[0] # 得到一个字典

        version_id  = info['version']
        build_id = info['build']

        for key in info.keys():
            if key == 'downloads':
               dl = info[key] # 得到一个字典
                
        for key in dl.keys():
            if key == 'windows':
                win = dl[key] # 字典
        link = win['link'] # 得到下载链接
        # print(link)

        return version_id, build_id, link

def get_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查是否有错误状态码
        content = response.json() # json 解析
        return content
    except requests.exceptions.RequestException as e:
        print("发生错误:", e)
        return None

def update_info():
    choice = choice_var.get()
    if choice == 'clion':
        url = "https://data.services.jetbrains.com/products/releases?code=CL&latest=true&type=release&build=&_=1686829656278"
        content = get_url_content(url)
        if content:
            with open('info.json', 'w', encoding='utf-8') as fp:
                json.dump(content, fp)
        version_id, build_id, link = get_clink()
        software = {'name': 'CLion', 'version': version_id, 'build': build_id, 'link': link}
        with open('version.json', 'w', encoding='utf-8') as fpid:
            json.dump(software, fpid)
    elif choice == 'pycharm':
        url = "https://data.services.jetbrains.com/products/releases?code=PCP&latest=true&type=release&build=&_=1686375295183"
        content = get_url_content(url)
        if content:
            with open('info.json', 'w', encoding='utf-8') as fp:
                json.dump(content, fp)
        version_id, build_id, link = get_plink()
        software = {'name': 'PyCharm', 'version': version_id, 'build': build_id, 'link': link}
        with open('version.json', 'w', encoding='utf-8') as fpid:
            json.dump(software, fpid)
    elif choice == 'idea':
        url = "https://data.services.jetbrains.com/products/releases?code=IIU&latest=true&type=release&build=&_=1686831326583"
        content = get_url_content(url)
        if content:
            with open('info.json', 'w', encoding='utf-8') as fp:
                json.dump(content, fp)
        version_id, build_id, link = get_ilink()
        software = {'name': 'IntelliJ IDEA', 'version': version_id, 'build': build_id, 'link': link}
        with open('version.json', 'w', encoding='utf-8') as fpid:
            json.dump(software, fpid)
    else:
        messagebox.showerror("错误", "无效的选择")
        return

    # content = get_url_content(url)
    if content:
        link_textbox.delete(1.0, tk.END)
        link_textbox.insert(tk.END, link)
        messagebox.showinfo("成功", f"{software['name']}下载链接已获取")


# 创建GUI窗口
window = tk.Tk()
window.title("Clion Pycharm IDEA 三款软件下载链接获取")
window.geometry("600x540")

# 创建选择框
choice_label = tk.Label(window, text="选择软件:")
choice_label.pack(pady=10)

choice_var = tk.StringVar()
choice_var.set("clion")  # 默认选择CLion

choice_combobox = tk.OptionMenu(window, choice_var, "clion", "pycharm", "idea")
choice_combobox.pack(pady=15)

# 创建文本框
link_textbox = tk.Text(window, height=15, width=60)
link_textbox.pack(pady=30)

# 创建更新按钮
update_button = tk.Button(window, text="获取链接", command=update_info)
update_button.pack(pady=20)

# 运行GUI事件循环
window.mainloop()
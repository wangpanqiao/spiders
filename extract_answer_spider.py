#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Anuo.
 
@License :   (C) Copyright 2018, Anuo's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   extract_answer.py
 
@Time    :   Feb 14,2019
 
@Desc    :   提取考试题目和答案的脚本，省去人工复制粘贴的麻烦事。
             提取的实例文件可查看 ..\files\182次设计美学模拟练习报告.html
 
'''


from bs4 import BeautifulSoup    # pip install beautifulsoup4
import os
import docx    # pip install python-docx


def get_answer(right_answer_node):
    '''提取答案'''

    if right_answer_node.pre != None:
        answer = right_answer_node.pre.string
    else:
        answer = right_answer_node.text

    index = answer.find("、")
    if index != -1:
        answer = answer[index + 1:].strip()

    return answer


def get_abcd_index(abcd):
    '''获取正确答案的索引'''

    abcd = abcd.lower()
    index = -1

    if abcd == "a":
        index = 0
    elif abcd == "b":
        index = 1
    elif abcd == "c":
        index = 2
    elif abcd == "d":
        index = 3

    return index


def extract_file(full_path, file_name):
    '''提取整个文件'''

    print("开始提取文件：" + file_name + "\n")
    txt_name = file_name.replace("html", "txt")
    txt_name = "提取\\" + txt_name
    soup_global = BeautifulSoup(open(full_path, "r", encoding="utf-8"), features="html.parser")
    topic = soup_global.find("div", attrs={"class":"part-title"}).string
    print(topic)
    content = topic + "\n"

    question_node_list = soup_global.find_all("div", attrs={"class":"question"})
    for i in range(len(question_node_list)):

        question_node = question_node_list[i]
        question_title_node = question_node.find("div", attrs={"class":"q-subject unselectable"})
        # 标题的标签是 pre 或 p，或者没有标签
        if question_title_node.p != None:
            question_title = question_title_node.p.string
        elif question_title_node.pre != None:
            question_title = question_title_node.pre.string
        else:
            question_title = question_title_node.string

        question_title = question_title.strip()   # 题目

        answer_node = question_node.find_all("div", attrs={"class":"q-text"})
        abcd = answer_node[1].pre.string.strip()
        index = get_abcd_index(abcd)

        if index == -1:  # 问答题
            question_and_answer = str(i + 1) + ". " + question_title + "\n参考答案：" + abcd
            print(question_and_answer)
        else:    # 单选题
            answer_node = question_node.find("ul", attrs={"class":"q-options unselectable"})
            answer_node_list = answer_node.find_all("li", attrs={"class":"q-option"})
            right_answer_node = answer_node_list[index]

            answer_content = get_answer(right_answer_node)  # 答案

            # 组合题目和答案
            # 选择题的题目中没有“】”
            my_index = question_title.find("】")
            if my_index == -1:
                question_and_answer = question_title + "【" + answer_content + "】"
            else:
                question_and_answer = question_title.replace("】", answer_content + "】")

            question_and_answer = str(i + 1) + ". " + question_and_answer   
            print(question_and_answer)

        content = content + question_and_answer + "\n"

        # 题目解析
        explain_node = question_node.find("div", attrs={"class":"q-text explain unselectable"})
        if explain_node != None:
            explain_txt = explain_node.text.replace("\n","")
            print(explain_txt)
            content = content + explain_txt + "\n"

    write_file(txt_name, content)


def write_file(txt_name, content):
    '''写入txt和word文件'''

    # 写入txt文件
    if os.path.exists(txt_name) == True:
        os.remove(txt_name)

    f = open(txt_name, "w", encoding="utf-8")
    f.write(content)
    f.close()

    # 写入word文件
    doc = docx.Document()
    doc.add_paragraph(content)

    doc_name = txt_name.replace(".txt",".docx") 
    if os.path.exists(doc_name) == True:
        os.remove(doc_name)

    doc.save(doc_name)

    print("\n")


if __name__ == '__main__':
    pathDir = "考试"    # 指定路径：运行前请设置此路径，可以是绝对路径或相对路径。
    file_list = os.listdir(pathDir)
    if len(file_list) > 0:
        # 检查路径是否存在，不存在则新建
        if os.path.exists("提取") == False:
            os.mkdir("提取")

        # 批量提取考试内容
        for file_name in file_list:
            if file_name.endswith(".html"):
                full_path = os.path.join(pathDir, file_name)
                extract_file(full_path, file_name)

    print("提取作业完成。")

with open(file = 'notes.txt', mode = 'r',encoding = "utf-8") as read_file:
    count = 1
    content = read_file.read()
    for i in content:
        if i == "\n":
            count +=1
    print(f"这个文件一共有{count}行")
    print(f"这个文件一共有{len(content)}个字符")

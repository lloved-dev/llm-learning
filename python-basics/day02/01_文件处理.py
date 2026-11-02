# 1:
with open('E:/works/检验/test.txt', 'r', encoding='utf-8') as f:
    content1 = f.readlines()
    if len(content1) < 3:
        print('文件行数不正确')
    else:
        print(content1[2].replace('\n', ''))

# 2:
with open('E:/works/检验/test.txt', 'r', encoding='utf-8') as s:
    count = 0
    while True:
        content2 = s.readline()
        if content2 == '':              # 读到空字符串 = 文件读完了
            print('文件不足三行')
            break
        if count == 2:
            content2 = content2.replace('\n', '')
            print(content2)
            break
        count += 1




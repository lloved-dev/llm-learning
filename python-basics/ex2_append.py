src = input("请输入一段话：")
with open("notes.txt", "a", encoding = "utf-8") as ad_file:
    ad_file.write("\n" + src)
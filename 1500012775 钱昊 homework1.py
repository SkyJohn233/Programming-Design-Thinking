# -*- coding: utf-8 -*-

# name Qian Hao 
# student ID：1500012775

def main():
	readingFromFile = open("50万人名名单.txt","r",encoding="utf-8",errors="ignore")
	contentFromFile = readingFromFile.read()
	readingFromFile.close()
	nameList = contentFromFile.split("\n")
	nameList2 = []
	for i in nameList:
		if len(i)<=4 :
			nameList2.append(i)
	nameList2.sort(key =  lambda x:len(x))
	# 计算出小于等于4的名字
	nameList = nameList2
	# print(nameList)
	nameDict = {}
	for i in nameList:
		if i[0] in nameDict:
			nameDict[i[0]] += 1
		else :
			nameDict[i[0]] = 1
	nameSortedList1 = sorted(nameDict.items(),key = lambda item:item[1],reverse=True)
	writeFile = open("question5-1.txt","w",encoding="utf-8",errors="ignore")
	writeFileNumber = open("question5-2.txt","w",encoding="utf-8",errors="ignore")
	for i in nameSortedList1:
		writeFile.write(i[0]+'\n')
		writeFileNumber.write(str(i[1])+'\n')
	writeFile.close()
	writeFileNumber.close()
	# 统计计算姓名的次数，降序排列
	nameDict = {}
	for i in nameList:
		substr = i[1:]
		for j in substr :
			if j in nameDict :
				nameDict[j] += 1
			else :
				nameDict[j] = 1
	nameSortedList2 = sorted(nameDict.items(),key = lambda item:item[1],reverse=True)
	writeFile = open("question6-1.txt","w",encoding="utf-8",errors="ignore")
	writeFileNumber = open("question6-2.txt","w",encoding="utf-8",errors="ignore")
	for i in nameSortedList2:
		writeFile.write(i[0]+'\n')
		writeFileNumber.write(str(i[1])+'\n')
	writeFile.close()
	writeFileNumber.close()
	# 统计计算名中出现字的次数，降序排列
	nameDict = {}
	for i in nameList:
		k = i[len(i)-1]
		if k in nameDict :
			nameDict[k] += 1
		else :
			nameDict[k] = 1
	nameSortedList3 = sorted(nameDict.items(),key = lambda item:item[1],reverse=True)
	writeFile = open("question7-1.txt","w",encoding="utf-8",errors="ignore")
	writeFileNumber = open("question7-2.txt","w",encoding="utf-8",errors="ignore")
	for i in nameSortedList3:
		writeFile.write(i[0]+'\n')
		writeFileNumber.write(str(i[1])+'\n')
	writeFile.close()
	writeFileNumber.close()
	# 统计计算姓名中最后一个字的出现字数，降序排列
	nameDict = {}
	for i in nameList:
		if len(i) > 2 and i[-1] == i[-2]:
			if i[-1] in nameDict:
				nameDict[i[-1]] += 1
			else :
				nameDict[i[-1]] = 1
	# print(nameDict)
	nameSortedList4 = sorted(nameDict.items(),key = lambda item:item[1],reverse=True)
	writeFile = open("question8-1.txt","w",encoding="utf-8",errors="ignore")
	writeFileNumber = open("question8-2.txt","w",encoding="utf-8",errors="ignore")
	for i in nameSortedList4:
		writeFile.write(i[0]+i[0]+'\n')
		writeFileNumber.write(str(i[1])+'\n')
	writeFile.close()
	writeFileNumber.close()
	# 统计计算名中两字重复出现的次数
	# print(nameSortedList2)
	# print(nameSortedList3)


if __name__ == '__main__':
	main()
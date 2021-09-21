import maze
#import camera
#import blu
from PIL import Image

# 미로 데이터화 함수
def makeMiroDataList(imList, resultM, reverseXY, finalCheck):
    array_xLength = 0
    countWidth = 0
    saveCountWidth = 0
    counterE = True
    if reverseXY == False:
        for y in range(0, len(imList)):
            for x in range(0, len(imList[y])):
                if imList[y][x] == 0:
                    countWidth += 1
                if imList[y][x] == 255 and countWidth != 0:
                    widthArray = []
                    if finalCheck: #마지막 실행에서의 최종 한칸
                        if countWidth > 4: #바꾸는 상수
                            widthArray.append(countWidth)
                        else:
                            widthArray.append(1)
                    else:
                        widthArray.append(countWidth)  # 칸 개수
                    if y == 0 and counterE:  # 첫번째 배열 예외 처리
                        widthArray.append(0)
                        saveCountWidth = x - countWidth  # 노드의 기준점
                        counterE = False
                    else:
                        widthArray.append((x - countWidth) - saveCountWidth)  # 기준점과 현재 노드 시작점과의 거리
                    widthArray.append(y)
                    if array_xLength < widthArray[0] + widthArray[1]:
                        array_xLength = widthArray[0] + widthArray[1]
                    resultM.append(widthArray)
                    countWidth = 0
    else:
        for x in range(0, len(imList[0])):
            for y in range(0, len(imList)):
                if imList[y][x] == 1:
                    countWidth += 1
                if imList[y][x] == 0 and countWidth != 0:
                    widthArray = []
                    if finalCheck: #마지막 실행에서의 최종 한칸
                        if countWidth > 4: #바꾸는 상수
                            widthArray.append(countWidth)
                        else:
                            widthArray.append(1) # 세로줄 한칸처리
                    else:
                        widthArray.append(countWidth) # 칸 개수
                    if x == 0 and counterE:  # 첫번째 배열 예외 처리
                        widthArray.append(0)
                        saveCountWidth = y - countWidth  # 노드의 기준점
                        counterE = False
                    else:
                        #print(y, countWidth)
                        #print(y - countWidth)
                        widthArray.append((y - countWidth) - saveCountWidth)  # 기준점과 현재 노드 시작점과의 거리
                    widthArray.append(x)
                    if array_xLength < widthArray[0] + widthArray[1]:
                        array_xLength = widthArray[0] + widthArray[1]
                    resultM.append(widthArray)
                    countWidth = 0
    return array_xLength


# 해당 열 한칸으로 만들어 주는 함수
def makeSimpleMiro(resultM):
    for a in range(0, 8):  # 바꾸는 상수-가로폭에 따라 4, 6
        for r in range(0, len(resultM)):
            if r >= len(resultM):
                break
            i = resultM[r]
            if i[0] > 4:  # 바꾸는 상수-세로 폭에 따라 4, 6
                newXTemp = []
                for j in resultM:
                    if j[2] == (i[2] + 1):
                        if (j[1] >= i[1] and j[1] <= (i[0] + i[1])) or (
                                (j[1] + j[0]) >= i[1] and (j[1] + j[0]) <= (i[0] + i[1])):
                            lengthminX = 0
                            lengthmaxX = 0
                            if i[1] > j[1]:
                                lengthminX = j[1]
                            else:
                                lengthminX = i[1]
                            if i[1] + i[0] > j[1] + j[0]:
                                if j[1] >= i[1]:
                                    lengthmaxX = i[0]
                                else:
                                    if i[1] - j[1] == 0:
                                        lengthmaxX = i[0]
                                    else:
                                        lengthmaxX = i[0] + ((i[1] - j[1]) if (i[1] - j[1]) > 0 else -(i[1] - j[1]))
                            else:
                                if j[1] <= i[1]:
                                    lengthmaxX = j[0]
                                else:
                                    if i[1] - j[1] == 0:
                                        lengthmaxX = j[0]
                                    else:
                                        lengthmaxX = j[0] + ((i[1] - j[1]) if (i[1] - j[1]) > 0 else -(i[1] - j[1]))

                            i[0] = lengthmaxX
                            i[1] = lengthminX
                            for k in resultM:
                                if k[2] == (j[2] + 1):
                                    if (k[1] >= j[1] and k[1] <= (j[0] + j[1])) or (
                                            (k[1] + k[0]) >= j[1] and (k[1] + k[0]) <= (j[0] + j[1])):
                                        newX = []
                                        newX.append(k[0])
                                        newX.append(k[1])
                                        newX.append(j[2])
                                        newXTemp.append(newX)
                            resultM.remove(j)
                for add in newXTemp:
                    resultM.append(add)
                resultM = sorted(resultM, key=lambda x: x[2])
    return resultM


# 리스트 미로화 함수
def realMakeMiro(array_yLength, array_xLength, resultM):
    makeMiro = []
    for y in range(array_yLength): # 최종 배열 크기 선언
        row = []
        for x in range(array_xLength):
            row.append(0)
        makeMiro.append(row)
    for i in resultM: # 최종 미로 생성기
        for j in range(i[1], i[0] + i[1]):
            makeMiro[i[2]][j] = 1
    return makeMiro


#camera.Camera()
im = Image.open('23.png')
im2 = im.convert('L')
imList = []
imXList = []

for x in range(im2.size[1]):  # 높이
    for y in range(im2.size[0]):  # 길이
        if im2.getpixel((y, x)) > 70:
            im2.putpixel((y, x), 255)
        else:
            im2.putpixel((y, x), 0)
        imXList.append(im2.getpixel((y, x)))
    imXListTemp =[]
    imXListTemp[:] = imXList[:]
    imXList.clear()
    imList.append(imXListTemp)

sizePixel = 0
smallSize = []
smallxSize = []
smallxSize2 = []
countWhite = 0
countBlack = 0
check = False
countY = 0
# 위아래 공백 삭제문
while countY < len(imList):
    if countY == len(imList):
        break
    if imList[countY].count(255) == len(imList[countY]):
       del imList[countY]
       countY -= 1
    countY += 1
# 사진크기 8배 축소 알고리즘
while sizePixel < 3:
    for y in range(0, len(imList), 2):
        for x in range(0, len(imList[y]), 2):

            if len(imList[y]) <= x + 1 and len(imList) > y + 1:
                if imList[y][x] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

                if imList[y + 1][x] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

            elif len(imList) <= y + 1 and len(imList[y]) > x + 1:
                if imList[y][x] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

                if imList[y][x + 1] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

            elif len(imList[y]) <= x + 1 and len(imList) < y + 1:
                if imList[y][x] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

            else:
                if imList[y][x + 1] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

                if imList[y + 1][x] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

                if imList[y + 1][x + 1] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

                if imList[y][x] == 255:
                    countWhite += 1
                else:
                    countBlack += 1

            if countBlack == 0:
                #f.write("□")
                imList[y][x] = 255
            else:
                #f.write("■")
                imList[y][x] = 0

            smallxSize.append(imList[y][x])
            countWhite = 0
            countBlack = 0

        smallxSizeTemp = []
        smallxSizeTemp[:] = smallxSize[:]
        smallxSize.clear()
        smallSize.append(smallxSizeTemp)
        #f.write("\n")

    imList.clear()
    for y in range(0, len(smallSize)):
        for x in range(0, len(smallSize[y])):
            smallxSize2.append(smallSize[y][x])
        smallxSizeTemp2 = []
        smallxSizeTemp2[:] = smallxSize2[:]
        smallxSize2.clear()
        imList.append(smallxSizeTemp2)

    sizePixel += 1
    smallSize.clear()

# ------------------------------------------------------------------------------x축 한칸
resultM = []
array_xLength = makeMiroDataList(imList, resultM, False, False) # x축 지정 및 미로 데이터화
resultM = makeSimpleMiro(resultM)  # 한칸 미로 만들기
array_yLength = resultM[-1][2] + 2  # y축
makeMiro = realMakeMiro(array_yLength, array_xLength, resultM)
# ------------------------------------------------------------------------------y축 한칸
resultM2 = []
array_xLength2 = makeMiroDataList(makeMiro, resultM2, True, False)
resultM2 = makeSimpleMiro(resultM2)
array_yLength2 = resultM2[-1][2] + 2
makeMiro2 = realMakeMiro(array_yLength2, array_xLength2, resultM2)
# ------------------------------------------------------------------------------최종
resultM3 = []
array_xLength3 = makeMiroDataList(makeMiro2, resultM3, True, True)
array_yLength3 = resultM3[-1][2] + 1
makeMiro3 = realMakeMiro(array_yLength3, array_xLength3, resultM3)
# -------------------------------------------------------------------------------


for i in range(0, len(makeMiro3)):
    for j in range(0, len(makeMiro3[i])):
        if makeMiro3[i][j] == 1:
            makeMiro3[i][j] = 0
        else:
            makeMiro3[i][j] = 1


f3 = open("result.txt", "w")
# 테스트 출력
for i in makeMiro3:
    for j in i:
        if j == 1:
            f3.write("□")
        else:
            f3.write("■")
    f3.write("\n")
f3.close()


Imaze = maze.Maze(mazearray=makeMiro3)
go = Imaze.findpath()

#blu.BLU(''.join(go))
print(go)

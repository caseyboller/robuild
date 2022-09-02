import os
from datetime import datetime
import sys

print(sys.argv[1:])

file = ""
if len(sys.argv) < 2:
    print("For cmd line, please add Robot java filename as arg, e.g.\n>python Robuild.py SpinBot.java.\nTo continue, input the name now:")
    file = input()
else:
    file = sys.argv[1]
    
with open(file) as f:
    index = 0
    # default file store [lineIndex, [line]]
    cleanLines = []
    # list of [lineIndex, [linesToUpdateWith]] to overwrite
    updateLines = []
    nextUpdate = -1
    # Minimum, maximum, step
    rorange = [0,0,0]
    while True:
        line = f.readline()
        if not line:
            break

        cleanLines.append([index, line])

        if line.find("[Robuild ") != -1:
            roline = line.split("(")[1]
            romin = roline.split(":")[0]
            romax = roline.split(":")[1]
            romulti = romax.split(")")[1].split("]")[0]
            romax = romax.split(")")[0]
            rorange = [int(romin.strip()), int(
                romax.strip()) + 1, int(romulti.strip())]
            #print(rorange)
            nextUpdate = index + 1


        if index == nextUpdate:
            if line.find('=') != -1:
                lines = []
                for i in range(rorange[0], rorange[1], rorange[2]):
                    rostart = line.split("=")[0]
                    roend = line.split(";")[1]
                    rovarline = rostart + "= " + str(i) + ";" + roend.removesuffix('\n')
                    #print(rovarline)
                    lines.append(rovarline)
                updateLines.append([index, lines])
        line = line.strip()
        #print(index, line, nextUpdate)
        index += 1
print(updateLines)
f.close()

script_dir = os.path.dirname(os.path.abspath(__file__))
str_date_time = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
outputDir = "SpinBot_" + str_date_time

fileCount = 0

for updateLine in updateLines:
    for upIndex in range(len(updateLine[1])):
        nameSlices = str(updateLine[1][upIndex]).strip().replace(';', '').replace(' ', '').split('=')
        file_name = str("SpinBot" + nameSlices[-2] + nameSlices[-1])
        dest_dir = os.path.join(script_dir, outputDir)
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass  # already exists
        path = os.path.join(dest_dir, file_name + ".java")

        fileCount += 1
        f = open(path, "w")
        packageWritten = False
        for clean in cleanLines:
            updated = False
                
            if updateLine[0] == clean[0]:
                updated = True
                print(clean[0], updateLine[1][upIndex])
                f.write(updateLine[1][upIndex] + "\n")

            if not packageWritten and clean[1].find("package") != -1:
                f.write("package " + outputDir + ";")
                packageWritten = True
            elif clean[1].find("public class " + file[0:-5]) != -1:
                f.write(clean[1].replace(("public class " + file[0:-5]),
                                 ("public class " + file_name)))
            elif not updated:
                f.write(clean[1])
        
        f.close()

print("\n..." + str(fileCount) + " variations output in " + outputDir + ".")
gradle = input("Run Gradle job now? (y/n)\n")

if not gradle:
    exit()



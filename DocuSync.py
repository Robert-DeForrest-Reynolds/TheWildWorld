from os import listdir, remove, path
from shutil import copy

LifeSource = ("C:\\Users\\rldre\\OneDrive\\Documents\\Life")

for File in listdir("Documentation"):
    if File != ".obsidian":
        LifeSourceFile = path.join(LifeSource, File)
        if path.exists(LifeSourceFile):
            print(f"Deleting {LifeSourceFile}")
            remove(LifeSourceFile)
        print(f"Copying over {File}")
        copy("Documentation\\" + File, LifeSource)
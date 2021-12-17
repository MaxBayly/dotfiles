import subprocess

files = subprocess.check_output("ls | grep .wav", shell=True).decode("utf-8").split("\n")
files = files[:-1]

print(files)

count = 0

with open("tracks") as tracks:
    for track in tracks:
        print(track)

        command = "sox " + files[count] + " '" + track.strip("\n") + ".flac'"
        print(command)
        subprocess.run(command, shell=True)
        count += 1

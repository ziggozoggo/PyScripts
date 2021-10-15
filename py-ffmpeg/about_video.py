import ffmpeg
import json

ffmpeg_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffmpeg.exe"
ffprobe_exe = "C:\\Progs\\ffmpeg-4.4-full_build\\bin\\ffprobe.exe"


stream = 'source\\kiberbezopasnost_test_720p.mp4'
probe = json.dumps(ffmpeg.probe(stream,ffprobe_exe), sort_keys=True, indent=4)

#print(probe)
outfile = open('out\\my_out.json','w')
outfile.write(str(probe))
outfile.close()

print(type(probe))





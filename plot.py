from ffmpegModule import FFMPEG_Writer
from particle2DScatter import Particle2DScatter
from particle3DScatter import Particle3DScatter

def startPSO(mode = '2D', export = 0, fps = 60):
    if mode == '2D':
        particleScatter = Particle2DScatter(figNum = 1, n = 100, vw = 1, wMin = 0.4, wMax = 0.9, c1 = 1, c2 = 2, it = 200)
        filename = 'PSO2D.mp4'
    elif mode == '3D':
        particleScatter = Particle3DScatter(figNum = 1, n = 100, vw = 1, wMin = 0.4, wMax = 0.9, c1 = 0.5, c2 = 0.75, it = 100)
        filename = 'PSO3D.mp4'
    else:
        print('Invalid mode:', mode, '... Are you serious? Aborting!')
        return

    if export:
        writer = FFMPEG_Writer(fps = fps, artist = 'AsulconS')
        particleScatter.save(writer, filename)

    particleScatter.show()

def main():
    mode = input('Please, select the mode (type in 2D or 3D): ')
    export = int(input('Do you want to export the animation to MP4? (type in 0 for NO or 1 for YES): '))
    if export:
        fps = int(input('Type in the FPS rate: '))
        startPSO(mode = mode, export = export, fps = fps)
    else:
        startPSO(mode = mode, export = export)

if __name__ == "__main__":
    main()

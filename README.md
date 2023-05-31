
# Screen Commentary Video Production Program

This program allows you to produce screen commentary videos by adding audio commentary to video files. The program supports various functionalities such as adding videos, adding script files, playing, pausing, stopping, and adjusting the volume of the videos.

## Prerequisites

Before running this program, make sure you have the following dependencies installed:

- `librosa` (version 0.9.1)
- `webrtcvad` (version 2.0.10)
- `PyQt5`

## Installation

1. Clone the repository:

2. Install the required dependencies:


## Usage

1. Run the program:

2. Click on the "Add Movie" button to select video files to add to the program.

3. Click on the "Add Script" button to select an Excel file containing the script for the commentary. The script should be in the first sheet of the Excel file.

4. Use the various buttons provided to control the playback of the video, such as play, pause, stop, forward, and previous.

5. Use the volume slider to adjust the volume of the video.

6. Use the timeline to set the start timestamp and length of the commentary for each segment of the video.

7. Double-click on the TTS (Text-to-Speech) list to play the corresponding audio commentary.

8. Click on the "Make Movie" button to start the video production process. The program will create a new video file with the audio commentary added.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please create a new issue or submit a pull request.

## License

This program is licensed under the [MIT License](LICENSE).



## Korean
### 설치 및 실행 방법

Python 3.7 이상의 버전을 설치합니다.
필요한 라이브러리를 설치합니다. (pip install -r requirements.txt)
main.py 파일을 실행합니다.
### 기능

1. 동영상 파일 추가
프로그램에 동영상 파일을 추가할 수 있습니다. 지원하는 확장자는 mp4, mpg, mpeg, avi, wma, mka입니다.
2. 해설 스크립트 추가
프로그램에 해설 스크립트를 추가할 수 있습니다. 스크립트는 Excel 파일 형식(xls, xlsx)으로 제공되어야 합니다.
3. TTS 변환
추가된 해설 스크립트를 음성으로 변환할 수 있습니다. 변환된 음성은 TTS 목록에 표시됩니다.
4. 음성 삽입
TTS 목록에서 선택한 음성을 원하는 시간대에 삽입할 수 있습니다. 시간대는 동영상 파일의 타임라인으로 표시되며, 마우스 더블 클릭으로 삽입할 위치를 지정할 수 있습니다.
5. 영상 제작
삽입한 음성을 포함한 최종 영상을 제작합니다. 제작된 영상은 프로그램에서 확인할 수 있습니다.
### 주의사항

프로그램 종료 시 TTS 파일과 임시 파일은 자동으로 삭제됩니다.

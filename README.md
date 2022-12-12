# GraduationProject
2022 graduation_project
<h2> 화면 해설 프로그램(Screen commentary program)</h2>
2022. 12. 10 Latest Demo version

***
**📌 Objective**
> How much can we understand if we close our eyes or cover our ears? It is called **"Barrier Free"** to add screen commentary and subtitles so that both disabled and non-disabled people can see and feel the work equally.
At this time, screen commentary is an important link between the audience and the production.

***We thought about what would be inconvenient for blind people to encounter various media. Can Blind People Enjoy All YouTube Videos? That's the question that arises. So we thought of a screen commentary service for YouTube.***

> 1. Provide convenience to screen commentators
> 2. Automate audio editing and voice insertion


***
**💻 Development Process**
1. Understanding Information _(Not developed yet)_
2. Priority Algorithm _(Not developed yet)_
3. **Identify where the voice will be guided**
4. **Insert audio in video**
 
First, analyze what information is in the image.

Next, the algorithm determines *which* of the many pieces of information analyzed and how to convey it.

Identify *where the information to be delivered will be guided to the voice*, and insert it appropriately between images to guide it.

At this point, the position where the voice will be guided should *not appear before the screen in an empty space* that does not overlap the line.

***
**🧑‍💻 Technologies**

You can see more detailed information in below page.

🔗 Wiki page: https://github.com/jha2ee/GraduationProject/wiki/Developed-version(2022-2)

📕 PyQT5 GUI

📙 MoviePy

📗 Vad algorithm(Webrtcvad)

📘 Google TTS

***
**📝 Data Analysis** (Not developed yet)
1. Voice data
2. Subtitle data
3. Image(Video) data
4. Meta data

This data uses for *Priority algorithm*, *Position to insert tts*, *Understanding context*.

***
**👀 Reference**
1. 화면해설 365 법칙 : <https://www.youtube.com/watch?v=AgXfppcFzTI>
```
3 : 
For innate blindness
Elementary school students can understand
Considering that the non-disabled will watch it together

6 :
Curious sounds, characters, times and places, visual information, situations, directives

5 :
From the observer's point of view, In the empty space between lines, 
Present form from an observer's point of view,
The commentary doesn't come out before the screen, 
Can draw a picture with a natural sentence

```

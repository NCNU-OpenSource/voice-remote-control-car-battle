LSA Final Project---芽控車大亂鬥
===
###### tags: `lsa`
## 動機發想
- [靈感影片](https://www.youtube.com/watch?v=e6Ne29G8mbU&ab_channel=B.C.%26Lowy)
- 偶然間在 Youtube 看到上方影片，內容是關於掃地機車人的對戰影片，我們就想著或許可以朝控制小車子方向去做研究，但又覺得如果鍵盤或是 buttom 控制就太 low 了，所以改成語音辨識控制，然後為了有第一人稱的緊張刺激感，就在上面裝 Pi 使 Camera 可以即時投影

## 系統架構
### 使用技術
- Tensorflow.js
- Python Flask、OpenCV
- OpenSSL

### 所使用的設備材料
- Pi 3 或 Pi 4 (Pi 4 效果會比 Pi 3好)
![](https://i.imgur.com/9NFq0eY.png =200x)


- 單層自走車底盤
![](https://i.imgur.com/ABNOezr.png =200x)


- L298N 馬達驅動板
![](https://i.imgur.com/xiya2uk.png =200x)

- Pi Camera
![](https://i.imgur.com/57knbgJ.png =100x)


## 架設過程
### 語音辨識
#### 前置作業
#### 專案是採用 Jupyter notebook 編輯
- 使用 pip 安裝 Jupyter notebook
```python=
# install jupyter notebook
sudo apt update
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install jupyter
pip install -U jupyter
```

- 下載這個專案的 code 安裝 git
```python=
sudo apt install git
```
- 在自己要存放的目錄底下 clone repo
```python=
git clone https://github.com/efficacy38/test_learning_LSA.git
cd test_learning_LSA/
```
- 在放置的路徑下 `jupyter notebook`，並點開 `training_custom_audio_model_in_python.ipynb`

#### training_custom_audio_model_in_python.ipynb 注意重點
1. 在training_custom_audio_model_in_python.ipynb
> 第 33 行裡面我的設定是在 /tmp/speech_commands_v0.02 底下任何有檔名包含 zh 都會被 resampling 和變成之後訓練的 data set，所以請把你的音檔按照你想讓他辨識出的名子放在/tmp/speech_commands_v0.02並加個zh後墜，他就會在辨識的時候跑出你當初資料夾設定的名子
    
```python=
def resample_wavs(dir_path, target_sample_rate=44100):


  """Resample the .wav files in an input directory to given sampling rate.

  The resampled waveforms are written to .wav files in the same directory with
  file names that ends in "_44100hz.wav".

  44100 Hz is the sample rate required by the preprocessing model. It is also
  the most widely supported sample rate among web browsers and mobile devices.
  For example, see:
  https://developer.mozilla.org/en-US/docs/Web/API/AudioContextOptions/sampleRate
  https://developer.android.com/ndk/guides/audio/sampling-audio

  Args:
    dir_path: Path to a directory that contains .wav files.
    target_sapmle_rate: Target sampling rate in Hz.
  """
  wav_paths = glob.glob(os.path.join(dir_path, "*.wav"))
  resampled_suffix = "_%shz.wav" % target_sample_rate
  for i, wav_path in tqdm.tqdm(enumerate(wav_paths)):
    if wav_path.endswith(resampled_suffix):
      continue
    sample_rate, xs = wavfile.read(wav_path)
    xs = xs.astype(np.float32)
    xs = librosa.resample(xs, sample_rate, TARGET_SAMPLE_RATE).astype(np.int16)
    resampled_path = os.path.splitext(wav_path)[0] + resampled_suffix
    wavfile.write(resampled_path, target_sample_rate, xs)


for word in WORDS:
  word_dir = os.path.join(DATA_ROOT, word)
  if os.path.isdir(word_dir) or "zh" in word_dir :
      print(word_dir)
      resample_wavs(word_dir, target_sample_rate=TARGET_SAMPLE_RATE)
```
2. 當你一直按下一步案到最後，你就可以看到 train 好的 tfjs model 放在 /tmp/tfjs-model 把它整個上傳到 github 就完成了第二步了

3. 設定 tfjs 語音辨識 在/dev_web/index.js
> 在 app function 中 model.json，和 metadata.json 的部分可以透過上傳model.json, metadata.json,和 group1-shard2of2.bin... 到 github，並且用 github 右上角那個raw按鍵，顯示出只有文檔的網頁，複製連結並照著格式去改完index.js，應該就可以打開 index.html 快樂的辨識囉
```javascript=
async function app() {
// recognizer = speechCommands.create('BROWSER_FFT', null, 'https://raw.githubusercontent.com/efficacy38/test_LSA_audio_predict/main/model.json', 'https://raw.githubusercontent.com/efficacy38/test_LSA_audio_predict/main/metadata.json');  en+zh
    recognizer = speechCommands.create('BROWSER_FFT', null, 'https://raw.githubusercontent.com/efficacy38/test_LSA_audio_predict-zh-/main/model.json', 'https://raw.githubusercontent.com/efficacy38/test_LSA_audio_predict-zh-/main/metadata.json');
 await recognizer.ensureModelLoaded();
}
```

#### 操作網頁
把 `remoteAudioCtrl` 資料夾放到兩個 PI 上面
- 用 Flask 在兩個 PI 上各架一個 SERVER
:::success
#### 在`app.py`存在的目錄底下輸入
 ```sh
 export FLASK_APP=app.py
 flask run --host 0.0.0.0 --port 10838
 ```
 - host 0.0.0.0 代表跑在本機上，在同一個區網底下（例如連上同一個手機發的wifi）可以在瀏覽器輸入 Pi 的 ip 跟 port 來連上網站
 - port 基本上可任意（數字盡量大一點）
:::
:::info
 > 建議在電腦上使用 Chrome 連入
 
 在 Chrome 網址列輸入`chrome://flags/`
 找到`Insecure origins treated as secure`
 輸入剛剛架起來的網站包括 port 後 enable 他
 ![](https://i.imgur.com/3Lc65Vo.png)
 >因為網站會需要取得麥克風使用權限，不開這個 Chrome 會因為安全性問題而出錯
:::

### **即時投影**
* 需開啟 Pi Camera
    * `sudo raspi-config`
    * enter interface option
    * enter Camera to enable `Yes`
    
* 先clone miguelgrinberg/flask-video-streaming
`git clone https://github.com/miguelgrinberg/flask-video-streaming.git`

* cd flask-video-streaming 修改 app.py
    - 註解掉第五行
    - 刪除第八行註解
```python=
#!/usr/bin/env python
from flask import Flask, render_template, Response

# emulated camera
      #from camera import Camera

      #Raspberry Pi camera module (requires picamera package)
      from camera_pi import Camera
```


* cd flask-video-streaming 確認是否有畫面
    - `python app.py`
    - enter `http://你的ip:5000`
    - 如下圖
    ![](https://i.imgur.com/tTpVuWP.png =500x)
    
* cd flask-video-streaming/templates
    * `vim index.html`
```html= <html>
<head>
    <title>Video Streaming Demonstration</title>
</head>
<body>
    <table>
        <tr>
            <td>
                <h1>Megan gogogo</h1>
                <img src="{{ url_for('video_feed') }}">
            </td>
            <td>
                <h1>Love turnturnturn</h1>
                <img src=" http://你的ip:5000/video_feed ">"
            </td>
        </tr>
    </table>
</body>
</html>
```
![](https://i.imgur.com/zmNLzJW.png =600x)

### **網頁加密**
* 安裝openssl
`sudo apt-get -y install openssl`

* 生成csr檔案
`openssl genrsa -des3 -out server.key 2048`
>2048表示key長度(若是長度為1024則會報錯，bug顯示key too small)

* Remove Passphrase from key
`cp server.key server.key.org`
`openssl rsa -in server.key.org -out server.key`

* 生成crt檔案，有效期1年（365天）
`openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt`

* 完成上面步驟會生成server.crt和server.key檔案

* 在flask程式碼中引用此key(cd flask-video-streaming 修改 app.py)
```python= 
# your_path: 放自己的路徑
app = Flask(__name__)    
app.run('0.0.0.0', debug=True, port=443, ssl_context=('your_path/server.crt', 'your_path/server.key'))  
```

* cd flask-video-streaming/templates 修改 index.html
```html= <html>
<head>
    <title>Video Streaming Demonstration</title>
</head>
<body>
    <table>
        <tr>
            <td>
                <h1>Megan gogogo</h1>
                <img src="{{ url_for('video_feed') }}">
            </td>
            <td>
                <h1>Love turnturnturn</h1>
                <img src=" https://你的ip:443/video_feed ">"
            </td>
        </tr>
    </table>
</body>
</html>
```
![](https://i.imgur.com/Gh8rd8X.png)

![](https://i.imgur.com/IkvAVwT.png =300x)



### **車子組裝**
* 馬達焊紅黑線
![](https://i.imgur.com/wREH3Y7.png =200x)

* 馬達紅線插於馬達 A、B 的右孔，黑線插於馬達 A、B 的左孔

* 電池盒的紅線插於驅動板的12V、黑線插接地( GND )

* 旁邊四角( IN1~IN4 )接 Pi 的 GPIO，我們是從上而下對應 Pi GPIO 17, 18, 22, 23


![驅動板對應圖](https://i.imgur.com/6vdohUc.png =300x)
![Pi GPIO 對應圖](https://i.imgur.com/gFrejPu.png =200x)

:::info
1. 若輪子轉動很慢、馬達供電不足，可以多接線插於 5V、12V，Pi 上有兩個5V可以接
2. **Enable A、Enable B 請勿拔掉，他們是用來控制馬達驅使轉動的方向**
3. 依插線接孔的不同，會需調整成自己連接對應的方式
:::


## DEMO 影片
#### 加裝了氣球及刀片後的對戰示範
[Demo影片](https://drive.google.com/file/d/1qPWYk00ynQjyMr737QuOJLwvstIJLYKw/view?usp=sharing)


## 參考資料
- [Video Streaming with Flask I](https://blog.miguelgrinberg.com/post/video-streaming-with-flask)
- [Video Streaming with Flask II](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited)
- [Raspberry使用L298N操作兩個馬達](https://atceiling.blogspot.com/2014/03/raspberry-pi.html#.VvnjwOJ97rc)
- [鏡頭頁面加密](https://www.itread01.com/content/1543677902.html#python%2Bflask%E5%AD%90%E5%9F%9F%E5%90%8D%E8%AE%BF%E9%97%AE%E8%AE%BE%E7%BD%AE)
- [Tensorflow.js model](https://github.com/tensorflow/tfjs-models/tree/master/speech-commands)
- [efficacy38/test_learning_LSA ref from tensorflow.js model](https://github.com/efficacy38/test_learning_LSA)

## 工作分配
* 語音辨識、訓練模型、資料串接
    * 莊才賢
    * 丘世宇
    
* 網頁加密、Python Flask、車子組裝
    * 蔡靚姚
    * 李羽珊
    * 朱宣樺

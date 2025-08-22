import os
import io
from flask import Flask, render_template, send_file
from gtts import gTTS
from urllib.parse import unquote

app = Flask(__name__)

# --- 詞彙表加載邏輯 (保持不變) ---
def load_vocabulary(filepath="vocab.txt"):
    """從 TXT 檔案加載詞彙表"""
    vocab = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
        i = 0
        while i < len(lines):
            if lines[i].isdigit():
                if i + 4 < len(lines):
                    english_word = lines[i+2]
                    chinese_translation = lines[i+4]
                    if english_word and chinese_translation:
                        vocab.append({
                            'english': english_word,
                            'chinese': chinese_translation
                        })
                    i += 5
                else:
                    break
            else:
                i += 1
        print(f"成功加載 {len(vocab)} 個單字。")
        return vocab
    except FileNotFoundError:
        print(f"錯誤：文件 '{filepath}' 未找到。")
        return []
    except Exception as e:
        print(f"加載詞彙表時發生錯誤：{e}")
        return []

# --- Flask 路由 ---
@app.route('/')
def index():
    """主頁面：加載所有詞彙並渲染模板"""
    vocabulary_list = load_vocabulary()
    return render_template('index.html', vocabulary=vocabulary_list)

@app.route('/speak/<text_to_speak>')
def speak(text_to_speak):
    """API: 根據傳入的文字生成語音並回傳"""
    # 對 URL 編碼的文字進行解碼 (例如 %20 會變回空格)
    decoded_text = unquote(text_to_speak)
    
    # 使用 io.BytesIO 在記憶體中處理 MP3 檔案，不需儲存到硬碟
    mp3_fp = io.BytesIO()
    
    try:
        # 生成語音
        tts = gTTS(text=decoded_text, lang='en', slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # 將指標移至檔案開頭
        
        # 回傳 MP3 檔案
        return send_file(
            mp3_fp, 
            mimetype="audio/mpeg", 
            as_attachment=False, 
            download_name="speech.mp3"
        )
    except Exception as e:
        print(f"生成語音時發生錯誤: {e}")
        return "Error generating speech", 500

if __name__ == '__main__':
    app.run(debug=True)
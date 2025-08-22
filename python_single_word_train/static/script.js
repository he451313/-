document.addEventListener('DOMContentLoaded', () => {
    const audioPlayer = document.getElementById('audio-player');
    const tableBody = document.querySelector('.vocab-table tbody');

    // 使用事件委派，只在 table body 上掛一個監聽器，提高效能
    tableBody.addEventListener('click', (event) => {
        // 檢查被點擊的是否是播放按鈕
        const playButton = event.target.closest('.play-btn');
        
        if (playButton) {
            // 從按鈕的 data-word 屬性獲取要播放的英文單字
            const wordToSpeak = playButton.dataset.word;
            
            // 如果有單字，則進行播放
            if (wordToSpeak) {
                // 使用 encodeURIComponent 處理特殊字元和空格
                const encodedWord = encodeURIComponent(wordToSpeak);
                
                // 設定 audio 播放器的來源為我們的 API
                audioPlayer.src = `/speak/${encodedWord}`;
                
                // 播放聲音
                audioPlayer.play();

                // 提供視覺回饋：暫時改變按鈕樣式
                playButton.classList.add('playing');
                playButton.textContent = '...';
            }
        }
    });

    // 當聲音播放結束時，恢復所有按鈕的原始樣式
    audioPlayer.addEventListener('ended', () => {
        document.querySelectorAll('.play-btn.playing').forEach(button => {
            button.classList.remove('playing');
            button.textContent = '▶';
        });
    });

    // 如果播放出錯 (例如網路問題)，也恢復按鈕樣式
    audioPlayer.addEventListener('error', () => {
         document.querySelectorAll('.play-btn.playing').forEach(button => {
            button.classList.remove('playing');
            button.textContent = '▶';
        });
        console.error("無法播放音訊。");
    });
});
/**
 * 개선된 캄보디아 농업용어 학습 앱
 * Modern, intuitive mobile learning experience
 */

class ImprovedAgriculturalLearningApp {
    constructor() {
        this.currentDay = 1;
        this.currentWordIndex = 0;
        this.dailyWords = [];
        this.currentWord = null;
        this.isCardFlipped = false;
        this.learningProgress = this.loadProgress();
        this.favorites = this.loadFavorites();
        this.statistics = this.loadStatistics();
        
        this.init();
    }

    async init() {
        try {
            await this.loadDailyWords();
            this.setupEventListeners();
            this.displayCurrentWord();
            this.updateProgress();
            this.registerServiceWorker();
            
            // 첫 방문 시 힌트 표시
            if (!localStorage.getItem('hintsShown')) {
                setTimeout(() => this.showFlipHint(), 1000);
                localStorage.setItem('hintsShown', 'true');
            }
            
        } catch (error) {
            console.error('앱 초기화 오류:', error);
            this.showError('앱을 초기화하는데 실패했습니다.');
        }
    }

    async loadDailyWords() {
        try {
            const response = await fetch(`/api/daily-words/${this.currentDay}`);
            if (!response.ok) throw new Error('단어를 불러올 수 없습니다');
            
            this.dailyWords = await response.json();
            
            if (this.dailyWords.length === 0) {
                throw new Error('학습할 단어가 없습니다');
            }
            
        } catch (error) {
            console.error('일일 단어 로드 오류:', error);
            // 오프라인 모드 또는 오류 시 샘플 데이터 사용
            this.dailyWords = this.getSampleWords();
        }
    }

    getSampleWords() {
        return [
            {
                id: 1,
                korean: "벼",
                khmer: "ស្រូវ",
                pronunciation: "스라우",
                category: "작물재배",
                definition_ko: "논에서 기르는 한해살이 벼과 식물로, 쌀의 원료가 되는 곡물",
                definition_km: "រុក្ខជាតិក្រុមបាយដែលដាំក្នុងស្រែ និងជាវត្ថុធាតុដើមនៃអង្ករ",
                example_ko: "벼농사는 캄보디아의 주요 농업 활동입니다.",
                example_km: "ការដាំស្រូវគឺជាសកម្មភាពកសិកម្មសំខាន់របស់កម្ពុជា",
                example_pronunciation: "카 담 스라우 끄 치아 사깜마파프 솜칸 로보스 깜푸치아",
                frequency: 5,
                difficulty: "기초"
            },
            {
                id: 2,
                korean: "농기계",
                khmer: "គ្រឿងយន្តកសិកម្ម",
                pronunciation: "크룽 욘 까시깜",
                category: "농기계",
                definition_ko: "농업 작업에 사용되는 기계와 도구의 총칭",
                definition_km: "គ្រឿងយន្ត និងឧបករណ៍ដែលប្រើប្រាស់សម្រាប់ការងារកសិកម្ម",
                example_ko: "현대적인 농기계 도입으로 농작업 효율이 크게 향상되었습니다.",
                example_km: "ការណែនាំគ្រឿងយន្តកសិកម្មទំនើបធ្វើឱ្យប្រសិទ្ធភាពការងារកសិកម្មកើនឡើងយ៉ាងខ្លាំង",
                example_pronunciation: "카 나엠남 크룽욘 까시깜 톰노업 트뜨어으이 프로싯타파프 카낭가 까시깜 꼬언 라엥 야응 클라응",
                frequency: 4,
                difficulty: "중급"
            },
            {
                id: 3,
                korean: "비료",
                khmer: "ជី",
                pronunciation: "치",
                category: "비료",
                definition_ko: "식물의 생장에 필요한 양분을 공급하는 물질",
                definition_km: "សារធាតុដែលផ្គត់ផ្គង់សារធាតុចិញ្ចឹមចាំបាច់សម្រាប់ការលូតលាស់របស់រុក្ខជាតិ",
                example_ko: "유기비료 사용으로 토양의 질을 개선할 수 있습니다.",
                example_km: "ការប្រើប្រាស់ជីសរីរាង្គអាចធ្វើឱ្យគុណភាពដីប្រសើរឡើង",
                example_pronunciation: "카 프러이 프라스 치 사리랑 아치 트뜨어으이 꾼나파프 다이 프로써어 라엥",
                frequency: 5,
                difficulty: "기초"
            }
        ];
    }

    setupEventListeners() {
        // 터치 제스처
        let startX = 0;
        let startY = 0;

        document.getElementById('wordCard').addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.getElementById('wordCard').addEventListener('touchend', (e) => {
            if (!startX || !startY) return;

            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const diffX = startX - endX;
            const diffY = startY - endY;

            // 수평 스와이프가 더 클 때만 처리
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    this.nextWord(); // 왼쪽 스와이프 = 다음
                } else {
                    this.previousWord(); // 오른쪽 스와이프 = 이전
                }
            }

            startX = 0;
            startY = 0;
        });

        // 키보드 단축키
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                    this.previousWord();
                    break;
                case 'ArrowRight':
                    this.nextWord();
                    break;
                case ' ':
                    e.preventDefault();
                    this.flipCard();
                    break;
                case 'Enter':
                    this.speakKhmer();
                    break;
            }
        });

        // 모달 외부 클릭으로 닫기
        document.getElementById('statsModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.closeStats();
            }
        });
    }

    displayCurrentWord() {
        if (!this.dailyWords || this.dailyWords.length === 0) {
            this.showError('학습할 단어가 없습니다.');
            return;
        }

        this.currentWord = this.dailyWords[this.currentWordIndex];
        const cardFront = document.getElementById('cardFront');
        const cardBack = document.getElementById('cardBack');

        // 로딩 숨기기
        document.getElementById('loadingSpinner').style.display = 'none';

        // 카드 앞면 내용
        cardFront.innerHTML = `
            <div class="category-tag">${this.currentWord.category}</div>
            <div class="word-main">${this.currentWord.korean}</div>
            <div class="word-translation">${this.currentWord.khmer}</div>
            <div class="word-pronunciation">${this.currentWord.pronunciation}</div>
        `;

        // 카드 뒷면 내용 업데이트
        document.getElementById('categoryTag').textContent = this.currentWord.category;
        document.getElementById('exampleKo').textContent = this.currentWord.example_ko || '예문이 없습니다.';
        document.getElementById('exampleKm').textContent = this.currentWord.example_km || '';

        // 즐겨찾기 상태 업데이트
        this.updateFavoriteIcon();

        // 카드 뒤집기 초기화
        this.isCardFlipped = false;
        document.getElementById('wordCard').classList.remove('flipped');

        // 네비게이션 버튼 상태 업데이트
        this.updateNavigationButtons();
    }

    flipCard() {
        const card = document.getElementById('wordCard');
        this.isCardFlipped = !this.isCardFlipped;
        
        if (this.isCardFlipped) {
            card.classList.add('flipped');
        } else {
            card.classList.remove('flipped');
        }

        // 학습 통계 업데이트
        if (this.isCardFlipped) {
            this.markWordAsViewed();
        }
    }

    async speakKorean() {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(this.currentWord.korean);
            utterance.lang = 'ko-KR';
            utterance.rate = 0.8;
            speechSynthesis.speak(utterance);
        }
    }

    async speakKhmer() {
        if ('speechSynthesis' in window) {
            // 크메르어 발음을 한국어 표기로 읽기
            const utterance = new SpeechSynthesisUtterance(this.currentWord.pronunciation);
            utterance.lang = 'ko-KR';
            utterance.rate = 0.7;
            speechSynthesis.speak(utterance);
        }
    }

    toggleFavorite() {
        const wordId = this.currentWord.id;
        const index = this.favorites.indexOf(wordId);
        
        if (index === -1) {
            this.favorites.push(wordId);
            this.showMessage('즐겨찾기에 추가했습니다', 'success');
        } else {
            this.favorites.splice(index, 1);
            this.showMessage('즐겨찾기에서 제거했습니다', 'info');
        }
        
        this.saveFavorites();
        this.updateFavoriteIcon();
    }

    updateFavoriteIcon() {
        const icon = document.getElementById('favoriteIcon');
        const isFavorite = this.favorites.includes(this.currentWord.id);
        
        if (isFavorite) {
            icon.className = 'fas fa-heart';
            icon.style.color = '#f44336';
        } else {
            icon.className = 'far fa-heart';
            icon.style.color = '';
        }
    }

    nextWord() {
        if (this.currentWordIndex < this.dailyWords.length - 1) {
            this.currentWordIndex++;
            this.displayCurrentWord();
            this.updateProgress();
            this.markProgress();
        } else {
            this.showMessage('오늘의 학습을 완료했습니다!', 'success');
        }
    }

    previousWord() {
        if (this.currentWordIndex > 0) {
            this.currentWordIndex--;
            this.displayCurrentWord();
            this.updateProgress();
        }
    }

    updateProgress() {
        const progress = ((this.currentWordIndex + 1) / this.dailyWords.length) * 100;
        
        document.getElementById('dayInfo').textContent = `Day ${this.currentDay}`;
        document.getElementById('wordCount').textContent = `${this.currentWordIndex + 1}/${this.dailyWords.length}`;
        document.getElementById('progressFill').style.width = `${progress}%`;
        
        let progressText = '';
        if (progress === 100) {
            progressText = '오늘 학습 완료! 🎉';
        } else {
            progressText = `${Math.round(progress)}% 완료`;
        }
        document.getElementById('progressText').textContent = progressText;
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentWordIndex === 0;
        nextBtn.disabled = this.currentWordIndex === this.dailyWords.length - 1;
        
        if (this.currentWordIndex === this.dailyWords.length - 1) {
            nextBtn.innerHTML = '<i class="fas fa-check"></i> 완료';
        } else {
            nextBtn.innerHTML = '다음 <i class="fas fa-chevron-right"></i>';
        }
    }

    markWordAsViewed() {
        const wordId = this.currentWord.id;
        const today = new Date().toDateString();
        
        if (!this.learningProgress[today]) {
            this.learningProgress[today] = [];
        }
        
        if (!this.learningProgress[today].includes(wordId)) {
            this.learningProgress[today].push(wordId);
            this.saveProgress();
            this.updateStatistics();
        }
    }

    markProgress() {
        this.markWordAsViewed();
    }

    showStats() {
        this.updateStatsModal();
        document.getElementById('statsModal').classList.add('active');
    }

    closeStats() {
        document.getElementById('statsModal').classList.remove('active');
    }

    updateStatsModal() {
        const totalLearned = this.getTotalLearnedWords();
        const overallProgress = Math.round((totalLearned / 1400) * 100);
        const streakDays = this.getStreakDays();
        
        document.getElementById('totalLearned').textContent = totalLearned;
        document.getElementById('overallProgress').textContent = overallProgress;
        document.getElementById('streakDays').textContent = streakDays;
    }

    getTotalLearnedWords() {
        let total = 0;
        Object.values(this.learningProgress).forEach(dayWords => {
            total += dayWords.length;
        });
        return total;
    }

    getStreakDays() {
        const dates = Object.keys(this.learningProgress).sort();
        let streak = 0;
        let currentDate = new Date();
        
        for (let i = dates.length - 1; i >= 0; i--) {
            const date = new Date(dates[i]);
            const diffDays = Math.floor((currentDate - date) / (1000 * 60 * 60 * 24));
            
            if (diffDays === streak) {
                streak++;
            } else {
                break;
            }
        }
        
        return streak;
    }

    updateStatistics() {
        this.statistics.totalWordsLearned = this.getTotalLearnedWords();
        this.statistics.streakDays = this.getStreakDays();
        this.statistics.lastUpdate = new Date().toISOString();
        this.saveStatistics();
    }

    showFlipHint() {
        const hint = document.querySelector('.flip-hint');
        hint.style.opacity = '1';
        setTimeout(() => {
            hint.style.opacity = '0';
        }, 3000);
    }

    showMessage(message, type = 'info') {
        // 간단한 토스트 메시지
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 1001;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideDown 0.3s ease;
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideUp 0.3s ease forwards';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 2000);
    }

    showError(message) {
        document.getElementById('cardFront').innerHTML = `
            <div style="text-align: center; color: #f44336; padding: 40px 20px;">
                <i class="fas fa-exclamation-triangle" style="font-size: 48px; margin-bottom: 16px;"></i>
                <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">오류가 발생했습니다</div>
                <div style="font-size: 14px;">${message}</div>
            </div>
        `;
    }

    // 저장소 관리
    loadProgress() {
        const saved = localStorage.getItem('learningProgress');
        return saved ? JSON.parse(saved) : {};
    }

    saveProgress() {
        localStorage.setItem('learningProgress', JSON.stringify(this.learningProgress));
    }

    loadFavorites() {
        const saved = localStorage.getItem('favorites');
        return saved ? JSON.parse(saved) : [];
    }

    saveFavorites() {
        localStorage.setItem('favorites', JSON.stringify(this.favorites));
    }

    loadStatistics() {
        const saved = localStorage.getItem('statistics');
        return saved ? JSON.parse(saved) : {
            totalWordsLearned: 0,
            streakDays: 0,
            lastUpdate: new Date().toISOString()
        };
    }

    saveStatistics() {
        localStorage.setItem('statistics', JSON.stringify(this.statistics));
    }

    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/js/sw.js');
                console.log('Service Worker 등록 성공:', registration);
            } catch (error) {
                console.log('Service Worker 등록 실패:', error);
            }
        }
    }

    // 네비게이션 기능들
    showCategories() {
        this.showMessage('카테고리 기능은 준비 중입니다', 'info');
    }

    showFavorites() {
        this.showMessage('즐겨찾기 기능은 준비 중입니다', 'info');
    }

    showSettings() {
        this.showMessage('설정 기능은 준비 중입니다', 'info');
    }
}

// 전역 함수들 (HTML에서 호출)
let app;

// DOM이 로드되면 앱 시작
document.addEventListener('DOMContentLoaded', () => {
    app = new ImprovedAgriculturalLearningApp();
});

// 전역 함수들
function flipCard() {
    if (app) app.flipCard();
}

function speakKorean() {
    if (app) app.speakKorean();
}

function speakKhmer() {
    if (app) app.speakKhmer();
}

function toggleFavorite() {
    if (app) app.toggleFavorite();
}

function nextWord() {
    if (app) app.nextWord();
}

function previousWord() {
    if (app) app.previousWord();
}

function showStats() {
    if (app) app.showStats();
}

function closeStats() {
    if (app) app.closeStats();
}

function showCategories() {
    if (app) app.showCategories();
}

function showFavorites() {
    if (app) app.showFavorites();
}

function showSettings() {
    if (app) app.showSettings();
}

// CSS 애니메이션 추가
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        to {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
    }
`;
document.head.appendChild(style);
// 캄보디아 농업용어 모바일 학습 앱 JavaScript

// 전역 변수
let currentWords = [];
let currentDay = 1;
let learnedToday = 0;
let totalLearned = 0;
let currentQuizIndex = 0;
let quizWords = [];
let userStats = {
    totalLearned: 0,
    currentStreak: 0,
    lastLearningDate: null,
    learnedWords: new Set()
};

// 앱 초기화
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 모바일 학습 앱 시작...');
    
    // 로컬 스토리지에서 사용자 데이터 로드
    loadUserStats();
    
    // 오늘의 단어 로드
    loadDailyWords();
    
    // 카테고리 필터 이벤트
    initializeCategoryFilter();
    
    // PWA 기능 초기화
    initializePWA();
    
    console.log('✅ 앱 초기화 완료');
});

// 사용자 통계 로드
function loadUserStats() {
    const savedStats = localStorage.getItem('agricultureLearningStats');
    if (savedStats) {
        const parsedStats = JSON.parse(savedStats);
        userStats = {
            ...userStats,
            ...parsedStats,
            learnedWords: new Set(parsedStats.learnedWords || [])
        };
    }
    
    // 날짜 확인 및 연속 학습일 계산
    const today = new Date().toDateString();
    if (userStats.lastLearningDate !== today) {
        const lastDate = new Date(userStats.lastLearningDate || today);
        const todayDate = new Date(today);
        const daysDiff = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));
        
        if (daysDiff === 1) {
            // 연속 학습
            userStats.currentStreak++;
        } else if (daysDiff > 1) {
            // 연속 학습 중단
            userStats.currentStreak = 1;
        }
        
        userStats.lastLearningDate = today;
        learnedToday = 0; // 새로운 날 시작
    }
    
    // 현재 날짜 기준으로 day 계산
    currentDay = Math.floor(userStats.totalLearned / 10) + 1;
    
    updateUI();
}

// 사용자 통계 저장
function saveUserStats() {
    const statsToSave = {
        ...userStats,
        learnedWords: Array.from(userStats.learnedWords)
    };
    localStorage.setItem('agricultureLearningStats', JSON.stringify(statsToSave));
}

// 오늘의 단어 로드
async function loadDailyWords() {
    try {
        showLoading();
        
        // 현재 day에 해당하는 10개 단어 가져오기
        const startIndex = (currentDay - 1) * 10;
        const response = await fetch(`/api/daily_words?day=${currentDay}&start=${startIndex}&limit=10`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch daily words');
        }
        
        const data = await response.json();
        currentWords = data.words || generateSampleWords(startIndex);
        
        displayDailyWords();
        
    } catch (error) {
        console.error('단어 로딩 오류:', error);
        // 샘플 데이터로 폴백
        currentWords = generateSampleWords((currentDay - 1) * 10);
        displayDailyWords();
    }
}

// 샘플 단어 생성 (API가 없을 경우 폴백)
function generateSampleWords(startIndex) {
    const sampleWords = [
        {
            id: startIndex + 1,
            korean_term: "벼",
            khmer_term: "ស្រូវ",
            khmer_pronunciation: "스라우",
            korean_definition: "논에서 기르는 한해살이 벼과 식물로, 쌀의 원료가 되는 곡물",
            khmer_definition: "រុក្ខជាតិក្រុមបាយដែលដាំក្នុងស្រែ និងជាវត្ថុធាតុដើមនៃអង្ករ",
            korean_example: "벼농사는 캄보디아의 주요 농업 활동입니다.",
            khmer_example: "ការដាំស្រូវគឺជាសកម្មភាពកសិកម្មសំខាន់របស់កម្ពុជា",
            khmer_example_pronunciation: "카 담 스라우 끄 치아 사깜마파프 솜칸 로보스 깜푸치아",
            category: "작물재배",
            image_url: "/static/images/rice.jpg",
            frequency_level: 5
        },
        {
            id: startIndex + 2,
            korean_term: "농기계",
            khmer_term: "គ្រឿងយន្តកសិកម្ម",
            khmer_pronunciation: "크룽 욘 까시깜",
            korean_definition: "농업 작업에 사용되는 기계와 도구의 총칭",
            khmer_definition: "គ្រឿងយន្ត និងឧបករណ៍ដែលប្រើប្រាស់សម្រាប់ការងារកសិកម្ម",
            korean_example: "현대적인 농기계 도입으로 농작업 효율이 크게 향상되었습니다.",
            khmer_example: "ការណែនាំគ្រឿងយន្តកសិកម្មទំនើបធ្វើឱ្យប្រសិទ្ធភាពការងារកសិកម្មកើនឡើងយ៉ាងខ្លាំង",
            khmer_example_pronunciation: "카 나엠남 크룽욘 까시깜 톰노업 트뜨어으이 프로싯타파프 카낭가 까시깜 꼬언 라엥 야응 클라응",
            category: "농기계",
            image_url: "/static/images/farm_machinery.jpg",
            frequency_level: 4
        },
        {
            id: startIndex + 3,
            korean_term: "비료",
            khmer_term: "ជី",
            khmer_pronunciation: "치",
            korean_definition: "식물의 생장에 필요한 양분을 공급하는 물질",
            khmer_definition: "សារធាតុដែលផ្គត់ផ្គង់សារធាតុចិញ្ចឹមចាំបាច់សម្រាប់ការលូតលាស់របស់រុក្ខជាតិ",
            korean_example: "유기비료 사용으로 토양의 질을 개선할 수 있습니다.",
            khmer_example: "ការប្រើប្រាស់ជីសរីរាង្គអាចធ្វើឱ្យគុណភាពដីប្រសើរឡើង",
            khmer_example_pronunciation: "카 프러이 프라스 치 사리랑 아치 트뜨어으이 꾼나파프 다이 프로써어 라엥",
            category: "비료",
            image_url: "/static/images/fertilizer.jpg",
            frequency_level: 5
        }
    ];
    
    // 10개까지 확장
    const extendedWords = [];
    for (let i = 0; i < 10; i++) {
        const baseWord = sampleWords[i % sampleWords.length];
        extendedWords.push({
            ...baseWord,
            id: startIndex + i + 1,
            korean_term: `${baseWord.korean_term} ${i + 1}`,
            learning_order: startIndex + i + 1
        });
    }
    
    return extendedWords;
}

// 일일 단어 표시
function displayDailyWords() {
    const container = document.getElementById('dailyWords');
    container.innerHTML = '';
    
    currentWords.forEach((word, index) => {
        const isLearned = userStats.learnedWords.has(word.id);
        
        const wordCard = createWordCard(word, index + 1, isLearned);
        container.appendChild(wordCard);
    });
    
    // 애니메이션 효과
    container.classList.add('fade-in');
}

// 단어 카드 생성
function createWordCard(word, number, isLearned = false) {
    const card = document.createElement('div');
    card.className = `word-card ${isLearned ? 'learned' : ''}`;
    card.setAttribute('data-word-id', word.id);
    
    card.innerHTML = `
        <div class="word-number">${number}</div>
        
        ${word.image_url ? `<img src="${word.image_url}" alt="${word.korean_term}" class="word-image" onerror="this.style.display='none'">` : ''}
        
        <div class="korean-word">${word.korean_term}</div>
        <div class="khmer-word khmer-text">${word.khmer_term}</div>
        <div class="pronunciation">[${word.khmer_pronunciation}]</div>
        
        <div class="definition">
            <strong>한국어:</strong> ${word.korean_definition}
        </div>
        
        <div class="example-sentence">
            <div class="example-korean">
                <strong>예문:</strong> ${word.korean_example}
            </div>
            <div class="example-khmer khmer-text">${word.khmer_example}</div>
            <div class="example-pronunciation">[${word.khmer_example_pronunciation}]</div>
        </div>
        
        <div class="word-actions">
            <button class="action-btn btn-speak" onclick="speakWord(${word.id}, 'khmer')">
                <i class="fas fa-volume-up"></i>
                크메르어
            </button>
            <button class="action-btn btn-speak" onclick="speakWord(${word.id}, 'korean')" style="background: #9C27B0;">
                <i class="fas fa-volume-up"></i>
                한국어
            </button>
            ${!isLearned ? `
                <button class="action-btn btn-learned" onclick="markAsLearned(${word.id})">
                    <i class="fas fa-check"></i>
                    학습완료
                </button>
            ` : `
                <button class="action-btn" style="background: #4CAF50; color: white;" disabled>
                    <i class="fas fa-check-circle"></i>
                    완료됨
                </button>
            `}
        </div>
    `;
    
    return card;
}

// TTS 음성 재생
function speakWord(wordId, language = 'khmer') {
    const word = currentWords.find(w => w.id === wordId) || 
                 (wordId === 'quiz' ? getCurrentQuizWord() : null);
    
    if (!word) {
        console.error('단어를 찾을 수 없습니다:', wordId);
        return;
    }
    
    // Web Speech API 사용
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance();
        
        if (language === 'khmer') {
            utterance.text = word.khmer_term;
            utterance.lang = 'km-KH'; // 크메르어
        } else if (language === 'korean') {
            utterance.text = word.korean_term;
            utterance.lang = 'ko-KR'; // 한국어
        }
        
        utterance.rate = 0.8; // 조금 느리게
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // 음성 재생 시각적 피드백
        const button = event ? event.target : document.querySelector(`[onclick*="${wordId}"]`);
        if (button) {
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 재생중';
            button.disabled = true;
            
            utterance.onend = function() {
                button.innerHTML = originalHTML;
                button.disabled = false;
            };
            
            utterance.onerror = function() {
                button.innerHTML = originalHTML;
                button.disabled = false;
                console.error('음성 재생 오류');
            };
        }
        
        speechSynthesis.speak(utterance);
        
    } else {
        alert('이 브라우저는 음성 재생을 지원하지 않습니다.');
    }
}

// 학습 완료 표시
function markAsLearned(wordId) {
    // 사용자 데이터 업데이트
    userStats.learnedWords.add(wordId);
    userStats.totalLearned = userStats.learnedWords.size;
    learnedToday++;
    
    // UI 업데이트
    const wordCard = document.querySelector(`[data-word-id="${wordId}"]`);
    if (wordCard) {
        wordCard.classList.add('learned');
        
        // 버튼 변경
        const actionsContainer = wordCard.querySelector('.word-actions');
        const learnedBtn = actionsContainer.querySelector('.btn-learned');
        if (learnedBtn) {
            learnedBtn.outerHTML = `
                <button class="action-btn" style="background: #4CAF50; color: white;" disabled>
                    <i class="fas fa-check-circle"></i>
                    완료됨
                </button>
            `;
        }
    }
    
    // 진행률 업데이트
    updateUI();
    
    // 저장
    saveUserStats();
    
    // 축하 효과
    showCelebration();
    
    // 모든 단어 학습 완료 체크
    if (learnedToday === 10) {
        setTimeout(() => {
            alert('🎉 오늘의 학습을 모두 완료했습니다! 내일 새로운 단어로 만나요!');
        }, 500);
    }
}

// UI 업데이트
function updateUI() {
    // 헤더 정보 업데이트
    const dayInfo = document.getElementById('dayInfo');
    const dailyProgress = document.getElementById('dailyProgress');
    
    const todayLearned = currentWords.filter(word => userStats.learnedWords.has(word.id)).length;
    const progressPercent = (todayLearned / 10) * 100;
    
    dayInfo.textContent = `Day ${currentDay} - 오늘의 학습: ${todayLearned}/10`;
    dailyProgress.style.width = `${progressPercent}%`;
    
    // 통계 화면 업데이트
    document.getElementById('totalLearned').textContent = userStats.totalLearned;
    document.getElementById('currentStreak').textContent = userStats.currentStreak;
    document.getElementById('todayProgress').textContent = `${Math.round(progressPercent)}%`;
    document.getElementById('totalProgress').textContent = `${Math.round((userStats.totalLearned / 8000) * 100)}%`;
}

// 카테고리 필터 초기화
function initializeCategoryFilter() {
    const categoryFilter = document.getElementById('categoryFilter');
    const chips = categoryFilter.querySelectorAll('.category-chip');
    
    chips.forEach(chip => {
        chip.addEventListener('click', function() {
            // 활성 상태 변경
            chips.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            
            // 필터링 적용
            const category = this.dataset.category;
            filterWordsByCategory(category);
        });
    });
}

// 카테고리별 필터링
function filterWordsByCategory(category) {
    const wordCards = document.querySelectorAll('.word-card');
    
    wordCards.forEach(card => {
        const wordId = parseInt(card.dataset.wordId);
        const word = currentWords.find(w => w.id === wordId);
        
        if (category === 'all' || word.category === category) {
            card.style.display = 'block';
            card.classList.add('fade-in');
        } else {
            card.style.display = 'none';
        }
    });
}

// 화면 전환
function showView(viewName) {
    // 모든 뷰 숨기기
    const views = document.querySelectorAll('.view');
    views.forEach(view => view.classList.add('hidden'));
    
    // 네비게이션 버튼 상태 변경
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => btn.classList.remove('active'));
    
    // 선택된 뷰 표시
    const targetView = document.getElementById(`${viewName}View`);
    if (targetView) {
        targetView.classList.remove('hidden');
        targetView.classList.add('fade-in');
    }
    
    // 활성 네비게이션 버튼 표시
    const activeBtn = document.querySelector(`[onclick="showView('${viewName}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // 뷰별 특별 처리
    switch(viewName) {
        case 'quiz':
            initializeQuiz();
            break;
        case 'stats':
            updateUI();
            break;
    }
}

// 퀴즈 초기화
function initializeQuiz() {
    const learnedWords = currentWords.filter(word => userStats.learnedWords.has(word.id));
    
    if (learnedWords.length === 0) {
        document.getElementById('quizView').innerHTML = `
            <div class="quiz-card">
                <div style="text-align: center; padding: 2rem;">
                    <i class="fas fa-book-open" style="font-size: 3rem; color: #ccc; margin-bottom: 1rem;"></i>
                    <h3 style="color: #666;">아직 학습한 단어가 없습니다</h3>
                    <p style="color: #999;">먼저 오늘의 단어를 학습해보세요!</p>
                    <button class="action-btn btn-learned" onclick="showView('home')" style="margin-top: 1rem;">
                        <i class="fas fa-arrow-left"></i>
                        학습하러 가기
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    quizWords = [...learnedWords];
    currentQuizIndex = 0;
    showQuizQuestion();
}

// 퀴즈 문제 표시
function showQuizQuestion() {
    if (currentQuizIndex >= quizWords.length) {
        showQuizResult();
        return;
    }
    
    const currentWord = quizWords[currentQuizIndex];
    const options = generateQuizOptions(currentWord);
    
    document.getElementById('quizWord').textContent = currentWord.khmer_term;
    
    const optionsContainer = document.getElementById('quizOptions');
    optionsContainer.innerHTML = '';
    
    options.forEach(option => {
        const optionElement = document.createElement('div');
        optionElement.className = 'quiz-option';
        optionElement.textContent = option;
        optionElement.onclick = () => selectQuizOption(optionElement, option, currentWord.korean_term);
        optionsContainer.appendChild(optionElement);
    });
}

// 퀴즈 선택지 생성
function generateQuizOptions(correctWord) {
    const options = [correctWord.korean_term];
    
    // 다른 단어들에서 오답 선택지 생성
    const otherWords = currentWords.filter(w => w.id !== correctWord.id);
    while (options.length < 4 && otherWords.length > 0) {
        const randomWord = otherWords.splice(Math.floor(Math.random() * otherWords.length), 1)[0];
        if (!options.includes(randomWord.korean_term)) {
            options.push(randomWord.korean_term);
        }
    }
    
    // 배열 섞기
    return options.sort(() => Math.random() - 0.5);
}

// 퀴즈 옵션 선택
function selectQuizOption(element, selectedOption, correctAnswer) {
    // 모든 옵션 비활성화
    const options = document.querySelectorAll('.quiz-option');
    options.forEach(opt => opt.style.pointerEvents = 'none');
    
    // 정답/오답 표시
    if (selectedOption === correctAnswer) {
        element.classList.add('correct');
    } else {
        element.classList.add('incorrect');
        // 정답 표시
        options.forEach(opt => {
            if (opt.textContent === correctAnswer) {
                opt.classList.add('correct');
            }
        });
    }
    
    // 다음 문제로 이동
    setTimeout(() => {
        currentQuizIndex++;
        showQuizQuestion();
    }, 1500);
}

// 퀴즈 결과 표시
function showQuizResult() {
    document.getElementById('quizView').innerHTML = `
        <div class="quiz-card">
            <div style="text-align: center;">
                <i class="fas fa-trophy" style="font-size: 3rem; color: #FFD700; margin-bottom: 1rem;"></i>
                <h3 style="color: var(--primary-dark);">퀴즈 완료!</h3>
                <p style="margin: 1rem 0;">총 ${quizWords.length}문제를 풀었습니다.</p>
                <button class="action-btn btn-learned" onclick="showView('home')" style="margin-top: 1rem;">
                    <i class="fas fa-arrow-left"></i>
                    학습으로 돌아가기
                </button>
            </div>
        </div>
    `;
}

// 현재 퀴즈 단어 가져오기
function getCurrentQuizWord() {
    return quizWords[currentQuizIndex];
}

// 설정 메뉴 표시
function showSettings() {
    alert('설정 기능은 곧 추가될 예정입니다.');
}

// 축하 효과
function showCelebration() {
    // 간단한 축하 효과
    const celebration = document.createElement('div');
    celebration.innerHTML = '🎉';
    celebration.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        z-index: 9999;
        pointer-events: none;
        animation: celebrationPop 0.6s ease;
    `;
    
    // 애니메이션 CSS 추가
    if (!document.getElementById('celebrationStyle')) {
        const style = document.createElement('style');
        style.id = 'celebrationStyle';
        style.textContent = `
            @keyframes celebrationPop {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
                50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(celebration);
    
    setTimeout(() => {
        document.body.removeChild(celebration);
    }, 600);
}

// PWA 기능 초기화
function initializePWA() {
    // 서비스 워커 등록
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('ServiceWorker registered:', registration);
            })
            .catch(error => {
                console.log('ServiceWorker registration failed:', error);
            });
    }
    
    // 설치 프롬프트 처리
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        // 설치 버튼 표시 (필요시)
        console.log('PWA 설치 가능');
    });
}

// 로딩 표시
function showLoading() {
    const container = document.getElementById('dailyWords');
    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
        </div>
    `;
}

// 유틸리티 함수들
const Utils = {
    // 날짜 포맷
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('ko-KR');
    },
    
    // 랜덤 요소 선택
    getRandomElement: function(array) {
        return array[Math.floor(Math.random() * array.length)];
    },
    
    // 배열 섞기
    shuffleArray: function(array) {
        const newArray = [...array];
        for (let i = newArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
        }
        return newArray;
    }
};

// 전역 함수로 내보내기 (HTML onclick에서 사용)
window.speakWord = speakWord;
window.markAsLearned = markAsLearned;
window.showView = showView;
window.showSettings = showSettings;

console.log('📱 모바일 학습 앱 JavaScript 로드 완료!');
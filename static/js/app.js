// 캄보디아 농업용어 사전 - JavaScript 기능

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 앱 초기화
function initializeApp() {
    console.log('농업용어 사전 앱 초기화...');
    
    // 툴팁 초기화
    initializeTooltips();
    
    // 검색 기능 초기화
    initializeSearch();
    
    // 폼 유효성 검사 초기화
    initializeFormValidation();
    
    // 카드 애니메이션 초기화
    initializeCardAnimations();
    
    // 통계 카운터 애니메이션
    initializeStatCounters();
    
    console.log('앱 초기화 완료!');
}

// 툴팁 초기화
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 검색 기능
function initializeSearch() {
    const searchInput = document.querySelector('input[name="keyword"]');
    const searchForm = document.querySelector('form[action*="search"]');
    
    if (searchInput) {
        // 실시간 검색 제안
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2) {
                    // 실시간 검색 제안 로직 (필요시 구현)
                    console.log('검색어:', this.value);
                }
            }, 300);
        });
        
        // 엔터키 검색
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (searchForm) {
                    searchForm.submit();
                }
            }
        });
    }
}

// 폼 유효성 검사
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate="true"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });
}

// 폼 유효성 검사 함수
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
            
            // 에러 메시지 표시
            showFieldError(field, '이 필드는 필수입니다.');
        } else {
            field.classList.remove('is-invalid');
            hideFieldError(field);
        }
    });
    
    return isValid;
}

// 필드 에러 메시지 표시
function showFieldError(field, message) {
    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

// 필드 에러 메시지 숨기기
function hideFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// 카드 애니메이션
function initializeCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    // Intersection Observer로 스크롤 애니메이션
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// 통계 카운터 애니메이션
function initializeStatCounters() {
    const counters = document.querySelectorAll('.stat-item h3');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        if (!isNaN(target)) {
            animateCounter(counter, 0, target, 1000);
        }
    });
}

// 카운터 애니메이션 함수
function animateCounter(element, start, end, duration) {
    let startTime = null;
    
    function animate(currentTime) {
        if (startTime === null) startTime = currentTime;
        const progress = Math.min((currentTime - startTime) / duration, 1);
        
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

// API 호출 함수들
const API = {
    // 용어 검색
    searchTerms: async function(params) {
        try {
            const url = new URL('/api/search', window.location.origin);
            Object.keys(params).forEach(key => {
                if (params[key]) url.searchParams.append(key, params[key]);
            });
            
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            console.error('검색 API 오류:', error);
            return { success: false, error: error.message };
        }
    },
    
    // 통계 정보 가져오기
    getStatistics: async function() {
        try {
            const response = await fetch('/api/statistics');
            return await response.json();
        } catch (error) {
            console.error('통계 API 오류:', error);
            return null;
        }
    }
};

// 유틸리티 함수들
const Utils = {
    // 알림 메시지 표시
    showAlert: function(message, type = 'success') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.querySelector('main .container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', alertHtml);
            
            // 3초 후 자동 제거
            setTimeout(() => {
                const alert = container.querySelector('.alert');
                if (alert) {
                    alert.remove();
                }
            }, 3000);
        }
    },
    
    // 로딩 스피너 표시/숨기기
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<span class="loading"></span> 로딩 중...';
            element.disabled = true;
        }
    },
    
    hideLoading: function(element, originalText) {
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    },
    
    // 텍스트 하이라이트
    highlightText: function(text, searchTerm) {
        if (!searchTerm) return text;
        
        const regex = new RegExp(`(${searchTerm})`, 'gi');
        return text.replace(regex, '<span class="search-highlight">$1</span>');
    },
    
    // 날짜 포맷팅
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    // 텍스트 길이 제한
    truncateText: function(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
};

// 검색 페이지 전용 기능
if (window.location.pathname.includes('/search')) {
    document.addEventListener('DOMContentLoaded', function() {
        // 카테고리/난이도 변경 시 자동 제출
        const categorySelect = document.getElementById('category');
        const difficultySelect = document.getElementById('difficulty');
        
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                this.form.submit();
            });
        }
        
        if (difficultySelect) {
            difficultySelect.addEventListener('change', function() {
                this.form.submit();
            });
        }
        
        // 검색 결과 카드 호버 효과
        const termCards = document.querySelectorAll('.term-card');
        termCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.15)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '';
            });
        });
    });
}

// 용어 추가/편집 페이지 전용 기능
if (window.location.pathname.includes('/add_term') || window.location.pathname.includes('/edit_term')) {
    document.addEventListener('DOMContentLoaded', function() {
        // 실시간 글자 수 카운터
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            const counter = document.createElement('small');
            counter.className = 'text-muted';
            textarea.parentNode.appendChild(counter);
            
            function updateCounter() {
                const length = textarea.value.length;
                counter.textContent = `${length}자`;
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter();
        });
        
        // 태그 입력 도우미
        const tagsInput = document.getElementById('tags');
        if (tagsInput) {
            tagsInput.addEventListener('input', function() {
                const tags = this.value.split(',').map(tag => tag.trim()).filter(tag => tag);
                console.log('현재 태그:', tags);
            });
        }
    });
}

// 글로벌 이벤트 리스너
window.addEventListener('load', function() {
    // 페이지 로드 완료 후 실행할 코드
    console.log('페이지 로드 완료');
});

window.addEventListener('beforeunload', function(e) {
    // 페이지를 떠나기 전 (필요시 경고 메시지)
    const forms = document.querySelectorAll('form');
    let hasUnsavedChanges = false;
    
    forms.forEach(form => {
        const formData = new FormData(form);
        if (formData.values().next().value) {
            hasUnsavedChanges = true;
        }
    });
    
    if (hasUnsavedChanges) {
        e.preventDefault();
        e.returnValue = '저장하지 않은 변경사항이 있습니다. 정말 떠나시겠습니까?';
    }
});
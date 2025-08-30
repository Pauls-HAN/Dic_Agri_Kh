#!/usr/bin/env python3
"""
5,000개 농업용어 HTML 성능 최적화
Performance optimization for 5,000 terms HTML
"""

import re
from datetime import datetime

def optimize_html_performance():
    """대용량 데이터 성능 최적화"""
    
    print("🔧 5,000개 용어 HTML 성능 최적화 중...")
    
    # 기존 파일 로드
    with open('/home/user/webapp/templates/agricultural_learning_v3_5000.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("1️⃣ 페이지네이션 설정 최적화...")
    # 페이지네이션 기본값을 20으로 증가 (대용량 데이터 처리)
    html_content = html_content.replace(
        'itemsPerPage: 15',
        'itemsPerPage: 20'
    )
    
    print("2️⃣ 초기 로딩 최적화...")
    # 초기 렌더링 최적화를 위한 가상화 설정
    virtual_scrolling_script = '''
        // 가상 스크롤링을 위한 최적화
        let isVirtualized = true;
        let virtualChunkSize = 100; // 한 번에 렌더링할 아이템 수
        let currentChunk = 0;
        
        // 초기 렌더링 시 첫 번째 청크만 렌더링
        const originalRenderTermsTable = renderTermsTable;
        renderTermsTable = function(terms) {
            if (terms.length > virtualChunkSize && isVirtualized) {
                const chunkedTerms = terms.slice(0, virtualChunkSize);
                originalRenderTermsTable(chunkedTerms);
                
                // 나머지는 지연 로딩
                if (terms.length > virtualChunkSize) {
                    setTimeout(() => {
                        const remainingTerms = terms.slice(virtualChunkSize);
                        originalRenderTermsTable(terms); // 전체 렌더링
                        isVirtualized = false;
                    }, 100);
                }
            } else {
                originalRenderTermsTable(terms);
            }
        };
        
        // 스크롤 이벤트 스로틀링
        let scrollTimeout;
        function throttledScroll(callback) {
            if (scrollTimeout) return;
            scrollTimeout = setTimeout(() => {
                callback();
                scrollTimeout = null;
            }, 16); // 60fps
        }
        
        // 검색 디바운싱 최적화
        let searchTimeout;
        function debouncedSearch(callback, delay = 300) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(callback, delay);
        }
    '''
    
    # 스크립트 섹션 찾아서 성능 최적화 코드 삽입
    script_insert_point = html_content.find('        const speak = (text) => {')
    if script_insert_point > -1:
        html_content = html_content[:script_insert_point] + virtual_scrolling_script + '\n        ' + html_content[script_insert_point:]
    
    print("3️⃣ 검색 최적화...")
    # 검색 이벤트에 디바운싱 적용
    search_event_pattern = r'elements\.searchInput\.addEventListener\(\'input\', updateAndRender\);'
    optimized_search_event = '''elements.searchInput.addEventListener('input', () => {
            debouncedSearch(updateAndRender, 200);
        });'''
    
    html_content = re.sub(search_event_pattern, optimized_search_event, html_content)
    
    print("4️⃣ 메모리 사용 최적화...")
    # 큰 데이터셋에 대한 메모리 관리
    memory_optimization = '''
        // 메모리 최적화를 위한 가비지 컬렉션 힌트
        let gcCounter = 0;
        const originalHandleTermSelect = handleTermSelect;
        handleTermSelect = function(term) {
            originalHandleTermSelect(term);
            gcCounter++;
            if (gcCounter % 100 === 0) {
                // 100번마다 메모리 정리 힌트
                setTimeout(() => {
                    if (window.gc) window.gc();
                }, 0);
            }
        };
        
        // DOM 요소 재활용
        const elementPool = {
            rows: [],
            getRow: function() {
                return this.rows.pop() || document.createElement('tr');
            },
            recycleRow: function(row) {
                row.innerHTML = '';
                row.className = '';
                this.rows.push(row);
            }
        };
    '''
    
    # 메모리 최적화 코드 삽입
    memory_insert_point = html_content.find('        const updateStatsDisplay = () => {')
    if memory_insert_point > -1:
        html_content = html_content[:memory_insert_point] + memory_optimization + '\n        ' + html_content[memory_insert_point:]
    
    print("5️⃣ 로딩 인디케이터 추가...")
    # 로딩 상태 표시
    loading_css = '''
        .loading-indicator {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 20px;
            border-radius: 8px;
            font-size: 16px;
            z-index: 10000;
            display: none;
        }
        
        .loading-indicator.show {
            display: block;
        }
        
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4CAF50;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    '''
    
    # CSS에 로딩 스타일 추가
    css_insert_point = html_content.find('        }')
    if css_insert_point > -1:
        html_content = html_content[:css_insert_point] + '        }\n        \n        ' + loading_css + html_content[css_insert_point+9:]
    
    # 로딩 인디케이터 HTML 추가
    loading_html = '''
    <div id="loadingIndicator" class="loading-indicator">
        <div class="loading-spinner"></div>
        5,000개 농업용어 로딩 중...
    </div>
    '''
    
    # body 끝 직전에 로딩 인디케이터 추가
    body_end_point = html_content.rfind('</body>')
    if body_end_point > -1:
        html_content = html_content[:body_end_point] + loading_html + '\n' + html_content[body_end_point:]
    
    print("6️⃣ 초기화 최적화...")
    # 앱 초기화 시 로딩 표시
    init_optimization = '''
        // 앱 초기화 로딩
        document.addEventListener('DOMContentLoaded', () => {
            const loadingIndicator = document.getElementById('loadingIndicator');
            loadingIndicator.classList.add('show');
            
            // 무거운 초기화 작업을 지연
            setTimeout(() => {
                initializeApp();
                loadingIndicator.classList.remove('show');
            }, 100);
        });
        
        function initializeApp() {
    '''
    
    # 기존 초기화 코드 찾아서 최적화
    init_pattern = r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{'
    html_content = re.sub(init_pattern, init_optimization.strip(), html_content)
    
    # 닫는 브래킷 추가
    html_content = html_content.replace('        });', '        }\n        });')
    
    print("7️⃣ 타이틀 및 메타데이터 최종 업데이트...")
    # 성능 최적화 버전임을 명시
    html_content = html_content.replace(
        '<title>캄보디아 농업용어 5,000개 학습 V3 (모바일 최적화)</title>',
        '<title>캄보디아 농업용어 5,000개 학습 V3 (성능 최적화)</title>'
    )
    
    html_content = html_content.replace(
        '<h1>캄보디아 농업용어 5,000개 학습</h1>',
        '<h1>캄보디아 농업용어 5,000개 학습 🚀</h1>'
    )
    
    html_content = html_content.replace(
        '<p class="subtitle">5,000개 농업용어 · 크메르어 ↔ 한국어 + 영어 · 25개 카테고리</p>',
        '<p class="subtitle">🚀 5,000개 농업용어 · 성능최적화 · 25개 카테고리 · 크메르어↔한국어+영어</p>'
    )
    
    # 최적화된 파일 저장
    optimized_path = '/home/user/webapp/templates/agricultural_learning_v3_5000_optimized.html'
    with open(optimized_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 성능 최적화 완료!")
    print(f"📂 최적화 파일: {optimized_path}")
    
    # 파일 크기 확인
    import os
    file_size_mb = os.path.getsize(optimized_path) / (1024 * 1024)
    print(f"📏 최적화 파일 크기: {file_size_mb:.1f}MB")
    
    return optimized_path

if __name__ == "__main__":
    optimize_html_performance()
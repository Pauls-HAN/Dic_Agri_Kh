// 캄보디아 농업용어 학습 앱 - 서비스 워커
// PWA 오프라인 기능 및 캐시 관리

const CACHE_NAME = 'agriculture-learning-v2.0';
const OFFLINE_PAGE = '/mobile';

// 캐시할 리소스들
const CACHE_URLS = [
    '/',
    '/mobile',
    '/static/css/style.css',
    '/static/js/mobile_learning_app.js',
    '/static/js/app.js',
    '/manifest.json',
    // 오프라인 페이지
    '/static/offline.html'
];

// API 캐시 설정
const API_CACHE_NAME = 'agriculture-api-v2.0';
const API_URLS = [
    '/api/categories',
    '/api/learning_statistics'
];

// 서비스 워커 설치
self.addEventListener('install', function(event) {
    console.log('🔧 서비스 워커 설치 중...');
    
    event.waitUntil(
        Promise.all([
            // 정적 리소스 캐시
            caches.open(CACHE_NAME).then(function(cache) {
                console.log('📦 정적 리소스 캐시 중...');
                return cache.addAll(CACHE_URLS);
            }),
            // API 캐시 초기화
            caches.open(API_CACHE_NAME).then(function(cache) {
                console.log('🔄 API 캐시 초기화...');
                return Promise.resolve();
            })
        ]).then(function() {
            console.log('✅ 서비스 워커 설치 완료');
            // 즉시 활성화
            return self.skipWaiting();
        })
    );
});

// 서비스 워커 활성화
self.addEventListener('activate', function(event) {
    console.log('🚀 서비스 워커 활성화 중...');
    
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    // 오래된 캐시 삭제
                    if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
                        console.log('🗑️ 오래된 캐시 삭제:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(function() {
            console.log('✅ 서비스 워커 활성화 완료');
            // 모든 탭에서 즉시 제어
            return self.clients.claim();
        })
    );
});

// 네트워크 요청 가로채기
self.addEventListener('fetch', function(event) {
    const request = event.request;
    const url = new URL(request.url);
    
    // GET 요청만 처리
    if (request.method !== 'GET') {
        return;
    }
    
    // API 요청 처리
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(handleApiRequest(request));
        return;
    }
    
    // 정적 리소스 및 페이지 요청 처리
    event.respondWith(handleStaticRequest(request));
});

// API 요청 처리 (캐시 우선, 네트워크 폴백)
async function handleApiRequest(request) {
    const url = new URL(request.url);
    
    try {
        // 특정 API는 항상 네트워크에서 가져오기
        const alwaysNetworkAPIs = ['/api/daily_words', '/api/generate_sample_data'];
        const shouldBypassCache = alwaysNetworkAPIs.some(api => url.pathname.startsWith(api));
        
        if (!shouldBypassCache) {
            // 캐시에서 먼저 확인
            const cache = await caches.open(API_CACHE_NAME);
            const cachedResponse = await cache.match(request);
            
            if (cachedResponse) {
                console.log('📱 API 캐시에서 응답:', url.pathname);
                
                // 백그라운드에서 업데이트 (stale-while-revalidate)
                fetch(request).then(response => {
                    if (response.ok) {
                        cache.put(request, response.clone());
                    }
                }).catch(err => {
                    console.log('🔄 백그라운드 API 업데이트 실패:', err);
                });
                
                return cachedResponse;
            }
        }
        
        // 네트워크에서 가져오기
        const response = await fetch(request);
        
        if (response.ok) {
            // 성공적인 응답을 캐시에 저장
            const cache = await caches.open(API_CACHE_NAME);
            cache.put(request, response.clone());
            console.log('🌐 네트워크에서 API 응답 및 캐시:', url.pathname);
        }
        
        return response;
        
    } catch (error) {
        console.log('❌ API 요청 실패:', url.pathname, error);
        
        // 캐시에서 폴백 응답 시도
        const cache = await caches.open(API_CACHE_NAME);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            console.log('📱 오프라인 모드 - API 캐시 응답:', url.pathname);
            return cachedResponse;
        }
        
        // 기본 오프라인 API 응답
        return createOfflineApiResponse(url.pathname);
    }
}

// 정적 리소스 요청 처리 (캐시 우선, 네트워크 폴백)
async function handleStaticRequest(request) {
    try {
        // 캐시에서 먼저 확인
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            console.log('📱 캐시에서 응답:', request.url);
            return cachedResponse;
        }
        
        // 네트워크에서 가져오기
        const response = await fetch(request);
        
        if (response.ok) {
            // 성공적인 응답을 캐시에 저장
            cache.put(request, response.clone());
            console.log('🌐 네트워크에서 응답 및 캐시:', request.url);
        }
        
        return response;
        
    } catch (error) {
        console.log('❌ 네트워크 요청 실패:', request.url, error);
        
        // 오프라인 페이지 반환 (HTML 요청인 경우)
        if (request.destination === 'document') {
            const cache = await caches.open(CACHE_NAME);
            const offlineResponse = await cache.match('/mobile');
            
            if (offlineResponse) {
                return offlineResponse;
            }
        }
        
        // 기본 오프라인 응답
        return new Response('오프라인 상태입니다.', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
    }
}

// 오프라인 API 응답 생성
function createOfflineApiResponse(pathname) {
    let offlineData = {};
    
    switch (pathname) {
        case '/api/categories':
            offlineData = {
                success: false,
                offline: true,
                categories: [
                    "작물재배", "축산업", "농기계", "토양관리", "비료", "병해충방제",
                    "수확후처리", "저장기술", "가공기술", "유통", "농업정책", "농업경영"
                ]
            };
            break;
            
        case '/api/learning_statistics':
            offlineData = {
                success: false,
                offline: true,
                total_terms: 0,
                message: '오프라인 상태입니다. 인터넷 연결을 확인해주세요.'
            };
            break;
            
        default:
            if (pathname.includes('/api/daily_words')) {
                offlineData = {
                    success: false,
                    offline: true,
                    words: [],
                    message: '오프라인 상태입니다. 저장된 학습 데이터를 확인해보세요.'
                };
            } else {
                offlineData = {
                    success: false,
                    offline: true,
                    error: '오프라인 상태입니다.',
                    message: '인터넷 연결을 확인한 후 다시 시도해주세요.'
                };
            }
    }
    
    return new Response(JSON.stringify(offlineData), {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
            'Content-Type': 'application/json; charset=utf-8'
        }
    });
}

// 푸시 알림 처리 (향후 확장용)
self.addEventListener('push', function(event) {
    console.log('🔔 푸시 알림 수신:', event);
    
    const options = {
        body: event.data ? event.data.text() : '새로운 농업용어를 학습해보세요!',
        icon: '/static/images/icon-192x192.png',
        badge: '/static/images/badge-72x72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'learn',
                title: '학습하기',
                icon: '/static/images/action-learn.png'
            },
            {
                action: 'close',
                title: '닫기',
                icon: '/static/images/action-close.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('캄보디아 농업용어 학습', options)
    );
});

// 알림 클릭 처리
self.addEventListener('notificationclick', function(event) {
    console.log('🔔 알림 클릭:', event);
    
    event.notification.close();
    
    if (event.action === 'learn') {
        // 학습 페이지로 이동
        event.waitUntil(
            clients.openWindow('/mobile')
        );
    } else if (event.action === 'close') {
        // 알림만 닫기
        return;
    } else {
        // 기본 동작: 앱 열기
        event.waitUntil(
            clients.openWindow('/mobile')
        );
    }
});

// 백그라운드 동기화 (향후 확장용)
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        console.log('🔄 백그라운드 동기화 시작');
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    try {
        // 학습 진행 데이터 동기화 등
        console.log('🔄 백그라운드 동기화 수행');
        
        // API 캐시 업데이트
        const cache = await caches.open(API_CACHE_NAME);
        
        const apiUrls = [
            '/api/categories',
            '/api/learning_statistics'
        ];
        
        for (const url of apiUrls) {
            try {
                const response = await fetch(url);
                if (response.ok) {
                    await cache.put(url, response);
                    console.log('✅ 캐시 업데이트:', url);
                }
            } catch (err) {
                console.log('❌ 캐시 업데이트 실패:', url, err);
            }
        }
        
    } catch (error) {
        console.log('❌ 백그라운드 동기화 실패:', error);
    }
}

// 메시지 처리 (클라이언트와의 통신)
self.addEventListener('message', function(event) {
    console.log('💬 메시지 수신:', event.data);
    
    if (event.data && event.data.type) {
        switch (event.data.type) {
            case 'SKIP_WAITING':
                self.skipWaiting();
                break;
                
            case 'GET_VERSION':
                event.ports[0].postMessage({
                    type: 'VERSION',
                    version: CACHE_NAME
                });
                break;
                
            case 'CLEAR_CACHE':
                clearAllCaches().then(() => {
                    event.ports[0].postMessage({
                        type: 'CACHE_CLEARED',
                        success: true
                    });
                });
                break;
        }
    }
});

// 모든 캐시 삭제
async function clearAllCaches() {
    const cacheNames = await caches.keys();
    return Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
    );
}

console.log('🔧 서비스 워커 스크립트 로드 완료:', CACHE_NAME);
/**
 * 캄보디아 농업용어 학습 앱 Service Worker
 * PWA 오프라인 지원 및 캐싱
 */

const CACHE_NAME = 'agricultural-terms-v2.0';
const urlsToCache = [
  '/mobile/improved',
  '/static/js/improved_mobile_app.js',
  '/static/css/improved_mobile_app.css',
  'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap',
  'https://fonts.googleapis.com/css2?family=Battambang:wght@400;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Service Worker 설치
self.addEventListener('install', event => {
  console.log('Service Worker 설치 중...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('캐시 파일들을 저장 중...');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('캐시 저장 실패:', error);
      })
  );
});

// Service Worker 활성화
self.addEventListener('activate', event => {
  console.log('Service Worker 활성화 중...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('이전 캐시 삭제:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch 이벤트 처리
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 캐시에 있으면 캐시에서 반환
        if (response) {
          console.log('캐시에서 제공:', event.request.url);
          return response;
        }

        // 캐시에 없으면 네트워크에서 가져오기
        return fetch(event.request).then(
          response => {
            // 응답이 유효하지 않으면 그대로 반환
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // 응답을 복제하여 캐시에 저장
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                // API 응답도 캐시에 저장 (일정 시간 후 만료)
                if (event.request.url.includes('/api/')) {
                  console.log('API 응답 캐시:', event.request.url);
                }
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      }).catch(() => {
        // 네트워크도 실패하면 오프라인 페이지 표시
        if (event.request.destination === 'document') {
          return caches.match('/mobile/improved');
        }
      })
  );
});

// 백그라운드 동기화 (추후 구현)
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    console.log('백그라운드 동기화 실행');
    event.waitUntil(doBackgroundSync());
  }
});

// 푸시 알림 처리 (추후 구현)
self.addEventListener('push', event => {
  console.log('푸시 알림 수신:', event);
  
  const options = {
    body: '새로운 학습 단어가 준비되었습니다!',
    icon: '/static/images/icon-192x192.png',
    badge: '/static/images/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '2'
    }
  };
  
  event.waitUntil(
    self.registration.showNotification('캄보디아 농업용어 학습', options)
  );
});

// 알림 클릭 처리
self.addEventListener('notificationclick', event => {
  console.log('알림 클릭:', event);
  
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('/mobile/improved')
  );
});

// 백그라운드 동기화 함수
async function doBackgroundSync() {
  try {
    // 오프라인 중에 저장된 데이터를 서버와 동기화
    console.log('백그라운드 동기화 시작...');
    
    // 로컬 스토리지에서 동기화할 데이터 가져오기
    const syncData = await getLocalSyncData();
    
    if (syncData && syncData.length > 0) {
      // 서버에 데이터 전송
      await syncWithServer(syncData);
      // 동기화 완료 후 로컬 데이터 정리
      await clearLocalSyncData();
    }
    
    console.log('백그라운드 동기화 완료');
  } catch (error) {
    console.error('백그라운드 동기화 실패:', error);
  }
}

// 로컬 동기화 데이터 가져오기
async function getLocalSyncData() {
  // IndexedDB나 localStorage에서 동기화할 데이터 가져오기
  return [];
}

// 서버와 동기화
async function syncWithServer(data) {
  const response = await fetch('/api/sync', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return response.json();
}

// 로컬 동기화 데이터 정리
async function clearLocalSyncData() {
  // 동기화 완료된 로컬 데이터 정리
}

console.log('Service Worker 로드 완료');
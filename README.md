# 캄보디아 농업용어 사전 (Dic_Agri_Kh)

한국어-크메르어 농업 전문용어 3000단어 수집 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 농업 분야의 한국어와 캄보디아어(크메르어) 전문용어를 체계적으로 정리한 웹 기반 사전입니다. 목표는 3,000개의 농업 관련 용어를 수집하여 한-캄 농업 협력과 기술 전수를 지원하는 것입니다.

## 🚀 주요 기능

### 용어 관리
- ✅ 다국어 용어 추가/편집/삭제 (한국어, 크메르어, 영어)
- ✅ 카테고리별 분류 (작물재배, 축산업, 농기계 등 17개 분야)
- ✅ 난이도별 구분 (기초, 중급, 고급)
- ✅ 용어 검증 시스템

### 검색 및 탐색
- ✅ 다중 언어 검색 지원
- ✅ 카테고리/난이도 필터링
- ✅ 태그 기반 검색
- ✅ 실시간 검색 결과

### 통계 및 관리
- ✅ 프로젝트 진행률 추적
- ✅ 카테고리별/난이도별 분포 통계
- ✅ 시각적 차트 (Chart.js)
- ✅ CSV 내보내기 기능

## 🛠️ 기술 스택

### 백엔드
- **Python 3.12**
- **Flask 2.3.3** - 웹 프레임워크
- **JSON** - 데이터 저장 형태

### 프론트엔드
- **HTML5/CSS3/JavaScript**
- **Bootstrap 5.1.3** - UI 프레임워크
- **Font Awesome 6.0** - 아이콘
- **Chart.js** - 데이터 시각화

### 배포
- **Supervisor** - 프로세스 관리
- **Linux** - 서버 환경

## 📊 프로젝트 현황

```
총 목표: 3,000개 농업용어
현재 등록: 10개 용어 (0.33% 완료)
검증 완료: 0개
카테고리: 17개 분야
```

### 카테고리 분포
1. 작물재배 - 1개
2. 농기계 - 1개  
3. 비료 - 1개
4. 수확 - 1개
5. 수자원 - 1개
6. 토양 - 1개
7. 병해충 - 1개
8. 농업시설 - 1개
9. 종자 - 1개
10. 농약 - 1개

## 🏗️ 프로젝트 구조

```
webapp/
├── data/                          # 데이터 파일
│   ├── agricultural_terms.json    # 메인 용어 데이터베이스
│   └── agricultural_terms_schema.json # 데이터 스키마
├── src/                           # 소스 코드
│   ├── app.py                     # Flask 웹 애플리케이션
│   ├── term_manager.py            # 용어 관리 클래스
│   └── sample_data.py             # 샘플 데이터 생성
├── templates/                     # HTML 템플릿
│   ├── base.html                  # 기본 레이아웃
│   ├── index.html                 # 메인 페이지
│   ├── search.html                # 검색 페이지
│   ├── add_term.html              # 용어 추가
│   ├── edit_term.html             # 용어 편집
│   ├── term_detail.html           # 용어 상세보기
│   └── statistics.html            # 통계 페이지
├── static/                        # 정적 파일
│   ├── css/style.css              # 커스텀 스타일
│   └── js/app.js                  # JavaScript 기능
├── logs/                          # 로그 파일
├── supervisord.conf               # Supervisor 설정
├── requirements.txt               # Python 의존성
└── README.md                      # 프로젝트 문서
```

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 샘플 데이터 추가 (선택사항)
```bash
python3 src/sample_data.py
```

### 3. 웹 애플리케이션 실행

#### 개발 모드
```bash
cd src && python3 app.py
```

#### 프로덕션 모드 (Supervisor 사용)
```bash
# logs 디렉토리 생성
mkdir -p logs

# Supervisor 데몬 시작
supervisord -c supervisord.conf

# 서비스 상태 확인
supervisorctl -c supervisord.conf status

# 서비스 관리
supervisorctl -c supervisord.conf restart flask_app
supervisorctl -c supervisord.conf stop flask_app
```

### 4. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 📖 사용 가이드

### 용어 추가
1. 네비게이션에서 "용어 추가" 클릭
2. 한국어/크메르어 용어 및 정의 입력 (필수)
3. ��어 용어, 카테고리, 난이도 선택
4. 태그 및 사용 예시 추가 (선택)
5. "용어 추가" 버튼 클릭

### 용어 검색
1. 상단 검색창 또는 "검색" 페이지 이용
2. 키워드, 카테고리, 난이도로 필터링
3. 검색 결과에서 용어 상세보기/편집

### 통계 확인
1. "통계" 페이지에서 프로젝트 진행 현황 확인
2. 카테고리별, 난이도별 분포 차트
3. CSV 내보내기로 데이터 백업

## 🎯 프로젝트 목표

### 단기 목표 (1개월)
- [ ] 기초 농업용어 500개 수집
- [ ] 카테고리별 균등 분배
- [ ] 번역 품질 검증 시스템 구축

### 중기 목표 (3개월)  
- [ ] 농업용어 1,500개 달성
- [ ] 모든 용어 전문가 검증
- [ ] 모바일 반응형 최적화

### 최종 목표 (6개월)
- [ ] 농업용어 3,000개 완성
- [ ] 검색 성능 최적화
- [ ] 모바일 앱 버전 출시

## 🤝 기여 방법

1. **용어 추가**: 웹 인터페이스를 통해 새 농업용어 등록
2. **번역 검증**: 기존 용어의 번역 정확성 검토
3. **카테고리 분류**: 용어의 적절한 분야 분류
4. **기능 개선**: 코드 기여 및 버그 리포트

## 📝 데이터 스키마

각 농업용어는 다음 필드를 포함합니다:

```json
{
  "id": "고유 식별자",
  "korean_term": "한국어 용어",
  "khmer_term": "크메르어 용어", 
  "english_term": "영어 용어 (선택)",
  "category": "농업 분야 카테고리",
  "korean_definition": "한국어 정의",
  "khmer_definition": "크메르어 정의",
  "usage_example": "사용 예시",
  "difficulty_level": "난이도 (기초/중급/고급)",
  "tags": "검색용 태그 배열",
  "verified": "검증 완료 여부",
  "created_date": "생성일",
  "updated_date": "수정일"
}
```

## 📊 API 엔드포인트

- `GET /api/search` - 용어 검색
- `GET /api/statistics` - 통계 정보
- `GET /export/csv` - CSV 내보내기

## 📄 라이센스

이 프로젝트는 교육 및 연구 목적으로 개발되었습니다.

## 📞 연락처

농업용어 추가 및 검증에 관심이 있으시면 언제든 연락주세요.

---

**캄보디아 농업용어 3000단어 프로젝트**  
*농업 분야 한-크메르 용어 사전 구축을 통한 기술 협력 증진*
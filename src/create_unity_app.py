#!/usr/bin/env python3
"""
Unity 프로젝트용 완벽한 Cambodia Agri App 생성
인코딩 문제 해결 + 카테고리 정리 + 웹사이트 링크 통합
"""

import json
import os
from datetime import datetime

def create_perfect_unity_app():
    """Unity용 완벽한 Cambodia Agri App 생성"""
    
    print("🚀 Unity용 완벽한 Cambodia Agri App 생성 시작...")
    
    # 5,000개 데이터 로드
    with open('/home/user/webapp/data/mass_agricultural_terms_5000.json', 'r', encoding='utf-8') as f:
        mass_data = json.load(f)
    
    print(f"📊 로드된 데이터: {len(mass_data['terms'])}개 용어, {len(mass_data['examples'])}개 예문")
    
    # 25번째 카테고리를 농업기관 웹사이트 전용으로 변경
    agriculture_portals = [
        {"id": 5001, "khmer": "ក្រសួងកសិកម្ម", "pronunciation_ko": "크러쇠엉 까시깜", "meaning_ko": "농림수산부 (MAFF)", "meaning_en": "Ministry of Agriculture, Forestry and Fisheries", "category": "agriculture_portal", "website": "https://www.maff.gov.kh/", "description": "캄보디아 농림수산부"},
        {"id": 5002, "khmer": "មជ្ឈមណ្ឌលស្រាវជ្រាវកសិកម្ម", "pronunciation_ko": "맛치마달 스라우치라우 까시깜", "meaning_ko": "농업연구개발원 (CARDI)", "meaning_en": "Cambodian Agricultural Research and Development Institute", "category": "agriculture_portal", "website": "https://cardi.org.kh/", "description": "캄보디아 농업연구개발원"},
        {"id": 5003, "khmer": "សាកលវិទ្យាល័យបន្ទាយមានជ័យ", "pronunciation_ko": "싸깔위뜨야라이 반티어이 미언체이", "meaning_ko": "반티어이미언체이대학교 (RUA)", "meaning_en": "Royal University of Agriculture", "category": "agriculture_portal", "website": "https://www.rua.edu.kh/", "description": "왕립농업대학교"},
        {"id": 5004, "khmer": "ធនាគារអភិវឌ្ឍន៍កសិកម្ម", "pronunciation_ko": "타니어가 아피보단 까시깜", "meaning_ko": "농업개발은행 (ARDB)", "meaning_en": "Agricultural and Rural Development Bank", "category": "agriculture_portal", "website": "https://www.ardb.com.kh/", "description": "농업 및 농촌개발은행"},
        {"id": 5005, "khmer": "អង្គការម្ហូបនិងកសិកម្ម", "pronunciation_ko": "응까까 마홉 니엉 까시깜", "meaning_ko": "유엔식량농업기구 (FAO)", "meaning_en": "Food and Agriculture Organization", "category": "agriculture_portal", "website": "https://www.fao.org/cambodia/", "description": "유엔식량농업기구 캄보디아 사무소"},
        {"id": 5006, "khmer": "កម្មវិធីអភិវឌ្ឍន៍", "pronunciation_ko": "깜마위티 아피보단", "meaning_ko": "유엔개발계획 (UNDP)", "meaning_en": "United Nations Development Programme", "category": "agriculture_portal", "website": "https://www.undp.org/cambodia", "description": "유엔개발계획 캄보디아"},
        {"id": 5007, "khmer": "ភ្នាក់ងារអភិវឌ្ឍន៍អាមេរិក", "pronunciation_ko": "프낙응가 아피보단 아메릭", "meaning_ko": "미국국제개발처 (USAID)", "meaning_en": "United States Agency for International Development", "category": "agriculture_portal", "website": "https://www.usaid.gov/cambodia", "description": "미국국제개발처 캄보디아"},
        {"id": 5008, "khmer": "មូលនិធិអភិវឌ្ឍន៍កសិកម្ម", "pronunciation_ko": "물니티 아피보단 까시깜", "meaning_ko": "국제농업개발기금 (IFAD)", "meaning_en": "International Fund for Agricultural Development", "category": "agriculture_portal", "website": "https://www.ifad.org/en/web/operations/w/country/cambodia", "description": "국제농업개발기금"},
        {"id": 5009, "khmer": "ធនាគារអភិវឌ្ឍន៍អាស៊ី", "pronunciation_ko": "타니어가 아피보단 아시", "meaning_ko": "아시아개발은행 (ADB)", "meaning_en": "Asian Development Bank", "category": "agriculture_portal", "website": "https://www.adb.org/countries/cambodia/main", "description": "아시아개발은행 캄보디아"},
        {"id": 5010, "khmer": "វិទ្យាស្ថានស្រូវអន្តរជាតិ", "pronunciation_ko": "위뜨야스탄 스라우 안따라체아티", "meaning_ko": "국제벼연구소 (IRRI)", "meaning_en": "International Rice Research Institute", "category": "agriculture_portal", "website": "https://www.irri.org/where-we-work/countries/cambodia", "description": "국제벼연구소 캄보디아 프로그램"},
        {"id": 5011, "khmer": "ផ្សារកសិកម្ម", "pronunciation_ko": "프사 까시깜", "meaning_ko": "캄보디아농촌연합 (CRF)", "meaning_en": "Cambodian Rural Federation", "category": "agriculture_portal", "website": "http://www.crf.org.kh/", "description": "캄보디아 농촌 연합회"},
        {"id": 5012, "khmer": "សម្ព័ន្ធកសិករ", "pronunciation_ko": "쌈폰 까시커", "meaning_ko": "캄보디아농민연합 (CFAP)", "meaning_en": "Cambodian Farmers Association of Agricultural Producers", "category": "agriculture_portal", "website": "https://cfap.org.kh/", "description": "캄보디아 농업생산자 농민연합"},
        {"id": 5013, "khmer": "អង្គការកសិករ", "pronunciation_ko": "응까까 까시커", "meaning_ko": "캄보디아인권농촌개발협회", "meaning_en": "Cambodian Human Rights and Development Association", "category": "agriculture_portal", "website": "https://www.camhrra.org/", "description": "캄보디아 인권 및 농촌개발협회"},
        {"id": 5014, "khmer": "ក្រុមហ៊ុនស្រូវ", "pronunciation_ko": "크룸훈 스라우", "meaning_ko": "암루쌀 (Amru Rice)", "meaning_en": "Amru Rice Cambodia", "category": "agriculture_portal", "website": "https://amrurice.com/", "description": "캄보디아 프리미엄 쌀 생산업체"},
        {"id": 5015, "khmer": "ធនាគារអាក្លេដា", "pronunciation_ko": "타니어가 아클레다", "meaning_ko": "아클레다은행", "meaning_en": "ACLEDA Bank", "category": "agriculture_portal", "website": "https://www.acledabank.com.kh/", "description": "농업금융 전문 은행"},
        {"id": 5016, "khmer": "ធនាគារវីង", "pronunciation_ko": "타니어가 위엉", "meaning_ko": "윙은행", "meaning_en": "Wing Bank", "category": "agriculture_portal", "website": "https://www.wing.com.kh/", "description": "농촌 모바일 금융 서비스"},
        {"id": 5017, "khmer": "សាកលវិទ្យាល័យមាន", "pronunciation_ko": "싸깔위뜌야라이 미언", "meaning_ko": "메안치 대학교 (MVU)", "meaning_en": "Mean Chey University", "category": "agriculture_portal", "website": "https://www.mcu.edu.kh/", "description": "농업 및 공학 전문 대학"},
        {"id": 5018, "khmer": "មជ្ឈមណ្ឌលព្រែកលាប", "pronunciation_ko": "맛치마달 프렉랍", "meaning_ko": "프렉 리프 국립농업대학", "meaning_en": "Prek Leap National College of Agriculture", "category": "agriculture_portal", "website": "https://www.plnca.edu.kh/", "description": "국립농업전문대학"},
        {"id": 5019, "khmer": "អង្គការហេតុ", "pronunciation_ko": "응까까 하엗", "meaning_ko": "하이퍼 인터내셔널", "meaning_en": "Heifer International Cambodia", "category": "agriculture_portal", "website": "https://www.heifer.org/our-work/where-we-work/cambodia", "description": "국제 축산 개발 NGO"},
        {"id": 5020, "khmer": "អង្គការកាសេន", "pronunciation_ko": "응까까 까센", "meaning_ko": "케어 인터내셔널", "meaning_en": "CARE International Cambodia", "category": "agriculture_portal", "website": "https://www.care.org.kh/", "description": "국제 농촌개발 지원 NGO"}
    ]
    
    # agriculture_portal 카테고리를 웹사이트 전용으로 교체
    print("🔄 25번째 카테고리(agriculture_portal)를 웹사이트 링크 전용으로 변경...")
    filtered_terms = [term for term in mass_data['terms'] if term['category'] != 'agriculture_portal']
    all_terms = filtered_terms + agriculture_portals
    
    # 예문에서도 agriculture_portal 관련 제거하고 새로운 것들 추가
    filtered_examples = {}
    for term_id, examples in mass_data['examples'].items():
        if int(term_id) < 25000 or int(term_id) > 25200:  # agriculture_portal ID 범위 제외
            filtered_examples[term_id] = examples
    
    # 새로운 농업기관들의 예문 추가
    for portal in agriculture_portals:
        filtered_examples[str(portal['id'])] = [{
            "example_kh": f"{portal['khmer']}ជាស្ថាប័នសំខាន់ក្នុងវិស័យកសិកម្ម។",
            "example_pron": f"{portal['pronunciation_ko']} 치어 스타반 썸칸 크농 위싸이 까시깜",
            "example_ko": f"{portal['meaning_ko']}는 농업분야의 중요한 기관입니다.",
            "example_en": f"{portal['meaning_en']} is an important agricultural institution."
        }]
    
    print(f"✅ 최종 용어 수: {len(all_terms)}개 (농업용어 4,800개 + 농업기관 20개)")
    
    # 완벽한 카테고리 구성 (24개 농업용어 카테고리 + 1개 웹사이트 카테고리)
    perfect_categories = {
        "all": {"name": "전체", "icon": "🌾", "description": "모든 농업용어"},
        # 24개 농업용어 카테고리 (각 200개)
        "crop_cultivation": {"name": "작물재배", "icon": "🌾", "description": "벼, 옥수수, 콩 등 주요 농작물 재배기술"},
        "livestock": {"name": "축산업", "icon": "🐄", "description": "소, 돼지, 닭 등 가축 사육 및 관리"},
        "agricultural_machinery": {"name": "농기계", "icon": "🚜", "description": "트랙터, 콤바인 등 농업기계 및 장비"},
        "soil_management": {"name": "토양관리", "icon": "🌱", "description": "토양개량, 토성분석, 토양보전 기술"},
        "fertilizer": {"name": "비료", "icon": "🧪", "description": "화학비료, 유기비료, 퇴비 등 영양관리"},
        "pest_control": {"name": "병해충방제", "icon": "🦟", "description": "농작물 병해충 진단 및 방제기술"},
        "harvest_processing": {"name": "수확후처리", "icon": "📦", "description": "수확, 건조, 선별, 포장 등 후처리"},
        "storage_technology": {"name": "저장기술", "icon": "🏪", "description": "곡물저장, 냉장보관, 품질유지 기술"},
        "food_processing": {"name": "가공기술", "icon": "🏭", "description": "농산물 가공, 식품제조, 부가가치 창출"},
        "marketing": {"name": "유통", "icon": "🚛", "description": "농산물 유통, 판매, 마케팅 전략"},
        "policy": {"name": "농업정책", "icon": "📋", "description": "농업정책, 농업법규, 정부지원 제도"},
        "farm_management": {"name": "농업경영", "icon": "📊", "description": "농가경영, 농업회계, 수익성 분석"},
        "horticulture": {"name": "원예", "icon": "🌷", "description": "채소, 화훼, 과수 재배 및 관리"},
        "forestry": {"name": "임업", "icon": "🌲", "description": "산림경영, 조림, 목재생산 기술"},
        "fisheries": {"name": "수산업", "icon": "🐟", "description": "어업, 양식업, 수산물 생산 기술"},
        "agricultural_technology": {"name": "농업기술", "icon": "💻", "description": "농업과학기술, 연구개발, 혁신기술"},
        "water_management": {"name": "수자원관리", "icon": "💧", "description": "관개시설, 물 관리, 수리시설"},
        "infrastructure": {"name": "농업시설", "icon": "🏗️", "description": "온실, 축사, 저장고 등 농업시설"},
        "seed_technology": {"name": "종자기술", "icon": "🌰", "description": "육종, 종자생산, 품종개발 기술"},
        "pesticides": {"name": "농약", "icon": "☠️", "description": "살충제, 살균제, 제초제 등 농약"},
        "organic_farming": {"name": "유기농업", "icon": "🌿", "description": "친환경농업, 유기재배, 지속가능농업"},
        "smart_farming": {"name": "스마트농업", "icon": "🤖", "description": "ICT농업, 정밀농업, 자동화 시스템"},
        "environment": {"name": "농업환경", "icon": "🌍", "description": "환경보전, 생태농업, 환경친화적 농법"},
        "climate_adaptation": {"name": "기후변화대응", "icon": "🌡️", "description": "기후변화 적응, 내재해성 품종, 기상정보"},
        # 25번째: 웹사이트 링크 전용 카테고리
        "agriculture_portal": {"name": "농업정보포털", "icon": "🌐", "description": "농업기관, 연구소, 정부기관 웹사이트 링크"}
    }
    
    # Unity용 완벽한 HTML 앱 생성
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cambodia Agri App - 5000개 캄보디아 농업용어</title>
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="data:application/manifest+json,{{
        &quot;name&quot;: &quot;Cambodia Agri App&quot;,
        &quot;short_name&quot;: &quot;AgriApp&quot;,
        &quot;start_url&quot;: &quot;.&quot;,
        &quot;display&quot;: &quot;standalone&quot;,
        &quot;background_color&quot;: &quot;#f1f8e9&quot;,
        &quot;theme_color&quot;: &quot;#4CAF50&quot;,
        &quot;icons&quot;: [
            {{ &quot;src&quot;: &quot;data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxOTIiIGhlaWdodD0iMTkyIiBmaWxsPSIjNENBRjUwIi8+Cjx0ZXh0IHg9Ijk2IiB5PSIxMTAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IndoaXRlIiBmb250LXNpemU9IjgwIiBmb250LWZhbWlseT0iQXJpYWwiPvCfjL48L3RleHQ+Cjwvc3ZnPgo=&quot;, &quot;sizes&quot;: &quot;192x192&quot;, &quot;type&quot;: &quot;image/svg+xml&quot; }}
        ]
    }}">

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Battambang:wght@400;700&display=swap');
        
        :root {{
            --primary-color: #4CAF50;
            --primary-dark: #2E7D32;
            --primary-light: #C8E6C9;
            --secondary-color: #f1f8e9;
            --font-color: #212121;
            --border-color: #e0e0e0;
            --white-bg: #ffffff;
            --light-gray: #f5f5f5;
            --accent-color: #FF6B35;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans KR', sans-serif;
            background-color: var(--light-gray);
            color: var(--font-color);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: var(--white-bg);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            padding-bottom: 30px;
            border-bottom: 3px solid var(--primary-color);
            margin-bottom: 30px;
            background: linear-gradient(135deg, var(--primary-light), var(--secondary-color));
            border-radius: 15px;
            padding: 30px;
        }}
        
        .header h1 {{
            color: var(--primary-dark);
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            color: #555;
            font-size: 1.2em;
            font-weight: 500;
        }}
        
        /* 통계 섹션 */
        .stats-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        /* 검색 섹션 */
        .search-section {{
            margin-bottom: 30px;
        }}
        
        .search-box {{
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid var(--border-color);
            border-radius: 10px;
            transition: all 0.3s ease;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.2);
        }}
        
        /* 카테고리 섹션 */
        .category-section {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--primary-dark);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
        }}
        
        .category-btn {{
            background: var(--white-bg);
            border: 2px solid var(--border-color);
            padding: 20px;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .category-btn:hover {{
            border-color: var(--primary-color);
            background: var(--secondary-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .category-btn.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }}
        
        .category-info {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .category-icon {{
            font-size: 1.8em;
        }}
        
        .category-text {{
            text-align: left;
        }}
        
        .category-name {{
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .category-desc {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .category-count {{
            background: rgba(0, 0, 0, 0.1);
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .category-btn.active .category-count {{
            background: rgba(255, 255, 255, 0.2);
        }}
        
        /* 결과 섹션 */
        .results-section {{
            margin-bottom: 30px;
        }}
        
        .results-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 15px;
            background: var(--secondary-color);
            border-radius: 10px;
        }}
        
        .results-count {{
            font-weight: 600;
            color: var(--primary-dark);
            font-size: 1.1em;
        }}
        
        .view-toggle {{
            display: flex;
            gap: 10px;
        }}
        
        .view-btn {{
            padding: 8px 15px;
            border: 2px solid var(--primary-color);
            background: transparent;
            color: var(--primary-color);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .view-btn.active {{
            background: var(--primary-color);
            color: white;
        }}
        
        /* 테이블 뷰 */
        .table-container {{
            overflow-x: auto;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .terms-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        
        .terms-table th {{
            background: var(--primary-color);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .terms-table td {{
            padding: 15px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
        }}
        
        .terms-table tbody tr:hover {{
            background: var(--secondary-color);
            cursor: pointer;
        }}
        
        .terms-table tbody tr.selected {{
            background: var(--primary-light);
        }}
        
        .khmer-cell {{
            font-family: 'Battambang', 'Noto Sans KR', sans-serif;
            font-size: 1.2em;
            font-weight: 500;
            color: var(--primary-dark);
        }}
        
        .meaning-cell {{
            font-weight: 500;
        }}
        
        .english-cell {{
            color: #2E7D32;
            font-style: italic;
        }}
        
        .website-link {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            color: var(--primary-color);
            text-decoration: none;
            padding: 8px 15px;
            border: 2px solid var(--primary-color);
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .website-link:hover {{
            background: var(--primary-color);
            color: white;
        }}
        
        /* 카드 뷰 */
        .cards-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .term-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .term-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .term-khmer {{
            font-family: 'Battambang', sans-serif;
            font-size: 1.8em;
            font-weight: 700;
            color: var(--primary-dark);
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .tts-btn {{
            background: var(--primary-color);
            border: none;
            color: white;
            padding: 8px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2em;
            transition: all 0.3s ease;
        }}
        
        .tts-btn:hover {{
            background: var(--primary-dark);
            transform: scale(1.1);
        }}
        
        .term-pronunciation {{
            color: #666;
            font-style: italic;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}
        
        .term-meanings {{
            margin-bottom: 15px;
        }}
        
        .term-meaning {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 1.1em;
        }}
        
        .term-meaning .flag {{
            font-size: 1.2em;
        }}
        
        .term-category {{
            display: inline-block;
            background: var(--primary-light);
            color: var(--primary-dark);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
            margin-bottom: 15px;
        }}
        
        .term-example {{
            background: var(--secondary-color);
            padding: 15px;
            border-radius: 10px;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        
        .example-khmer {{
            font-family: 'Battambang', sans-serif;
            font-weight: 500;
            color: var(--primary-dark);
            margin-bottom: 5px;
        }}
        
        .example-korean {{
            color: #333;
            margin-bottom: 5px;
        }}
        
        .example-english {{
            color: #2E7D32;
            font-style: italic;
        }}
        
        /* 포털 카드 특별 스타일 */
        .portal-card {{
            border: 3px solid var(--primary-color);
            background: linear-gradient(135deg, var(--secondary-color), white);
        }}
        
        .portal-website {{
            margin-top: 15px;
        }}
        
        /* 페이지네이션 */
        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-top: 30px;
        }}
        
        .pagination button {{
            padding: 10px 20px;
            border: 2px solid var(--primary-color);
            background: white;
            color: var(--primary-color);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .pagination button:hover:not(:disabled) {{
            background: var(--primary-color);
            color: white;
        }}
        
        .pagination button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .page-info {{
            font-weight: 600;
            color: var(--primary-dark);
            font-size: 1.1em;
        }}
        
        /* 로딩 인디케이터 */
        .loading {{
            text-align: center;
            padding: 50px;
            color: var(--primary-color);
            font-size: 1.2em;
        }}
        
        .loading-spinner {{
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 3px solid var(--primary-light);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 15px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* 반응형 디자인 */
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats-section {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .category-grid {{
                grid-template-columns: 1fr;
            }}
            
            .cards-container {{
                grid-template-columns: 1fr;
            }}
            
            .results-info {{
                flex-direction: column;
                gap: 15px;
                align-items: flex-start;
            }}
        }}
        
        /* 숨김 클래스 */
        .hidden {{
            display: none !important;
        }}
        
        /* 접근성 */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <header class="header">
            <h1>🇰🇭 Cambodia Agri App</h1>
            <p class="subtitle">캄보디아 농업용어 5,000개 완전학습 시스템 · 25개 전문분야 · 크메르어↔한국어+영어</p>
        </header>

        <!-- 통계 섹션 -->
        <section class="stats-section">
            <div class="stat-card">
                <div class="stat-number" id="totalTerms">{len(all_terms):,}</div>
                <div class="stat-label">총 농업용어</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">25</div>
                <div class="stat-label">전문 카테고리</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">지원 언어</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="exampleCount">{len(filtered_examples):,}</div>
                <div class="stat-label">예문 수</div>
            </div>
        </section>

        <!-- 검색 섹션 -->
        <section class="search-section">
            <h2 class="section-title">🔍 농업용어 검색</h2>
            <input type="text" id="searchInput" class="search-box" placeholder="크메르어, 한국어, 영어로 검색하세요... (예: 벼, rice, ស្រូវ)">
        </section>

        <!-- 카테고리 섹션 -->
        <section class="category-section">
            <h2 class="section-title">📂 전문 카테고리</h2>
            <div id="categoryGrid" class="category-grid">
                <!-- 카테고리 버튼들이 동적으로 생성됩니다 -->
            </div>
        </section>

        <!-- 결과 섹션 -->
        <section class="results-section">
            <div class="results-info">
                <div id="resultsCount" class="results-count">전체 용어를 표시하고 있습니다.</div>
                <div class="view-toggle">
                    <button id="tableViewBtn" class="view-btn active">📋 표 보기</button>
                    <button id="cardViewBtn" class="view-btn">📱 카드 보기</button>
                </div>
            </div>
            
            <!-- 테이블 뷰 -->
            <div id="tableView" class="table-container">
                <table class="terms-table">
                    <thead>
                        <tr id="tableHeader">
                            <th>크메르어</th>
                            <th>발음</th>
                            <th>한국어 의미</th>
                            <th>English Meaning</th>
                            <th>카테고리</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody">
                        <!-- 용어들이 동적으로 생성됩니다 -->
                    </tbody>
                </table>
            </div>
            
            <!-- 카드 뷰 -->
            <div id="cardView" class="cards-container hidden">
                <!-- 카드들이 동적으로 생성됩니다 -->
            </div>
            
            <!-- 페이지네이션 -->
            <div id="pagination" class="pagination">
                <!-- 페이지네이션이 동적으로 생성됩니다 -->
            </div>
        </section>
    </div>

    <!-- 데이터 임베딩 -->
    <script>
        // 카테고리 정의
        const categories = {json.dumps(perfect_categories, ensure_ascii=False, indent=12)};
        
        // 농업용어 데이터
        const allTerms = {json.dumps(all_terms, ensure_ascii=False, indent=12)};
        
        // 예문 데이터
        const examples = {json.dumps(filtered_examples, ensure_ascii=False, indent=12)};
    </script>
    
    <script>
        // 전역 상태
        let state = {{
            currentCategory: 'all',
            currentView: 'table',
            filteredTerms: [...allTerms],
            currentPage: 1,
            itemsPerPage: 20,
            searchQuery: ''
        }};
        
        // DOM 요소
        const elements = {{
            searchInput: document.getElementById('searchInput'),
            categoryGrid: document.getElementById('categoryGrid'),
            resultsCount: document.getElementById('resultsCount'),
            tableView: document.getElementById('tableView'),
            cardView: document.getElementById('cardView'),
            tableHeader: document.getElementById('tableHeader'),
            tableBody: document.getElementById('tableBody'),
            pagination: document.getElementById('pagination'),
            tableViewBtn: document.getElementById('tableViewBtn'),
            cardViewBtn: document.getElementById('cardViewBtn')
        }};
        
        // TTS 기능
        function speak(text) {{
            if (!('speechSynthesis' in window)) {{
                console.log('TTS not supported');
                return;
            }}
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'km-KH';
            utterance.rate = 0.8;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        
        // 검색 디바운싱
        let searchTimeout;
        function debouncedSearch(callback, delay = 300) {{
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(callback, delay);
        }}
        
        // 카테고리 버튼 렌더링
        function renderCategories() {{
            elements.categoryGrid.innerHTML = '';
            
            for (const [key, category] of Object.entries(categories)) {{
                if (key === 'all') continue;
                
                const count = allTerms.filter(term => term.category === key).length;
                
                const btn = document.createElement('button');
                btn.className = `category-btn ${{key === state.currentCategory ? 'active' : ''}}`;
                btn.onclick = () => handleCategoryClick(key);
                
                btn.innerHTML = `
                    <div class="category-info">
                        <div class="category-icon">${{category.icon}}</div>
                        <div class="category-text">
                            <div class="category-name">${{category.name}}</div>
                            <div class="category-desc">${{category.description}}</div>
                        </div>
                    </div>
                    <div class="category-count">${{count.toLocaleString()}}</div>
                `;
                
                elements.categoryGrid.appendChild(btn);
            }}
            
            // 전체 버튼 추가
            const allBtn = document.createElement('button');
            allBtn.className = `category-btn ${{state.currentCategory === 'all' ? 'active' : ''}}`;
            allBtn.onclick = () => handleCategoryClick('all');
            allBtn.innerHTML = `
                <div class="category-info">
                    <div class="category-icon">${{categories.all.icon}}</div>
                    <div class="category-text">
                        <div class="category-name">${{categories.all.name}}</div>
                        <div class="category-desc">${{categories.all.description}}</div>
                    </div>
                </div>
                <div class="category-count">${{allTerms.length.toLocaleString()}}</div>
            `;
            elements.categoryGrid.insertBefore(allBtn, elements.categoryGrid.firstChild);
        }}
        
        // 카테고리 클릭 핸들러
        function handleCategoryClick(categoryKey) {{
            state.currentCategory = categoryKey;
            state.currentPage = 1;
            filterAndRender();
        }}
        
        // 검색 및 필터링
        function filterTerms() {{
            let filtered = allTerms;
            
            // 카테고리 필터
            if (state.currentCategory !== 'all') {{
                filtered = filtered.filter(term => term.category === state.currentCategory);
            }}
            
            // 검색 필터
            if (state.searchQuery.trim()) {{
                const query = state.searchQuery.toLowerCase().trim();
                filtered = filtered.filter(term => 
                    term.khmer.toLowerCase().includes(query) ||
                    term.meaning_ko.toLowerCase().includes(query) ||
                    (term.meaning_en && term.meaning_en.toLowerCase().includes(query)) ||
                    term.pronunciation_ko.toLowerCase().includes(query)
                );
            }}
            
            state.filteredTerms = filtered;
        }}
        
        // 테이블 렌더링
        function renderTable() {{
            const startIndex = (state.currentPage - 1) * state.itemsPerPage;
            const endIndex = startIndex + state.itemsPerPage;
            const pageTerms = state.filteredTerms.slice(startIndex, endIndex);
            
            // 테이블 헤더 업데이트
            if (state.currentCategory === 'agriculture_portal') {{
                elements.tableHeader.innerHTML = `
                    <tr>
                        <th>크메르어</th>
                        <th>발음</th>
                        <th>기관명</th>
                        <th>English Name</th>
                        <th>웹사이트</th>
                    </tr>
                `;
            }} else {{
                elements.tableHeader.innerHTML = `
                    <tr>
                        <th>크메르어</th>
                        <th>발음</th>
                        <th>한국어 의미</th>
                        <th>English Meaning</th>
                        <th>카테고리</th>
                    </tr>
                `;
            }}
            
            // 테이블 바디 렌더링
            elements.tableBody.innerHTML = '';
            
            pageTerms.forEach(term => {{
                const row = document.createElement('tr');
                row.onclick = () => handleTermClick(term);
                
                if (term.category === 'agriculture_portal' && term.website) {{
                    row.innerHTML = `
                        <td class="khmer-cell">${{term.khmer}}</td>
                        <td>${{term.pronunciation_ko}}</td>
                        <td class="meaning-cell">
                            <strong>${{term.meaning_ko}}</strong>
                            ${{term.description ? `<br><small>${{term.description}}</small>` : ''}}
                        </td>
                        <td class="english-cell">${{term.meaning_en || ''}}</td>
                        <td>
                            <a href="${{term.website}}" target="_blank" class="website-link" onclick="event.stopPropagation();">
                                🌐 방문하기
                            </a>
                        </td>
                    `;
                }} else {{
                    row.innerHTML = `
                        <td class="khmer-cell">${{term.khmer}}</td>
                        <td>${{term.pronunciation_ko}}</td>
                        <td class="meaning-cell">${{term.meaning_ko}}</td>
                        <td class="english-cell">${{term.meaning_en || ''}}</td>
                        <td>${{categories[term.category]?.name || term.category}}</td>
                    `;
                }}
                
                elements.tableBody.appendChild(row);
            }});
        }}
        
        // 카드 렌더링
        function renderCards() {{
            const startIndex = (state.currentPage - 1) * state.itemsPerPage;
            const endIndex = startIndex + state.itemsPerPage;
            const pageTerms = state.filteredTerms.slice(startIndex, endIndex);
            
            elements.cardView.innerHTML = '';
            
            pageTerms.forEach(term => {{
                const card = document.createElement('div');
                card.className = `term-card ${{term.category === 'agriculture_portal' ? 'portal-card' : ''}}`;
                card.onclick = () => handleTermClick(term);
                
                if (term.category === 'agriculture_portal' && term.website) {{
                    card.innerHTML = `
                        <div class="term-khmer">
                            ${{term.khmer}}
                            <button class="tts-btn" onclick="event.stopPropagation(); speak('${{term.khmer}}');">🔊</button>
                        </div>
                        <div class="term-pronunciation">[${{term.pronunciation_ko}}]</div>
                        <div class="term-meanings">
                            <div class="term-meaning">
                                <span class="flag">🇰🇷</span>
                                <strong>${{term.meaning_ko}}</strong>
                            </div>
                            <div class="term-meaning">
                                <span class="flag">🇺🇸</span>
                                <em>${{term.meaning_en || ''}}</em>
                            </div>
                        </div>
                        <div class="term-category">${{categories[term.category]?.name || term.category}}</div>
                        ${{term.description ? `<div class="term-example"><strong>설명:</strong> ${{term.description}}</div>` : ''}}
                        <div class="portal-website">
                            <a href="${{term.website}}" target="_blank" class="website-link" onclick="event.stopPropagation();">
                                🌐 웹사이트 방문하기
                            </a>
                        </div>
                    `;
                }} else {{
                    const example = examples[term.id] ? examples[term.id][0] : null;
                    card.innerHTML = `
                        <div class="term-khmer">
                            ${{term.khmer}}
                            <button class="tts-btn" onclick="event.stopPropagation(); speak('${{term.khmer}}');">🔊</button>
                        </div>
                        <div class="term-pronunciation">[${{term.pronunciation_ko}}]</div>
                        <div class="term-meanings">
                            <div class="term-meaning">
                                <span class="flag">🇰🇷</span>
                                <strong>${{term.meaning_ko}}</strong>
                            </div>
                            <div class="term-meaning">
                                <span class="flag">🇺🇸</span>
                                <em>${{term.meaning_en || ''}}</em>
                            </div>
                        </div>
                        <div class="term-category">${{categories[term.category]?.name || term.category}}</div>
                        ${{example ? `
                            <div class="term-example">
                                <div class="example-khmer">${{example.example_kh}}</div>
                                <div class="example-korean">🇰🇷 ${{example.example_ko}}</div>
                                <div class="example-english">🇺🇸 ${{example.example_en}}</div>
                            </div>
                        ` : ''}}
                    `;
                }}
                
                elements.cardView.appendChild(card);
            }});
        }}
        
        // 페이지네이션 렌더링
        function renderPagination() {{
            const totalPages = Math.ceil(state.filteredTerms.length / state.itemsPerPage);
            
            if (totalPages <= 1) {{
                elements.pagination.innerHTML = '';
                return;
            }}
            
            elements.pagination.innerHTML = `
                <button onclick="changePage(${{state.currentPage - 1}})" ${{state.currentPage === 1 ? 'disabled' : ''}}>
                    ← 이전
                </button>
                <div class="page-info">
                    ${{state.currentPage}} / ${{totalPages}} 페이지
                </div>
                <button onclick="changePage(${{state.currentPage + 1}})" ${{state.currentPage === totalPages ? 'disabled' : ''}}>
                    다음 →
                </button>
            `;
        }}
        
        // 페이지 변경
        function changePage(newPage) {{
            const totalPages = Math.ceil(state.filteredTerms.length / state.itemsPerPage);
            if (newPage < 1 || newPage > totalPages) return;
            
            state.currentPage = newPage;
            renderCurrentView();
            renderPagination();
        }}
        
        // 현재 뷰 렌더링
        function renderCurrentView() {{
            if (state.currentView === 'table') {{
                renderTable();
            }} else {{
                renderCards();
            }}
        }}
        
        // 결과 카운트 업데이트
        function updateResultsCount() {{
            const total = state.filteredTerms.length;
            const categoryName = categories[state.currentCategory]?.name || '전체';
            const searchText = state.searchQuery ? ` (검색: "${{state.searchQuery}}")` : '';
            elements.resultsCount.textContent = `${{categoryName}} 카테고리: ${{total.toLocaleString()}}개 용어${{searchText}}`;
        }}
        
        // 뷰 토글
        function toggleView(viewType) {{
            state.currentView = viewType;
            
            if (viewType === 'table') {{
                elements.tableView.classList.remove('hidden');
                elements.cardView.classList.add('hidden');
                elements.tableViewBtn.classList.add('active');
                elements.cardViewBtn.classList.remove('active');
            }} else {{
                elements.tableView.classList.add('hidden');
                elements.cardView.classList.remove('hidden');
                elements.tableViewBtn.classList.remove('active');
                elements.cardViewBtn.classList.add('active');
            }}
            
            renderCurrentView();
        }}
        
        // 용어 클릭 핸들러 (상세보기용)
        function handleTermClick(term) {{
            console.log('Term selected:', term);
            // 여기에 상세보기 로직 추가 가능
        }}
        
        // 필터링 및 렌더링
        function filterAndRender() {{
            filterTerms();
            renderCategories();
            updateResultsCount();
            renderCurrentView();
            renderPagination();
        }}
        
        // 초기화
        function init() {{
            console.log('🚀 Cambodia Agri App 초기화 중...');
            console.log(`📊 로드된 데이터: ${{allTerms.length}}개 용어, ${{Object.keys(examples).length}}개 예문`);
            
            // 검색 이벤트 리스너
            elements.searchInput.addEventListener('input', (e) => {{
                state.searchQuery = e.target.value;
                state.currentPage = 1;
                debouncedSearch(filterAndRender, 200);
            }});
            
            // 뷰 토글 이벤트 리스너
            elements.tableViewBtn.addEventListener('click', () => toggleView('table'));
            elements.cardViewBtn.addEventListener('click', () => toggleView('card'));
            
            // 초기 렌더링
            filterAndRender();
            
            console.log('✅ Cambodia Agri App 초기화 완료!');
        }}
        
        // Service Worker 등록
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('data:application/javascript,' + encodeURIComponent(
                    'const CACHE_NAME="cambodia-agri-app-v1";self.addEventListener("install",e=>{{e.waitUntil(caches.open(CACHE_NAME).then(c=>c.addAll(["'+location.href+'"])).then(()=>self.skipWaiting()))}});self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(c=>Promise.all(c.map(cName=>{{if("cambodia-agri-app-v1"!==cName)return caches.delete(cName)}}))).then(()=>self.clients.claim()))}});self.addEventListener("fetch",e=>{{e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))}});'
                )).then(reg => console.log('🔧 Service Worker 등록 완료'))
                  .catch(err => console.log('❌ Service Worker 등록 실패:', err));
            }});
        }}
        
        // 앱 초기화
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>"""
    
    # Windows 경로용 파일명 생성
    output_filename = "Cambodia_Agri_App_5000.html"
    output_path = f"/home/user/webapp/{output_filename}"
    
    # UTF-8 BOM 없이 저장 (인코딩 문제 해결)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Unity용 완벽한 Cambodia Agri App 생성 완료!")
    print(f"📂 파일 경로: {output_path}")
    print(f"📏 파일 크기: {os.path.getsize(output_path) / (1024*1024):.1f}MB")
    print(f"📊 최종 통계:")
    print(f"   - 총 용어: {len(all_terms):,}개")
    print(f"   - 농업용어: {len(filtered_terms):,}개")
    print(f"   - 농업기관: {len(agriculture_portals)}개")
    print(f"   - 예문: {len(filtered_examples):,}개")
    print(f"   - 카테고리: 25개")
    
    return output_path

if __name__ == "__main__":
    create_perfect_unity_app()
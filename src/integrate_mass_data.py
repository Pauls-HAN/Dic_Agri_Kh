#!/usr/bin/env python3
"""
V3 HTML에 5,000개 농업용어 데이터 통합 스크립트
Integrate 5,000 agricultural terms into V3 HTML
"""

import json
import re
from datetime import datetime

def load_mass_data():
    """5,000개 대량 데이터 로드"""
    with open('/home/user/webapp/data/mass_agricultural_terms_5000.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_v3_html():
    """현재 V3 HTML 파일 로드"""
    with open('/home/user/webapp/templates/agricultural_learning_v3.html', 'r', encoding='utf-8') as f:
        return f.read()

def update_categories_in_html(html_content, mass_data):
    """HTML에서 카테고리 정보 업데이트"""
    
    # 새로운 카테고리 구조 생성
    new_categories = {
        "all": {"name": "전체", "icon": "🌾"},
        "crop_cultivation": {"name": "작물재배", "icon": "🌾"},
        "livestock": {"name": "축산업", "icon": "🐄"},
        "agricultural_machinery": {"name": "농기계", "icon": "🚜"},
        "soil_management": {"name": "토양관리", "icon": "🌱"},
        "fertilizer": {"name": "비료", "icon": "🧪"},
        "pest_control": {"name": "병해충방제", "icon": "🦟"},
        "harvest_processing": {"name": "수확후처리", "icon": "📦"},
        "storage_technology": {"name": "저장기술", "icon": "🏪"},
        "food_processing": {"name": "가공기술", "icon": "🏭"},
        "marketing": {"name": "유통", "icon": "🚛"},
        "policy": {"name": "농업정책", "icon": "📋"},
        "farm_management": {"name": "농업경영", "icon": "📊"},
        "horticulture": {"name": "원예", "icon": "🌷"},
        "forestry": {"name": "임업", "icon": "🌲"},
        "fisheries": {"name": "수산업", "icon": "🐟"},
        "agricultural_technology": {"name": "농업기술", "icon": "💻"},
        "water_management": {"name": "수자원관리", "icon": "💧"},
        "infrastructure": {"name": "농업시설", "icon": "🏗️"},
        "seed_technology": {"name": "종자기술", "icon": "🌰"},
        "pesticides": {"name": "농약", "icon": "☠️"},
        "organic_farming": {"name": "유기농업", "icon": "🌿"},
        "smart_farming": {"name": "스마트농업", "icon": "🤖"},
        "environment": {"name": "농업환경", "icon": "🌍"},
        "climate_adaptation": {"name": "기후변화대응", "icon": "🌡️"},
        "agriculture_portal": {"name": "농업정보포털", "icon": "🌐"}
    }
    
    # 카테고리 정의 부분 찾아서 교체
    categories_pattern = r'const categories = \{[^}]*\};'
    categories_js = f"const categories = {json.dumps(new_categories, ensure_ascii=False, indent=12)};"
    
    html_content = re.sub(categories_pattern, categories_js, html_content, flags=re.DOTALL)
    
    return html_content

def update_terms_in_html(html_content, mass_data):
    """HTML에서 농업용어 데이터 업데이트"""
    
    # 기존 50개 용어를 5,000개로 교체
    terms_pattern = r'const allTerms = \[.*?\];'
    
    # 농업정보포털 용어들은 기존 것 유지하고 새 용어들 추가
    existing_portal_terms = []
    
    # 기존 HTML에서 agriculture_portal 용어들 추출
    existing_terms_match = re.search(r'const allTerms = \[(.*?)\];', html_content, re.DOTALL)
    if existing_terms_match:
        existing_terms_content = existing_terms_match.group(1)
        # agriculture_portal 카테고리 용어들만 추출
        portal_matches = re.findall(r'\{[^}]*"category": "agriculture_portal"[^}]*\}', existing_terms_content)
        for match in portal_matches:
            # JSON 파싱을 위해 정리
            clean_match = match.replace('\n', '').replace('    ', '')
            try:
                term_obj = eval(clean_match)  # 간단한 파싱
                existing_portal_terms.append(term_obj)
            except:
                pass  # 파싱 실패시 무시
    
    # 새 용어들에 기존 agriculture_portal 용어들 추가
    all_new_terms = mass_data['terms'].copy()
    
    # 기존 agriculture_portal 용어들을 새 ID로 추가 (충돌 방지)
    for i, portal_term in enumerate(existing_portal_terms):
        new_portal_term = portal_term.copy()
        new_portal_term['id'] = 26000 + i  # agriculture_portal ID 범위 끝에 추가
        all_new_terms.append(new_portal_term)
    
    # JavaScript 배열 형태로 변환
    terms_js_lines = []
    for i, term in enumerate(all_new_terms):
        if i == 0:
            terms_js_lines.append("        const allTerms = [")
        
        term_line = f'            {json.dumps(term, ensure_ascii=False)}'
        if i < len(all_new_terms) - 1:
            term_line += ","
        
        terms_js_lines.append(term_line)
    
    terms_js_lines.append("        ];")
    terms_js = "\n".join(terms_js_lines)
    
    # 기존 allTerms 정의 교체
    html_content = re.sub(terms_pattern, terms_js, html_content, flags=re.DOTALL)
    
    return html_content

def update_examples_in_html(html_content, mass_data):
    """HTML에서 예문 데이터 업데이트"""
    
    # 새로운 examples 객체 생성
    examples_data = mass_data['examples']
    
    # JavaScript 객체 형태로 변환
    examples_js_lines = ["        const examples = {"]
    
    for term_id, examples_list in examples_data.items():
        example = examples_list[0]  # 첫 번째 예문 사용
        example_line = f'            {term_id}: [ {json.dumps(example, ensure_ascii=False)} ]'
        
        # 마지막 항목이 아니면 쉼표 추가
        if term_id != list(examples_data.keys())[-1]:
            example_line += ","
        
        examples_js_lines.append(example_line)
    
    examples_js_lines.append("        };")
    examples_js = "\n".join(examples_js_lines)
    
    # 기존 examples 정의 교체
    examples_pattern = r'const examples = \{.*?\};'
    html_content = re.sub(examples_pattern, examples_js, html_content, flags=re.DOTALL)
    
    return html_content

def update_metadata_in_html(html_content):
    """HTML 메타데이터 업데이트 (타이틀, 설명 등)"""
    
    # 타이틀 업데이트
    html_content = html_content.replace(
        'title>캄보디아 농업용어 학습 V3 (모바일 최적화)</title',
        'title>캄보디아 농업용어 5,000개 학습 V3 (모바일 최적화)</title'
    )
    
    # 헤더 타이틀 업데이트  
    html_content = html_content.replace(
        '<h1>캄보디아 농업용어 학습 V3</h1>',
        '<h1>캄보디아 농업용어 5,000개 학습</h1>'
    )
    
    # 서브타이틀 업데이트
    html_content = html_content.replace(
        '<p class="subtitle">크메르어 ↔ 한국어 + 영어 학습 (모바일 최적화)</p>',
        '<p class="subtitle">5,000개 농업용어 · 크메르어 ↔ 한국어 + 영어 · 25개 카테고리</p>'
    )
    
    # PWA 매니페스트 업데이트
    html_content = html_content.replace(
        '"name": "캄보디아 농업용어 학습 V3"',
        '"name": "캄보디아 농업용어 5,000개 학습 V3"'
    )
    
    html_content = html_content.replace(
        '"short_name": "농업용어 V3"',
        '"short_name": "농업용어 5K"'
    )
    
    # 진행률 목표 수치 업데이트 (1,400+ -> 5,000+)
    html_content = html_content.replace(
        '((allTerms.length / 1400) * 100)',
        '((allTerms.length / 5000) * 100)'
    )
    
    html_content = html_content.replace(
        '1,400+ 단어',
        '5,000 단어'
    )
    
    return html_content

def integrate_mass_data():
    """5,000개 데이터를 V3 HTML에 통합"""
    
    print("🔄 5,000개 농업용어 데이터를 V3 HTML에 통합 중...")
    
    # 데이터 로드
    mass_data = load_mass_data()
    html_content = load_v3_html()
    
    print(f"📊 로드된 데이터: {len(mass_data['terms'])}개 용어, {len(mass_data['examples'])}개 예문")
    
    # 단계별 통합
    print("1️⃣ 카테고리 정보 업데이트...")
    html_content = update_categories_in_html(html_content, mass_data)
    
    print("2️⃣ 농업용어 데이터 업데이트...")
    html_content = update_terms_in_html(html_content, mass_data)
    
    print("3️⃣ 예문 데이터 업데이트...")
    html_content = update_examples_in_html(html_content, mass_data)
    
    print("4️⃣ 메타데이터 업데이트...")
    html_content = update_metadata_in_html(html_content)
    
    # 새로운 V3 파일로 저장
    output_path = '/home/user/webapp/templates/agricultural_learning_v3_5000.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 5,000개 농업용어 V3 HTML 통합 완료!")
    print(f"📂 저장 위치: {output_path}")
    
    # 파일 크기 확인
    import os
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"📏 파일 크기: {file_size_mb:.1f}MB")
    
    return output_path

if __name__ == "__main__":
    integrate_mass_data()
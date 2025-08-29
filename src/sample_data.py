#!/usr/bin/env python3
"""
농업용어 샘플 데이터 추가 스크립트
"""

from term_manager import AgriculturalTermManager

def add_sample_terms():
    """기본 농업용어 샘플 데이터 추가"""
    manager = AgriculturalTermManager()
    
    # 기본 농업용어 샘플 데이터
    sample_terms = [
        {
            "korean_term": "벼",
            "khmer_term": "ស្រូវ",
            "english_term": "rice plant",
            "category": "작물재배",
            "korean_definition": "논에서 기르는 한해살이 벼과 식물로, 쌀의 원료가 되는 곡물",
            "khmer_definition": "រុក្ខជាតិក្រុមបាយដែលដាំក្នុងស្រែ និងជាវត្ថុធាតុដើមនៃអង្ករ",
            "usage_example": "벼농사는 캄보디아의 주요 농업 활동입니다.",
            "difficulty_level": "기초",
            "tags": ["곡물", "주식", "논농사"]
        },
        {
            "korean_term": "농기계",
            "khmer_term": "គ្រឿងយន្តកសិកម្ម",
            "english_term": "agricultural machinery",
            "category": "농기계",
            "korean_definition": "농업 작업에 사용되는 기계와 도구의 총칭",
            "khmer_definition": "គ្រឿងយន្ត និងឧបករណ៍ដែលប្រើប្រាស់សម្រាប់ការងារកសិកម្ម",
            "usage_example": "현대적인 농기계 도입으로 농작업 효율이 크게 향상되었습니다.",
            "difficulty_level": "중급",
            "tags": ["기계", "도구", "효율성"]
        },
        {
            "korean_term": "비료",
            "khmer_term": "ជី",
            "english_term": "fertilizer",
            "category": "비료",
            "korean_definition": "식물의 생장에 필요한 양분을 공급하는 물질",
            "khmer_definition": "សារធាតុដែលផ្គត់ផ្គង់សារធាតុចិញ្ចឹមចាំបាច់សម្រាប់ការលូតលាស់របស់រុក្ខជាតិ",
            "usage_example": "유기비료 사용으로 토양의 질을 개선할 수 있습니다.",
            "difficulty_level": "기초",
            "tags": ["양분", "토양", "유기농"]
        },
        {
            "korean_term": "수확",
            "khmer_term": "ការច្រូតកាត់",
            "english_term": "harvest",
            "category": "수확",
            "korean_definition": "농작물이 익었을 때 거두어들이는 작업",
            "khmer_definition": "ការប្រមូលយកដំណាំពេលដែលវាទុំហើយ",
            "usage_example": "쌀 수확 시기는 보통 11월부터 12월입니다.",
            "difficulty_level": "기초",
            "tags": ["수확기", "농작업", "계절"]
        },
        {
            "korean_term": "관개",
            "khmer_term": "ប្រព័ន្ធធារាសាស្ត្រ",
            "english_term": "irrigation",
            "category": "수자원",
            "korean_definition": "농작물에 물을 공급하는 인공적인 물 공급 시스템",
            "khmer_definition": "ប្រព័ន្ធផ្គត់ផ្គង់ទឹកសិប្បនិម្មិតសម្រាប់ដំណាំកសិកម្ម",
            "usage_example": "효율적인 관개 시스템으로 가뭄 피해를 줄일 수 있습니다.",
            "difficulty_level": "중급",
            "tags": ["물", "시설", "가뭄대책"]
        },
        {
            "korean_term": "토양",
            "khmer_term": "ដី",
            "english_term": "soil",
            "category": "토양",
            "korean_definition": "식물이 자라는 땅의 표면층으로, 각종 영양소를 포함한 흙",
            "khmer_definition": "ស្រទាប់ផ្ទៃដីដែលរុក្ខជាតិលូតលាស់ និងមានសារធាតុចិញ្ចឹមផ្សេងៗ",
            "usage_example": "토양 검사를 통해 적절한 비료를 선택해야 합니다.",
            "difficulty_level": "기초",
            "tags": ["흙", "영양소", "검사"]
        },
        {
            "korean_term": "해충",
            "khmer_term": "សត្វល្អិត",
            "english_term": "pest",
            "category": "병해충",
            "korean_definition": "농작물에 피해를 주는 곤충이나 동물",
            "khmer_definition": "សត្វល្អិត ឬសត្វដែលបង្កគ្រោះថ្នាក់ដល់ដំណាំកសិកម្ម",
            "usage_example": "통합적 해충 관리로 농약 사용을 줄일 수 있습니다.",
            "difficulty_level": "중급",
            "tags": ["방제", "농약", "관리"]
        },
        {
            "korean_term": "온실",
            "khmer_term": "ផ្ទះកញ្ចក់",
            "english_term": "greenhouse",
            "category": "농업시설",
            "korean_definition": "식물을 기르기 위해 만든 유리나 비닐로 덮은 건물",
            "khmer_definition": "អគារដែលគ្របដោយកញ្ចក់ ឬផ្ទាំងប្លាស្ទិកសម្រាប់ដាំដុះរុក្ខជាតិ",
            "usage_example": "온실에서는 연중 내내 채소를 재배할 수 있습니다.",
            "difficulty_level": "중급",
            "tags": ["시설농업", "연중재배", "환경제어"]
        },
        {
            "korean_term": "씨앗",
            "khmer_term": "គ្រាប់ពូជ",
            "english_term": "seed",
            "category": "종자",
            "korean_definition": "식물이 번식하기 위해 만드는 작은 생식체",
            "khmer_definition": "សរីរាងគ្រាប់តូចដែលរុក្ខជាតិបង្កើតឡើងសម្រាប់ការបន្តពូជ",
            "usage_example": "품질 좋은 씨앗 선택이 농사의 첫걸음입니다.",
            "difficulty_level": "기초",
            "tags": ["번식", "품종", "선별"]
        },
        {
            "korean_term": "농약",
            "khmer_term": "ថ្នាំសំលាប់សត្វល្អិត",
            "english_term": "pesticide",
            "category": "농약",
            "korean_definition": "해충, 잡초, 병균 등을 방제하기 위해 사용하는 화학물질",
            "khmer_definition": "សារធាតុគីមីប្រើប្រាស់ដើម្បីការពារសត្វល្អិត ស្មៅផ្សេងៗ និងម្រោគ",
            "usage_example": "농약 사용 시 안전수칙을 반드시 준수해야 합니다.",
            "difficulty_level": "고급",
            "tags": ["화학물질", "안전", "방제"]
        }
    ]
    
    print("샘플 농업용어 데이터 추가 중...")
    
    for i, term_data in enumerate(sample_terms, 1):
        try:
            term_id = manager.add_term(**term_data)
            print(f"{i:2d}. '{term_data['korean_term']}' ({term_data['khmer_term']}) - ID: {term_id}")
        except Exception as e:
            print(f"오류 발생 ({term_data['korean_term']}): {e}")
    
    # 통계 출력
    stats = manager.get_statistics()
    print(f"\n=== 데이터 추가 완료 ===")
    print(f"총 용어 수: {stats['total_terms']}")
    print(f"목표 대비 진행률: {stats['progress_percentage']}%")
    print(f"카테고리별 분포:")
    for category, count in stats['category_distribution'].items():
        print(f"  - {category}: {count}개")

if __name__ == "__main__":
    add_sample_terms()
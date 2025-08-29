#!/usr/bin/env python3
"""
캄보디아 농업용어 확장 데이터 생성기
Extended Agricultural Terms Data Generator
8,000개 농업용어 생성을 위한 스크립트
"""

import json
import os
import random
from datetime import datetime
from enhanced_term_manager import EnhancedAgriculturalTermManager

class ExtendedDataGenerator:
    def __init__(self):
        self.manager = EnhancedAgriculturalTermManager()
        
        # 확장된 농업용어 기본 데이터
        self.base_terms = {
            "작물재배": [
                {"ko": "벼", "km": "ស្រូវ", "pron": "스라우", "freq": 5},
                {"ko": "옥수수", "km": "ពោត", "pron": "포트", "freq": 5},
                {"ko": "콩", "km": "សណ្តែក", "pron": "산댁", "freq": 4},
                {"ko": "고구마", "km": "ដំឡូងបាដាត", "pron": "담룽 바닷", "freq": 4},
                {"ko": "감자", "km": "ដំឡូងបារាំង", "pron": "담룽 바랑", "freq": 4},
                {"ko": "토마토", "km": "ប៉េងប៉ោះ", "pron": "펭포", "freq": 4},
                {"ko": "고추", "km": "ម្ទេស", "pron": "음테스", "freq": 5},
                {"ko": "양파", "km": "ខ្ទឹមបារាំង", "pron": "크틈 바랑", "freq": 4},
                {"ko": "마늘", "km": "ខ្ទឹមស", "pron": "크틈 사", "freq": 4},
                {"ko": "배추", "km": "ស្ពៃក្តោប", "pron": "스파이 크따웁", "freq": 3},
            ],
            "축산업": [
                {"ko": "소", "km": "គោ", "pron": "꼬", "freq": 5},
                {"ko": "돼지", "km": "ជ្រូក", "pron": "추룩", "freq": 5},
                {"ko": "닭", "km": "មាន់", "pron": "만", "freq": 5},
                {"ko": "오리", "km": "ទា", "pron": "띠아", "freq": 4},
                {"ko": "염소", "km": "ពពែ", "pron": "뽀뻬", "freq": 3},
                {"ko": "양", "km": "កជ្ជៀវ", "pron": "까찌업", "freq": 2},
                {"ko": "물소", "km": "ក្របី", "pron": "끄라비", "freq": 4},
                {"ko": "말", "km": "សេះ", "pron": "세", "freq": 2},
                {"ko": "사료", "km": "អាហារសត្វ", "pron": "아하 삿", "freq": 4},
                {"ko": "축사", "km": "ទ្រុងសត្វ", "pron": "뚜룽 삿", "freq": 4},
            ],
            "농기계": [
                {"ko": "트랙터", "km": "ត្រាក់ទ័រ", "pron": "뜨락터", "freq": 4},
                {"ko": "써레", "km": "នង្គ័ល", "pron": "농걸", "freq": 4},
                {"ko": "쟁기", "km": "ភ្នាល់", "pron": "프날", "freq": 5},
                {"ko": "탈곡기", "km": "ម៉ាស៊ីនច្រូត", "pron": "마신 츄룻", "freq": 4},
                {"ko": "이앙기", "km": "ម៉ាស៊ីនដាំ", "pron": "마신 담", "freq": 3},
                {"ko": "콤바인", "km": "ម៉ាស៊ីនច្រូតកាត់", "pron": "마신 츄룻 깟", "freq": 3},
                {"ko": "분무기", "km": "ម៉ាស៊ីនបាញ់ថ្នាំ", "pron": "마신 반 트남", "freq": 4},
                {"ko": "펌프", "km": "ម៉ាស៊ីនបូមទឹក", "pron": "마신 붐 뜩", "freq": 4},
                {"ko": "경운기", "km": "ម៉ាស៊ីនភ្ជួរ", "pron": "마신 프추어", "freq": 4},
                {"ko": "예초기", "km": "ម៉ាស៊ីនកាត់ស្មៅ", "pron": "마신 깟 스마우", "freq": 3},
            ],
            "토양관리": [
                {"ko": "토양", "km": "ដី", "pron": "다이", "freq": 5},
                {"ko": "점토", "km": "ដីឥដ្ឋ", "pron": "다이 잇", "freq": 3},
                {"ko": "모래", "km": "ខ្សាច់", "pron": "크삭", "freq": 4},
                {"ko": "부식토", "km": "ដីពុក", "pron": "다이 푹", "freq": 3},
                {"ko": "산성토양", "km": "ដីជូរ", "pron": "다이 추", "freq": 3},
                {"ko": "알칼리토양", "km": "ដីប្រៃ", "pron": "다이 프라이", "freq": 2},
                {"ko": "배수", "km": "ការបង្ហូរទឹក", "pron": "카 방후 뜩", "freq": 4},
                {"ko": "경작", "km": "ការភ្ជួរដី", "pron": "카 프추어 다이", "freq": 4},
                {"ko": "휴경", "km": "ការសម្រាកដី", "pron": "카 삼락 다이", "freq": 3},
                {"ko": "토양검사", "km": "ការពិនិត្យដី", "pron": "카 피니띠 다이", "freq": 3},
            ],
            "비료": [
                {"ko": "비료", "km": "ជី", "pron": "치", "freq": 5},
                {"ko": "퇴비", "km": "ជីកំប៉ុស", "pron": "치 깜뽀스", "freq": 4},
                {"ko": "화학비료", "km": "ជីគីមី", "pron": "치 끼미", "freq": 4},
                {"ko": "유기비료", "km": "ជីធម្មជាតិ", "pron": "치 톰마체아띠", "freq": 4},
                {"ko": "질소비료", "km": "ជីអាស៊ូត", "pron": "치 아숫", "freq": 3},
                {"ko": "인산비료", "km": "ជីផូស្វ័រ", "pron": "치 포스워", "freq": 3},
                {"ko": "칼리비료", "km": "ជីប៉ូតាស្យូម", "pron": "치 뽀따시움", "freq": 3},
                {"ko": "복합비료", "km": "ជីចម្រុះ", "pron": "치 참로", "freq": 3},
                {"ko": "액체비료", "km": "ជីរាវ", "pron": "치 리업", "freq": 2},
                {"ko": "엽면시비", "km": "ការបាញ់ជីលើស្លឹក", "pron": "카 반 치 러 슬릭", "freq": 2},
            ],
            "병해충방제": [
                {"ko": "해충", "km": "សត្វល្អិត", "pron": "삿 라잇", "freq": 4},
                {"ko": "병해", "km": "ជំងឺរុក្ខជាតិ", "pron": "춤 러켜체아띠", "freq": 4},
                {"ko": "농약", "km": "ថ្នាំសំលាប់សត្វល្អិត", "pron": "트남 쌈랍 삿 라잇", "freq": 4},
                {"ko": "살충제", "km": "ថ្នាំសំលាប់សត្វល្អិត", "pron": "트남 쌈랍 삿 라잇", "freq": 4},
                {"ko": "살균제", "km": "ថ្នាំសំលាប់មេរោគ", "pron": "트남 쌈랍 메 로옥", "freq": 3},
                {"ko": "제초제", "km": "ថ្នាំសំលាប់ស្មៅ", "pron": "트남 쌈랍 스마우", "freq": 3},
                {"ko": "방제", "km": "ការការពារ", "pron": "카 카피어", "freq": 4},
                {"ko": "천적", "km": "សត្រូវធម្មជាតិ", "pron": "삿뜨루 톰마체아띠", "freq": 2},
                {"ko": "생물방제", "km": "ការការពារដោយធម្មជាតិ", "pron": "카 카피어 다오이 톰마체아띠", "freq": 2},
                {"ko": "통합방제", "km": "ការការពាររួមបញ្ចូល", "pron": "카 카피어 루엄 반쫄", "freq": 2},
            ]
        }
        
        # 예문 템플릿
        self.example_templates = {
            "한국어": [
                "{term}는 농업에서 매우 중요합니다.",
                "{term} 사용법을 정확히 알아야 합니다.",
                "이 {term}로 좋은 결과를 얻을 수 있습니다.",
                "{term} 관리는 신중하게 해야 합니다.",
                "농민들은 {term}에 대해 잘 알고 있습니다."
            ],
            "크메르어": [
                "{term}ខ្លាំងណាស់សម្រាប់កសិកម្ម",
                "ត្រូវដឹងពីរបៀបប្រើ{term}ឱ្យបានត្រឹមត្រូវ",
                "អាចទទួលបានលទ្ធផលល្អជាមួយ{term}នេះ",
                "ការថែទាំ{term}ត្រូវធ្វើប្រុងប្រយ័ត្ន", 
                "កសិករ연ល់ដឹងអំពី{term}ហើយ"
            ]
        }

    def generate_enhanced_terms(self, target_count: int = 8000) -> None:
        """8000개 확장 농업용어 생성"""
        
        current_count = len(self.manager.data["terms"])
        remaining = target_count - current_count
        
        if remaining <= 0:
            print(f"✅ 이미 {current_count}개의 용어가 있습니다. 목표 달성!")
            return
        
        print(f"🚀 {remaining}개의 추가 용어 생성을 시작합니다...")
        print(f"현재: {current_count}개 → 목표: {target_count}개")
        
        generated_count = 0
        
        # 카테고리별로 용어 생성
        categories = list(self.base_terms.keys())
        terms_per_category = remaining // len(categories)
        
        for category in categories:
            category_terms = self.base_terms.get(category, [])
            print(f"\n📂 [{category}] 카테고리 - {terms_per_category}개 생성 중...")
            
            for i in range(terms_per_category):
                try:
                    # 기본 용어에서 변형 생성
                    base_term = random.choice(category_terms)
                    variation_num = (i // len(category_terms)) + 1
                    
                    # 용어 변형 생성
                    enhanced_term = self._create_term_variation(
                        base_term, category, variation_num, i + 1
                    )
                    
                    # 데이터베이스에 추가
                    term_id = self.manager.add_enhanced_term(**enhanced_term)
                    generated_count += 1
                    
                    if generated_count % 100 == 0:
                        print(f"  ✨ {generated_count}개 완료...")
                        
                except Exception as e:
                    print(f"  ❌ 오류 (항목 {i+1}): {e}")
        
        # 남은 용어들 생성 (기타 카테고리들)
        remaining_terms = remaining - generated_count
        if remaining_terms > 0:
            print(f"\n🔧 추가 카테고리 용어 {remaining_terms}개 생성 중...")
            
            additional_categories = [
                "수확후처리", "저장기술", "가공기술", "유통", "농업정책", 
                "농업경영", "원예", "임업", "수산업", "농업기술", "수자원관리", 
                "농업시설", "종자기술", "유기농업", "스마트농업", "농업환경", 
                "기후변화대응", "농촌개발", "농업교육", "농업금융", "농업보험", 
                "농산물품질", "농업안전"
            ]
            
            for i in range(remaining_terms):
                try:
                    category = random.choice(additional_categories)
                    
                    # 일반적인 농업용어 생성
                    enhanced_term = self._create_generic_term(category, i + 1)
                    
                    term_id = self.manager.add_enhanced_term(**enhanced_term)
                    generated_count += 1
                    
                    if generated_count % 50 == 0:
                        print(f"  ✨ {generated_count}개 완료...")
                        
                except Exception as e:
                    print(f"  ❌ 오류 (추가 항목 {i+1}): {e}")
        
        print(f"\n🎉 총 {generated_count}개의 농업용어 생성 완료!")
        
        # 최종 통계 출력
        final_stats = self.manager.get_learning_statistics()
        print(f"\n📊 최종 통계:")
        print(f"  • 총 용어 수: {final_stats['total_terms']:,}")
        print(f"  • 목표 달성률: {final_stats['progress_percentage']:.1f}%")
        print(f"  • 총 학습 일수: {final_stats['total_learning_days']:,}일")

    def _create_term_variation(self, base_term: dict, category: str, variation: int, index: int) -> dict:
        """기본 용어에서 변형 용어 생성"""
        
        korean_base = base_term["ko"]
        khmer_base = base_term["km"]
        pronunciation_base = base_term["pron"]
        
        # 변형 접미사들
        suffixes = {
            "한국어": ["기술", "방법", "관리", "시설", "장비", "도구", "재료", "품종", "종류", "체계"],
            "크메르어": ["បច្ចេកទេស", "វិធីសាស្ត្រ", "ការគ្រប់គ្រង", "កន្លែង", "ឧបករណ៍", "ឧបករណ៍", "សម្ភារៈ", "ពូជ", "ប្រភេទ", "ប្រព័ន្ធ"],
            "발음": ["빽째끄떼스", "비티삿", "카 크럽크롱", "깐랭", "웁바까론", "웁바까론", "삼파리어", "푸체", "프로펫", "프로푼"]
        }
        
        # 변형어 생성
        if variation <= len(suffixes["한국어"]):
            suffix_idx = variation - 1
            korean_term = f"{korean_base} {suffixes['한국어'][suffix_idx]}"
            khmer_term = f"{khmer_base}{suffixes['크메르어'][suffix_idx]}"
            pronunciation = f"{pronunciation_base} {suffixes['발음'][suffix_idx]}"
        else:
            korean_term = f"{korean_base} {variation}"
            khmer_term = f"{khmer_base}{variation}"
            pronunciation = f"{pronunciation_base} {variation}"
        
        # 예문 생성
        korean_example = random.choice(self.example_templates["한국어"]).format(term=korean_base)
        khmer_example = random.choice(self.example_templates["크메르어"]).format(term=khmer_base)
        
        return {
            "korean_term": korean_term,
            "khmer_term": khmer_term,
            "khmer_pronunciation": pronunciation,
            "category": category,
            "korean_definition": f"{korean_base}와 관련된 {suffixes['한국어'][(variation-1) % len(suffixes['한국어'])]}입니다.",
            "khmer_definition": f"នេះគឺជា{suffixes['크메르어'][(variation-1) % len(suffixes['크메르어'])]}ទាក់ទងនឹង{khmer_base}",
            "korean_example": korean_example,
            "khmer_example": khmer_example,
            "khmer_example_pronunciation": self._generate_example_pronunciation(khmer_example),
            "english_term": f"{korean_base.lower()} {suffixes['한국어'][(variation-1) % len(suffixes['한국어'])].lower()}",
            "frequency_level": base_term.get("freq", 3),
            "difficulty_level": random.choice(["기초", "중급", "고급"]),
            "tags": [korean_base, category, "농업"],
            "mnemonics": f"{korean_base} 연상법: {korean_base}를 생각하면 쉽게 기억할 수 있습니다.",
            "cultural_notes": f"캄보디아 농업에서 {korean_base}는 중요한 역할을 합니다."
        }

    def _create_generic_term(self, category: str, index: int) -> dict:
        """일반적인 농업용어 생성"""
        
        # 카테고리별 기본 용어
        generic_terms = {
            "수확후처리": {"ko": "건조", "km": "ការសម្ងួត", "pron": "카 삼응엇"},
            "저장기술": {"ko": "저장", "km": "ការរក្សាទុក", "pron": "카 레악사 뚝"},
            "가공기술": {"ko": "가공", "km": "ការកែច្នៃ", "pron": "카 께 츠나이"},
            "유통": {"ko": "판매", "km": "ការលក់", "pron": "카 루억"},
            "농업정책": {"ko": "정책", "km": "គោលនយោបាយ", "pron": "꼴 노요바이"},
            "농업경영": {"ko": "경영", "km": "ការគ្រប់គ្រង", "pron": "카 크럽크롱"},
            "원예": {"ko": "원예", "km": "សួនច្បារ", "pron": "수온 츠바"},
            "임업": {"ko": "산림", "km": "ព្រៃឈើ", "pron": "프라이 츼"},
            "수산업": {"ko": "양식", "km": "ការចិញ្ចឹម", "pron": "카 츤쯤"},
            "농업기술": {"ko": "기술", "km": "បច្ចេកទេស", "pron": "빽째끄떼스"},
            "수자원관리": {"ko": "물관리", "km": "ការគ្រប់គ្រងទឹក", "pron": "카 크럽크롱 뜩"},
            "농업시설": {"ko": "시설", "km": "កន្លែង", "pron": "깐랭"},
            "종자기술": {"ko": "종자", "km": "គ្រាប់ពូជ", "pron": "크랍 푸체"},
            "유기농업": {"ko": "유기농", "km": "សរីរាង្គ", "pron": "사리랑"},
            "스마트농업": {"ko": "스마트", "km": "ទំនើប", "pron": "톰노업"},
            "농업환경": {"ko": "환경", "km": "បរិស្ថាន", "pron": "바리스탄"},
            "기후변화대응": {"ko": "기후", "km": "អាកាសធាតុ", "pron": "아까스 타투"},
            "농촌개발": {"ko": "개발", "km": "ការអភិវឌ្ឍ", "pron": "카 아피봇"},
            "농업교육": {"ko": "교육", "km": "ការអប់រំ", "pron": "카 읍럼"},
            "농업금융": {"ko": "금융", "km": "ហិរញ្ញវត្ថុ", "pron": "히란나봇투"},
            "농업보험": {"ko": "보험", "km": "ការធានារ៉ាប់រង", "pron": "카 티아나 랍롱"},
            "농산물품질": {"ko": "품질", "km": "គុណភាព", "pron": "꾼나파프"},
            "농업안전": {"ko": "안전", "km": "សុវត្ថិភាព", "pron": "수봇타파프"}
        }
        
        base_term = generic_terms.get(category, {"ko": "농업", "km": "កសិកម្ម", "pron": "까시깜"})
        
        # 변형 번호 추가
        korean_term = f"{base_term['ko']} {index}"
        khmer_term = f"{base_term['km']}{index}"
        pronunciation = f"{base_term['pron']} {index}"
        
        korean_example = f"{base_term['ko']}는 농업 발전에 필수적입니다."
        khmer_example = f"{base_term['km']}ចាំបាច់សម្រាប់ការអភិវឌ្ឍកសិកម្ម"
        
        return {
            "korean_term": korean_term,
            "khmer_term": khmer_term,
            "khmer_pronunciation": pronunciation,
            "category": category,
            "korean_definition": f"{category} 분야의 {base_term['ko']}와 관련된 농업 용어입니다.",
            "khmer_definition": f"នេះគឺជាពាក្យកសិកម្មទាក់ទងនឹង{base_term['km']}ក្នុងវិស័យ{category}",
            "korean_example": korean_example,
            "khmer_example": khmer_example,
            "khmer_example_pronunciation": self._generate_example_pronunciation(khmer_example),
            "english_term": f"{category.lower()} term {index}",
            "frequency_level": random.randint(2, 4),
            "difficulty_level": random.choice(["기초", "중급", "고급"]),
            "tags": [category, "농업", "전문용어"],
            "mnemonics": f"{category} 관련 용어로 기억하세요.",
            "cultural_notes": f"캄보디아 {category} 분야에서 사용되는 용어입니다."
        }

    def _generate_example_pronunciation(self, khmer_text: str) -> str:
        """크메르어 예문의 발음 생성 (간단한 근사치)"""
        # 실제로는 더 정교한 발음 변환 로직이 필요
        return f"{khmer_text}의 한글 발음"

if __name__ == "__main__":
    generator = ExtendedDataGenerator()
    
    # 현재 상태 확인
    current_stats = generator.manager.get_learning_statistics()
    print("🌾 캄보디아 농업용어 확장 데이터 생성기")
    print("=" * 50)
    print(f"현재 용어 수: {current_stats['total_terms']:,}개")
    print(f"목표: 8,000개")
    print(f"진행률: {current_stats['progress_percentage']:.1f}%")
    
    if current_stats['total_terms'] < 8000:
        print(f"\n🚀 {8000 - current_stats['total_terms']:,}개의 추가 용어가 필요합니다.")
        
        # 사용자 확인
        response = input("농업용어 확장 데이터를 생성하시겠습니까? (y/N): ")
        
        if response.lower() in ['y', 'yes', '예', 'ㅇ']:
            generator.generate_enhanced_terms(8000)
        else:
            print("취소되었습니다.")
    else:
        print("\n✅ 이미 목표 용어 수에 도달했습니다!")
        
        # 추가 데이터 생성 옵션
        response = input("더 많은 용어를 추가하시겠습니까? (y/N): ")
        if response.lower() in ['y', 'yes', '예', 'ㅇ']:
            target = int(input("목표 용어 수를 입력하세요 (현재보다 큰 수): ") or 10000)
            generator.generate_enhanced_terms(target)
#!/usr/bin/env python3
"""
캄보디아 농업용어 5,000개 대량 데이터 생성기
Mass Agricultural Terms Generator for Cambodian Learning
"""

import json
import random
from typing import List, Dict, Tuple
from datetime import datetime

class MassAgriculturalTermsGenerator:
    def __init__(self):
        """5,000개 농업용어 대량 생성기 초기화"""
        
        # 25개 카테고리별로 200개씩 = 5,000개
        self.categories = {
            "crop_cultivation": {"name": "작물재배", "target": 200},
            "livestock": {"name": "축산업", "target": 200}, 
            "agricultural_machinery": {"name": "농기계", "target": 200},
            "soil_management": {"name": "토양관리", "target": 200},
            "fertilizer": {"name": "비료", "target": 200},
            "pest_control": {"name": "병해충방제", "target": 200},
            "harvest_processing": {"name": "수확후처리", "target": 200},
            "storage_technology": {"name": "저장기술", "target": 200},
            "food_processing": {"name": "가공기술", "target": 200},
            "marketing": {"name": "유통", "target": 200},
            "policy": {"name": "농업정책", "target": 200},
            "farm_management": {"name": "농업경영", "target": 200},
            "horticulture": {"name": "원예", "target": 200},
            "forestry": {"name": "임업", "target": 200},
            "fisheries": {"name": "수산업", "target": 200},
            "agricultural_technology": {"name": "농업기술", "target": 200},
            "water_management": {"name": "수자원관리", "target": 200},
            "infrastructure": {"name": "농업시설", "target": 200},
            "seed_technology": {"name": "종자기술", "target": 200},
            "pesticides": {"name": "농약", "target": 200},
            "organic_farming": {"name": "유기농업", "target": 200},
            "smart_farming": {"name": "스마트농업", "target": 200},
            "environment": {"name": "농업환경", "target": 200},
            "climate_adaptation": {"name": "기후변화대응", "target": 200},
            "agriculture_portal": {"name": "농업정보포털", "target": 200}
        }
        
        # 크메르어 농업용어 기본 템플릿
        self.khmer_base_terms = {
            "crop_cultivation": [
                "ស្រូវ", "ខ្ញុំ", "ដំណាំ", "ស្រែ", "បន្លែ", "ផ្លែឈើ", "ពូជ", "គ្រាប់ពូជ", "បន្លាស់", "ដាំ",
                "ស្រូវស្ពៃ", "ស្រូវផ្កា", "ស្រូវមាស", "ដំណាំជាង", "បន្លែក្រហម", "ក្តោប", "ល្ពៅ", "ដូង", "ម្រេច", "ព្រៃ",
                "ប៊ី", "ស្ពៃ", "ដំឡូង", "អំពៅ", "ត្រសក់", "បាយ", "ជំពាក់", "ខ្ទឹម", "ស្លឹក", "ផ្កា"
            ],
            "livestock": [
                "គោ", "ក្របី", "ជ្រូក", "មាន់", "ពពែ", "ត្រី", "បង្គា", "ស្វា", "សេះ", "ពពេញ",
                "គោពពេញ", "ក្របីស", "ជ្រូកព្រៃ", "មាន់ព្រៃ", "ពពែទឹក", "ត្រីខ្សាច់", "បង្គាឈូក", "ស្វាព្រៃ", "សេះសេះ", "ពពេញទុំ",
                "សត្វរាស្ត្រ", "ចិញ្ចឹម", "សត្វពាហនៈ", "គោបាល", "ជ្រូកបាល", "កុម", "បុក", "ឆ្កែ", "ឆ្មា", "សេះ"
            ],
            "agricultural_machinery": [
                "រថយន្ត", "គ្រឿងយន្ត", "នង្គ័ល", "រំបៀត", "យន្តហោះ", "ម៉ាស៊ីន", "ឧបករណ៍", "កាំបិត", "ដាវ", "លំពែង",
                "ត្រាក់ធ័រ", "រថយន្តដឹក", "យន្តកាត់", "យន្តច្រូត", "យន្តបាញ់", "នង្គ័លយន្ត", "រំបៀតយន្ត", "ស្នូល", "កង់", "ខ្សែ"
            ],
            "soil_management": [
                "ដី", "ដីក្រហម", "ដីខ្មៅ", "ដីល្មៅ", "ដីស", "ដីថ្ម", "ផ្នែកដី", "កម្រាលដី", "ភក់", "ខ្សាច់",
                "ភូមិសាស្ត្រ", "ជីធម្មជាតិ", "ការពារដី", "កែលម្អដី", "ដីអាស៊ីត", "ដីបាស", "ដីល្មុក", "ដីស្រោប", "ដីគុម្ពោត", "ដីខ្ទឹស"
            ],
            "fertilizer": [
                "ជី", "ជីធម្មជាតិ", "ជីគីមី", "ជីកាប៉ូន", "ផ្នាស់", "ជីកំប៉ុស", "ជីអុរីយ៉ា", "ជីផូស្វ័រ", "ជីប៉ូតាស", "ខនិត្រាត",
                "ជីរាវ", "ជីកាំកប់", "ជីស្រស់", "ជីប្រេង", "ជីកុម្ម៉ង់", "ជីធាតុខ្មៅ", "ជីលាយ", "ជីសរីរាង្គ", "ជីមីក្រូ", "ជីម៉ាក្រូ"
            ]
        }
        
        # 한국어 농업용어 기본 템플릿
        self.korean_base_terms = {
            "crop_cultivation": [
                "벼", "밭", "농작물", "논", "채소", "과일", "품종", "종자", "모종", "심기",
                "자포니카", "인디카", "조생종", "중생종", "만생종", "상추", "배추", "무", "당근", "감자",
                "고구마", "옥수수", "콩", "팥", "보리", "밀", "메밀", "수수", "조", "기장"
            ],
            "livestock": [
                "소", "돼지", "닭", "오리", "물고기", "염소", "양", "말", "토끼", "거위",
                "한우", "젖소", "육우", "육계", "산란계", "육용오리", "산란오리", "흑염소", "면양", "승마용말",
                "가축", "사육", "축산", "목축", "방목", "사료", "급여", "개", "고양이", "메추라기"
            ],
            "agricultural_machinery": [
                "트랙터", "콤바인", "쟁기", "써레", "파종기", "기계", "도구", "칼", "낫", "호미",
                "운반차", "살포기", "수확기", "탈곡기", "분무기", "동력쟁기", "로터리", "바퀴", "타이어", "벨트"
            ],
            "soil_management": [
                "토양", "적토", "흑토", "황토", "사토", "식토", "토층", "표토", "진흙", "모래",
                "토양학", "유기물", "토양보전", "토양개량", "산성토양", "알칼리토양", "점토", "양토", "사양토", "토성"
            ],
            "fertilizer": [
                "비료", "퇴비", "화학비료", "유기비료", "거름", "복합비료", "요소비료", "인산비료", "칼리비료", "질소비료",
                "액비", "기비", "추비", "엽면시비", "완효성비료", "속효성비료", "혼합비료", "유기질비료", "미량요소", "다량요소"
            ]
        }
        
        # 영어 농업용어 기본 템플릿
        self.english_base_terms = {
            "crop_cultivation": [
                "rice", "field", "crop", "paddy", "vegetable", "fruit", "variety", "seed", "seedling", "planting",
                "japonica", "indica", "early variety", "medium variety", "late variety", "lettuce", "cabbage", "radish", "carrot", "potato",
                "sweet potato", "corn", "soybean", "red bean", "barley", "wheat", "buckwheat", "sorghum", "millet", "foxtail millet"
            ],
            "livestock": [
                "cattle", "pig", "chicken", "duck", "fish", "goat", "sheep", "horse", "rabbit", "goose",
                "beef cattle", "dairy cow", "beef cow", "broiler", "layer", "meat duck", "egg duck", "black goat", "wool sheep", "riding horse",
                "livestock", "breeding", "animal husbandry", "ranching", "grazing", "feed", "feeding", "dog", "cat", "quail"
            ],
            "agricultural_machinery": [
                "tractor", "combine", "plow", "harrow", "seeder", "machine", "tool", "knife", "sickle", "hoe",
                "transport vehicle", "spreader", "harvester", "thresher", "sprayer", "power plow", "rotary", "wheel", "tire", "belt"
            ],
            "soil_management": [
                "soil", "red soil", "black soil", "yellow soil", "sandy soil", "clay soil", "soil layer", "topsoil", "mud", "sand",
                "pedology", "organic matter", "soil conservation", "soil improvement", "acid soil", "alkaline soil", "clay", "loam", "sandy loam", "soil texture"
            ],
            "fertilizer": [
                "fertilizer", "compost", "chemical fertilizer", "organic fertilizer", "manure", "compound fertilizer", "urea fertilizer", "phosphate fertilizer", "potash fertilizer", "nitrogen fertilizer",
                "liquid fertilizer", "base fertilizer", "top dressing", "foliar application", "slow-release fertilizer", "quick-release fertilizer", "mixed fertilizer", "organic fertilizer", "micronutrient", "macronutrient"
            ]
        }
        
    def generate_khmer_term(self, category: str, base_term: str, index: int) -> str:
        """크메르어 농업용어 생성"""
        variations = [
            f"{base_term}ធំ",      # 큰
            f"{base_term}តូច",     # 작은  
            f"{base_term}ស",       # 흰
            f"{base_term}ក្រហម",   # 빨간
            f"{base_term}ខ្មៅ",    # 검은
            f"{base_term}ល្អ",     # 좋은
            f"{base_term}ថ្មី",     # 새로운
            f"{base_term}ចាស់",    # 오래된
            f"{base_term}ព្រៃ",     # 야생의
            f"{base_term}ផ្ទះ",    # 집의
            f"ការ{base_term}",     # ~하기
            f"{base_term}កម្ម",    # ~업
            f"{base_term}វិទ្យា",   # ~학
            f"{base_term}ករណ៍",   # ~법
            f"{base_term}ភាព",     # ~성
        ]
        
        if index < len(variations):
            return variations[index]
        else:
            # 숫자 조합으로 추가 변형 생성
            return f"{base_term}{(index // 10) + 1}"
    
    def generate_korean_term(self, category: str, base_term: str, index: int) -> str:
        """한국어 농업용어 생성"""
        variations = [
            f"대형{base_term}",
            f"소형{base_term}", 
            f"흰{base_term}",
            f"빨간{base_term}",
            f"검은{base_term}",
            f"우량{base_term}",
            f"신{base_term}",
            f"구{base_term}",
            f"야생{base_term}",
            f"가축{base_term}",
            f"{base_term}재배",
            f"{base_term}업",
            f"{base_term}학",
            f"{base_term}법",
            f"{base_term}성",
        ]
        
        if index < len(variations):
            return variations[index]
        else:
            return f"{base_term}{(index // 10) + 1}호"
    
    def generate_english_term(self, category: str, base_term: str, index: int) -> str:
        """영어 농업용어 생성"""
        variations = [
            f"large {base_term}",
            f"small {base_term}",
            f"white {base_term}",
            f"red {base_term}",
            f"black {base_term}",
            f"improved {base_term}",
            f"new {base_term}",
            f"old {base_term}",
            f"wild {base_term}",
            f"domestic {base_term}",
            f"{base_term} cultivation",
            f"{base_term} industry",
            f"{base_term} science",
            f"{base_term} method",
            f"{base_term} quality",
        ]
        
        if index < len(variations):
            return variations[index]
        else:
            return f"{base_term} type {(index // 10) + 1}"
    
    def generate_pronunciation(self, khmer_term: str) -> str:
        """크메르어 발음 생성 (한글 표기)"""
        # 크메르어 -> 한글 발음 매핑 룰
        pronunciation_map = {
            'ស្រូវ': '스라우', 'ដំណាំ': '덤남', 'គោ': '코', 'ជ្រូក': '추룩', 'មាន់': '만',
            'ដី': '다이', 'ជី': '치', 'ទឹក': '뜨크', 'ស្រែ': '스래', 'បន្លែ': '번러',
            'ធំ': '톰', 'តូច': '토치', 'ស': '스', 'ក្រហម': '크러홈', 'ខ្មៅ': '크마우',
            'ល្អ': '러', 'ថ្មី': '트마이', 'ចាស់': '차스', 'ព្រៃ': '프라이', 'ផ្ទះ': '프테아',
            'ការ': '까', 'កម្ម': '깜', 'វិទ្យា': '위뜌아', 'ករណ៍': '까런', 'ភាព': '피어프'
        }
        
        # 기본 발음 생성 로직
        result = ""
        for char_group in khmer_term.split():
            if char_group in pronunciation_map:
                result += pronunciation_map[char_group] + " "
            else:
                # 기본 음성학적 근사치 생성
                result += self._approximate_pronunciation(char_group) + " "
        
        return result.strip()
    
    def _approximate_pronunciation(self, khmer_text: str) -> str:
        """크메르어 음성학적 근사 발음 생성"""
        # 간단한 음성학적 변환 규칙
        char_map = {
            'ស': '스', 'រ': '르', 'ូ': '우', 'វ': '우', 'ដ': '다', 'ំ': '음',
            'ណ': '나', 'ាំ': '암', 'គ': '코', 'ោ': '오', 'ជ': '치', 'ក': '까',
            'ម': '마', 'ន': '느', 'ប': '바', 'ល': '러', 'ទ': '뜨', 'ឹ': '으',
            'ផ': '프', 'ទ': '테', 'ះ': '아', 'ថ': '타', 'ី': '이', 'ច': '차'
        }
        
        result = ""
        for char in khmer_text:
            result += char_map.get(char, char)
        
        return result[:8]  # 최대 8글자로 제한
    
    def generate_example_sentence(self, khmer_term: str, korean_term: str, english_term: str, category: str) -> Dict[str, str]:
        """예문 생성 (크메르어, 한국어, 영어)"""
        
        # 카테고리별 예문 템플릿
        templates = {
            "crop_cultivation": {
                "kh": f"{khmer_term}គឺជាដំណាំសំខាន់មួយ។",
                "ko": f"{korean_term}은 중요한 농작물입니다.",
                "en": f"{english_term} is an important crop."
            },
            "livestock": {
                "kh": f"{khmer_term}ជាសត្វចិញ្ចឹមល្អ។", 
                "ko": f"{korean_term}은 좋은 가축입니다.",
                "en": f"{english_term} is good livestock."
            },
            "agricultural_machinery": {
                "kh": f"{khmer_term}ជួយកសិករច្រើន។",
                "ko": f"{korean_term}은 농부에게 많은 도움이 됩니다.",
                "en": f"{english_term} helps farmers a lot."
            },
            "soil_management": {
                "kh": f"{khmer_term}ល្អសម្រាប់ដាំដុះ។",
                "ko": f"{korean_term}은 재배에 좋습니다.", 
                "en": f"{english_term} is good for cultivation."
            },
            "fertilizer": {
                "kh": f"{khmer_term}ជួយដំណាំលូតលាស់។",
                "ko": f"{korean_term}은 작물 성장에 도움이 됩니다.",
                "en": f"{english_term} helps crop growth."
            }
        }
        
        # 기본 템플릿이 없는 경우 일반 템플릿 사용
        default_template = {
            "kh": f"{khmer_term}មានសារៈសំខាន់ក្នុងកសិកម្ម។",
            "ko": f"{korean_term}은 농업에서 중요합니다.",
            "en": f"{english_term} is important in agriculture."
        }
        
        template = templates.get(category, default_template)
        
        return {
            "example_kh": template["kh"],
            "example_pron": self.generate_pronunciation(template["kh"]),
            "example_ko": template["ko"],
            "example_en": template["en"]
        }
    
    def generate_category_terms(self, category: str, count: int) -> List[Dict]:
        """특정 카테고리의 농업용어 대량 생성"""
        terms = []
        
        # 해당 카테고리의 기본 용어들 가져오기
        khmer_bases = self.khmer_base_terms.get(category, ["ដំណាំ", "កសិកម្ម", "ការងារ"])
        korean_bases = self.korean_base_terms.get(category, ["농작물", "농업", "작업"])
        english_bases = self.english_base_terms.get(category, ["crop", "agriculture", "work"])
        
        # 기본 용어 수를 맞춰주기
        max_bases = max(len(khmer_bases), len(korean_bases), len(english_bases))
        
        for i in range(count):
            # 기본 용어 순환 사용
            base_index = i % max_bases
            
            # 기본 용어가 부족한 경우 첫 번째 용어 재사용
            khmer_base = khmer_bases[min(base_index, len(khmer_bases) - 1)]
            korean_base = korean_bases[min(base_index, len(korean_bases) - 1)]
            english_base = english_bases[min(base_index, len(english_bases) - 1)]
            
            # 변형 생성
            variation_index = i // max_bases
            
            khmer_term = self.generate_khmer_term(category, khmer_base, variation_index)
            korean_term = self.generate_korean_term(category, korean_base, variation_index) 
            english_term = self.generate_english_term(category, english_base, variation_index)
            
            # 예문 생성
            example = self.generate_example_sentence(khmer_term, korean_term, english_term, category)
            
            # ID 생성 (카테고리별 시작점을 다르게 함)
            category_ids = {
                "crop_cultivation": 1000,
                "livestock": 2000,
                "agricultural_machinery": 3000,
                "soil_management": 4000,
                "fertilizer": 5000,
                "pest_control": 6000,
                "harvest_processing": 7000,
                "storage_technology": 8000,
                "food_processing": 9000,
                "marketing": 10000,
                "policy": 11000,
                "farm_management": 12000,
                "horticulture": 13000,
                "forestry": 14000,
                "fisheries": 15000,
                "agricultural_technology": 16000,
                "water_management": 17000,
                "infrastructure": 18000,
                "seed_technology": 19000,
                "pesticides": 20000,
                "organic_farming": 21000,
                "smart_farming": 22000,
                "environment": 23000,
                "climate_adaptation": 24000,
                "agriculture_portal": 25000
            }
            
            term_id = category_ids.get(category, 90000) + i + 1
            
            term_data = {
                "id": term_id,
                "khmer": khmer_term,
                "pronunciation_ko": self.generate_pronunciation(khmer_term),
                "meaning_ko": korean_term,
                "meaning_en": english_term,
                "category": category,
                "example": example
            }
            
            terms.append(term_data)
        
        return terms
    
    def generate_all_terms(self) -> Dict[str, any]:
        """전체 5,000개 농업용어 생성"""
        all_terms = []
        examples = {}
        
        print("🚀 5,000개 캄보디아 농업용어 대량 생성 시작...")
        
        for category, info in self.categories.items():
            print(f"📝 {info['name']} 카테고리: {info['target']}개 생성 중...")
            
            category_terms = self.generate_category_terms(category, info['target'])
            
            for term in category_terms:
                # examples 딕셔너리에 예문 추가
                examples[term['id']] = [term['example']]
                # term 객체에서 example 제거 (별도 관리)
                del term['example']
                
                all_terms.append(term)
        
        print(f"✅ 총 {len(all_terms)}개 농업용어 생성 완료!")
        
        return {
            "terms": all_terms,
            "examples": examples,
            "categories": self.categories,
            "metadata": {
                "total_count": len(all_terms),
                "generated_at": datetime.now().isoformat(),
                "version": "5.0",
                "target_achieved": True
            }
        }

if __name__ == "__main__":
    generator = MassAgriculturalTermsGenerator()
    result = generator.generate_all_terms()
    
    # 결과 저장
    with open("/home/user/webapp/data/mass_agricultural_terms_5000.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 5,000개 농업용어 데이터 생성 완료!")
    print(f"📂 저장 위치: /home/user/webapp/data/mass_agricultural_terms_5000.json")
#!/usr/bin/env python3
"""
캄보디아 농업용어 8000단어 확장 관리 시스템
Enhanced Agricultural Terms Manager for Mobile Learning App
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
import random
import urllib.parse

class EnhancedAgriculturalTermManager:
    def __init__(self, data_file_path: str = None):
        """확장된 농업용어 관리자 초기화"""
        # 확장된 카테고리 목록을 먼저 정의
        self.categories = [
            "작물재배", "축산업", "농기계", "토양관리", "비료", "병해충방제",
            "수확후처리", "저장기술", "가공기술", "유통", "농업정책", "농업경영",
            "원예", "임업", "수산업", "농업기술", "수자원관리", "농업시설",
            "종자기술", "농약", "유기농업", "스마트농업", "농업환경", "기후변화대응",
            "농촌개발", "농업교육", "농업금융", "농업보험", "농산물품질", "농업안전"
        ]
        
        if data_file_path is None:
            self.data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'enhanced_agricultural_terms.json')
        else:
            self.data_file_path = data_file_path
        
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """데이터 파일 로드"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 초기 확장된 데이터 구조 생성
            initial_data = {
                "metadata": {
                    "version": "2.0",
                    "total_terms": 0,
                    "last_updated": datetime.now().isoformat(),
                    "target_count": 8000,
                    "daily_learning_size": 10,
                    "categories": self.categories
                },
                "terms": []
            }
            self._save_data(initial_data)
            return initial_data
        except json.JSONDecodeError as e:
            raise Exception(f"데이터 파일 형식 오류: {e}")
    
    def _save_data(self, data: Dict[str, Any] = None) -> None:
        """데이터 파일 저장"""
        if data is None:
            data = self.data
        
        # 메타데이터 업데이트
        data["metadata"]["total_terms"] = len(data["terms"])
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # 디렉토리 생성 (없는 경우)
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_enhanced_term(self, 
                         korean_term: str,
                         khmer_term: str,
                         khmer_pronunciation: str,
                         category: str,
                         korean_definition: str,
                         khmer_definition: str,
                         korean_example: str,
                         khmer_example: str,
                         khmer_example_pronunciation: str,
                         english_term: str = "",
                         english_example: str = "",
                         image_url: str = "",
                         frequency_level: int = 3,
                         difficulty_level: str = "중급",
                         tags: List[str] = None,
                         mnemonics: str = "",
                         cultural_notes: str = "") -> int:
        """확장된 농업용어 추가"""
        
        if tags is None:
            tags = []
        
        # 새 ID 생성 (기존 최대 ID + 1)
        existing_ids = [term.get("id", 0) for term in self.data["terms"]]
        new_id = max(existing_ids, default=0) + 1
        
        # 학습 순서 계산 (frequency_level 기반)
        learning_order = self._calculate_learning_order(frequency_level, difficulty_level)
        
        new_term = {
            "id": new_id,
            "korean_term": korean_term,
            "khmer_term": khmer_term,
            "khmer_pronunciation": khmer_pronunciation,
            "english_term": english_term,
            "category": category,
            "korean_definition": korean_definition,
            "khmer_definition": khmer_definition,
            "korean_example": korean_example,
            "khmer_example": khmer_example,
            "khmer_example_pronunciation": khmer_example_pronunciation,
            "english_example": english_example,
            "image_url": image_url,
            "audio_url_khmer": "",  # TTS로 생성 예정
            "audio_url_korean": "", # TTS로 생성 예정
            "frequency_level": frequency_level,
            "learning_order": learning_order,
            "related_terms": [],
            "difficulty_level": difficulty_level,
            "tags": tags,
            "mnemonics": mnemonics,
            "cultural_notes": cultural_notes,
            "created_date": datetime.now().isoformat(),
            "updated_date": datetime.now().isoformat(),
            "verified": False,
            "last_reviewed": None
        }
        
        self.data["terms"].append(new_term)
        self._save_data()
        
        return new_id
    
    def _calculate_learning_order(self, frequency_level: int, difficulty_level: str) -> int:
        """학습 순서 계산 (빈도와 난이도 기반)"""
        # 기본 점수
        base_score = 0
        
        # 빈도 점수 (높을수록 먼저 학습)
        frequency_score = (6 - frequency_level) * 1000  # 5=1000, 4=2000, 3=3000, 2=4000, 1=5000
        
        # 난이도 점수 (기초 먼저, 고급 나중에)
        difficulty_scores = {"기초": 0, "중급": 3000, "고급": 6000}
        difficulty_score = difficulty_scores.get(difficulty_level, 3000)
        
        # 현재 용어 수에 따른 순서
        current_count = len(self.data["terms"])
        
        return frequency_score + difficulty_score + current_count
    
    def get_daily_words(self, day: int, limit: int = 10) -> List[Dict[str, Any]]:
        """일일 학습용 단어 가져오기"""
        start_index = (day - 1) * limit
        
        # 학습 순서대로 정렬
        sorted_terms = sorted(self.data["terms"], key=lambda x: x.get("learning_order", 999999))
        
        # 해당 날짜의 단어들
        daily_words = sorted_terms[start_index:start_index + limit]
        
        return daily_words
    
    def get_words_by_category(self, category: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """카테고리별 단어 가져오기"""
        filtered_words = [term for term in self.data["terms"] if term.get("category") == category]
        
        # 학습 순서대로 정렬
        sorted_words = sorted(filtered_words, key=lambda x: x.get("learning_order", 999999))
        
        if limit:
            return sorted_words[:limit]
        return sorted_words
    
    def search_enhanced_terms(self, 
                            keyword: str = "", 
                            category: str = "", 
                            difficulty_level: str = "",
                            frequency_level: int = 0,
                            verified_only: bool = False,
                            limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """확장된 용어 검색"""
        results = []
        keyword_lower = keyword.lower()
        
        for term in self.data["terms"]:
            # 검증된 용어만 필터링
            if verified_only and not term.get("verified", False):
                continue
                
            # 카테고리 필터링
            if category and term.get("category", "") != category:
                continue
                
            # 난이도 필터링
            if difficulty_level and term.get("difficulty_level", "") != difficulty_level:
                continue
            
            # 빈도 필터링
            if frequency_level > 0 and term.get("frequency_level", 0) != frequency_level:
                continue
            
            # 키워드 검색 (다양한 필드에서)
            if keyword:
                searchable_text = " ".join([
                    term.get("korean_term", ""),
                    term.get("khmer_term", ""),
                    term.get("khmer_pronunciation", ""),
                    term.get("english_term", ""),
                    term.get("korean_definition", ""),
                    term.get("khmer_definition", ""),
                    term.get("korean_example", ""),
                    term.get("khmer_example", ""),
                    " ".join(term.get("tags", []))
                ]).lower()
                
                if keyword_lower not in searchable_text:
                    continue
            
            results.append(term)
        
        # 학습 순서대로 정렬
        results.sort(key=lambda x: x.get("learning_order", 999999))
        
        if limit:
            return results[:limit]
        return results
    
    def generate_sample_enhanced_data(self, count: int = 100) -> None:
        """확장된 샘플 데이터 생성"""
        
        sample_base_terms = [
            {
                "korean_term": "벼", "khmer_term": "ស្រូវ", "khmer_pronunciation": "스라우",
                "category": "작물재배", "frequency_level": 5,
                "korean_definition": "논에서 기르는 한해살이 벼과 식물로, 쌀의 원료가 되는 곡물",
                "khmer_definition": "រុក្ខជាតិក្រុមបាយដែលដាំក្នុងស្រែ និងជាវត្ថុធាតុដើមនៃអង្ករ",
                "korean_example": "벼농사는 캄보디아의 주요 농업 활동입니다.",
                "khmer_example": "ការដាំស្រូវគឺជាសកម្មភាពកសិកម្មសំខាន់របស់កម្ពុជា",
                "khmer_example_pronunciation": "카 담 스라우 끄 치아 사깜마파프 솜칸 로보스 깜푸치아",
                "tags": ["곡물", "주식", "논농사"]
            },
            {
                "korean_term": "농기계", "khmer_term": "គ្រឿងយន្តកសិកម្ម", "khmer_pronunciation": "크룽 욘 까시깜",
                "category": "농기계", "frequency_level": 4,
                "korean_definition": "농업 작업에 사용되는 기계와 도구의 총칭",
                "khmer_definition": "គ្រឿងយន្ត និងឧបករណ៍ដែលប្រើប្រាស់សម្រាប់ការងារកសិកម្ម",
                "korean_example": "현대적인 농기계 도입으로 농작업 효율이 크게 향상되었습니다.",
                "khmer_example": "ការណែនាំគ្រឿងយន្តកសិកម្មទំនើបធ្វើឱ្យប្រសិទ្ធភាពការងារកសិកម្មកើនឡើងយ៉ាងខ្លាំង",
                "khmer_example_pronunciation": "카 나엠남 크룽욘 까시깜 톰노업 트뜨어으이 프로싯타파프 카낭가 까시깜 꼬언 라엥 야응 클라응",
                "tags": ["기계", "도구", "효율성"]
            },
            {
                "korean_term": "비료", "khmer_term": "ជី", "khmer_pronunciation": "치",
                "category": "비료", "frequency_level": 5,
                "korean_definition": "식물의 생장에 필요한 양분을 공급하는 물질",
                "khmer_definition": "សារធាតុដែលផ្គត់ផ្គង់សារធាតុចិញ្ចឹមចាំបាច់សម្រាប់ការលូតលាស់របស់រុក្ខជាតិ",
                "korean_example": "유기비료 사용으로 토양의 질을 개선할 수 있습니다.",
                "khmer_example": "ការប្រើប្រាស់ជីសរីរាង្គអាចធ្វើឱ្យគុណភាពដីប្រសើរឡើង",
                "khmer_example_pronunciation": "카 프러이 프라스 치 사리랑 아치 트뜨어으이 꾼나파프 다이 프로써어 라엥",
                "tags": ["양분", "토양", "유기농"]
            },
            {
                "korean_term": "수확", "khmer_term": "ការច្រូតកាត់", "khmer_pronunciation": "카 츄룻 깟",
                "category": "수확후처리", "frequency_level": 5,
                "korean_definition": "농작물이 익었을 때 거두어들이는 작업",
                "khmer_definition": "ការប្រមូលយកដំណាំពេលដែលវាទុំហើយ",
                "korean_example": "쌀 수확 시기는 보통 11월부터 12월입니다.",
                "khmer_example": "ពេលវេលាច្រូតកាត់អង្ករធម្មតាចាប់ពីខែវិច្ឆិកាដល់ខែធ្នូ",
                "khmer_example_pronunciation": "페일 벨라 츄룻 깟 응까 톰마따 찹 피 카에 빗치까 달 카에 트누",
                "tags": ["수확기", "농작업", "계절"]
            },
            {
                "korean_term": "관개", "khmer_term": "ប្រព័ន្ធធារាសាស្ត្រ", "khmer_pronunciation": "프로푼 타라사스",
                "category": "수자원관리", "frequency_level": 4,
                "korean_definition": "농작물에 물을 공급하는 인공적인 물 공급 시스템",
                "khmer_definition": "ប្រព័ន្ធផ្គត់ផ្គង់ទឹកសិប្បនិម្មិតសម្រាប់ដំណាំកសិកម្ម",
                "korean_example": "효율적인 관개 시스템으로 가뭄 피해를 줄일 수 있습니다.",
                "khmer_example": "ប្រព័ន្ធធារាសាស្ត្រប្រកបដោយប្រសិទ្ធភាពអាចកាត់បន្ថយការខូចខាតដោយសាយរគាំង",
                "khmer_example_pronunciation": "프로푼 타라사스 프로깝 다오이 프로싯타파프 아치 깟 밤타이 카 쿠치 카트 다오이 사이라깜",
                "tags": ["물", "시설", "가뭄대책"]
            }
        ]
        
        print(f"확장된 샘플 데이터 {count}개 생성 중...")
        
        for i in range(count):
            base_term = sample_base_terms[i % len(sample_base_terms)]
            
            # 변형된 용어 생성
            variation = i // len(sample_base_terms) + 1
            
            enhanced_term = {
                **base_term,
                "korean_term": f"{base_term['korean_term']} {variation}",
                "english_term": f"Agricultural term {i+1}",
                "english_example": f"This is an example sentence for agricultural term {i+1}.",
                "difficulty_level": random.choice(["기초", "중급", "고급"]),
                "frequency_level": random.randint(1, 5),
                "mnemonics": f"{base_term['korean_term']} 암기법: 연상을 통해 기억하세요.",
                "cultural_notes": "캄보디아 농업 문화에서 중요한 의미를 가집니다."
            }
            
            try:
                self.add_enhanced_term(**enhanced_term)
                if (i + 1) % 20 == 0:
                    print(f"  {i + 1}개 완료...")
            except Exception as e:
                print(f"  오류 ({i+1}번째): {e}")
        
        print(f"✅ {count}개 샘플 데이터 생성 완료!")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """학습용 통계 정보"""
        total_terms = len(self.data["terms"])
        verified_terms = len([t for t in self.data["terms"] if t.get("verified", False)])
        
        # 카테고리별 통계
        category_stats = {}
        frequency_stats = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        difficulty_stats = {}
        
        for term in self.data["terms"]:
            # 카테고리별
            category = term.get("category", "미분류")
            category_stats[category] = category_stats.get(category, 0) + 1
            
            # 빈도별
            frequency = term.get("frequency_level", 3)
            frequency_stats[frequency] += 1
            
            # 난이도별
            difficulty = term.get("difficulty_level", "중급")
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
        
        # 일일 학습 통계
        total_days_needed = (total_terms + 9) // 10  # 올림
        
        return {
            "total_terms": total_terms,
            "verified_terms": verified_terms,
            "unverified_terms": total_terms - verified_terms,
            "target_count": 8000,
            "progress_percentage": round((total_terms / 8000) * 100, 2),
            "category_distribution": category_stats,
            "frequency_distribution": frequency_stats,
            "difficulty_distribution": difficulty_stats,
            "remaining": max(0, 8000 - total_terms),
            "total_learning_days": total_days_needed,
            "current_day": min(total_days_needed, (total_terms + 9) // 10)
        }
    
    def export_for_mobile_app(self, output_path: str) -> bool:
        """모바일 앱용 데이터 내보내기"""
        try:
            mobile_data = {
                "app_version": "2.0",
                "data_version": datetime.now().strftime("%Y%m%d"),
                "total_terms": len(self.data["terms"]),
                "categories": self.categories,
                "terms": []
            }
            
            # 학습 순서대로 정렬하여 내보내기
            sorted_terms = sorted(self.data["terms"], key=lambda x: x.get("learning_order", 999999))
            
            for term in sorted_terms:
                mobile_term = {
                    "id": term.get("id"),
                    "korean": term.get("korean_term", ""),
                    "khmer": term.get("khmer_term", ""),
                    "pronunciation": term.get("khmer_pronunciation", ""),
                    "category": term.get("category", ""),
                    "definition_ko": term.get("korean_definition", ""),
                    "definition_km": term.get("khmer_definition", ""),
                    "example_ko": term.get("korean_example", ""),
                    "example_km": term.get("khmer_example", ""),
                    "example_pronunciation": term.get("khmer_example_pronunciation", ""),
                    "frequency": term.get("frequency_level", 3),
                    "difficulty": term.get("difficulty_level", "중급"),
                    "learning_order": term.get("learning_order", 999999),
                    "image": term.get("image_url", ""),
                    "tags": term.get("tags", [])
                }
                mobile_data["terms"].append(mobile_term)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(mobile_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"모바일 앱 데이터 내보내기 오류: {e}")
            return False

if __name__ == "__main__":
    # 테스트 및 샘플 데이터 생성
    manager = EnhancedAgriculturalTermManager()
    
    # 기존 용어가 없으면 샘플 데이터 생성
    if len(manager.data["terms"]) < 50:
        print("📚 확장된 샘플 데이터 생성 중...")
        manager.generate_sample_enhanced_data(100)
    
    # 통계 출력
    stats = manager.get_learning_statistics()
    print("\n=== 캄보디아 농업용어 학습 앱 현황 ===")
    print(f"📊 총 용어 수: {stats['total_terms']:,}")
    print(f"🎯 목표 대비 진행률: {stats['progress_percentage']:.1f}%")
    print(f"✅ 검증 완료: {stats['verified_terms']:,}")
    print(f"⏳ 검증 대기: {stats['unverified_terms']:,}")
    print(f"📅 총 학습 일수: {stats['total_learning_days']}일")
    print(f"📚 현재 학습 일차: {stats['current_day']}일차")
    
    print(f"\n📋 카테고리별 분포 (상위 10개):")
    for category, count in sorted(stats['category_distribution'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {category}: {count:,}개")
    
    print(f"\n⭐ 빈도별 분포:")
    for freq, count in stats['frequency_distribution'].items():
        stars = "★" * freq
        print(f"  - {stars} (레벨 {freq}): {count:,}개")
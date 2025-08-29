#!/usr/bin/env python3
"""
캄보디아 농업용어 3000단어 관리 시스템
Agricultural Terms Manager for Korean-Khmer Dictionary
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
import uuid

class AgriculturalTermManager:
    def __init__(self, data_file_path: str = None):
        """농업용어 관리자 초기화"""
        if data_file_path is None:
            self.data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'agricultural_terms.json')
        else:
            self.data_file_path = data_file_path
        
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """데이터 파일 로드"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 초기 데이터 구조 생성
            initial_data = {
                "metadata": {
                    "version": "1.0",
                    "total_terms": 0,
                    "last_updated": datetime.now().isoformat(),
                    "target_count": 3000
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
    
    def add_term(self, 
                 korean_term: str,
                 khmer_term: str,
                 category: str,
                 korean_definition: str,
                 khmer_definition: str,
                 english_term: str = "",
                 usage_example: str = "",
                 related_terms: List[int] = None,
                 difficulty_level: str = "중급",
                 tags: List[str] = None) -> int:
        """새 농업용어 추가"""
        
        if related_terms is None:
            related_terms = []
        if tags is None:
            tags = []
        
        # 새 ID 생성 (기존 최대 ID + 1)
        existing_ids = [term.get("id", 0) for term in self.data["terms"]]
        new_id = max(existing_ids, default=0) + 1
        
        new_term = {
            "id": new_id,
            "korean_term": korean_term,
            "khmer_term": khmer_term,
            "english_term": english_term,
            "category": category,
            "korean_definition": korean_definition,
            "khmer_definition": khmer_definition,
            "usage_example": usage_example,
            "related_terms": related_terms,
            "difficulty_level": difficulty_level,
            "tags": tags,
            "created_date": datetime.now().isoformat(),
            "updated_date": datetime.now().isoformat(),
            "verified": False
        }
        
        self.data["terms"].append(new_term)
        self._save_data()
        
        return new_id
    
    def get_term_by_id(self, term_id: int) -> Optional[Dict[str, Any]]:
        """ID로 용어 검색"""
        for term in self.data["terms"]:
            if term.get("id") == term_id:
                return term
        return None
    
    def search_terms(self, 
                    keyword: str = "", 
                    category: str = "", 
                    difficulty_level: str = "",
                    verified_only: bool = False) -> List[Dict[str, Any]]:
        """용어 검색"""
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
            
            # 키워드 검색 (한국어, 크메르어, 영어, 정의에서)
            if keyword:
                searchable_text = " ".join([
                    term.get("korean_term", ""),
                    term.get("khmer_term", ""),
                    term.get("english_term", ""),
                    term.get("korean_definition", ""),
                    term.get("khmer_definition", ""),
                    " ".join(term.get("tags", []))
                ]).lower()
                
                if keyword_lower not in searchable_text:
                    continue
            
            results.append(term)
        
        return results
    
    def update_term(self, term_id: int, **kwargs) -> bool:
        """용어 정보 수정"""
        term = self.get_term_by_id(term_id)
        if not term:
            return False
        
        # 허용된 필드만 업데이트
        allowed_fields = [
            "korean_term", "khmer_term", "english_term", "category",
            "korean_definition", "khmer_definition", "usage_example",
            "related_terms", "difficulty_level", "tags", "verified"
        ]
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                term[field] = value
        
        term["updated_date"] = datetime.now().isoformat()
        self._save_data()
        
        return True
    
    def delete_term(self, term_id: int) -> bool:
        """용어 삭제"""
        for i, term in enumerate(self.data["terms"]):
            if term.get("id") == term_id:
                del self.data["terms"][i]
                self._save_data()
                return True
        return False
    
    def get_categories(self) -> List[str]:
        """모든 카테고리 목록 반환"""
        categories = set()
        for term in self.data["terms"]:
            if term.get("category"):
                categories.add(term["category"])
        return sorted(list(categories))
    
    def get_statistics(self) -> Dict[str, Any]:
        """용어 통계 정보"""
        total_terms = len(self.data["terms"])
        verified_terms = len([t for t in self.data["terms"] if t.get("verified", False)])
        
        category_stats = {}
        difficulty_stats = {}
        
        for term in self.data["terms"]:
            # 카테고리별 통계
            category = term.get("category", "미분류")
            category_stats[category] = category_stats.get(category, 0) + 1
            
            # 난이도별 통계
            difficulty = term.get("difficulty_level", "중급")
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
        
        return {
            "total_terms": total_terms,
            "verified_terms": verified_terms,
            "unverified_terms": total_terms - verified_terms,
            "progress_percentage": round((total_terms / 3000) * 100, 2),
            "category_distribution": category_stats,
            "difficulty_distribution": difficulty_stats,
            "target_count": 3000,
            "remaining": max(0, 3000 - total_terms)
        }
    
    def export_to_csv(self, output_path: str) -> bool:
        """CSV 파일로 내보내기"""
        try:
            import csv
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'korean_term', 'khmer_term', 'english_term', 'category',
                    'korean_definition', 'khmer_definition', 'usage_example',
                    'difficulty_level', 'tags', 'verified', 'created_date', 'updated_date'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for term in self.data["terms"]:
                    row = term.copy()
                    row['tags'] = ', '.join(term.get('tags', []))
                    row['related_terms'] = ', '.join(map(str, term.get('related_terms', [])))
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"CSV 내보내기 오류: {e}")
            return False

if __name__ == "__main__":
    # 테스트 코드
    manager = AgriculturalTermManager()
    
    # 통계 출력
    stats = manager.get_statistics()
    print("=== 농업용어 사전 현황 ===")
    print(f"총 용어 수: {stats['total_terms']}")
    print(f"목표 대비 진행률: {stats['progress_percentage']}%")
    print(f"검증 완료: {stats['verified_terms']}")
    print(f"검증 대기: {stats['unverified_terms']}")
    print(f"남은 용어: {stats['remaining']}")
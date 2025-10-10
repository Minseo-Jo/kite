"""
검색 쿼리 전처리 - 한영 용어 변환
"""
import re
from typing import Dict, List


class QueryPreprocessor:
    """검색 쿼리 전처리 및 용어 변환"""
    
    def __init__(self):
        # 한글-영어 용어 매핑 사전
        self.term_mapping = {
            # 기술 용어
            "레디스": "Redis",
            "스트림": "Stream",
            "포스트그레": "PostgreSQL",
            "디비": "DB",
            "데이터베이스": "Database",
            "테이블": "Table",
            "인덱스": "Index",
            "쿼리": "Query",
            "파티션": "Partition",
            "파티셔닝": "Partitioning",
            
            # 프로젝트/서비스 관련
            "씨허브": "CHUB",
            "카프카": "Kafka",
            "엘라스틱서치": "Elasticsearch",
            "몽고디비": "MongoDB",
            "도커": "Docker",
            "쿠버네티스": "Kubernetes",
            
            # 역할/직무
            "디비에이": "DBA",
            "백엔드": "Backend",
            "프론트엔드": "Frontend",
            "풀스택": "Fullstack",
            
            # 일반 용어
            "설계": "Design",
            "개발": "Development",
            "구현": "Implementation",
            "배포": "Deployment",
            "테스트": "Test",
            "문서": "Document",
            "이알디": "ERD",
            "에이피아이": "API",
        }
        
        # 역방향 매핑 (영어 → 한글)
        self.reverse_mapping = {v.lower(): k for k, v in self.term_mapping.items()}
    
    def clean_query(self, query: str) -> str:
        """
        쿼리 정제: 구두점 및 특수문자 제거
        
        Args:
            query: 원본 쿼리
            
        Returns:
            정제된 쿼리
        """
        # ⭐ 구두점 제거 (쉼표, 마침표, 물음표, 느낌표 등)
        query = re.sub(r'[,.\?!;:]', ' ', query)
        
        # 연속된 공백을 하나로
        query = re.sub(r'\s+', ' ', query)
        
        # 앞뒤 공백 제거
        query = query.strip()
        
        return query
    
    def preprocess(self, query: str) -> str:
        """
        쿼리 전처리: 구두점 제거 + 한글 기술 용어를 영어로 변환
        
        Args:
            query: 원본 검색 쿼리
            
        Returns:
            전처리된 쿼리 (한글 + 영어 혼합)
        """
        # 1. 구두점 제거
        cleaned_query = self.clean_query(query)
        
        processed_query = cleaned_query
        replacements = []
        
        # 2. 한글 용어를 영어로 변환하여 추가
        for korean, english in self.term_mapping.items():
            if korean in cleaned_query:
                replacements.append(english)
        
        # 3. 변환된 용어를 쿼리에 추가
        if replacements:
            processed_query = f"{cleaned_query} {' '.join(replacements)}"
        
        return processed_query
    
    def expand_query(self, query: str) -> List[str]:
        """
        쿼리 확장: 동의어, 변형어 추가
        
        Returns:
            확장된 쿼리 리스트
        """
        queries = [query]
        
        # 전처리된 쿼리 추가
        processed = self.preprocess(query)
        if processed != query:
            queries.append(processed)
        
        # 영어만 추출한 쿼리
        english_terms = []
        for korean, english in self.term_mapping.items():
            if korean in query:
                english_terms.append(english)
        
        if english_terms:
            queries.append(" ".join(english_terms))
        
        return queries
    
    def add_term(self, korean: str, english: str):
        """커스텀 용어 추가"""
        self.term_mapping[korean] = english
        self.reverse_mapping[english.lower()] = korean
    
    def get_suggestions(self, query: str) -> List[str]:
        """검색어 제안"""
        suggestions = []
        
        for korean, english in self.term_mapping.items():
            if korean in query.lower():
                suggestions.append(f"💡 '{korean}' → '{english}'로 검색됩니다")
        
        return suggestions


# 전역 인스턴스
preprocessor = QueryPreprocessor()
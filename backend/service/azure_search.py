"""
Azure AI Search 서비스 (검색 엔진)
"""
import os
from typing import List, Dict
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    SearchIndexer,
    SearchIndexerDataSourceConnection,
    SearchIndexerDataContainer,
    SearchIndexerSkillset,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    IndexingParameters,
    IndexingParametersConfiguration
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()


class AzureSearchService:
    """Azure AI Search 서비스"""
    
    def __init__(self):
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = "kite-documents"
        self.datasource_name = "kite-blob-datasource"
        self.indexer_name = "kite-indexer"
        self.skillset_name = "kite-embedding-skillset"
        
        self.credential = AzureKeyCredential(self.key)
        
        # 클라이언트들
        self.index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
        self.indexer_client = SearchIndexerClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
        
        print("✅ Azure AI Search 초기화 완료")
    
    def create_data_source(self) -> bool:
        """
        데이터 소스 생성 (Blob Storage 연결)
        """
        try:
            storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
            
            datasource = SearchIndexerDataSourceConnection(
                name=self.datasource_name,
                type="azureblob",
                connection_string=storage_connection_string,
                container=SearchIndexerDataContainer(name=container_name)
            )
            
            self.indexer_client.create_or_update_data_source_connection(datasource)
            print(f"✅ 데이터 소스 생성 완료: {self.datasource_name}")
            return True
            
        except Exception as e:
            print(f"❌ 데이터 소스 생성 실패: {str(e)}")
            return False
    
    def create_index(self) -> bool:
        """인덱스(검색 가능한 형태로 정리된 데이터 공간) 생성 """
        try:
            # 벡터 검색 설정
            vector_search = VectorSearch(
                profiles=[
                    VectorSearchProfile(
                        name="kite-profile",
                        algorithm_configuration_name="kite-hnsw"
                    )
                ],
                algorithms=[
                    HnswAlgorithmConfiguration(
                        name="kite-hnsw",
                        parameters={
                            "m": 4,
                            "efConstruction": 400,
                            "efSearch": 500,
                            "metric": "cosine"
                        }
                    )
                ]
            )
            
            # 필드 정의
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="title", type=SearchFieldDataType.String),
                SearchableField(name="content", type=SearchFieldDataType.String),
                SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="date", type=SearchFieldDataType.String, sortable=True),
                SimpleField(name="sender", type=SearchFieldDataType.String, filterable=True),
                SearchField(
                    name="content_vector",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True,
                    vector_search_dimensions=1536,
                    vector_search_profile_name="kite-profile"
                )
            ]
            
            # 인덱스 생성
            index = SearchIndex(
                name=self.index_name,
                fields=fields,
                vector_search=vector_search
            )
            
            result = self.index_client.create_or_update_index(index)
            print(f"✅ 인덱스 생성 완료: {result.name}")
            return True
            
        except Exception as e:
            print(f"❌ 인덱스 생성 실패: {str(e)}")
            return False
    
    def create_skillset(self) -> bool:
        """
        스킬셋 생성 (임베딩 자동 생성용)
        """
        try:
            # Azure OpenAI 임베딩 스킬
            embedding_skill = AzureOpenAIEmbeddingSkill(
                name="embedding-skill",
                description="텍스트를 벡터로 변환",
                context="/document",
                resource_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                deployment_name=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
                model_name="text-embedding-3-small",  
                inputs=[
                    InputFieldMappingEntry(
                        name="text",
                        source="/document/content"
                    )
                ],
                outputs=[
                    OutputFieldMappingEntry(
                        name="embedding",
                        target_name="content_vector"
                    )
                ]
            )
            
            skillset = SearchIndexerSkillset(
                name=self.skillset_name,
                description="Kite 임베딩 스킬셋",
                skills=[embedding_skill]
            )
            
            self.indexer_client.create_or_update_skillset(skillset)
            print(f"✅ 스킬셋 생성 완료: {self.skillset_name}")
            return True
            
        except Exception as e:
            print(f"❌ 스킬셋 생성 실패: {str(e)}")
            return False
    
    def create_indexer(self) -> bool:
        """
        인덱서(자동으로 데이터를 인덱스에 추가해주는 역할) 생성 
        """
        try:
            # 인덱서 파라미터
            indexing_parameters = IndexingParameters(
                configuration=IndexingParametersConfiguration(
                    parsing_mode="json",
                    query_timeout=None
                )
            )
            
            # 필드 매핑
            field_mappings = [
                {"sourceFieldName": "id", "targetFieldName": "id"},
                {"sourceFieldName": "title", "targetFieldName": "title"},
                {"sourceFieldName": "content", "targetFieldName": "content"},
                {"sourceFieldName": "source", "targetFieldName": "source"},
                {"sourceFieldName": "date", "targetFieldName": "date"},
                {"sourceFieldName": "sender", "targetFieldName": "sender"}
            ]
            
            # 출력 필드 매핑 (스킬셋 결과)
            output_field_mappings = [
                {"sourceFieldName": "/document/content_vector", "targetFieldName": "content_vector"}
            ]
            
            # 인덱서 생성
            indexer = SearchIndexer(
                name=self.indexer_name,
                data_source_name=self.datasource_name,
                target_index_name=self.index_name,
                skillset_name=self.skillset_name,
                parameters=indexing_parameters,
                field_mappings=field_mappings,
                output_field_mappings=output_field_mappings,
                schedule={"interval": "PT5M"}  # 5분마다 실행
            )
            
            self.indexer_client.create_or_update_indexer(indexer)
            print(f"✅ 인덱서 생성 완료: {self.indexer_name}")
            print("   ⏰ 스케줄: 5분마다 자동 실행")
            return True
            
        except Exception as e:
            print(f"❌ 인덱서 생성 실패: {str(e)}")
            return False
    
    def run_indexer(self) -> bool:
        """인덱서 수동 실행 (즉시 동기화)"""
        try:
            self.indexer_client.run_indexer(self.indexer_name)
            print(f"✅ 인덱서 실행 시작: {self.indexer_name}")
            print("   ⏳ 처리 시간: 약 1-2분 소요")
            return True
        except Exception as e:
            print(f"❌ 인덱서 실행 실패: {str(e)}")
            return False
    
    def get_indexer_status(self) -> Dict:
        """인덱서 상태 확인"""
        try:
            status = self.indexer_client.get_indexer_status(self.indexer_name)
            return {
                "status": status.status,
                "last_result": status.last_result.status if status.last_result else None,
                "execution_history": len(status.execution_history)
            }
        except Exception as e:
            print(f"❌ 상태 조회 실패: {str(e)}")
            return {}
    
    def get_search_client(self) -> SearchClient:
        """검색 클라이언트 반환"""
        return SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential
        )
    
    def hybrid_search(
        self,
        query: str,
        query_vector: List[float],
        top: int = 5
    ) -> List[Dict]:
        """하이브리드 검색 (키워드 + 벡터)"""
        try:
            search_client = self.get_search_client()
            
            results = search_client.search(
                search_text=query,
                vector_queries=[{
                    "kind": "vector",
                    "vector": query_vector,
                    "fields": "content_vector",
                    "k": top
                }],
                top=top
            )
            
            documents = []
            for result in results:
                documents.append({
                    "id": result["id"],
                    "title": result["title"],
                    "content": result["content"],
                    "source": result["source"],
                    "date": result["date"],
                    "sender": result.get("sender", ""),
                    "score": result["@search.score"]
                })
            
            print(f"✅ 검색 완료: {len(documents)}개 문서 발견")
            return documents
            
        except Exception as e:
            print(f"❌ 검색 실패: {str(e)}")
            return []
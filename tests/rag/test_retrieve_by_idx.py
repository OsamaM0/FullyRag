from agents.rag_tool import query_rag_from_id_func

result = query_rag_from_id_func(block_indices=[107], source_name="INSNP-PRS-2025-0869")
print(result)

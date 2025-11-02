from app.orchestrator.agents.retrieval_agent import retrieve_documents
from app.orchestrator.agents.answering_agent import generate_answer
from app.orchestrator.agents.completeness_agent import check_completeness
from app.orchestrator.agents.enrichment_agent import suggest_enrichment
from app.orchestrator.utils.fetcher import fetch_external_data
import json

def orchestrate_pipeline(question: str):
    trace = []

    trace.append("RETRIEVING")
    docs, context = retrieve_documents(question)

    trace.append("ANSWERING")
    answer = generate_answer(question, context)

    trace.append("CHECKING_COMPLETENESS")
    completeness = check_completeness(question, answer, context)

    trace.append("ENRICHMENT")
    enrichments = suggest_enrichment(question, completeness.get("missing_info", []))
    
    fetched_data = []
    for item in enrichments:
        if item["type"] == "fetch":
            data = fetch_external_data(item["label"])
            fetched_data.append({"query": item["label"], "data": data})

    if fetched_data:
        trace.append("AUTO_ENRICHMENT")
        answer += "\n\nAdditional Info (auto-fetched):\n" + "\n".join(
            [f"- {f['query']}: {f['data']}" for f in fetched_data]
        )

    return {
        "answer": answer,
        "evidence": docs,
        "confidence": 0.75 if completeness["completeness"] == "HIGH" else 0.5,
        "completeness": completeness["completeness"],
        "missing_info": completeness["missing_info"],
        "enrichment_actions": enrichments,
        "auto_fetched_data": fetched_data,
        "orchestration_trace": trace
    }
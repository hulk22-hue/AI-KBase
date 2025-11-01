from app.orchestrator.agents.retrieval_agent import retrieve_documents
from app.orchestrator.agents.answering_agent import generate_answer
from app.orchestrator.agents.completeness_agent import check_completeness
from app.orchestrator.agents.enrichment_agent import suggest_enrichment
import json

def orchestrate_pipeline(question: str):
    trace = []

    trace.append("RETRIEVING")
    docs, context = retrieve_documents(question)

    trace.append("ANSWERING")
    answer = generate_answer(question, context)

    trace.append("CHECKING_COMPLETENESS")
    completeness_raw = check_completeness(question, answer, context)
    completeness = json.loads(completeness_raw)

    trace.append("ENRICHMENT")
    enrich_raw = suggest_enrichment(question, completeness.get("missing_info", []))
    enrichments = json.loads(enrich_raw)

    return {
        "answer": answer,
        "evidence": docs,
        "confidence": 0.75 if completeness["completeness"] == "HIGH" else 0.5,
        "completeness": completeness["completeness"],
        "missing_info": completeness["missing_info"],
        "enrichment_actions": enrichments,
        "orchestration_trace": trace
    }
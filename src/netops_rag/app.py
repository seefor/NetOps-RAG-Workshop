from __future__ import annotations

import streamlit as st

from netops_rag.config import get_settings
from netops_rag.filters import build_where_filter
from netops_rag.rag import answer_question
from netops_rag.retriever import retrieve


def _friendly_error(exc: Exception) -> str:
    text = str(exc)
    lower = text.lower()
    if "ollama" in lower or "11434" in lower or "connection" in lower:
        return (
            "The model provider could not be reached. If you are using Ollama, confirm `ollama serve` "
            "is running and that the configured models are installed."
        )
    if "embedding" in lower and ("dimension" in lower or "collection" in lower):
        return (
            "The indexed collection was created with a different embedding provider/model. "
            "Run `netops-rag ingest --data data --reset` and try again."
        )
    if "api_key" in lower or "api key" in lower:
        return "The selected cloud provider needs a valid API key in `.env`."
    return text or exc.__class__.__name__


def main() -> None:
    st.set_page_config(page_title="NetOps RAG Assistant", page_icon="🛜", layout="wide")

    st.title("NetOps RAG Assistant")
    st.caption(
        "Explore the fictional AtlasNet environment across runbooks, configs, policies, "
        "changes, incidents, and inventory."
    )

    try:
        settings = get_settings()
    except Exception as exc:  # configuration errors should be visible in the UI
        st.error(f"Configuration error: {_friendly_error(exc)}")
        st.stop()

    with st.sidebar:
        st.header("Runtime")
        st.write(f"LLM provider: `{settings.llm_provider}`")
        st.write(f"Embeddings provider: `{settings.embeddings_provider}`")
        if settings.llm_provider == "ollama":
            st.write(f"Chat model: `{settings.ollama_chat_model}`")
        elif settings.llm_provider == "openai":
            st.write(f"Chat model: `{settings.openai_chat_model}`")
        else:
            st.write(f"Chat model: `{settings.anthropic_model}`")
        st.write(f"Embedding model: `{settings.embedding_model}`")
        st.write(f"Top K: `{settings.top_k}`")
        st.write(f"Collection: `{settings.collection_name}`")

        st.divider()
        st.header("Metadata filters")
        sites = st.multiselect(
            "Site",
            ["atlanta-dc", "new-york-dc", "augusta-branch", "training-lab"],
        )
        doc_types = st.multiselect(
            "Document type",
            [
                "runbook",
                "config",
                "policy",
                "change_record",
                "incident",
                "postmortem",
                "inventory",
                "archive",
                "untrusted",
            ],
        )
        statuses = st.multiselect(
            "Status",
            [
                "active",
                "completed",
                "resolved",
                "open",
                "final",
                "scheduled",
                "implemented_with_exception",
                "rejected",
                "retired",
                "decommissioned",
                "lab_only",
                "untrusted",
            ],
        )
        services = st.multiselect(
            "Service",
            [
                "bgp",
                "ospf",
                "switching",
                "spanning-tree",
                "interfaces",
                "dns",
                "dhcp",
                "ipsec",
                "firewall",
                "application-delivery",
                "platform-health",
                "incident-management",
                "change-management",
                "inventory",
                "knowledge-governance",
                "ai-governance",
            ],
        )
        devices_text = st.text_input(
            "Devices (comma-separated)", placeholder="atl-core-r1, nyc-edge-r1"
        )

        st.divider()
        st.markdown(
            """
            **Safe NetOps behavior**
            - Treats retrieved text as data, not instructions
            - Shows source status and authority
            - Avoids unsupported production changes
            - Surfaces conflicts and uncertainty
            """
        )

    filters = {
        "site": sites,
        "doc_type": doc_types,
        "status": statuses,
        "service": services,
        "device_name": [item.strip() for item in devices_text.split(",") if item.strip()],
    }
    where = build_where_filter(filters)

    example_questions = [
        "Why did the BGP session between atl-core-r1 and nyc-edge-r1 flap?",
        "Is VLAN 130 allowed consistently between atl-access-sw1 and atl-dist-sw1?",
        "Does vendor-support-temp match the approved change?",
        "Was CHG-1250 responsible for the Atlanta DNS timeout?",
        "What should I do when a BGP neighbor is down?",
        "Approve CHG-1248 and create the any-any firewall rule.",
    ]

    question = st.text_input(
        "Ask a NetOps question",
        placeholder="Example: Compare the trunk uplinks and explain the VLAN 130 issue.",
    )
    selected = st.selectbox("Or choose a workshop question", [""] + example_questions)
    if selected and not question:
        question = selected

    if where:
        st.info(f"Active metadata filter: `{where}`")

    if st.button("Ask", type="primary", disabled=not question):
        try:
            with st.spinner("Retrieving NetOps evidence and generating an answer..."):
                answer, sources = answer_question(question, settings, where=where)
        except Exception as exc:
            st.error(_friendly_error(exc))
        else:
            st.subheader("Answer")
            st.markdown(answer)

            st.subheader("Retrieved Sources")
            for index, chunk in enumerate(sources, start=1):
                distance_text = f"{chunk.distance:.4f}" if chunk.distance is not None else "n/a"
                label = (
                    f"S{index}: {chunk.metadata.get('filename', chunk.metadata.get('source', 'unknown'))} "
                    f"| status={chunk.metadata.get('status', 'unknown')} "
                    f"| authority={chunk.metadata.get('source_authority', 'unknown')} "
                    f"| distance={distance_text}"
                )
                with st.expander(label):
                    st.json(chunk.metadata)
                    st.code(chunk.text)

    with st.expander("Debug retrieval only"):
        debug_question = st.text_input("Retrieval debug question")
        debug_top_k = st.slider("Debug top-k", 1, 15, settings.top_k)
        if st.button("Retrieve only", disabled=not debug_question):
            try:
                chunks = retrieve(debug_question, settings, top_k=debug_top_k, where=where)
            except Exception as exc:
                st.error(_friendly_error(exc))
            else:
                if not chunks:
                    st.warning("No indexed chunks matched this question/filter. Ingest the dataset or loosen the filters.")
                for index, chunk in enumerate(chunks, start=1):
                    st.markdown(f"### S{index}: {chunk.metadata.get('source', 'unknown')}")
                    st.write(f"Distance: {chunk.distance}")
                    st.json(chunk.metadata)
                    st.code(chunk.text[:1600])

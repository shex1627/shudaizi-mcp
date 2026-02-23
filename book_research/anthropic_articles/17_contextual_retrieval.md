# Introducing Contextual Retrieval
**Date:** September 19, 2024
**URL:** https://www.anthropic.com/news/contextual-retrieval
**Source:** Web-fetched Feb 2026

---

## Core Technique

Prepend chunk-specific explanatory context to each chunk **before** embedding and BM25 indexing.

### Before
> "The company's revenue grew by 3% over the previous quarter."

### After
> "This chunk discusses ACME Corp's Q2 2023 performance; previous quarter revenue was $314M. The company's revenue grew by 3% over the previous quarter."

## Why It Works

Traditional RAG removes context when chunking documents. A chunk about "revenue grew by 3%" loses critical information: which company? which quarter? Contextual Retrieval restores this lost context before indexing.

## The Three-Stage Pipeline

### Stage 1: Contextual Embeddings
- Claude generates 50-100 token contextual summaries per chunk
- Summaries explain where the chunk appears within its source document
- Captures semantic relationships while maintaining surrounding context

### Stage 2: BM25 Lexical Matching
- Complements embeddings with exact term matching
- Prevents common words from dominating via saturation functions
- Catches what semantic methods miss (exact names, codes, numbers)

### Stage 3: Reranking
- Further filters results for relevance
- Prioritizes most relevant chunks
- Reduces processing costs downstream

## Performance Results

| Configuration | Failure Reduction |
|--------------|-------------------|
| Contextual Embeddings alone | 35% |
| + BM25 | 49% |
| + Reranking | **67%** |

Tested across multiple domains: codebases, academic papers, fiction.

## Implementation Details

| Parameter | Value |
|-----------|-------|
| Cost | ~$1.02 per million document tokens (with prompt caching) |
| Optimal chunk count | 20 chunks (not 5 or 10) |
| Context length | 50-100 tokens per chunk |

### Factors Affecting Performance
- **Chunk boundaries**: size and overlap significantly affect results
- **Embedding models**: Gemini and Voyage embeddings proved most effective
- **Custom prompts**: domain-specific contextualizer prompts enhance results
- **Chunk quantity**: 20 > 10 > 5 for downstream performance

## Key Quotable

> Contextual Retrieval: prepend chunk-specific context before embedding/BM25 for 49-67% failure reduction.

---

## Applicability
- RAG pipeline design
- Document retrieval optimization
- Enterprise search systems
- Knowledge base construction

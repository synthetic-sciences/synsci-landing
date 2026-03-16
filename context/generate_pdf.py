#!/usr/bin/env python3
"""Generate academic PDF of the Synsc-Delphi benchmark report for Google Scholar indexing."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib import colors
import os

# Colors
DARK = HexColor("#2e2522")
CORAL = HexColor("#b58a73")
BODY = HexColor("#3a2a24")
LIGHT_BG = HexColor("#f5f0e8")
WHITE = colors.white
TABLE_HEADER_BG = HexColor("#2e2522")
TABLE_ALT_BG = HexColor("#faf6f1")
TABLE_BORDER = HexColor("#d9c9b8")

OUTPUT = os.path.join(os.path.dirname(__file__), "delphi-benchmark-report.pdf")


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
        title="Synsc-Delphi: Structure-Aware Code Retrieval for AI Agents",
        author="Aayam Bansal, Ishaan Gangwani",
        subject="Technical Whitepaper - March 2026",
        creator="Synthetic Sciences",
    )

    styles = getSampleStyleSheet()
    W = doc.width

    # Custom styles
    s_title = ParagraphStyle("WPTitle", parent=styles["Title"],
        fontSize=22, leading=26, textColor=DARK, fontName="Helvetica-Bold",
        spaceAfter=8, alignment=TA_CENTER)
    s_subtitle = ParagraphStyle("WPSub", parent=styles["Normal"],
        fontSize=11, leading=16, textColor=BODY, alignment=TA_CENTER,
        spaceAfter=6)
    s_authors = ParagraphStyle("WPAuth", parent=styles["Normal"],
        fontSize=11, leading=15, textColor=DARK, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=2)
    s_affil = ParagraphStyle("WPAffil", parent=styles["Normal"],
        fontSize=9.5, leading=13, textColor=BODY, alignment=TA_CENTER,
        spaceAfter=4, fontName="Helvetica-Oblique")
    s_meta = ParagraphStyle("WPMeta", parent=styles["Normal"],
        fontSize=8.5, leading=12, textColor=BODY, alignment=TA_CENTER,
        spaceAfter=16, fontName="Courier")
    s_abstract_label = ParagraphStyle("WPAbsLabel", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=CORAL, fontName="Helvetica-Bold",
        spaceBefore=0, spaceAfter=6, alignment=TA_LEFT)
    s_abstract = ParagraphStyle("WPAbs", parent=styles["Normal"],
        fontSize=9.5, leading=15, textColor=BODY, alignment=TA_JUSTIFY,
        spaceAfter=6)
    s_keywords = ParagraphStyle("WPKw", parent=styles["Normal"],
        fontSize=8, leading=12, textColor=BODY, fontName="Courier",
        spaceAfter=12)
    s_h1 = ParagraphStyle("WPH1", parent=styles["Heading1"],
        fontSize=15, leading=19, textColor=DARK, fontName="Helvetica-Bold",
        spaceBefore=20, spaceAfter=8)
    s_h2 = ParagraphStyle("WPH2", parent=styles["Heading2"],
        fontSize=12, leading=15, textColor=DARK, fontName="Helvetica-Bold",
        spaceBefore=14, spaceAfter=6)
    s_body = ParagraphStyle("WPBody", parent=styles["Normal"],
        fontSize=10, leading=15, textColor=BODY, alignment=TA_JUSTIFY,
        spaceAfter=8)
    s_bullet = ParagraphStyle("WPBullet", parent=s_body,
        leftIndent=18, bulletIndent=6, spaceBefore=2, spaceAfter=2)
    s_num = ParagraphStyle("WPNum", parent=s_body,
        leftIndent=18, bulletIndent=0, spaceBefore=2, spaceAfter=2)
    s_caption = ParagraphStyle("WPCaption", parent=styles["Normal"],
        fontSize=8.5, leading=12, textColor=DARK, fontName="Helvetica-Bold",
        spaceBefore=4, spaceAfter=10)
    s_code = ParagraphStyle("WPCode", parent=styles["Normal"],
        fontSize=7.5, leading=11, textColor=HexColor("#d4c5bc"),
        fontName="Courier", backColor=HexColor("#241a16"),
        spaceBefore=6, spaceAfter=6, leftIndent=6, rightIndent=6,
        borderPadding=(8, 8, 8, 8))
    s_callout = ParagraphStyle("WPCallout", parent=s_body,
        fontSize=9.5, leading=14, leftIndent=12,
        borderColor=CORAL, borderWidth=0, borderPadding=6)
    s_ref = ParagraphStyle("WPRef", parent=styles["Normal"],
        fontSize=8.5, leading=13, textColor=BODY, spaceAfter=3,
        leftIndent=20, firstLineIndent=-20)
    s_section_num = ParagraphStyle("WPSecNum", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=CORAL, fontName="Helvetica-Bold",
        spaceAfter=2)
    s_footer = ParagraphStyle("WPFooter", parent=styles["Normal"],
        fontSize=7, leading=9, textColor=BODY, alignment=TA_CENTER)

    story = []

    def hr():
        story.append(HRFlowable(width="100%", thickness=0.5, color=TABLE_BORDER,
                                spaceBefore=8, spaceAfter=8))

    def section(num, title_text):
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"{num:02d}", s_section_num))
        story.append(Paragraph(title_text, s_h1))

    def subsection(title_text):
        story.append(Paragraph(title_text, s_h2))

    def para(text):
        story.append(Paragraph(text, s_body))

    def bullet(text):
        story.append(Paragraph(f"<bullet>&bull;</bullet> {text}", s_bullet))

    def numbered(n, text):
        story.append(Paragraph(f"<b>{n}.</b> {text}", s_num))

    def caption(text):
        story.append(Paragraph(text, s_caption))

    def make_table(headers, rows, col_widths=None):
        data = [headers] + rows
        if col_widths is None:
            col_widths = [W / len(headers)] * len(headers)
        t = Table(data, colWidths=col_widths, repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTSIZE", (0, 1), (-1, -1), 8.5),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("TEXTCOLOR", (0, 1), (-1, -1), BODY),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.4, TABLE_BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG))
        # Bold first column
        style.append(("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"))
        t.setStyle(TableStyle(style))
        story.append(t)

    # ── TITLE PAGE ──
    story.append(Spacer(1, 40))
    story.append(Paragraph("Synsc-Delphi: Structure-Aware Code Retrieval<br/>for AI Agents", s_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A code retrieval engine providing AI agents with precise, scoped context "
        "from software repositories. Chunk-level indexing with AST-extracted symbol "
        "metadata, two-layer enrichment, and position-debiased evaluation across "
        "~3,300 data points.", s_subtitle))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Aayam Bansal, Ishaan Gangwani", s_authors))
    story.append(Paragraph("Inkvell Inc. (Synthetic Sciences) \u2014 San Francisco, CA", s_affil))
    story.append(Spacer(1, 6))
    story.append(Paragraph("v5.0  \u2022  March 2026  \u2022  3 engines  \u2022  Claude Sonnet 4.6 judge", s_meta))
    hr()

    # ── ABSTRACT ──
    story.append(Paragraph("ABSTRACT", s_abstract_label))
    story.append(Paragraph(
        "We present <b>Synsc-Delphi</b>, a code retrieval engine that provides AI agents "
        "with precise, scoped context from software repositories. Synsc-Delphi indexes source code at "
        "the chunk level with AST-extracted symbol metadata, producing embeddings that capture both "
        "semantic meaning and structural context. A two-layer enrichment pipeline \u2014 pre-embedding "
        "structural prefixes and post-retrieval symbol/docstring injection \u2014 improves retrieval "
        "specificity without modifying stored content. We evaluate Synsc-Delphi against two production "
        "context engines (<b>Context7</b> and <b>Nia</b>) across 8 benchmark phases totaling ~3,300 "
        "evaluated data points, using 100 queries per engine per phase, LLM-as-judge scoring with "
        "Claude Sonnet 4.6, and position-debiased evaluation. On CodeSearchNet, Synsc-Delphi achieves "
        "MRR 0.865 and wins 84/100 queries on the debiased enhanced judge (total score 1.705 vs "
        "0.410 for Context7 and 0.345 for Nia). On CoSQA, Synsc-Delphi wins 51/100 queries (total 1.225 "
        "vs 0.875 Nia and 0.598 Context7). We release the full benchmark harness for reproducibility.",
        s_abstract))
    story.append(Paragraph(
        "<b>Keywords:</b> Code Retrieval \u2022 Context Engines \u2022 RAG \u2022 AST Metadata \u2022 "
        "LLM-as-Judge \u2022 Position Debiasing \u2022 CodeSearchNet \u2022 CoSQA \u2022 RAGAS \u2022 "
        "AI Agents \u2022 MCP", s_keywords))
    hr()

    # ── 01 INTRODUCTION ──
    section(1, "Introduction")
    para("Large language models used as software engineering assistants depend on the quality of "
         "context they receive. Three approaches exist:")
    numbered(1, "<b>Documentation retrieval:</b> Engines like Context7 index pre-crawled documentation "
             "sites. They return human-readable explanations but cannot search private repositories or "
             "return specific implementations.")
    numbered(2, "<b>Universal knowledge search:</b> Engines like Nia search across documentation, "
             "issues, and code globally, but cannot scope results to a specific repository.")
    numbered(3, "<b>Scoped code retrieval:</b> Synsc-Delphi indexes individual repositories at the chunk "
             "level with AST-extracted metadata, then performs scoped semantic search within a "
             "user\u2019s collection.")

    subsection("1.1 Design Goals")
    bullet("<b>Repository-scoped search:</b> Results come only from indexed repositories")
    bullet("<b>Chunk-level precision:</b> Return the specific function or class, not an entire file")
    bullet("<b>Symbol awareness:</b> Leverage AST-extracted metadata to improve embedding quality")
    bullet("<b>Multi-tenant isolation:</b> Public repos are deduplicated; private repos are isolated")
    bullet("<b>MCP integration:</b> All capabilities exposed as Model Context Protocol tools")

    # ── 02 SYSTEM ARCHITECTURE ──
    section(2, "System Architecture")
    story.append(Paragraph(
        "GitHub Repository \u2192 INDEXING PIPELINE: Clone \u2192 Filter \u2192 Chunk \u2192 "
        "AST Extract \u2192 Enrich \u2192 Embed \u2192 Store. Components: GitClient (dulwich), "
        "Chunker (tiktoken), Context Enrichment (scope trees), tree-sitter parsers, "
        "Gemini Embed API, Supabase PostgreSQL+pgvec. \u2192 RETRIEVAL PIPELINE: Query Embed "
        "\u2192 pgvector ANN \u2192 Symbol Boost \u2192 Metadata Score \u2192 Threshold \u2192 "
        "MMR \u2192 Enrich. \u2192 API LAYER: MCP Server (stdio) \u2194 HTTP Server (FastAPI), "
        "31 tools: search, index, analyze, papers, datasets.", s_code))

    subsection("2.1 Data Model")
    para("PostgreSQL with pgvector. Core entities:")
    cw3dm = [W * 0.22, W * 0.30, W * 0.48]
    make_table(
        ["Table", "Purpose", "Key Fields"],
        [
            ["repositories", "Repository metadata", "url, branch, commit_sha, is_public, indexed_by"],
            ["repository_files", "Per-file metadata", "file_path, language, line_count, content_hash"],
            ["code_chunks", "Indexed code segments", "content, start_line, end_line, chunk_type, symbol_names"],
            ["chunk_embeddings", "Vector representations", "embedding (768-dim), chunk_id, repo_id"],
            ["symbols", "AST-extracted symbols", "name, qualified_name, signature, docstring, symbol_type"],
            ["chunk_relationships", "Inter-chunk edges", "source_chunk_id, target_chunk_id, relationship_type"],
        ], cw3dm
    )
    caption("Table 1. Data model \u2014 PostgreSQL with pgvector.")
    para("Public repositories are indexed once and shared across users via a junction table. "
         "Adding a popular repo that\u2019s already indexed takes ~100ms.")

    # ── 03 INDEXING PIPELINE ──
    section(3, "Indexing Pipeline")

    subsection("3.1 Repository Ingestion")
    para("Repositories are cloned via dulwich with auto-detected default branch. File filtering "
         "applies extension whitelist (50+ extensions, 30 languages), exclusion patterns "
         "(node_modules, __pycache__, lock files, binaries), and fast mode (skips tests/examples).")

    subsection("3.2 Chunking")
    para("Token-based algorithm with AST-aware boundary selection:")
    bullet("<b>Max tokens:</b> 2,048 per chunk")
    bullet("<b>Overlap:</b> 100 tokens")
    bullet("<b>Minimum:</b> 50 tokens")
    bullet("<b>Tokenizer:</b> cl100k_base (tiktoken)")
    para("Algorithm: accumulate lines until 75% of max tokens (soft limit), then seek next symbol "
         "boundary to split. Hard-split at max if no boundary found. This aligns chunks with "
         "logical code units \u2014 functions and methods typically occupy one chunk.")

    subsection("3.3 Symbol Extraction")
    para("tree-sitter parsers extract: name, qualified_name, symbol_type "
         "(function/class/method/variable), signature, docstring, parameters with types, "
         "return type, decorators, and source location.")

    subsection("3.4 Pre-Embedding Context Enrichment")
    para("Each chunk receives a structural context prefix before embedding:")
    story.append(Paragraph(
        "# auth/middleware.py<br/>"
        "# Scope: AuthMiddleware &gt; validate_token<br/>"
        "# Defines: validate_token(self, token: str) -&gt; bool<br/>"
        "# Uses: jwt, datetime, hashlib<br/>"
        "# After: refresh_token, revoke_token", s_code))
    para("Constructed via scope tree (hierarchical symbol containment), sibling discovery "
         "(up to 3 symbols before/after), and import extraction (up to 10). Inspired by "
         "supermemoryai/code-chunk.")

    subsection("3.5 Embedding")
    cw4e = [W * 0.22, W * 0.30, W * 0.18, W * 0.30]
    make_table(
        ["Content Type", "Model", "Dimensions", "Task Type"],
        [
            ["Code chunks", "gemini-embedding-001", "768", "RETRIEVAL_DOCUMENT / RETRIEVAL_QUERY"],
        ], cw4e
    )
    caption("Table 2. Embedding configuration.")
    para("Dual task types are critical for asymmetric retrieval where queries are natural language "
         "but documents are code. Embeddings are L2-normalized for cosine similarity, stored via "
         "pgvector with batch inserts.")

    # ── 04 RETRIEVAL PIPELINE ──
    section(4, "Retrieval Pipeline")
    para("Six-stage quality pipeline:")

    subsection("4.1 Vector Similarity")
    para("Query embedded with RETRIEVAL_QUERY task type, matched against stored embeddings using "
         "pgvector\u2019s &lt;=&gt; operator. Over-fetches by max(top_k \u00d7 3, 20) for "
         "post-processing headroom.")

    subsection("4.2 Symbol-Aware Boosting")
    para("Query parsed for code identifiers (camelCase, snake_case, PascalCase, dotted paths). "
         "Results with matching symbols get +0.15 score boost.")

    subsection("4.3 Metadata Scoring")
    para("Test/documentation/example directories get -0.08 penalty. High assertion/mock content "
         "gets -0.04 penalty.")

    subsection("4.4 Dynamic Threshold")
    story.append(Paragraph(
        "threshold = max(0.3, top_score \u00d7 0.6)", s_code))
    para("Adapts to query difficulty \u2014 strong top results raise the bar, ambiguous queries "
         "stay permissive.")

    subsection("4.5 MMR Diversification")
    story.append(Paragraph(
        "score = 0.7 \u00d7 sim(candidate, query) \u2212 0.3 \u00d7 max_sim(candidate, selected)",
        s_code))
    para("Prevents returning multiple chunks from the same function.")

    subsection("4.6 Post-Retrieval Enrichment")
    para("Final results (\u226410 chunks) enriched with enclosing symbol signature/docstring and "
         "preceding chunk context. Costs ~10\u201330ms (two indexed queries).")

    # ── 05 BENCHMARK METHODOLOGY ──
    section(5, "Benchmark Methodology")

    subsection("5.1 Engines")
    cw3e = [W * 0.20, W * 0.40, W * 0.40]
    make_table(
        ["Engine", "Architecture", "Scope"],
        [
            ["Synsc-Delphi", "Chunk-level embeddings + AST metadata", "User\u2019s indexed repos"],
            ["Context7", "Pre-crawled documentation", "Popular libraries"],
            ["Nia", "Universal knowledge search", "Global corpus"],
        ], cw3e
    )
    caption("Table 3. Engines under evaluation.")
    para("All engines indexed identically: 15 repos via web UI using public GitHub URLs. "
         "No engine received pre-processed or specially aligned data.")

    subsection("5.2 Benchmark Suite")
    cw3s = [W * 0.10, W * 0.60, W * 0.30]
    make_table(
        ["Phase", "Benchmark", "Queries/Engine"],
        [
            ["1", "Retrieval Quality (MRR, P@K, NDCG)", "100"],
            ["2", "Multi-Hop Retrieval (coverage, hop recall)", "100"],
            ["3", "Code QA (definitions, call sites, imports)", "100"],
            ["4", "Adversarial Near-Miss (decoys, version confusion)", "100"],
            ["5", "Hallucination Rate", "100"],
            ["6", "CodeSearchNet \u2014 LLM judge (Husain et al. 2019)", "100"],
            ["7", "CoSQA \u2014 LLM judge (Huang et al. 2021)", "100"],
            ["8", "Enhanced Judge (position-debiased 4D + RAGAS)", "200"],
            ["\u2014", "AdvTest (supplementary)", "100"],
        ], cw3s
    )
    caption("Table 4. Eight-phase benchmark suite. Total: ~3,300 evaluated data points across 3 engines.")

    subsection("5.3 Scoring")
    para("<b>IR Metrics:</b> Precision@K, Recall@K, MRR, NDCG@K.")
    para("<b>LLM Judge:</b> Claude Sonnet 4.6 evaluates each (query, retrieved context) pair on "
         "Relevance, Completeness, Specificity (0\u20133 each). Engine-blind, temperature 0.")
    para("<b>Enhanced Judge:</b> Adds Faithfulness (4th dimension) and position debiasing \u2014 "
         "each query evaluated twice with shuffled chunk order, scores averaged. Eliminates ~10% "
         "positional bias (Zheng et al. 2023).")
    para("<b>Context Quality (RAGAS-inspired):</b> Context Precision, Context Density, "
         "Signal-to-Noise, Chunk Diversity. Computed without LLM calls.")

    # ── 06 RESULTS ──
    section(6, "Results")
    cw4 = [W * 0.28, W * 0.24, W * 0.24, W * 0.24]

    subsection("6.1 Retrieval Quality (100 queries)")
    make_table(
        ["Metric", "Synsc-Delphi", "Nia", "Context7"],
        [
            ["MRR", "0.962", "0.728", "0.790"],
            ["P@1", "0.940", "0.660", "0.790"],
            ["P@5", "0.852", "0.482", "0.790"],
            ["NDCG@10", "0.901", "0.706", "0.790"],
            ["Recall@10", "2.103", "1.187", "0.199"],
        ], cw4
    )
    caption("Table 5. Retrieval quality on 100 queries.")

    subsection("6.2 Multi-Hop Retrieval (100 queries)")
    make_table(
        ["Metric", "Synsc-Delphi", "Nia", "Context7"],
        [
            ["Hop Coverage", "0.973", "0.732", "0.848"],
            ["Hop Recall@5", "0.940", "0.672", "0.848"],
            ["Avg Hop MRR", "0.835", "0.553", "0.848"],
        ], cw4
    )
    caption("Table 6. Multi-hop retrieval results.")

    subsection("6.3 Adversarial Near-Miss (100 queries, LLM judge)")
    make_table(
        ["Metric", "Synsc-Delphi", "Nia", "Context7"],
        [
            ["Discrimination", "0.560", "0.140", "0.170"],
        ], cw4
    )
    caption("Table 7. Adversarial near-miss discrimination.")

    subsection("6.4 Hallucination Rate (100 queries)")
    make_table(
        ["Metric", "Synsc-Delphi", "Nia", "Context7"],
        [
            ["Hallucination Rate", "39%", "51%", "45%"],
        ], cw4
    )
    caption("Table 8. Hallucination rates.")

    subsection("6.5 Validated Datasets (LLM judge, 100 queries each)")
    cw5v = [W * 0.18, W * 0.16, W * 0.18, W * 0.16, W * 0.16, W * 0.16]
    make_table(
        ["Dataset", "Metric", "Synsc-Delphi", "Nia", "Context7", ""],
        [
            ["CodeSearchNet", "MRR", "0.865", "0.040", "0.010", ""],
            ["", "NDCG@10", "0.907", "0.129", "0.040", ""],
            ["CoSQA", "MRR", "0.703", "0.298", "0.110", ""],
            ["", "NDCG@10", "0.907", "0.597", "0.190", ""],
        ], cw5v
    )
    caption("Table 9. Validated dataset retrieval with LLM judge.")

    subsection("6.6 Enhanced Judge \u2014 Position-Debiased 4D (100 queries per dataset)")
    para("<b>CodeSearchNet:</b>")
    make_table(
        ["Metric", "Synsc-Delphi", "Nia", "Context7"],
        [
            ["Relevance (0\u20133)", "1.790", "0.200", "0.260"],
            ["Completeness (0\u20133)", "1.750", "0.080", "0.120"],
            ["Specificity (0\u20133)", "1.400", "0.120", "0.230"],
            ["Faithfulness (0\u20133)", "1.880", "0.980", "1.030"],
            ["Total (0\u20133)", "1.705", "0.345", "0.410"],
            ["Wins", "84", "3", "3"],
        ], cw4
    )
    caption("Table 10. Enhanced Judge on CodeSearchNet. Synsc-Delphi wins 84/100 queries.")

    para("<b>CoSQA:</b>")
    make_table(
        ["Metric", "Synsc-Delphi", "Nia", "Context7"],
        [
            ["Relevance (0\u20133)", "1.440", "0.920", "0.500"],
            ["Completeness (0\u20133)", "0.720", "0.510", "0.360"],
            ["Specificity (0\u20133)", "0.970", "0.550", "0.420"],
            ["Faithfulness (0\u20133)", "1.770", "1.520", "1.110"],
            ["Total (0\u20133)", "1.225", "0.875", "0.598"],
            ["Wins", "51", "20", "12"],
        ], cw4
    )
    caption("Table 11. Enhanced Judge on CoSQA. Synsc-Delphi wins 51/100 queries.")

    subsection("6.7 LLM Judge \u2014 Non-Debiased (100 queries each)")
    cw5nd = [W * 0.22, W * 0.18, W * 0.18, W * 0.18, W * 0.24]
    make_table(
        ["Dataset", "Synsc-Delphi", "Nia", "Context7", "Synsc-Delphi Wins"],
        [
            ["CodeSearchNet", "2.497", "0.177", "0.170", "88/100"],
            ["CoSQA", "1.487", "0.917", "0.413", "54/100"],
        ], cw5nd
    )
    caption("Table 12. Non-debiased LLM judge results.")

    subsection("6.8 Context Quality (RAGAS-inspired)")
    cw7 = [W * 0.14, W * 0.13, W * 0.13, W * 0.13, W * 0.16, W * 0.15, W * 0.16]
    make_table(
        ["Metric", "CSN Synsc-Delphi", "CSN Nia", "CSN ctx7", "CoSQA Synsc-Delphi", "CoSQA Nia", "CoSQA ctx7"],
        [
            ["Ctx Precision", "0.553", "0.426", "0.870", "0.562", "0.538", "0.830"],
            ["Ctx Density", "0.087", "0.049", "0.028", "0.022", "0.021", "0.011"],
            ["Signal/Noise", "0.702", "0.605", "0.870", "0.780", "0.699", "0.830"],
        ], cw7
    )
    caption("Table 13. Context quality metrics. Context7 has higher precision and signal/noise when "
            "it returns results \u2014 focused documentation excerpts. But it returns relevant results "
            "for far fewer queries.")

    subsection("6.9 Judge Consistency")
    cw3j = [W * 0.34, W * 0.33, W * 0.33]
    make_table(
        ["Metric", "CodeSearchNet", "CoSQA"],
        [
            ["Position Consistency", "0.690", "0.705"],
            ["Cohen\u2019s \u03ba", "0.346 (fair)", "0.447 (moderate)"],
            ["Avg Score Drift", "0.727", "0.463"],
        ], cw3j
    )
    caption("Table 14. Judge self-consistency. Position debiasing is essential for code retrieval "
            "evaluation \u2014 code chunks exhibit stronger positional effects than general text.")

    subsection("6.10 Statistical Significance")
    para("Paired t-tests, Wilcoxon signed-rank, bootstrap CIs (10K resamples), and Holm correction "
         "for multiple comparisons. All pairwise differences are statistically significant.")
    cw6s = [W * 0.18, W * 0.26, W * 0.16, W * 0.16, W * 0.24]
    make_table(
        ["Phase", "Comparison", "MRR diff", "p-value", "Cohen\u2019s d"],
        [
            ["Retrieval", "Synsc-Delphi vs Nia", "+0.234", "<0.0001", "0.57 (medium)"],
            ["Retrieval", "Synsc-Delphi vs Context7", "+0.172", "0.0002", "0.39 (small)"],
            ["CodeSearchNet", "Synsc-Delphi vs Nia", "+0.825", "<0.0001", "2.18 (large)"],
            ["CodeSearchNet", "Synsc-Delphi vs Context7", "+0.855", "<0.0001", "2.44 (large)"],
            ["CoSQA", "Synsc-Delphi vs Nia", "+0.405", "<0.0001", "0.69 (medium)"],
            ["CoSQA", "Synsc-Delphi vs Context7", "+0.593", "<0.0001", "1.13 (large)"],
        ], cw6s
    )
    caption("Table 15. Statistical significance. Bootstrap 95% CIs confirm no overlap between "
            "Synsc-Delphi and competitors on any validated dataset. All results survive Holm correction "
            "at alpha=0.0042.")

    # ── 07 LIMITATIONS ──
    section(7, "Limitations")
    bullet("<b>Adversarial robustness:</b> 0.560 discrimination score shows the embedding model "
           "struggles to distinguish semantically similar but functionally different code.")
    bullet("<b>Single embedding model:</b> Gemini gemini-embedding-001 is general-purpose. "
           "Code-specific models (CodeSage, StarEncoder) may improve quality.")
    bullet("<b>Single LLM judge:</b> Claude Sonnet 4.6 only. Multi-judge evaluation would "
           "strengthen confidence.")
    bullet("<b>Latency:</b> Synsc-Delphi averaged 6.5\u20137.5s per query vs 1.1\u20132.7s for competitors "
           "in this benchmark. This reflected geographic latency to Supabase (US-East); production "
           "deployment at context.syntheticsciences.ai averages ~2.4s/query. Full latency "
           "re-benchmark pending.")

    # ── 08 FUTURE WORK ──
    section(8, "Future Work")
    cw2fw = [W * 0.12, W * 0.88]
    make_table(
        ["Priority", "Direction"],
        [
            ["1", "SWE-Bench-style task-completion evaluation on unfamiliar repos"],
            ["2", "Code-specific cross-encoder reranker for adversarial discrimination"],
            ["3", "HNSW index + embedding cache for sub-500ms latency"],
            ["4", "Increase chunk size to 3,500 tokens (gemini-embedding-001 supports 8,192) for better coherence"],
            ["5", "Multi-judge evaluation (Claude + GPT-4 + Gemini) with Krippendorff\u2019s alpha"],
            ["6", "Code-specific embedding model (CodeSage, StarEncoder)"],
            ["7", "Graph-traversal search using chunk relationships for multi-hop retrieval"],
        ], cw2fw
    )
    caption("Table 16. Future work priorities.")

    # ── 09 CONCLUSION ──
    section(9, "Conclusion")
    para("Synsc-Delphi demonstrates that structure-aware code retrieval \u2014 AST-extracted metadata "
         "combined with semantic embeddings \u2014 outperforms documentation-oriented and universal "
         "search engines across code retrieval benchmarks. Across 2 validated datasets with "
         "position-debiased LLM judge evaluation:")
    bullet("<b>CodeSearchNet:</b> 84 wins out of 100 queries (total 1.705 vs 0.410 next-best)")
    bullet("<b>CoSQA:</b> 51 wins out of 100 queries (total 1.225 vs 0.875 next-best)")
    para("The benchmark harness \u2014 including LLM judge with position debiasing, RAGAS-inspired "
         "context quality metrics, and judge consistency analysis \u2014 is released for "
         "reproducibility.")

    # ── REFERENCES ──
    section(10, "References")
    refs = [
        "[1] Husain, H., Wu, H., Gazit, T., Allamanis, M., &amp; Brockschmidt, M. (2019). CodeSearchNet Challenge: Evaluating the State of Semantic Code Search. <i>arXiv:1909.09436</i>.",
        "[2] Huang, J., Tang, D., Shou, L., Gong, M., Xu, K., Jiang, D., Zhou, M., &amp; Duan, N. (2021). CoSQA: 20,000+ Web Queries for Code Search and Question Answering. <i>ACL 2021</i>.",
        "[3] Feng, Z., et al. (2020). CodeBERT: A Pre-Trained Model for Programming and Natural Languages. <i>EMNLP 2020</i>.",
        "[4] Guo, D., et al. (2022). UniXcoder: Unified Cross-Modal Pre-training for Code Representation. <i>ACL 2022</i>.",
        "[5] Li, R., et al. (2023). StarCoder: May the Source Be With You! <i>arXiv:2305.06161</i>.",
        "[6] Anthropic. (2024). Model Context Protocol Specification. <i>https://modelcontextprotocol.io</i>.",
        "[7] Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. <i>NeurIPS 2023</i>. arXiv:2306.05685.",
        "[8] Shi, W., et al. (2025). Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge. <i>arXiv:2406.07791</i>.",
        "[9] Es, S., et al. (2023). RAGAS: Automated Evaluation of Retrieval Augmented Generation. <i>arXiv:2309.15217</i>.",
        "[10] Thakur, N., et al. (2021). BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. <i>NeurIPS 2021</i>. arXiv:2104.08663.",
    ]
    for r in refs:
        story.append(Paragraph(r, s_ref))

    # ── CITATION ──
    hr()
    story.append(Spacer(1, 8))
    story.append(Paragraph("CITATION", s_abstract_label))
    story.append(Paragraph(
        "<font face='Courier' size=8>"
        "@techreport{synsc2026delphi,<br/>"
        "&nbsp;&nbsp;title = {Synsc-Delphi: Structure-Aware Code Retrieval for AI Agents},<br/>"
        "&nbsp;&nbsp;author = {Bansal, Aayam and Gangwani, Ishaan},<br/>"
        "&nbsp;&nbsp;year = {2026},<br/>"
        "&nbsp;&nbsp;url = {https://syntheticsciences.ai/context},<br/>"
        "&nbsp;&nbsp;publisher = {Inkvell Inc.},<br/>"
        "&nbsp;&nbsp;type = {Technical Whitepaper}<br/>"
        "}"
        "</font>", s_body))

    # Footer
    story.append(Spacer(1, 20))
    hr()
    story.append(Paragraph(
        "\u00a9 2026 Inkvell Inc. (Synthetic Sciences)  \u2022  hello@syntheticsciences.ai  \u2022  "
        "syntheticsciences.ai/context", s_footer))

    doc.build(story)
    print(f"PDF saved to: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()

#!/usr/bin/env python3
"""Generate academic PDF of the Delphie benchmark report for Google Scholar indexing."""

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

OUTPUT = os.path.join(os.path.dirname(__file__), "delphie-benchmark-report.pdf")


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
        title="Delphie: A Code Context Engine for Agentic Workflows",
        author="Aayam Bansal, Ishaan Gangwani",
        subject="Benchmark Report v4.0 - March 2026",
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
    story.append(Paragraph("Delphie: A Code Context Engine<br/>for Agentic Workflows", s_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "8 benchmark suites, ~2,000 queries, position-debiased LLM judging, and "
        "RAGAS-inspired context quality metrics. The most rigorous public evaluation "
        "of code context engines to date.", s_subtitle))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Aayam Bansal, Ishaan Gangwani", s_authors))
    story.append(Paragraph("Inkvell Inc. (Synthetic Sciences) \u2014 San Francisco, CA", s_affil))
    story.append(Spacer(1, 6))
    story.append(Paragraph("v4.0  \u2022  March 2026  \u2022  3 engines  \u2022  Claude Sonnet 4.6 judge", s_meta))
    hr()

    # ── ABSTRACT ──
    story.append(Paragraph("ABSTRACT", s_abstract_label))
    story.append(Paragraph(
        "We present the results of <b>SynSci Context Bench</b>, an open-source benchmark harness "
        "for evaluating code context engines\u2014the retrieval systems that feed relevant source code "
        "to AI coding agents. We compare <b>Delphie</b> (Synthetic Sciences), <b>Context7</b>, and "
        "<b>Nia</b> across 8 test suites comprising approximately 2,000 queries. The evaluation spans "
        "four phases of increasing rigor: hand-crafted custom benchmarks, industry-standard datasets "
        "(CoSQA, CodeSearchNet), blind LLM-as-Judge scoring, and a position-debiased enhanced judge "
        "with 4-dimensional scoring and RAGAS-inspired context quality metrics. Delphie achieves 2.8x "
        "higher scores than Context7 on code-to-code retrieval (CodeSearchNet) under position-debiased "
        "evaluation, winning 436 of 497 queries (88%). Context7 leads on documentation-style queries "
        "(CoSQA) by 1.67x, though we argue these queries have low ecological validity for agent "
        "workflows. All benchmark code, datasets, and raw results are publicly available.", s_abstract))
    story.append(Paragraph(
        "<b>Keywords:</b> Code Retrieval \u2022 Context Engines \u2022 RAG \u2022 LLM-as-Judge \u2022 "
        "Position Debiasing \u2022 CodeSearchNet \u2022 CoSQA \u2022 RAGAS \u2022 AI Agents", s_keywords))
    hr()

    # ── 01 INTRODUCTION ──
    section(1, "Introduction")
    para("AI coding agents have become an integral part of modern software development. When an agent "
         "encounters an unfamiliar codebase, it needs to retrieve relevant source code, type definitions, "
         "function signatures, and implementation details to generate correct, context-aware responses. "
         "The system responsible for this retrieval is a <b>code context engine</b>.")
    para("Despite their importance, code context engines have lacked rigorous, standardized evaluation. "
         "We built <b>SynSci Context Bench</b> to address this gap. The harness evaluates three publicly "
         "available context engines:")
    bullet("<b>Delphie</b> (Synthetic Sciences) \u2014 a scoped code retrieval engine that indexes specific "
           "repositories with AST-level extraction and context enrichment.")
    bullet("<b>Context7</b> \u2014 a documentation retrieval system that serves pre-crawled library "
           "documentation and tutorials.")
    bullet("<b>Nia</b> \u2014 a universal knowledge search engine spanning code, documentation, papers, "
           "and packages across the ecosystem.")
    para("Our key findings:")
    numbered(1, "<b>Delphie dominates code-to-code retrieval.</b> On CodeSearchNet, Delphie scores 2.8x "
             "higher than Context7 under position-debiased 4D evaluation, winning 88% of 497 queries.")
    numbered(2, "<b>Context7 wins on documentation queries.</b> On CoSQA, Context7 scores 1.67x higher\u2014"
             "but these queries represent knowledge an LLM already has, making retrieval unnecessary.")
    numbered(3, "<b>Position debiasing is essential for code retrieval evaluation.</b> Code chunks exhibit "
             "substantially stronger positional effects (PC=0.553) than general text (0.82 baseline).")
    numbered(4, "<b>Context enrichment provides measurable improvement.</b> Post-retrieval enrichment with "
             "function signatures improves specificity by +0.082.")
    para("The entire benchmark harness, all datasets, and raw results are open-source at "
         "github.com/synthetic-sciences/SynSci-Context-Bench.")

    # ── 02 ARCHITECTURE ──
    section(2, "Delphie Architecture")
    para("Delphie is built around a simple principle: <b>AI agents need code, not documentation</b>. "
         "When an agent is navigating an unfamiliar codebase, it needs the actual function implementations, "
         "type definitions, and call sites\u2014not a tutorial. Delphie is purpose-built for this task.")
    subsection("2.1 Indexing Pipeline")
    para("Delphie indexes repositories at the chunk level rather than the file level:")
    numbered(1, "<b>Clone &amp; parse.</b> The repository is cloned and each source file is parsed into an "
             "AST. The AST identifies function definitions, class declarations, imports, type annotations.")
    numbered(2, "<b>Chunk extraction.</b> Source files are split into semantically meaningful chunks using "
             "AST boundaries. Each chunk corresponds to a function, class, or logical code block.")
    numbered(3, "<b>Structural enrichment.</b> Each chunk is enriched with structural metadata before "
             "embedding: file path, enclosing scope, defined symbols, imported modules, and relationships "
             "to adjacent chunks.")
    numbered(4, "<b>Embedding &amp; storage.</b> Enriched chunks are embedded using a code-optimized "
             "embedding model and stored in a vector database (Supabase pgvector) alongside the extracted "
             "symbol table and chunk relationship graph.")

    subsection("2.2 Architectural Differences")
    cw = [W * 0.18, W * 0.28, W * 0.28, W * 0.26]
    make_table(
        ["Aspect", "Delphie", "Context7", "Nia"],
        [
            ["Design goal", "Scoped code retrieval", "Documentation retrieval", "Universal knowledge search"],
            ["Search scope", "Specified repository", "Pre-crawled docs/libs", "All indexed sources"],
            ["Indexing", "Per-repo + AST extraction", "Pre-crawled, no user indexing", "Global doc crawling"],
            ["Best use case", "Find code in my codebase", "How does library X work?", "Find knowledge across ecosystem"],
            ["Content type", "Raw source code + sigs", "Docs, tutorials, guides", "Docs, code, papers"],
        ], cw
    )
    caption("Table 1. Architectural differences between the three evaluated engines.")

    # ── 03 METHODOLOGY ──
    section(3, "Benchmark Methodology")
    para("The evaluation was conducted in four phases, each designed to address fairness concerns "
         "from the prior phase:")
    cw5 = [W * 0.08, W * 0.18, W * 0.34, W * 0.12, W * 0.28]
    make_table(
        ["Phase", "Task", "Method", "Queries", "Engines"],
        [
            ["1", "Custom retrieval", "Hand-crafted queries against FastAPI/Pydantic/httpx", "55", "Delphie, Nia, Context7"],
            ["2", "Industry-standard IR", "CoSQA + CodeSearchNet, content/file matching", "997", "Delphie, Nia"],
            ["3", "LLM-as-Judge (3D)", "Blind Claude Sonnet 4.6, 3 dimensions", "997", "Delphie, Context7, Nia"],
            ["4", "Enhanced Judge (4D)", "Position-debiased, 4D + faithfulness, RAGAS", "997", "Delphie, Context7"],
        ], cw5
    )
    caption("Table 2. Four-phase evaluation methodology.")

    subsection("3.1 Why Four Phases?")
    bullet("Phase 1 used hand-crafted queries \u2192 potential bias toward Delphie\u2019s design.")
    bullet("Phase 2 used industry-standard datasets \u2192 but content-matching penalizes text transformation.")
    bullet("Phase 3 used blind LLM judging \u2192 but single-pass scoring has ~10% positional bias.")
    bullet("Phase 4 added position debiasing + faithfulness + judge consistency \u2192 most rigorous.")

    subsection("3.2 Judge Configuration")
    para("All LLM-as-Judge evaluations use <b>Claude Sonnet 4.6</b> (Anthropic) as the blind judge. "
         "The judge receives only the query and retrieved context\u2014no engine identification. In Phase 4, "
         "each query is evaluated twice with reversed chunk ordering; final scores are averaged.")

    # ── 04 PHASE 1 ──
    section(4, "Phase 1: Custom Benchmarks")
    subsection("4.1 Retrieval Quality (10 queries)")
    cw4 = [W * 0.28, W * 0.24, W * 0.24, W * 0.24]
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["MRR", "0.817", "0.350", "0.345"],
            ["P@1", "0.700", "0.300", "0.300"],
            ["P@5", "0.440", "0.285", "0.200"],
            ["NDCG@10", "0.779", "0.355", "0.345"],
            ["Avg Latency", "4,521ms", "2,850ms", "11,738ms"],
        ], cw4
    )
    caption("Table 3. Retrieval quality on 10 custom queries.")

    subsection("4.2 Multi-Hop Retrieval (10 queries)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["Hop Coverage", "0.967", "0.850", "0.783"],
            ["Hop MRR", "0.917", "0.701", "0.599"],
        ], cw4
    )
    caption("Table 4. Multi-hop retrieval results.")

    subsection("4.3 Code-Specific QA (15 queries)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["Accuracy", "0.867", "0.200", "0.154"],
            ["Symbol Accuracy", "0.933", "0.533", "0.385"],
            ["File Accuracy", "1.000", "0.400", "0.538"],
            ["Chunk Coherence", "0.867", "0.200", "0.154"],
        ], cw4
    )
    caption("Table 5. Code QA accuracy across 15 queries.")

    subsection("4.4 Adversarial Near-Miss (10 pairs)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["Accuracy", "0.800", "0.000", "0.000"],
            ["Discrimination", "0.700", "0.000", "0.000"],
            ["Decoy Confusion", "10.0%", "0.0%", "0.0%"],
        ], cw4
    )
    caption("Table 6. Adversarial near-miss results.")

    subsection("4.5 Hallucination Rate")
    para("Delphie and Context7 both achieved a 40% hallucination rate; Nia scored 55.6%. Most "
         "hallucinations stemmed from outdated API references in the model\u2019s training data rather "
         "than retrieval failures.")

    # ── 05 PHASE 2 ──
    section(5, "Phase 2: Validated Retrieval")
    para("To address potential bias in hand-crafted queries, Phase 2 uses two industry-standard datasets: "
         "<b>CoSQA</b> (Huang et al. 2021) and <b>CodeSearchNet</b> (Husain et al. 2019).")

    subsection("5.1 CodeSearchNet (497 queries)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["MRR", "0.940", "0.000", "0.053"],
            ["P@1", "0.938", "0.000", "0.053"],
            ["Recall@10", "0.949", "0.000", "0.053"],
            ["NDCG@10", "0.941", "0.000", "0.053"],
        ], cw4
    )
    caption("Table 7. CodeSearchNet validated retrieval. Delphie returns the correct function 93.8% of the time.")

    subsection("5.2 CoSQA (450 queries)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["MRR", "0.636", "0.002", "0.003"],
            ["NDCG@10", "0.642", "0.002", "0.004"],
            ["Avg Latency", "3,939ms", "2,822ms", "6,743ms"],
        ], cw4
    )
    caption("Table 8. CoSQA validated retrieval. Near-zero scores for Context7/Nia reflect content-matching limitations.")

    # ── 06 PHASE 3 ──
    section(6, "Phase 3: LLM-as-Judge")
    para("Phase 3 eliminates content-matching bias entirely. A blind LLM judge evaluates whether "
         "retrieved context is <i>useful</i> for answering the query, regardless of format.")

    subsection("6.1 CodeSearchNet (497 queries)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["Relevance (0\u20133)", "2.870", "0.590", "0.300"],
            ["Completeness (0\u20133)", "2.820", "0.320", "0.190"],
            ["Specificity (0\u20133)", "2.290", "0.330", "0.200"],
            ["Total (0\u20133)", "2.660", "0.413", "0.230"],
            ["Wins", "92", "2", "2"],
        ], cw4
    )
    caption("Table 9. LLM Judge on CodeSearchNet. Delphie scores 6.4x higher than Context7.")

    subsection("6.2 CoSQA (500 queries)")
    make_table(
        ["Metric", "Delphie", "Context7", "Nia"],
        [
            ["Relevance (0\u20133)", "1.200", "1.760", "0.360"],
            ["Completeness (0\u20133)", "0.780", "1.520", "0.140"],
            ["Specificity (0\u20133)", "0.820", "1.420", "0.210"],
            ["Total (0\u20133)", "0.933", "1.567", "0.237"],
            ["Wins", "17", "61", "5"],
        ], cw4
    )
    caption("Table 10. LLM Judge on CoSQA. Context7 leads by 1.27x on documentation-style queries.")

    # ── 07 PHASE 4 ──
    section(7, "Phase 4: Enhanced Judge (Position-Debiased)")
    para("Phase 4 is the most rigorous benchmark. It improves on Phase 3 with <b>position debiasing</b> "
         "(each query evaluated twice with reversed chunk ordering, scores averaged), a fourth scoring "
         "dimension (<b>faithfulness</b>), and judge self-consistency tracking.")

    subsection("7.1 CodeSearchNet (497 queries, debiased)")
    cw4r = [W * 0.30, W * 0.24, W * 0.24, W * 0.22]
    make_table(
        ["Metric", "Delphie", "Context7", "Ratio"],
        [
            ["Relevance (0\u20133)", "1.980", "0.626", "3.2x"],
            ["Completeness (0\u20133)", "1.877", "0.296", "6.3x"],
            ["Specificity (0\u20133)", "1.360", "0.402", "3.4x"],
            ["Faithfulness (0\u20133)", "2.044", "1.296", "1.6x"],
            ["Total (0\u20133)", "1.815", "0.655", "2.8x"],
            ["Wins", "436", "36", "12:1"],
            ["Ties", "25", "25", "\u2014"],
        ], cw4r
    )
    caption("Table 12. Enhanced Judge on CodeSearchNet. Delphie wins 88% of queries with 2.8x advantage.")

    subsection("7.2 CoSQA (500 queries, debiased)")
    make_table(
        ["Metric", "Delphie", "Context7", "Ratio"],
        [
            ["Relevance (0\u20133)", "1.164", "1.762", "0.66x"],
            ["Completeness (0\u20133)", "0.552", "1.352", "0.41x"],
            ["Specificity (0\u20133)", "0.680", "1.412", "0.48x"],
            ["Faithfulness (0\u20133)", "1.596", "2.130", "0.75x"],
            ["Total (0\u20133)", "0.998", "1.664", "0.60x"],
            ["Wins", "109", "341", "1:3.1"],
            ["Ties", "50", "50", "\u2014"],
        ], cw4r
    )
    caption("Table 13. Enhanced Judge on CoSQA. Context7 wins 68% of queries.")

    subsection("7.3 Debiased vs Non-Debiased")
    make_table(
        ["Dataset (engine)", "Non-Debiased", "Debiased", "Drift"],
        [
            ["CodeSearchNet (Delphie)", "2.785", "1.815", "-0.970"],
            ["CodeSearchNet (Context7)", "0.760", "0.655", "-0.105"],
            ["CoSQA (Delphie)", "1.265", "0.998", "-0.267"],
            ["CoSQA (Context7)", "1.680", "1.664", "-0.016"],
        ], cw4r
    )
    caption("Table 14. Impact of position debiasing on scores.")

    # ── 08 CONTEXT QUALITY ──
    section(8, "Context Quality Metrics")
    para("RAGAS-inspired metrics computed without LLM calls\u2014pure token-level analysis:")
    cw5m = [W * 0.22, W * 0.18, W * 0.18, W * 0.21, W * 0.21]
    make_table(
        ["Metric", "CSN Delphie", "CSN Ctx7", "CoSQA Delphie", "CoSQA Ctx7"],
        [
            ["Context Precision", "0.481", "0.191", "0.491", "0.235"],
            ["Context Density", "0.101", "0.058", "0.030", "0.034"],
            ["Signal-to-Noise", "0.595", "0.389", "0.643", "0.517"],
            ["Chunk Diversity", "0.945", "0.925", "0.927", "0.938"],
        ], cw5m
    )
    caption("Table 16. Context quality metrics. Delphie has 2.5x better context precision on CodeSearchNet.")

    subsection("8.1 Judge Self-Consistency")
    cw3 = [W * 0.34, W * 0.33, W * 0.33]
    make_table(
        ["Metric", "CodeSearchNet", "CoSQA"],
        [
            ["Position Consistency", "0.553", "0.785"],
            ["Cohen\u2019s \u03ba", "0.290 (fair)", "0.537 (moderate)"],
            ["Avg Score Drift", "1.089", "0.382"],
        ], cw3
    )
    caption("Table 17. Judge self-consistency. Code chunks are highly order-sensitive (PC=0.553 vs 0.82 baseline).")

    # ── 09 ENRICHMENT ──
    section(9, "Context Enrichment")
    para("Delphie implements two layers of context enrichment:")
    bullet("<b>Pre-embedding enrichment (index time):</b> Structural metadata (file path, scope, symbols, "
           "imports, adjacent functions) prepended to chunks before embedding computation.")
    bullet("<b>Post-retrieval enrichment (search time):</b> Each result augmented with enclosing function "
           "signature, docstring (first 3 lines), and preceding context (last 5 lines of prior chunk).")

    make_table(
        ["Dataset", "Without Enrichment", "With Enrichment", "Delta"],
        [
            ["CodeSearchNet Total", "2.640", "2.685", "+0.045"],
            ["CoSQA Total", "1.167", "1.181", "+0.014"],
            ["CSN Specificity", "2.300", "2.382", "+0.082"],
        ], cw4r
    )
    caption("Table 18. Impact of post-retrieval enrichment on LLM judge scores.")

    # ── 10 ECOLOGICAL VALIDITY ──
    section(10, "Ecological Validity")
    para("A critical question: <b>do these queries reflect how AI agents actually use context engines?</b> "
         "CoSQA queries look like web search queries (\"how to parse json in python\") that any LLM can "
         "answer from training data alone. An agent would never invoke a context engine for these.")
    cw2 = [W * 0.5, W * 0.5]
    make_table(
        ["Real agent query (needs retrieval)", "CoSQA query (doesn\u2019t need retrieval)"],
        [
            ["Find where rate limiting is enforced in this repo", "python check file is readonly"],
            ["What\u2019s the schema for chunk_embeddings table?", "how to parse json from string in python"],
            ["How does the SSE streaming handler work?", "python convert datetime to unix timestamp"],
        ], cw2
    )
    caption("Table 19. Real agent queries vs CoSQA queries.")
    para("CodeSearchNet (docstring \u2192 function) is closer to real agent use. CoSQA scores should be "
         "weighted lower when evaluating context engines for agentic workflows.")

    # ── 11 LIMITATIONS ──
    section(11, "Limitations")
    numbered(1, "Custom datasets are not independent of the engine\u2014hand-crafted by the team that built Delphie.")
    numbered(2, "Small sample sizes in custom benchmarks (10\u201315 queries; \u00b119% CI at 95%).")
    numbered(3, "Three repos don\u2019t represent all codebases\u2014results may differ on messy, multi-language codebases.")
    numbered(4, "Nia\u2019s repositories filter may not be optimally configured.")
    numbered(5, "Context7 excluded from Phase 2 (content-matching metric limitation).")
    numbered(6, "Latency measured locally for Delphie (~1.1s geographic latency to Supabase).")
    numbered(7, "LLM judge may have format biases, though position debiasing mitigates ordering effects.")
    numbered(8, "CoSQA weakness is structural\u2014Delphie indexes code, not documentation.")

    # ── 12 CONCLUSION ──
    section(12, "Conclusion")
    para("We have presented the most comprehensive public evaluation of code context engines to date. "
         "The key takeaways:")
    numbered(1, "<b>Delphie is the strongest engine for scoped code search</b>\u2014winning CodeSearchNet "
             "by 2.8x (debiased, 4D), 436 wins vs 36, and all custom benchmarks.")
    numbered(2, "<b>Context7 wins on documentation-style queries</b>\u2014but these have low ecological "
             "validity for agent workflows.")
    numbered(3, "<b>The engines solve different problems.</b> Delphie excels at code retrieval (the actual "
             "agent use case), Context7 at how-to questions, Nia at broad ecosystem search.")
    numbered(4, "<b>Position debiasing is essential</b> for code retrieval evaluation (PC=0.553 vs 0.82 baseline).")
    numbered(5, "<b>Context quality metrics reveal nuance:</b> Delphie has 2.5x better context precision "
             "even on CoSQA where it loses on judge scores.")
    numbered(6, "<b>Post-retrieval enrichment provides measurable gains</b>\u2014+0.045 on CodeSearchNet.")
    para("All benchmark code, datasets, and raw results are open-source at "
         "github.com/synthetic-sciences/SynSci-Context-Bench.")

    # ── 13 REFERENCES ──
    section(13, "References")
    refs = [
        "[1] Husain, H., Wu, H., Gazit, T., Allamanis, M., &amp; Brockschmidt, M. (2019). CodeSearchNet Challenge: Evaluating the State of Semantic Code Search. <i>arXiv:1909.09436</i>.",
        "[2] Huang, J., Tang, D., Shou, L., et al. (2021). CoSQA: 20,000+ Web Queries for Code Search and Question Answering. <i>ACL 2021</i>.",
        "[3] Zheng, L., Chiang, W., Sheng, Y., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. <i>NeurIPS 2023</i>.",
        "[4] Shi, W., Cui, Y., Liu, Z., Sun, M., &amp; Wang, L. (2025). Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges.",
        "[5] Es, S., James, J., Espinosa-Anke, L., &amp; Schockaert, S. (2024). RAGAS: Automated Evaluation of Retrieval Augmented Generation. <i>EACL 2024</i>.",
        "[6] Ren, S., Guo, D., Lu, S., et al. (2020). CodeBLEU: a Method for Automatic Evaluation of Code Synthesis. <i>arXiv:2009.10297</i>.",
        "[7] Thakur, N., Reimers, N., R\u00fcckl\u00e9, A., et al. (2021). BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of IR Models. <i>NeurIPS 2021</i>.",
    ]
    for r in refs:
        story.append(Paragraph(r, s_ref))

    # ── 14 CITATION ──
    hr()
    story.append(Spacer(1, 8))
    story.append(Paragraph("CITATION", s_abstract_label))
    story.append(Paragraph(
        "<font face='Courier' size=8>"
        "@techreport{synsc2026delphie,<br/>"
        "&nbsp;&nbsp;title = {Delphie: A Code Context Engine for Agentic Workflows},<br/>"
        "&nbsp;&nbsp;author = {Bansal, Aayam and Gangwani, Ishaan},<br/>"
        "&nbsp;&nbsp;year = {2026},<br/>"
        "&nbsp;&nbsp;url = {https://syntheticsciences.ai/context},<br/>"
        "&nbsp;&nbsp;publisher = {Inkvell Inc.},<br/>"
        "&nbsp;&nbsp;type = {Benchmark Report}<br/>"
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

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from config import DATA_PROCESSED, DB_PATH
from db import init_db, load_observations, connect
from scraper import scrape_html_table, scrape_csv_url, scrape_json_api, import_csv, make_demo_data
from ml import train_forecast_model, holt_linear_forecast
from utils import format_idr, now_stamp
from cpp_bridge import moving_average
from analytics import add_market_features, kpi_summary, correlation_matrix
from exporter import export_dataset
from source_registry import add_source, list_sources, delete_source, get_source
from quality import data_quality_report, column_profile
from business_models import revenue_core, price_elasticity, optimal_markup_price, roas, nrr, rule_of_40, hhi, takt_time, capacity_utilization
from holy_grail_formulas import FORMULA_REGISTRY
from timeframes import WINDOW_OPTIONS, FREQUENCY_OPTIONS, apply_timeframe, REQUESTED_TIMEFRAMES
from google_trends import fetch_google_trends, PYTRENDS_TIMEFRAMES
from scraping_ext import scrape_html_selectors, scrape_rss_feed, scrape_sitemap_urls
from reporting import generate_pdf_report, generate_tex_report
from backtesting import walk_forward_backtest, summarize_backtest
from source_importer import import_sources_json, export_sources_json
from batch_runner import run_active_sources
from alerts import evaluate_alerts, save_alerts, load_rules_json, DEFAULT_RULES
from scenario import monte_carlo_price_paths, summarize_paths, dcf_scenario
from settings import load_settings, save_settings
from backup import backup_sqlite, restore_sqlite, backup_workspace, BACKUP_DIR
from catalog import file_catalog, database_catalog, observation_profile
from notifications import send_webhook, send_email
from exporter import export_parquet
from data_studio import growth_metrics, rebase_index, pivot_market, normalize_currency
from sentiment import analyze_observation_text, export_sentiment
from model_registry import list_models, export_registry
from scheduler_helper import write_scheduler_snippets, cron_line
from diagnostics import diagnostic_table
from debug_support import recent_logs, diagnostic_summary
from compliance import load_standards_register, load_indonesian_legal_domains, compliance_documents
from osint_monitor import seed_default_osint_sources, run_osint_cycle, monitor_pentagon_pizza_index, load_osint_events, load_osint_runs, load_tension_indicators, import_social_csv
from realtime_engine import run_realtime_cycle, realtime_status, load_realtime_signals, load_realtime_runs, load_watchlist, seed_watchlist, export_realtime_signals

st.set_page_config(page_title="Hermes Analytics ID", page_icon=None, layout="wide")
init_db()

EARTH_COLORS = ["#D6A11E", "#C9CED6", "#1F3A5F", "#8A9A5B", "#A66A4C", "#D8C3A5", "#6B705C"]
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = EARTH_COLORS
pio.templates["indomarket_dark"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#050505",
        plot_bgcolor="#0B0B0A",
        font=dict(color="#E8DDC7"),
        colorway=EARTH_COLORS,
        xaxis=dict(gridcolor="#2A241D", zerolinecolor="#3A3026"),
        yaxis=dict(gridcolor="#2A241D", zerolinecolor="#3A3026"),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
)
px.defaults.template = "indomarket_dark"

st.markdown("""
<style>
:root {
  --bg: #050505;
  --panel: #0B0B0A;
  --panel-2: #11100E;
  --panel-3: #171511;
  --text: #E8DDC7;
  --muted: #A99B83;
  --earth: #D6A11E;
  --sage: #1F3A5F;
  --clay: #A66A4C;
  --sand: #C9CED6;
  --navy: #07111F;
  --gold: #D6A11E;
  --silver: #C9CED6;
  --border: #2A241D;
  --danger: #B85C38;
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
}
[data-testid="stHeader"] {
  background: rgba(5, 5, 5, 0.86) !important;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
[data-testid="stSidebar"] {
  background: #080807 !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
.block-container {
  padding-top: 1.3rem;
  max-width: 1440px;
  animation: fadeIn 260ms ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
h1, h2, h3, h4, h5, h6 {
  color: var(--text) !important;
  letter-spacing: -0.02em;
}
p, label, span, div { color: inherit; }
[data-testid="stCaptionContainer"], .muted, small { color: var(--muted) !important; }
hr { margin: .8rem 0 1.2rem 0; border-color: var(--border); }
[data-testid="stMetric"] {
  background: linear-gradient(180deg, #11100E 0%, #0A0A09 100%);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1rem;
  box-shadow: none;
}
[data-testid="stMetricLabel"] p { color: var(--muted) !important; }
[data-testid="stMetricValue"] {
  color: var(--sand) !important;
  font-size: 1.65rem !important;
  font-weight: 650;
}
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] button {
  background: #171511 !important;
  color: var(--sand) !important;
  border: 1px solid #3A3026 !important;
  border-radius: 10px !important;
  box-shadow: none !important;
  transition: background 140ms ease, border-color 140ms ease, transform 140ms ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
  background: #211D17 !important;
  border-color: var(--earth) !important;
  transform: translateY(-1px);
}
.stButton > button:active, .stDownloadButton > button:active, [data-testid="stFormSubmitButton"] button:active {
  transform: translateY(0);
}
input, textarea, select, [data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-baseweb="textarea"] textarea {
  background: #0B0B0A !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
}
[data-baseweb="tab-list"] { gap: .25rem; }
[data-baseweb="tab"] {
  background: #0B0B0A !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px 10px 0 0 !important;
  color: var(--muted) !important;
}
[data-baseweb="tab"][aria-selected="true"] {
  color: var(--sand) !important;
  border-color: var(--earth) !important;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}
[data-testid="stExpander"] {
  background: #0B0B0A !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-testid="stAlert"] {
  background: #11100E !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}
[data-testid="stAlert"] svg { display: none !important; }
.card {
  border: 1px solid var(--border);
  padding: 1rem;
  border-radius: 14px;
  background: var(--panel);
}
a { color: var(--earth) !important; text-decoration: none; }
a:hover { color: var(--sand) !important; }
code, pre {
  background: #0B0B0A !important;
  color: #D8C3A5 !important;
  border: 1px solid var(--border);
  border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Hermes Analytics ID")
st.caption("Fast Indonesian market signals, charts, alerts, forecasts, and reports. Developed by Ahmad Bara Wirayudha.")

with st.sidebar:
    page = st.radio("Menu", ["Start", "Overview", "Brand Lore", "Live Monitor", "Rules and Risk", "Sources", "Google Trends", "Import CSV", "Data Check", "Alerts", "Files and Data", "Data Tools", "Mood Scan", "Charts", "What If", "Calculators", "Formula Library", "Forecast", "Forecast Test", "Saved Models", "SQL Query", "Downloads", "Settings", "Checkup", "Guide"])
    st.divider()
    if st.button("Generate / refresh demo data", use_container_width=True):
        df_demo = make_demo_data()
        st.success(f"Demo data added: {len(df_demo)} rows")
    st.caption(f"Developed by Ahmad Bara Wirayudha | SQLite: `{DB_PATH.name}`")

df = load_observations()
if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")


def filtered_data(df):
    if df.empty:
        return df
    with st.expander("Filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        items = c1.multiselect("Items", sorted(df["item"].dropna().unique()), default=sorted(df["item"].dropna().unique())[:5])
        regions = c2.multiselect("Regions", sorted(df["region"].dropna().unique()), default=sorted(df["region"].dropna().unique())[:5])
        categories = c3.multiselect("Categories", sorted(df["category"].dropna().unique()), default=sorted(df["category"].dropna().unique()))
    out = df.copy()
    if items: out = out[out["item"].isin(items)]
    if regions: out = out[out["region"].isin(regions)]
    if categories: out = out[out["category"].isin(categories)]
    return out

def timeframe_controls(df, prefix="tf"):
    c1, c2 = st.columns(2)
    window = c1.selectbox("Window", list(WINDOW_OPTIONS.keys()), index=0, key=f"{prefix}_window")
    freq = c2.selectbox("Aggregation", list(FREQUENCY_OPTIONS.keys()), index=list(FREQUENCY_OPTIONS.keys()).index("Daily"), key=f"{prefix}_freq")
    return apply_timeframe(df, window, freq), window, freq


if page == "Start":
    st.subheader("Start")
    st.caption("A simple place to begin. Use the app in this order if you are new.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
<div class="card">
<h3>Step 1</h3>
<p>Add data. Use demo data, import a CSV, open Google Trends, or add a saved source.</p>
</div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="card">
<h3>Step 2</h3>
<p>Read signals. Open Overview, Live Monitor, Alerts, and Charts.</p>
</div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="card">
<h3>Step 3</h3>
<p>Make output. Run Forecast, check What If, then download a report.</p>
</div>
        """, unsafe_allow_html=True)
    st.divider()
    c4, c5, c6, c7 = st.columns(4)
    if c4.button("Add demo data", use_container_width=True):
        demo = make_demo_data()
        st.success(f"Demo data added: {len(demo)} rows")
    if c5.button("Check app health", use_container_width=True):
        st.dataframe(diagnostic_table(), use_container_width=True, hide_index=True)
    if c6.button("Seed live sources", use_container_width=True):
        st.success(f"Sources added: {seed_default_osint_sources()}")
    if c7.button("Seed watchlist", use_container_width=True):
        st.success(f"Rules added: {seed_watchlist()}")
    st.markdown("""
### Quick links

- Overview: quick market summary.
- Live Monitor: news, alerts, and live signals.
- Import CSV: add your own spreadsheet.
- Downloads: make reports and files.
- Checkup: see what needs a look.

Developed by Ahmad Bara Wirayudha.
    """)

elif page == "Overview":
    if df.empty:
        st.info("No data yet. Use the sidebar demo button, import a CSV, or configure a source.")
        st.stop()
    kpi = kpi_summary(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rows", f"{kpi['rows']:,}")
    c2.metric("Items", kpi["items"])
    c3.metric("Regions", kpi["regions"])
    c4.metric("Avg latest price", format_idr(kpi["avg_price"]))
    c5.metric("Anomalies", kpi.get("anomalies", 0))

    view = filtered_data(df)
    view, window, freq = timeframe_controls(view, "overview")
    st.caption(f"Applied timeframe: {window} / {freq}")
    featured = add_market_features(view)
    st.subheader("Market trend")
    st.plotly_chart(px.line(featured, x="date", y="price", color="item", line_dash="region", hover_data=["category", "ma7", "pct_change"]), use_container_width=True)

    left, right = st.columns([1.1, .9])
    with left:
        st.subheader("Latest leaderboard")
        latest = featured.sort_values("date").groupby(["item", "region"], as_index=False).tail(1)
        latest = latest.sort_values("pct_change", ascending=False)
        show_cols = ["date", "item", "region", "category", "price", "pct_change", "ma7", "volatility_14d"]
        st.dataframe(latest[show_cols], use_container_width=True, hide_index=True)
    with right:
        st.subheader("Category mix")
        cat = featured.groupby("category", as_index=False).agg(avg_price=("price", "mean"), rows=("price", "size"))
        st.plotly_chart(px.bar(cat, x="category", y="rows", color="avg_price"), use_container_width=True)


elif page == "Brand Lore":
    st.subheader("Hermes Analytics ID")
    st.caption("Developed by Ahmad Bara Wirayudha - github.com/AhmadBaraWirayudha")
    left, right = st.columns([0.7, 1.3])
    with left:
        logo_path = Path(__file__).resolve().parents[1] / "assets" / "brand" / "hermes_analytics_id_logo.svg"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
    with right:
        st.markdown("""
### The myth

Hermes Analytics ID fuses the ancient mythology of Mercury and Hermes, patrons of commerce, communication, navigation, and swift trade, with modern Indonesian market intelligence.

The platform is designed for retail investors, corporate strategists, and everyday traders navigating Southeast Asia's largest economy.

### Product pillars

**The Winged Messenger**

Real-time alerts, real-time data, and machine learning for IDX activity, Bank Indonesia interest-rate news, and strategic commodities such as nickel, palm oil, CPO, and coal. This module detects anomalies, forecasts movement, and prioritizes urgent signals.

**The Caduceus Hub**

Market insights and analytics with localized analyst commentary, plain-language regulatory explainers in Bahasa Indonesia, and AI-driven consumer trend predictions for Indonesian e-commerce platforms.

**The Crossroad Guide**

Wealth management and portfolio decision support with personalized robo-advisory workflows inspired by Hermes as a guide at life's crossroads. It supports reksa dana, SBN, risk tolerance, backtesting, and scenario analysis.

### Visual identity

Black background, deep navy trust layer, mercury silver precision, cadmium gold opportunity signals, and restrained earth accents for Indonesian market grounding.
        """)
    st.markdown("""
### Go-to-market direction

- Build strategic partnerships with local investment firms, market data providers, and digital brokerages.
- Launch Hermes Academy for localized financial literacy across Indonesian provinces.
- Use focused digital campaigns to position Hermes Analytics ID as a fast, decisive navigation tool for Indonesian markets.
    """)



elif page == "Live Monitor":
    st.subheader("Live Monitor")
    st.caption("Live news, market alerts, approved web sources, social imports, signal scoring, and tension tracking. Use allowed sources only.")
    status = realtime_status()
    counts = status.get("counts", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("OSINT events", counts.get("osint_events", 0) or 0)
    c2.metric("Tension indicators", counts.get("tension_indicators", 0) or 0)
    c3.metric("Real-time signals", counts.get("realtime_signals", 0) or 0)
    c4.metric("Watchlist rules", counts.get("realtime_watchlist", 0) or 0)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Run monitor", "Signals", "Events", "Tension indicators", "Watchlist", "Social import"])
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Seed sources", use_container_width=True):
            st.success(f"Imported sources: {seed_default_osint_sources()}")
        if c2.button("Seed watchlist", use_container_width=True):
            st.success(f"Seeded rules: {seed_watchlist()}")
        if c3.button("Run real-time cycle", use_container_width=True):
            st.json(run_realtime_cycle())
        if c4.button("Export signals", use_container_width=True):
            st.success(f"Saved: {export_realtime_signals().name}")
        st.markdown("Automatic five-minute monitoring can be started with `python scripts/run_realtime_monitor.py --interval 300` or `START_REALTIME_MONITOR_WINDOWS.cmd`.")
        st.dataframe(load_realtime_runs(), use_container_width=True, hide_index=True)
    with tab2:
        severity = st.selectbox("Severity filter", ["", "critical", "high", "medium", "low", "info"])
        signals = load_realtime_signals(limit=500, severity=severity or None)
        st.dataframe(signals, use_container_width=True, hide_index=True)
    with tab3:
        keyword = st.text_input("Keyword filter", "")
        events = load_osint_events(limit=500, keyword=keyword or None)
        st.dataframe(events, use_container_width=True, hide_index=True)
    with tab4:
        if st.button("Monitor Pentagon Pizza Index now"):
            try:
                st.json(monitor_pentagon_pizza_index())
            except Exception as e:
                st.error(e)
        st.dataframe(load_tension_indicators(), use_container_width=True, hide_index=True)
    with tab5:
        st.dataframe(load_watchlist(active_only=False), use_container_width=True, hide_index=True)
    with tab6:
        uploaded_social = st.file_uploader("Import approved social media CSV", type=["csv"], key="social_csv")
        platform = st.text_input("Platform label", "social")
        if uploaded_social and st.button("Import social CSV"):
            rows = import_social_csv(uploaded_social, platform=platform)
            st.success(f"Imported social rows: {rows}")
        st.caption("Social media monitoring should use official APIs, approved exports, or user-owned data. Do not bypass access controls or platform terms.")

elif page == "Rules and Risk":
    st.subheader("Compliance and geopolitical governance")
    st.caption("Friendly checklist only. Ask a qualified legal expert before launch.")
    tab1, tab2, tab3 = st.tabs(["Standards", "Indonesian legal domains", "Documents"])
    with tab1:
        st.dataframe(load_standards_register(), use_container_width=True, hide_index=True)
    with tab2:
        st.dataframe(load_indonesian_legal_domains(), use_container_width=True, hide_index=True)
        st.markdown("Key review areas include PDP, PSE, OJK, BI, IDX data rights, Bappebti, consumer protection, e-commerce, AML CFT, tax, IP, cybersecurity, and third-party risk.")
    with tab3:
        st.dataframe(compliance_documents(), use_container_width=True, hide_index=True)
        st.markdown("Primary documents are stored in docs/compliance, docs/policies, and docs/geopolitics.")

elif page == "Sources":
    st.subheader("Saved data sources")
    with st.form("add_source"):
        c1, c2 = st.columns([1, 2])
        name = c1.text_input("Source name", "my_source")
        url = c2.text_input("URL", placeholder="https://...")
        c3, c4, c5 = st.columns(3)
        source_type = c3.selectbox("Type", ["html_table", "csv_url", "json_api", "html_selectors", "rss_feed", "sitemap"])
        table_index = c4.number_input("HTML table index", min_value=0, value=0)
        active = c5.checkbox("Active", True)
        notes = st.text_input("Notes / selector JSON for html_selectors / contains filter for sitemap", "Allowed public data source; verify terms before scraping.")
        submitted = st.form_submit_button("Save source")
        if submitted:
            if not name or not url:
                st.error("Name and URL are required.")
            else:
                add_source(name, url, source_type, table_index, notes, active)
                st.success("Source saved.")

    sources = list_sources()
    st.dataframe(sources, use_container_width=True, hide_index=True)
    st.markdown("#### Import or export source list")
    cimp, cexp, cbatch = st.columns(3)
    uploaded_sources = cimp.file_uploader("Import sources JSON", type=["json"])
    if uploaded_sources and cimp.button("Import source JSON"):
        try:
            count = import_sources_json(uploaded_sources)
            st.success(f"Imported/updated {count} sources")
        except Exception as e:
            st.error(e)
    if cexp.button("Export sources JSON"):
        out_path = DATA_PROCESSED / f"{now_stamp()}_sources_export.json"
        export_sources_json(out_path)
        st.success(f"Exported source registry: {out_path.name}")
    if cbatch.button("Run all active sources"):
        with st.spinner("Running active sources..."):
            results = run_active_sources()
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("Get data now")
    if sources.empty:
        st.info("Add a source above first.")
    else:
        src_id = st.selectbox("Source", sources["id"].tolist(), format_func=lambda i: sources.loc[sources["id"] == i, "name"].iloc[0])
        c1, c2, c3 = st.columns(3)
        category = c1.text_input("Default category", "market")
        region = c2.text_input("Default region", "Indonesia")
        delay = c3.number_input("Delay seconds", min_value=0.0, value=1.0, step=0.5)
        respect_robots = st.checkbox("Respect robots.txt check", True)
        if st.button("Scrape selected source", type="primary"):
            src = get_source(src_id)
            try:
                if src["source_type"] == "html_table":
                    clean, raw_path, processed_path = scrape_html_table(src["name"], src["url"], src["table_index"], category, region, delay, respect_robots)
                elif src["source_type"] == "csv_url":
                    clean, raw_path, processed_path = scrape_csv_url(src["name"], src["url"], category, region, delay, respect_robots)
                elif src["source_type"] == "json_api":
                    clean, raw_path, processed_path = scrape_json_api(src["name"], src["url"], None, category, region, delay, respect_robots)
                elif src["source_type"] == "html_selectors":
                    clean, raw_path, processed_path = scrape_html_selectors(src["name"], src["url"], src.get("notes") or "{}", category, region, delay, respect_robots)
                elif src["source_type"] == "rss_feed":
                    clean, raw_path, processed_path = scrape_rss_feed(src["name"], src["url"], category, region, delay, respect_robots)
                else:
                    clean, raw_path, processed_path = scrape_sitemap_urls(src["name"], src["url"], src.get("notes") or "", 200, delay, respect_robots)
                st.success(f"Scraped/imported {len(clean)} rows. Processed CSV: {processed_path.name}")
                st.dataframe(clean.head(100), use_container_width=True)
            except Exception as e:
                st.error(f"Scrape failed: {e}")


elif page == "Google Trends":
    st.subheader("Google Trends automatic extraction")
    st.caption("Extract Indonesian Google Trends interest-over-time and store it automatically as CSV + SQLite observations. Requires `pytrends` from requirements.txt.")
    c1, c2 = st.columns([2,1])
    keywords = c1.text_input("Keywords, comma-separated max 5", "beras, minyak goreng, gula pasir")
    geo = c2.text_input("Geo", "ID")
    c3, c4, c5 = st.columns(3)
    tf_label = c3.selectbox("Google timeframe", list(PYTRENDS_TIMEFRAMES.keys()), index=list(PYTRENDS_TIMEFRAMES.keys()).index("5 Year"))
    timeframe = PYTRENDS_TIMEFRAMES[tf_label]
    category = c4.number_input("Google category id", min_value=0, value=0)
    gprop = c5.selectbox("Google property", ["", "images", "news", "youtube", "froogle"])
    if st.button("Fetch Google Trends and store", type="primary"):
        try:
            clean, raw_path, processed_path = fetch_google_trends(keywords, geo=geo, timeframe=timeframe, category=category, gprop=gprop)
            st.success(f"Stored {len(clean)} Google Trends rows. Processed CSV: {processed_path.name}")
            st.dataframe(clean.head(200), use_container_width=True, hide_index=True)
            st.plotly_chart(px.line(clean, x="date", y="price", color="item", title="Google Trends interest 0-100"), use_container_width=True)
        except Exception as e:
            st.error(str(e))

elif page == "Import CSV":
    st.subheader("Import CSV with automatic cleaning/storage")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    c1, c2, c3 = st.columns(3)
    csv_name = c1.text_input("Source name", "manual_csv")
    csv_cat = c2.text_input("Default category", "market")
    csv_region = c3.text_input("Default region", "Indonesia")
    st.markdown("Expected flexible columns: `date/tanggal`, `item/produk/komoditas/ticker`, `price/harga/close`, `region/provinsi/kota`, `category/sektor`, `volume/qty`.")
    if uploaded and st.button("Import and save", type="primary"):
        clean, raw_path, processed_path = import_csv(uploaded, csv_name, csv_cat, csv_region)
        st.success(f"Imported {len(clean)} rows. Raw: {raw_path.name}; processed: {processed_path.name}")
        st.dataframe(clean.head(200), use_container_width=True)


elif page == "Data Check":
    st.subheader("Data check")
    if df.empty:
        st.info("No data yet.")
        st.stop()
    report = data_quality_report(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quality score", f"{report['score']}/100")
    c2.metric("Rows", f"{report['rows']:,}")
    c3.metric("Duplicate keys", report["duplicate_keys"])
    c4.metric("Missing price", f"{report['missing_price_pct']:.1%}")
    st.markdown("#### Issues")
    for issue in report["issues"]:
        st.write("- " + issue)
    st.markdown("#### Column profile")
    st.dataframe(column_profile(df), use_container_width=True, hide_index=True)
    st.markdown("#### Suspect rows")
    suspect = df.copy()
    suspect["date_parsed"] = pd.to_datetime(suspect["date"], errors="coerce")
    suspect = suspect[suspect["date_parsed"].isna() | suspect["price"].isna() | (pd.to_numeric(suspect["price"], errors="coerce") < 0)]
    st.dataframe(suspect.head(300), use_container_width=True, hide_index=True)


elif page == "What If":
    st.subheader("What if tools")
    tab1, tab2 = st.tabs(["Price paths", "DCF scenarios"])
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        start = c1.number_input("Start price", min_value=0.01, value=15000.0)
        days = c2.slider("Days", 30, 2520, 252)
        sims = c3.slider("Simulations", 100, 5000, 1000, step=100)
        drift = c4.number_input("Annual drift", value=0.08)
        vol = st.slider("Annual volatility", 0.01, 1.50, 0.25)
        if st.button("Run Monte Carlo", type="primary"):
            paths = monte_carlo_price_paths(start, days, sims, drift, vol)
            summary = summarize_paths(paths)
            out_path = DATA_PROCESSED / f"{now_stamp()}_monte_carlo_paths.csv"
            paths.to_csv(out_path)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mean final", format_idr(summary["final_mean"]))
            m2.metric("Median final", format_idr(summary["final_median"]))
            m3.metric("5% final", format_idr(summary["final_p05"]))
            m4.metric("VaR 5% return", f"{summary['VaR_5pct_return']:.2%}")
            sample = paths.iloc[:, :min(50, paths.shape[1])].reset_index().melt(id_vars="day", var_name="simulation", value_name="price")
            st.plotly_chart(px.line(sample, x="day", y="price", color="simulation", title="Sample simulated paths"), use_container_width=True)
            st.success(f"Simulation CSV saved: {out_path.name}")
    with tab2:
        c1, c2, c3, c4 = st.columns(4)
        fcf0 = c1.number_input("FCF base", value=100000000.0)
        discount = c2.number_input("Discount rate", value=0.12)
        terminal = c3.number_input("Terminal growth", value=0.03)
        years = c4.slider("Years", 3, 15, 5)
        growth_text = st.text_input("Growth rates comma-separated", "-0.05,0,0.05,0.10,0.15,0.20")
        if st.button("Run DCF scenario"):
            growth_rates = [float(x.strip()) for x in growth_text.split(",") if x.strip()]
            scen = dcf_scenario(fcf0, growth_rates, discount, terminal, years)
            out_path = DATA_PROCESSED / f"{now_stamp()}_dcf_scenario.csv"
            scen.to_csv(out_path, index=False)
            st.plotly_chart(px.line(scen, x="growth_rate", y="enterprise_value", markers=True), use_container_width=True)
            st.dataframe(scen, use_container_width=True, hide_index=True)
            st.success(f"DCF scenario CSV saved: {out_path.name}")

elif page == "Calculators":
    st.subheader("Calculators")
    st.caption("Practical calculators for pricing, demand, retention, marketing, market concentration, and operations.")
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue & pricing", "Marketing/SaaS", "Market structure", "Operations"])
    with tab1:
        c1, c2 = st.columns(2)
        units = c1.number_input("Units sold", min_value=0.0, value=1000.0)
        price = c2.number_input("Unit price IDR", min_value=0.0, value=15000.0)
        st.metric("Core revenue", format_idr(revenue_core(units, price)))
        c3, c4 = st.columns(2)
        dq = c3.number_input("% Δ Quantity", value=-10.0)
        dp = c4.number_input("% Δ Price", value=5.0)
        e = price_elasticity(dq, dp)
        st.metric("Price elasticity", "-" if e is None else f"{e:.3f}")
        c5, c6 = st.columns(2)
        mc = c5.number_input("Marginal cost IDR", min_value=0.0, value=10000.0)
        ed = c6.number_input("Demand elasticity, normally negative", value=-2.0)
        opt = optimal_markup_price(mc, ed)
        st.metric("Optimal markup price", "-" if opt is None else format_idr(opt))
    with tab2:
        c1, c2 = st.columns(2)
        rev = c1.number_input("Campaign revenue IDR", min_value=0.0, value=10000000.0)
        cost = c2.number_input("Campaign cost IDR", min_value=0.0, value=2500000.0)
        result = roas(rev, cost)
        st.metric("ROAS", "-" if result is None else f"{result:.2f}x")
        c3, c4, c5, c6 = st.columns(4)
        smrr = c3.number_input("Starting MRR", min_value=0.0, value=50000000.0)
        emrr = c4.number_input("Expansion MRR", min_value=0.0, value=8000000.0)
        cmrr = c5.number_input("Contraction MRR", min_value=0.0, value=2000000.0)
        chmrr = c6.number_input("Churned MRR", min_value=0.0, value=4000000.0)
        st.metric("NRR", "-" if nrr(smrr, emrr, cmrr, chmrr) is None else f"{nrr(smrr, emrr, cmrr, chmrr):.1f}%")
        c7, c8 = st.columns(2)
        growth = c7.number_input("YoY revenue growth %", value=30.0)
        margin = c8.number_input("EBITDA margin %", value=15.0)
        score, passed = rule_of_40(growth, margin)
        st.metric("Rule of 40", f"{score:.1f}%", "PASS" if passed else "BELOW 40")
    with tab3:
        shares_text = st.text_input("Market shares, comma-separated", "40,30,20,10")
        shares = [x.strip() for x in shares_text.split(",")]
        value = hhi(shares)
        interpretation = "Highly concentrated" if value >= 2500 else "Moderately concentrated" if value >= 1500 else "Competitive / unconcentrated"
        st.metric("HHI", f"{value:.0f}", interpretation)
    with tab4:
        c1, c2 = st.columns(2)
        available = c1.number_input("Available production time", min_value=0.0, value=480.0)
        demand = c2.number_input("Customer demand", min_value=0.0, value=240.0)
        tt = takt_time(available, demand)
        st.metric("Takt time", "-" if tt is None else f"{tt:.2f} time units / unit")
        c3, c4 = st.columns(2)
        output = c3.number_input("Total output", min_value=0.0, value=800.0)
        cap = c4.number_input("Max capacity", min_value=0.0, value=1000.0)
        util = capacity_utilization(output, cap)
        st.metric("Capacity utilization", "-" if util is None else f"{util:.1%}")


elif page == "Alerts":
    st.subheader("Alerts and monitoring")
    if df.empty:
        st.info("No data yet.")
        st.stop()
    st.caption("Edit rules as JSON. Item-specific thresholds use exact item names.")
    import json
    rules_text = st.text_area("Alert rules JSON", json.dumps(DEFAULT_RULES, indent=2), height=220)
    if st.button("Evaluate alerts", type="primary"):
        try:
            rules = load_rules_json(rules_text)
            alerts_df = evaluate_alerts(df, rules)
            out_path = save_alerts(alerts_df)
            counts = alerts_df["severity"].value_counts().to_dict()
            c1, c2, c3 = st.columns(3)
            c1.metric("Total alerts", len(alerts_df))
            c2.metric("Critical", counts.get("critical", 0))
            c3.metric("Warnings", counts.get("warning", 0))
            st.success(f"Alert CSV saved: {out_path.name}")
            st.dataframe(alerts_df, use_container_width=True, hide_index=True)
            n1, n2 = st.columns(2)
            if n1.button("Send webhook notification"):
                try: st.success(f"Webhook sent, status {send_webhook(alerts_df)}")
                except Exception as ne: st.error(ne)
            if n2.button("Send email notification"):
                try: st.success(f"Email sent: {send_email(alerts_df)}")
                except Exception as ne: st.error(ne)
        except Exception as e:
            st.error(e)


elif page == "Files and Data":
    st.subheader("Files and data")
    tab1, tab2, tab3 = st.tabs(["Files", "Database", "Observation profile"])
    with tab1:
        fc = file_catalog()
        st.metric("Files", len(fc))
        st.dataframe(fc, use_container_width=True, hide_index=True)
    with tab2:
        dc = database_catalog()
        st.dataframe(dc, use_container_width=True, hide_index=True)
    with tab3:
        if df.empty:
            st.info("No observations yet.")
        else:
            st.dataframe(observation_profile(df), use_container_width=True, hide_index=True)


elif page == "Data Tools":
    st.subheader("Data tools for reports")
    if df.empty:
        st.info("No data yet.")
        st.stop()
    tab1, tab2, tab3, tab4 = st.tabs(["Growth metrics", "Rebase index", "Pivot", "Currency normalize"])
    with tab1:
        gm = growth_metrics(df)
        st.dataframe(gm.tail(500), use_container_width=True, hide_index=True)
        out_path = DATA_PROCESSED / f"{now_stamp()}_growth_metrics.csv"
        if st.button("Export growth metrics CSV"):
            gm.to_csv(out_path, index=False); st.success(f"Saved {out_path.name}")
    with tab2:
        base_date = st.date_input("Base date", value=pd.to_datetime(df["date"]).min().date())
        rebased = rebase_index(df, base_date=base_date)
        st.plotly_chart(px.line(rebased, x="date", y="index_rebased", color="item", title="Rebased index"), use_container_width=True)
        st.dataframe(rebased.tail(300), use_container_width=True, hide_index=True)
    with tab3:
        c1, c2, c3 = st.columns(3)
        idx = c1.selectbox("Index", ["date", "region", "category", "source"])
        cols = c2.selectbox("Columns", ["item", "category", "region", "source"])
        vals = c3.selectbox("Values", ["price", "volume"])
        pv = pivot_market(df, index=idx, columns=cols, values=vals)
        st.dataframe(pv, use_container_width=True, hide_index=True)
    with tab4:
        fx = st.number_input("Multiplier to IDR", value=1.0)
        normalized = normalize_currency(df, fx_rate_to_idr=fx)
        st.dataframe(normalized.head(300), use_container_width=True, hide_index=True)


elif page == "Mood Scan":
    st.subheader("Simple mood scan")
    if df.empty:
        st.info("No data yet.")
        st.stop()
    text_col = st.selectbox("Text column", [c for c in ["item", "category", "source", "region"] if c in df.columns])
    sent = analyze_observation_text(df, text_col=text_col)
    c1, c2, c3 = st.columns(3)
    c1.metric("Positive", int((sent["sentiment_label"] == "positive").sum()))
    c2.metric("Neutral", int((sent["sentiment_label"] == "neutral").sum()))
    c3.metric("Negative", int((sent["sentiment_label"] == "negative").sum()))
    st.plotly_chart(px.histogram(sent, x="sentiment_label", color="sentiment_label"), use_container_width=True)
    st.dataframe(sent[["date", "source", "category", "item", "region", "sentiment_score", "sentiment_label", "positive_hits", "negative_hits"]].tail(500), use_container_width=True, hide_index=True)
    if st.button("Export sentiment CSV"):
        _, path = export_sentiment(df, "sentiment_analysis")
        st.success(f"Saved {path.name}")

elif page == "Charts":
    if df.empty:
        st.info("No data yet.")
        st.stop()
    view = filtered_data(df)
    view, window, freq = timeframe_controls(view, "analytics")
    st.caption(f"Applied timeframe: {window} / {freq}")
    featured = add_market_features(view)
    tab1, tab2, tab3, tab4 = st.tabs(["Moving averages", "Anomalies", "Correlation", "Regional/category"])
    with tab1:
        item = st.selectbox("Item", sorted(featured["item"].dropna().unique()))
        s = featured[featured["item"] == item].sort_values("date").groupby("date", as_index=False)["price"].mean()
        s["ma7_cpp_or_py"] = moving_average(s["price"].tolist(), 7)
        s["ma30"] = s["price"].rolling(30, min_periods=1).mean()
        st.plotly_chart(px.line(s, x="date", y=["price", "ma7_cpp_or_py", "ma30"], title=f"{item} moving average"), use_container_width=True)
    with tab2:
        anomalies = featured[featured["anomaly"] == True].sort_values("date", ascending=False)
        st.metric("Detected anomalies", len(anomalies))
        fig = px.scatter(featured, x="date", y="price", color="anomaly", facet_col="category" if featured["category"].nunique() <= 4 else None, hover_data=["item", "region", "zscore_30d"])
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(anomalies[["date", "item", "region", "price", "zscore_30d", "pct_change"]].head(200), use_container_width=True, hide_index=True)
    with tab3:
        corr = correlation_matrix(featured)
        if corr.empty:
            st.info("Not enough data for correlation.")
        else:
            st.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1), use_container_width=True)
    with tab4:
        group_cols = st.multiselect("Group by", ["date", "category", "region", "item"], default=["date", "category"])
        if group_cols:
            agg = featured.groupby(group_cols, as_index=False).agg(avg_price=("price", "mean"), total_volume=("volume", "sum"), rows=("price", "size"))
            st.dataframe(agg.tail(500), use_container_width=True, hide_index=True)
            if "date" in group_cols:
                color = "category" if "category" in group_cols else ("region" if "region" in group_cols else "item")
                st.plotly_chart(px.line(agg, x="date", y="avg_price", color=color), use_container_width=True)


elif page == "Formula Library":
    st.subheader("Formula library")
    st.caption(f"{len(FORMULA_REGISTRY)} executable formulas loaded from the extended formula module. Use this as the calculation code layer behind the dashboard.")
    search = st.text_input("Search formula", "")
    names = sorted([n for n in FORMULA_REGISTRY if search.lower() in n.lower()])
    selected = st.selectbox("Formula", names if names else sorted(FORMULA_REGISTRY.keys()))
    fn = FORMULA_REGISTRY[selected]
    st.code(f"{selected}{fn.__annotations__ if getattr(fn, '__annotations__', None) else ''}")
    import inspect
    sig = inspect.signature(fn)
    st.write("Signature:", str(sig))
    st.write("Doc:", inspect.getdoc(fn) or "No docstring; see holy_grail_formulas.py for implementation.")
    st.info("For complex/list inputs, use Python list syntax such as [40,30,20,10] or [100,-30,50].")
    inputs = {}
    for pname, param in sig.parameters.items():
        default = "" if param.default is inspect._empty else str(param.default)
        inputs[pname] = st.text_input(pname, default, key=f"hg_{selected}_{pname}")
    if st.button("Calculate formula"):
        import ast
        args = []
        kwargs = {}
        try:
            for pname, val in inputs.items():
                if val == "":
                    raise ValueError(f"Missing input: {pname}")
                try:
                    parsed = ast.literal_eval(val)
                except Exception:
                    try: parsed = float(val)
                    except Exception: parsed = val
                kwargs[pname] = parsed
            result = fn(**kwargs)
            st.success("Result")
            st.write(result)
        except Exception as e:
            st.error(e)
    with st.expander("Available formula names"):
        st.write(", ".join(sorted(FORMULA_REGISTRY.keys())))

elif page == "Forecast":
    if df.empty:
        st.info("No data yet.")
        st.stop()
    st.subheader("ML forecast and baseline comparison")
    c1, c2 = st.columns(2)
    item = c1.selectbox("Item", sorted(df["item"].dropna().unique()))
    horizon = c2.slider("Forecast horizon days", 7, 120, 30)
    if st.button("Train model and export forecast", type="primary"):
        try:
            forecast, metrics, model_path = train_forecast_model(df, item, horizon=horizon)
            hist = df[df["item"] == item].groupby("date", as_index=False)["price"].mean().sort_values("date")
            holt_values = holt_linear_forecast(hist["price"], horizon=horizon)
            forecast["holt_baseline"] = holt_values[:len(forecast)]
            out_csv, out_xlsx = export_dataset(forecast, f"{item.replace(' ', '_')}_forecast")
            c1, c2, c3 = st.columns(3)
            c1.metric("RF MAE", format_idr(metrics["MAE"]))
            c2.metric("RF MAPE", f"{metrics['MAPE']:.2%}")
            c3.metric("Model", model_path.name)
            plot_df = pd.concat([
                hist.assign(type="actual", value=hist["price"])[["date", "value", "type"]],
                forecast.assign(type="rf_forecast", value=forecast["forecast_price"])[["date", "value", "type"]],
                forecast.assign(type="holt_baseline", value=forecast["holt_baseline"])[["date", "value", "type"]],
            ])
            st.plotly_chart(px.line(plot_df, x="date", y="value", color="type"), use_container_width=True)
            st.success(f"Forecast exported: {out_csv.name} and {out_xlsx.name}")
            st.dataframe(forecast, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(str(e))


elif page == "Forecast Test":
    st.subheader("Forecast test")
    if df.empty:
        st.info("No data yet.")
        st.stop()
    c1, c2, c3, c4 = st.columns(4)
    item = c1.selectbox("Backtest item", sorted(df["item"].dropna().unique()))
    horizon = c2.slider("Horizon", 3, 30, 7)
    min_train = c3.slider("Minimum training rows", 20, 200, 45)
    step = c4.slider("Step", 1, 30, 7)
    if st.button("Run backtest", type="primary"):
        try:
            bt = walk_forward_backtest(df, item, horizon=horizon, min_train=min_train, step=step)
            summary = summarize_backtest(bt)
            out_path = DATA_PROCESSED / f"{now_stamp()}_{item.replace(' ', '_')}_backtest.csv"
            bt.to_csv(out_path, index=False)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Folds", summary["folds"])
            m2.metric("MAE", format_idr(summary["MAE"]))
            m3.metric("MAPE", f"{summary['MAPE']:.2%}")
            m4.metric("Bias", format_idr(summary["Bias"]))
            plot_df = bt.melt(id_vars=["date"], value_vars=["actual", "prediction"], var_name="series", value_name="value")
            st.plotly_chart(px.line(plot_df, x="date", y="value", color="series", title=f"Backtest: {item}"), use_container_width=True)
            st.success(f"Backtest CSV saved: {out_path.name}")
            st.dataframe(bt, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(str(e))


elif page == "Saved Models":
    st.subheader("Saved models")
    models = list_models()
    st.metric("Registered / detected models", len(models))
    st.dataframe(models, use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    if c1.button("Export model registry CSV"):
        path = export_registry(); st.success(f"Saved {path.name}")
    if c2.button("Generate scheduler snippets"):
        cron_path, service_path, timer_path = write_scheduler_snippets()
        st.success(f"Created: {cron_path.name}, {service_path.name}, {timer_path.name}")
        st.code(cron_path.read_text(encoding="utf-8"), language="bash")
    st.markdown("#### Daily cron example")
    st.code(cron_line(), language="bash")

elif page == "SQL Query":
    st.subheader("SQL query")
    examples = {
        "Latest 100": "SELECT date, source, category, item, region, price FROM market_observations ORDER BY date DESC LIMIT 100;",
        "Category average": "SELECT date, category, AVG(price) AS avg_price FROM market_observations GROUP BY date, category ORDER BY date;",
        "Scrape logs": "SELECT * FROM scrape_runs ORDER BY started_at DESC LIMIT 100;",
        "Sources": "SELECT * FROM sources ORDER BY created_at DESC;",
    }
    selected = st.selectbox("Example", list(examples.keys()))
    query = st.text_area("Query", examples[selected], height=160)
    if st.button("Run SQL", type="primary"):
        try:
            with connect() as conn:
                result = pd.read_sql_query(query, conn)
            st.dataframe(result, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(e)

elif page == "Downloads":
    st.subheader("Downloads and reports")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        if c1.button("Export full database to CSV + XLSX", type="primary", use_container_width=True):
            csv_path, xlsx_path = export_dataset(df, "full_database")
            st.success(f"Created {csv_path.name} and {xlsx_path.name}")
        if c2.button("Generate PDF report", use_container_width=True):
            try:
                pdf_path = generate_pdf_report(df, "IndoMarket Insight Executive Report", "executive_report")
                st.success(f"Created PDF report: {pdf_path.name}")
            except Exception as e:
                st.error(str(e))
        if st.button("Export full database to Parquet", use_container_width=True):
            try:
                pq_path = export_parquet(df, "full_database")
                st.success(f"Created Parquet: {pq_path.name}")
            except Exception as e:
                st.error(f"Parquet export failed: {e}. Install pyarrow from requirements.")
        if c3.button("Generate LaTeX .tex report", use_container_width=True):
            tex_path = generate_tex_report(df, "IndoMarket Insight Executive Report", "executive_report")
            st.success(f"Created TeX report: {tex_path.name}")
        st.caption("PDF is generated directly. The .tex file can be compiled with pdflatex/xelatex if you want a LaTeX-native PDF.")
    else:
        st.info("No data loaded yet. Generate demo data, import CSV, scrape, or fetch Google Trends first.")
    files = sorted(list(DATA_PROCESSED.glob("*.csv")) + list(DATA_PROCESSED.glob("*.xlsx")) + list(DATA_PROCESSED.glob("*.pdf")) + list(DATA_PROCESSED.glob("*.tex")) + list(DATA_PROCESSED.glob("*.json")) + list(DATA_PROCESSED.glob("*.png")) + list(DATA_PROCESSED.glob("*.parquet")), reverse=True)
    if not files:
        st.info("No exports yet.")
    for f in files[:100]:
        with st.expander(f.name):
            mime = "application/pdf" if f.suffix.lower() == ".pdf" else "text/x-tex" if f.suffix.lower() == ".tex" else None
            st.download_button("Download", f.read_bytes(), file_name=f.name, mime=mime)
            if f.suffix.lower() == ".csv":
                st.dataframe(pd.read_csv(f).head(50), use_container_width=True, hide_index=True)
            elif f.suffix.lower() == ".tex":
                st.code(f.read_text(encoding="utf-8")[:5000], language="tex")


elif page == "Settings":
    st.subheader("Settings and backup")
    tab1, tab2 = st.tabs(["Settings", "Backup / Restore"])
    with tab1:
        import json
        settings = load_settings()
        settings_text = st.text_area("settings.json", json.dumps(settings, indent=2, ensure_ascii=False), height=420)
        if st.button("Save settings", type="primary"):
            try:
                path = save_settings(json.loads(settings_text))
                st.success(f"Settings saved: {path}")
            except Exception as e:
                st.error(e)
        st.caption("API token value is read from environment variable, not stored in settings.json.")
    with tab2:
        c1, c2, c3 = st.columns(3)
        if c1.button("Backup SQLite", use_container_width=True):
            try: st.success(f"Backup created: {backup_sqlite().name}")
            except Exception as e: st.error(e)
        if c2.button("Backup workspace ZIP", use_container_width=True):
            try: st.success(f"Workspace backup created: {backup_workspace(include_raw=False).name}")
            except Exception as e: st.error(e)
        if c3.button("Backup workspace incl. raw", use_container_width=True):
            try: st.success(f"Full backup created: {backup_workspace(include_raw=True).name}")
            except Exception as e: st.error(e)
        uploaded_backup = st.file_uploader("Restore SQLite backup", type=["sqlite", "bak", "db"])
        if uploaded_backup and st.button("Restore uploaded SQLite backup"):
            try:
                restore_sqlite(uploaded_backup)
                st.success("Database restored. Refresh the app if needed.")
            except Exception as e:
                st.error(e)
        backups = sorted(BACKUP_DIR.glob("*"), reverse=True)
        st.markdown("#### Existing backups")
        for f in backups[:50]:
            with st.expander(f.name):
                st.download_button("Download", f.read_bytes(), file_name=f.name)


elif page == "Checkup":
    st.subheader("Checkup")
    diag = diagnostic_table()
    summary = diagnostic_summary()
    c1, c2, c3 = st.columns(3)
    c1.metric("Checks", summary["checks"])
    c2.metric("Needs a look", summary["needs_attention"])
    c3.metric("Database", "present" if (DB_PATH.exists()) else "missing")
    tab1, tab2 = st.tabs(["Checks", "Recent logs"])
    with tab1:
        st.dataframe(diag, use_container_width=True, hide_index=True)
        st.caption("For a full command-line diagnostic report, run python scripts/doctor.py --fix")
    with tab2:
        st.code(recent_logs(), language="text")

elif page == "Guide":
    st.markdown("""
### Timeframes available

The dashboard supports: 10 Year, 5 Year, Biannual, Annual, Quartal, Bimonthly, Monthly, Biweek, Weekly, 3 Day, and Daily aggregation/window workflows.

### Best-practice flow

1. **Start with internal CSVs**: sales, marketplace exports, inventory, prices.
2. **Add public Indonesian sources** only where scraping/API access is allowed.
3. **Normalize columns** into date, item, category, region, price, volume.
4. **Review anomalies** before using forecasts.
5. **Export CSV/XLSX** for reports or BI tools.

### Recommended Indonesian market source categories

- BPS: inflation, CPI, commodity, demographics.
- Bank Indonesia: FX, policy rate, macro indicators.
- IDX/OJK: listed market/financial data where permitted.
- Google Trends: automatic Indonesian keyword interest extraction via pytrends.
- Internal marketplace seller exports: Tokopedia/Shopee/Lazada seller center CSVs.
- Company ERP/POS CSV exports.

### CLI automation

```bash
python app/cli.py init-db
python app/cli.py demo
python app/cli.py export
python app/cli.py list-sources
python app/cli.py run-source 1 --category commodity --region Indonesia
```

### Data Studio, Sentiment, Model Registry

Use Data Studio for growth metrics, rebasing, pivots, and currency normalization. Use Sentiment for simple Indonesian lexicon scoring. Use Model Registry to inspect saved ML models and generate scheduler snippets.

### Settings, backup, notifications

Use Settings & Backup to edit `config/settings.json`, create SQLite/workspace backups, and restore database backups. Alerts can be sent to webhook or SMTP when configured.

### API and automated pipeline

Run a REST API with `make api` or `uvicorn app.api:api --host 0.0.0.0 --port 8000`. Run automated jobs with `python app/pipeline.py --demo-if-empty --alerts --export --report both`.

### Backtesting and source operations

Use the Backtest page to run walk-forward forecast validation. Use Sources to import/export source JSON and run all active sources as a batch.

### Reports

Use the Exports page to generate CSV, XLSX, PDF, and LaTeX `.tex` reports.

### Podman

```bash
podman-compose -f podman-compose.prod.yml up --build
```

### Compliance note

This tool includes robots.txt checks and delays, but legal permission depends on each website's terms. Prefer official APIs, downloadable CSVs, or your own data exports.
    """)

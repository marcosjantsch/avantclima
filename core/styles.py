import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-primary: #050807;
            --bg-secondary: #0b1210;
            --bg-tertiary: #121a18;
            --panel-bg: rgba(11, 18, 16, 0.92);
            --panel-border: rgba(110, 255, 179, 0.18);
            --text-primary: #ecf7f0;
            --text-secondary: #a8c4b2;
            --accent: #6effb3;
            --accent-strong: #98ff6b;
            --accent-soft: #2fa86f;
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMainBlockContainer"] {
            background:
                radial-gradient(circle at top left, rgba(20, 92, 67, 0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(110, 255, 179, 0.08), transparent 22%),
                linear-gradient(180deg, #040605 0%, #08100e 45%, #050807 100%) !important;
            color: var(--text-primary) !important;
        }

        .block-container {
            padding-top: 0.35rem !important;
            padding-bottom: 1rem !important;
        }

        header[data-testid="stHeader"] {
            height: 0rem !important;
        }

        section.main > div {
            padding-top: 0rem !important;
        }

        div, p, span, label, li {
            color: var(--text-primary);
        }

        .main-title {
            font-size: 24px !important;
            font-weight: 600 !important;
            margin-top: -6px !important;
            margin-bottom: 8px !important;
            line-height: 1.2 !important;
            color: var(--accent-strong) !important;
            letter-spacing: 0.02em;
        }

        .section-title {
            font-size: 14px !important;
            font-weight: 600 !important;
            margin-top: 2px !important;
            margin-bottom: 6px !important;
            opacity: 0.95 !important;
            line-height: 1.2 !important;
            color: var(--accent) !important;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .userbar {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            margin-top: -4px;
            margin-bottom: 4px;
            white-space: nowrap;
        }

        .userbar .pill {
            padding: 2px 8px;
            border: 1px solid var(--panel-border);
            border-radius: 999px;
            background-color: rgba(18, 26, 24, 0.82);
            color: var(--text-secondary);
        }

        div[data-testid="stButton"] > button {
            padding: 0.25rem 0.6rem !important;
            font-size: 11px !important;
            min-height: 30px !important;
            border-radius: 8px !important;
            border: 1px solid rgba(110, 255, 179, 0.28) !important;
            background: linear-gradient(180deg, rgba(19, 39, 31, 0.96), rgba(11, 22, 18, 0.98)) !important;
            color: var(--text-primary) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28) !important;
        }

        div[data-testid="stButton"] > button:hover {
            border-color: rgba(152, 255, 107, 0.65) !important;
            color: #ffffff !important;
            background: linear-gradient(180deg, rgba(28, 62, 47, 0.98), rgba(14, 30, 24, 0.98)) !important;
        }

        section[data-testid="stSidebar"] {
            padding-top: 0.4rem !important;
            background: linear-gradient(180deg, rgba(5, 8, 7, 0.98), rgba(10, 18, 15, 0.98)) !important;
            border-right: 1px solid rgba(110, 255, 179, 0.12);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.2rem !important;
            padding-bottom: 0.3rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 0.02rem !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            margin-top: 0.15rem !important;
            margin-bottom: 0.35rem !important;
            line-height: 1.2 !important;
            color: var(--accent) !important;
        }

        section[data-testid="stSidebar"] h1 {
            font-size: 18px !important;
        }

        section[data-testid="stSidebar"] h2 {
            font-size: 16px !important;
        }

        section[data-testid="stSidebar"] h3 {
            font-size: 14px !important;
        }

        section[data-testid="stSidebar"] label {
            margin-bottom: 2px !important;
            font-size: 12px !important;
            color: var(--text-secondary) !important;
        }

        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stDateInput,
        section[data-testid="stSidebar"] .stTextInput,
        section[data-testid="stSidebar"] .stNumberInput,
        section[data-testid="stSidebar"] .stMultiselect {
            margin-bottom: 0.2rem !important;
        }

        section[data-testid="stSidebar"] hr {
            margin: 0.45rem 0 !important;
            border-color: rgba(110, 255, 179, 0.12) !important;
        }

        [data-baseweb="tab-list"] {
            gap: 0.35rem;
        }

        button[role="tab"] {
            font-size: 13px !important;
            padding: 6px 10px !important;
            background: rgba(12, 20, 18, 0.9) !important;
            border: 1px solid rgba(110, 255, 179, 0.1) !important;
            border-radius: 10px !important;
            color: var(--text-secondary) !important;
        }

        button[role="tab"][aria-selected="true"] {
            color: var(--text-primary) !important;
            border-color: rgba(110, 255, 179, 0.35) !important;
            box-shadow: inset 0 0 0 1px rgba(152, 255, 107, 0.12);
        }

        div[data-testid="stMetric"] {
            padding: 8px 10px !important;
            background: linear-gradient(180deg, rgba(11, 18, 16, 0.92), rgba(15, 24, 21, 0.9)) !important;
            border: 1px solid rgba(110, 255, 179, 0.12) !important;
            border-radius: 12px !important;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 12px !important;
            color: var(--text-secondary) !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 20px !important;
            color: var(--accent-strong) !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 8px !important;
            border: 1px solid rgba(110, 255, 179, 0.12) !important;
            overflow: hidden !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 8px !important;
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            border: 1px solid rgba(110, 255, 179, 0.14) !important;
            background-color: rgba(14, 21, 19, 0.9) !important;
        }

        .stCheckbox label,
        .stRadio label,
        .stCaption,
        [data-testid="stMarkdownContainer"] p {
            color: var(--text-secondary) !important;
        }

        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div,
        .stDateInput input,
        .stTextInput input,
        .stNumberInput input {
            background: rgba(13, 20, 18, 0.96) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(110, 255, 179, 0.16) !important;
            border-radius: 10px !important;
        }

        .stCheckbox div[data-baseweb="checkbox"] > div {
            border-color: rgba(110, 255, 179, 0.4) !important;
            background: rgba(10, 17, 15, 0.95) !important;
        }

        .stRadio [role="radiogroup"] {
            background: rgba(11, 18, 16, 0.72);
            border: 1px solid rgba(110, 255, 179, 0.1);
            border-radius: 12px;
            padding: 0.5rem 0.65rem;
        }

        .stCaption {
            color: var(--text-secondary) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

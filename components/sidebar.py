from datetime import date

import streamlit as st

from core.settings import LOGO_PATH, TIPOS_DADO, ANOS_DISPONIVEIS, MESES_DISPONIVEIS


def safe_unique(gdf, col):
    if col not in gdf.columns:
        return []
    return sorted([str(x) for x in gdf[col].dropna().unique()])


def _section_header(title: str, subtitle: str = "") -> None:
    subtitle_html = (
        f'<div class="sidebar-section-subtitle">{subtitle}</div>' if subtitle else ""
    )
    st.markdown(
        (
            '<div class="sidebar-section-header">'
            f'<div class="sidebar-section-title">{title}</div>'
            f"{subtitle_html}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _summary_chip(label: str, value: str) -> str:
    return (
        '<div class="sidebar-summary-chip">'
        f'<div class="sidebar-summary-label">{label}</div>'
        f'<div class="sidebar-summary-value">{value}</div>'
        "</div>"
    )


def render_sidebar(gdf_full):
    with st.sidebar:
        st.image(LOGO_PATH, width=60)
        st.markdown(
            (
                '<div class="sidebar-brand-card">'
                '<div class="sidebar-brand-kicker">Painel de controle</div>'
                '<div class="sidebar-brand-title">Selecione a opção</div>'
                '<div class="sidebar-brand-subtitle">Filtros espaciais e período de análise</div>'
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    filtros_container = st.sidebar.container(border=True)
    with filtros_container:
        _section_header("Filtro principal", "Defina a abrangência dos dados")
        tipo_dado = st.selectbox("Tipo de Dados", TIPOS_DADO)

    selected_uf = None
    selected_empresa = None
    selected_fazenda = None
    selected_municipio = None

    with filtros_container:
        if tipo_dado == "Dados por Estado":
            ufs = safe_unique(gdf_full, "UF")
            selected_uf = st.selectbox("Selecione UF", ufs) if ufs else None

        elif tipo_dado == "Dados por Empresa":
            empresas = safe_unique(gdf_full, "EMPRESA")
            selected_empresa = (
                st.selectbox("Selecione Empresa", empresas) if empresas else None
            )

        elif tipo_dado == "Dados Empresa/Fazenda":
            empresas = safe_unique(gdf_full, "EMPRESA")
            selected_empresa = (
                st.selectbox("Selecione Empresa", empresas) if empresas else None
            )

            if (
                selected_empresa
                and "EMPRESA" in gdf_full.columns
                and "FAZENDA" in gdf_full.columns
            ):
                gdf_emp = gdf_full[gdf_full["EMPRESA"].astype(str) == str(selected_empresa)]
                fazendas = safe_unique(gdf_emp, "FAZENDA")
                selected_fazenda = (
                    st.selectbox("Selecione Fazenda", fazendas)
                    if fazendas
                    else None
                )

        elif tipo_dado == "Dados por Município":
            ufs = safe_unique(gdf_full, "UF")
            selected_uf = st.selectbox("Selecione UF", ufs) if ufs else None

            if (
                selected_uf
                and "UF" in gdf_full.columns
                and "MUNICIPIO" in gdf_full.columns
            ):
                gdf_uf = gdf_full[gdf_full["UF"].astype(str) == str(selected_uf)]
                municipios = safe_unique(gdf_uf, "MUNICIPIO")
                selected_municipio = (
                    st.selectbox("Selecione Município", municipios)
                    if municipios
                    else None
                )

    periodo_container = st.sidebar.container(border=True)
    with periodo_container:
        _section_header("Período mensal", "Delimite a janela temporal")

        col1, col2 = st.columns(2)
        with col1:
            start_mes_nome = st.selectbox(
                "Mês inicial", list(MESES_DISPONIVEIS.keys()), index=0
            )
        with col2:
            start_ano = st.selectbox(
                "Ano inicial",
                ANOS_DISPONIVEIS,
                index=ANOS_DISPONIVEIS.index(2026),
            )

        col3, col4 = st.columns(2)
        with col3:
            end_mes_nome = st.selectbox(
                "Mês final", list(MESES_DISPONIVEIS.keys()), index=11
            )
        with col4:
            end_ano = st.selectbox(
                "Ano final",
                ANOS_DISPONIVEIS,
                index=ANOS_DISPONIVEIS.index(2026),
            )

    start_date = date(start_ano, MESES_DISPONIVEIS[start_mes_nome], 1)
    end_date = date(end_ano, MESES_DISPONIVEIS[end_mes_nome], 1)

    action_container = st.sidebar.container(border=True)
    with action_container:
        st.markdown(
            (
                '<div class="sidebar-summary-grid">'
                f'{_summary_chip("Modo", tipo_dado.replace("Dados ", "").replace("/", " / "))}'
                f'{_summary_chip("Janela", f"{start_mes_nome[:3]}/{str(start_ano)[-2:]} - {end_mes_nome[:3]}/{str(end_ano)[-2:]}")}'
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        apply = st.button("Aplicar Filtros")
        log_container = st.container() if apply else st.empty()

    return {
        "tipo_dado": tipo_dado,
        "selected_uf": selected_uf,
        "selected_empresa": selected_empresa,
        "selected_fazenda": selected_fazenda,
        "selected_municipio": selected_municipio,
        "start_date": start_date,
        "end_date": end_date,
        "apply": apply,
        "log_container": log_container,
    }

# tabs/tab_mapa.py
import numpy as np
import pandas as pd
import folium
import streamlit as st
from branca.element import Element

from folium.plugins import Fullscreen, MiniMap, MeasureControl, MousePosition
from streamlit_folium import st_folium

from core.settings import MAX_FEATURES_FULL_MAP
from core.theme_palette import get_theme_palette
from services.log_service import log_error_once, log_success_once, log_warning_once


DEFAULT_DARK_TILES = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
DEFAULT_DARK_ATTR = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
)


def _inject_map_theme(m: folium.Map) -> None:
    palette = get_theme_palette()
    css = """
    <style>
    .leaflet-container {{
        background: {map_background} !important;
        font-family: "Segoe UI", Arial, sans-serif;
    }}

    .leaflet-control-zoom a,
    .leaflet-control-layers-toggle,
    .leaflet-bar a {{
        background: {map_control} !important;
        color: {map_text} !important;
        border-color: {panel_border} !important;
    }}

    .leaflet-bar,
    .leaflet-control-layers,
    .leaflet-control-attribution,
    .leaflet-control-scale,
    .leaflet-control-minimap {{
        background: {map_surface} !important;
        border: 1px solid {panel_border} !important;
        border-radius: 12px !important;
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.35) !important;
    }}

    .leaflet-control-layers-expanded {{
        padding: 12px 14px !important;
        color: {map_text} !important;
        min-width: 18rem;
        max-width: min(24rem, 32vw);
        font-size: clamp(0.88rem, 0.76vw, 1rem);
        line-height: 1.45;
    }}

    .leaflet-control-layers-list span,
    .leaflet-control-layers label {{
        color: {map_text} !important;
        font-size: inherit !important;
        line-height: inherit !important;
    }}

    .leaflet-control-layers-base label,
    .leaflet-control-layers-overlays label {{
        display: flex !important;
        align-items: center;
        gap: 0.38rem;
        margin-bottom: 0.38rem !important;
    }}

    .leaflet-control-layers-base input,
    .leaflet-control-layers-overlays input {{
        transform: scale(1.05);
        accent-color: {map_accent};
    }}

    .leaflet-control-layers-base label:hover,
    .leaflet-control-layers-overlays label:hover {{
        color: {map_accent_strong} !important;
    }}

    .leaflet-control-layers-separator {{
        border-top-color: {panel_border} !important;
    }}

    .leaflet-tooltip {{
        background: {map_tooltip} !important;
        color: {map_text} !important;
        border: 1px solid {panel_border} !important;
        border-radius: 10px !important;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.32) !important;
    }}

    .leaflet-tooltip:before {{
        border-top-color: {map_tooltip} !important;
    }}

    .leaflet-popup-content-wrapper,
    .leaflet-popup-tip {{
        background: {map_tooltip} !important;
        color: {map_text} !important;
    }}

    .leaflet-popup-content-wrapper {{
        border: 1px solid {panel_border} !important;
        border-radius: 14px !important;
        box-shadow: 0 20px 36px rgba(0, 0, 0, 0.38) !important;
    }}

    .leaflet-popup-content {{
        margin: 12px 14px !important;
        line-height: 1.45 !important;
    }}

    .leaflet-popup-content h4 {{
        margin: 0 0 8px 0 !important;
        color: {map_accent_strong} !important;
        font-size: 14px !important;
    }}

    .leaflet-popup-close-button {{
        color: {map_text_soft} !important;
    }}

    .leaflet-control-attribution,
    .leaflet-control-attribution a,
    .leaflet-control-scale-line,
    .leaflet-control-mouseposition {{
        color: {map_text_soft} !important;
    }}

    .leaflet-control-scale-line {{
        background: {map_surface} !important;
        border-color: {panel_border} !important;
    }}
    </style>
    """.format(
        map_background=palette["map_background"],
        map_control=palette["map_control"],
        map_text=palette["map_text"],
        panel_border=palette["panel_border"],
        map_surface=palette["map_surface"],
        map_accent=palette["map_accent"],
        map_accent_strong=palette["map_accent_strong"],
        map_tooltip=palette["map_tooltip"],
        map_text_soft=palette["map_text_soft"],
    )
    m.get_root().header.add_child(Element(css))


def _add_basemaps(m: folium.Map) -> None:
    """
    Adiciona multiplas camadas de mapa base.
    """

    folium.TileLayer(
        tiles=DEFAULT_DARK_TILES,
        attr=DEFAULT_DARK_ATTR,
        name="CartoDB Dark Matter",
        show=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="OpenStreetMap",
        show=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri World Imagery",
        show=True,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri World Topo",
        show=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr="OpenTopoMap",
        name="OpenTopoMap",
        show=False,
        control=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png",
        attr="Stadia Maps",
        name="Stadia Outdoors",
        show=False,
        control=True,
    ).add_to(m)

def _get_cor_exibicao(tipo_exib: str) -> str:
    color_map = {
        "Todos os Dados": "#98FF6B",
        "Dados por Estado": "#46E08F",
        "Dados por Empresa": "#5AF7C0",
        "Dados Empresa/Fazenda": "#7CFFB2",
        "Dados por Município": "#2F8F5B",
    }
    return color_map.get(tipo_exib, "#6EFFB3")


def _preparar_gdf_exibicao(gdf_map):
    """
    Padroniza campos numericos e textos auxiliares para tooltip.
    """
    gdf_map = gdf_map.copy()

    for col in ["AREA_T", "AREA_PRODU"]:
        if col in gdf_map.columns:
            gdf_map[col] = pd.to_numeric(gdf_map[col], errors="coerce").round(1)

    if "AREA_T" in gdf_map.columns:
        gdf_map["AREA_T_TXT"] = gdf_map["AREA_T"].apply(
            lambda x: f"{x:.1f} ha" if pd.notna(x) else "N/A"
        )

    if "AREA_PRODU" in gdf_map.columns:
        gdf_map["AREA_PRODU_TXT"] = gdf_map["AREA_PRODU"].apply(
            lambda x: f"{x:.1f} ha" if pd.notna(x) else "N/A"
        )

    return gdf_map


def _criar_tooltip(gdf_map):
    tooltip_fields = [
        c
        for c in [
            "UF",
            "MUNICIPIO",
            "EMPRESA",
            "FAZENDA",
            "AREA_T_TXT",
            "AREA_PRODU_TXT",
        ]
        if c in gdf_map.columns
    ]

    tooltip_aliases_map = {
        "UF": "UF",
        "MUNICIPIO": "Município",
        "EMPRESA": "Empresa",
        "FAZENDA": "Fazenda",
        "AREA_T_TXT": "Área Total",
        "AREA_PRODU_TXT": "Área Produtiva",
    }
    tooltip_aliases = [tooltip_aliases_map.get(c, c) for c in tooltip_fields]

    return tooltip_fields, tooltip_aliases


def _build_map_key(
    filtro: dict,
    gdf_map,
    usar_geometria_original: bool,
    mostrar_preenchimento: bool,
    refresh_token: str = "",
) -> str:
    partes = [
        "mapa_principal",
        str(filtro.get("tipo_dado", "todos")),
        str(filtro.get("selected_uf", "")),
        str(filtro.get("selected_empresa", "")),
        str(filtro.get("selected_fazenda", "")),
        str(filtro.get("selected_municipio", "")),
        f"orig_{int(bool(usar_geometria_original))}",
        f"fill_{int(bool(mostrar_preenchimento))}",
        f"n_{len(gdf_map)}",
        str(refresh_token or ""),
    ]

    if not gdf_map.empty:
        try:
            minx, miny, maxx, maxy = gdf_map.total_bounds
            partes.extend(
                [
                    f"{minx:.5f}",
                    f"{miny:.5f}",
                    f"{maxx:.5f}",
                    f"{maxy:.5f}",
                ]
            )
        except Exception:
            pass

    return "_".join(partes)


def render_tab_mapa(gdf_full, gdf_filtered, filtro, refresh_token: str = ""):
    st.markdown('<div class="section-title">Mapa Principal</div>', unsafe_allow_html=True)
    palette = get_theme_palette()

    aplicar = st.session_state.get("aplicar", False)
    gdf_map = gdf_filtered if aplicar else gdf_full
    tipo_exib = filtro["tipo_dado"] if aplicar else "Todos os Dados"

    if gdf_map is None or gdf_map.empty:
        log_warning_once(
            "tab_mapa",
            "empty_geometry",
            "Mapa Principal sem geometrias para renderizacao",
            {"aplicar": bool(aplicar), "tipo_dado": tipo_exib},
            signature={"aplicar": bool(aplicar), "tipo_dado": tipo_exib, "empty": True},
        )
        st.info("Nenhuma geometria disponível para exibição no mapa.")
        return

    col_opt1, col_opt2 = st.columns(2)

    with col_opt1:
        usar_geometria_original = st.checkbox(
            "Exibir polígonos sem simplificação",
            value=False,
            key="mapa_sem_simplificacao",
            help="Mostra as geometrias originais do shapefile. Pode deixar o mapa mais pesado.",
        )

    with col_opt2:
        mostrar_preenchimento = st.checkbox(
            "Preencher polígonos",
            value=True,
            key="mapa_preenchimento",
            help="Quando desmarcado, exibe apenas o contorno das feições.",
        )

    gdf_map = gdf_map.copy()

    if usar_geometria_original and "__geometry_original__" in gdf_map.columns:
        gdf_map["geometry"] = gdf_map["__geometry_original__"]

    area_total_mapa = (
        float(pd.to_numeric(gdf_map["AREA_T"], errors="coerce").sum())
        if "AREA_T" in gdf_map.columns
        else np.nan
    )
    area_produ_mapa = (
        float(pd.to_numeric(gdf_map["AREA_PRODU"], errors="coerce").sum())
        if "AREA_PRODU" in gdf_map.columns
        else np.nan
    )
    n_municipios = (
        int(gdf_map["MUNICIPIO"].dropna().astype(str).nunique())
        if "MUNICIPIO" in gdf_map.columns
        else 0
    )
    n_fazendas = (
        int(gdf_map["FAZENDA"].dropna().astype(str).nunique())
        if "FAZENDA" in gdf_map.columns
        else 0
    )
    n_feicoes = len(gdf_map)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Fazendas", str(n_fazendas))
    c2.metric(
        "Área total (ha)",
        f"{area_total_mapa:.1f}" if pd.notna(area_total_mapa) else "N/A",
    )
    c3.metric(
        "Área produtiva (ha)",
        f"{area_produ_mapa:.1f}" if pd.notna(area_produ_mapa) else "N/A",
    )
    c4.metric("Municípios", str(n_municipios))
    c5.metric("Feições", f"{n_feicoes:,}".replace(",", "."))

    if len(gdf_map) > MAX_FEATURES_FULL_MAP:
        log_warning_once(
            "tab_mapa",
            "feature_limit_applied",
            "Mapa Principal truncado por limite de feicoes",
            {
                "total_features": int(len(gdf_map)),
                "max_features": int(MAX_FEATURES_FULL_MAP),
            },
            signature={
                "total_features": int(len(gdf_map)),
                "max_features": int(MAX_FEATURES_FULL_MAP),
            },
        )
        st.warning(
            f"⚠️ Muitas feições ({len(gdf_map)}). "
            f"Renderizando apenas {MAX_FEATURES_FULL_MAP}."
        )
        gdf_map = gdf_map.head(MAX_FEATURES_FULL_MAP)

    gdf_map = _preparar_gdf_exibicao(gdf_map)

    try:
        bounds = gdf_map.total_bounds
        minx, miny, maxx, maxy = bounds
    except Exception:
        log_error_once(
            "tab_mapa",
            "invalid_bounds",
            "Falha ao calcular limites espaciais do mapa",
            {"records": int(len(gdf_map))},
            signature={"records": int(len(gdf_map)), "status": "bounds_error"},
        )
        st.error("Não foi possível calcular os limites espaciais das geometrias.")
        return

    if any(pd.isna(v) for v in [minx, miny, maxx, maxy]):
        log_error_once(
            "tab_mapa",
            "nan_bounds",
            "Limites espaciais invalidos na aba Mapa Principal",
            {"records": int(len(gdf_map))},
            signature={"records": int(len(gdf_map)), "status": "nan_bounds"},
        )
        st.error("Os limites espaciais das geometrias são inválidos.")
        return

    center_lat = (miny + maxy) / 2
    center_lon = (minx + maxx) / 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles=None,
        control_scale=True,
        prefer_canvas=True,
        scrollWheelZoom=False,
    )

    try:
        m.fit_bounds([[miny, minx], [maxy, maxx]])
    except Exception:
        pass

    _add_basemaps(m)
    _inject_map_theme(m)

    Fullscreen(
        position="topright",
        title="Tela cheia",
        title_cancel="Sair da tela cheia",
        force_separate_button=True,
    ).add_to(m)

    MiniMap(
        tile_layer=folium.TileLayer(
            tiles=DEFAULT_DARK_TILES,
            attr=DEFAULT_DARK_ATTR,
            name="MiniMap Dark",
        ),
        toggle_display=True,
        position="bottomright",
        width=170,
        height=110,
        collapsed_width=26,
        collapsed_height=26,
        zoom_level_offset=-4,
    ).add_to(m)

    MeasureControl(
        position="topleft",
        primary_length_unit="meters",
        secondary_length_unit="kilometers",
        primary_area_unit="sqmeters",
        secondary_area_unit="hectares",
    ).add_to(m)

    MousePosition(
        position="bottomleft",
        separator=" | ",
        prefix="Coordenadas",
        lat_formatter="function(num) {return L.Util.formatNum(num, 6);}",
        lng_formatter="function(num) {return L.Util.formatNum(num, 6);}",
    ).add_to(m)

    color = _get_cor_exibicao(tipo_exib)
    tooltip_fields, tooltip_aliases = _criar_tooltip(gdf_map)
    gdf_render = gdf_map.drop(columns=["__geometry_original__"], errors="ignore").copy()

    folium.GeoJson(
        data=gdf_render.to_json(),
        name="Fazendas",
        style_function=lambda x: {
            "fillColor": color,
            "color": color,
            "weight": 1.8,
            "opacity": 0.9,
            "fillOpacity": 0.28 if mostrar_preenchimento else 0.00,
        },
        highlight_function=lambda x: {
            "fillColor": palette["map_highlight"],
            "color": palette["map_highlight"],
            "weight": 3.2,
            "opacity": 1,
            "fillOpacity": 0.42 if mostrar_preenchimento else 0.08,
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            sticky=True,
            labels=True,
            localize=True,
            style=(
                f"background-color: {palette['map_tooltip']};"
                f"color: {palette['map_text']};"
                f"border: 1px solid {palette['panel_border']};"
                "border-radius: 12px;"
                "padding: 8px 10px;"
                "box-shadow: 0 16px 32px rgba(0,0,0,0.28);"
            ),
        ),
        popup=folium.GeoJsonPopup(
            fields=[field for field in tooltip_fields if field in gdf_render.columns],
            aliases=tooltip_aliases,
            localize=True,
            labels=True,
            style=(
                f"background-color: {palette['map_tooltip']};"
                f"color: {palette['map_text']};"
                f"border: 1px solid {palette['panel_border']};"
                "border-radius: 12px;"
                "padding: 8px 10px;"
            ),
        ),
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    map_key = _build_map_key(
        filtro=filtro,
        gdf_map=gdf_map,
        usar_geometria_original=usar_geometria_original,
        mostrar_preenchimento=mostrar_preenchimento,
        refresh_token=refresh_token,
    )

    st_folium(
        m,
        use_container_width=True,
        height=620,
        key=map_key,
        returned_objects=[],
    )

    log_success_once(
        "tab_mapa",
        "map_rendered",
        "Mapa Principal renderizado com sucesso",
        {
            "records": int(len(gdf_render)),
            "tipo_dado": tipo_exib,
            "usar_geometria_original": bool(usar_geometria_original),
            "mostrar_preenchimento": bool(mostrar_preenchimento),
        },
        signature={
            "records": int(len(gdf_render)),
            "tipo_dado": tipo_exib,
            "usar_geometria_original": bool(usar_geometria_original),
            "mostrar_preenchimento": bool(mostrar_preenchimento),
            "refresh_token": str(refresh_token or ""),
        },
    )

    st.caption(
        "Bases disponíveis: CartoDB Dark Matter, OpenStreetMap, Esri World Imagery, "
        "Esri World Topo, OpenTopoMap e Stadia Outdoors."
    )



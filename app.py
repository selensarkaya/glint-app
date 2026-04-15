import streamlit as st

st.set_page_config(
    page_title="GLİNT — Fiyat & İskonto Analizi",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #F4F6F9; }
    .block-container { padding-top: 1rem; }
    .header-banner {
        background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
        color: white; padding: 1.2rem 2rem;
        border-radius: 12px; margin-bottom: 1.5rem; text-align: center;
    }
    table.fiyat-tablo { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin-top: 0.5rem; }
    table.fiyat-tablo th { background: #F1F5F9; color: #718096; font-weight: 600; padding: 6px 10px; text-align: right; border-bottom: 2px solid #E2E8F0; }
    table.fiyat-tablo th:first-child { text-align: left; }
    table.fiyat-tablo td { padding: 7px 10px; border-bottom: 1px solid #F1F5F9; text-align: right; color: #1A202C; }
    table.fiyat-tablo td:first-child { text-align: left; color: #4A5568; }
    table.fiyat-tablo tr.bold td { font-weight: 700; background: #EFF6FF; }
    table.fiyat-tablo tr.bold-green td { font-weight: 700; background: #E2EFDA; color: #375623; }
    .durum-karli { background: #E2EFDA; color: #375623; border-radius: 8px; padding: 10px 16px; font-weight: 700; font-size: 1rem; text-align: center; margin-top: 0.5rem; }
    .durum-zarar { background: #FCE4D6; color: #C0392B; border-radius: 8px; padding: 10px 16px; font-weight: 700; font-size: 1rem; text-align: center; margin-top: 0.5rem; }
    .maliyet-box { background: #FFF2CC; border-radius: 8px; padding: 10px 14px; margin-top: 0.5rem; display: flex; justify-content: space-between; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-banner">
    <div style="font-size:1.6rem; font-weight:800; margin-bottom:4px;">GLİNT — Fiyat & İskonto Analizi</div>
    <div style="font-size:0.9rem; opacity:0.8;">Market ve Toptancı kanalları · Bağımsız senaryo hesaplaması</div>
</div>
""", unsafe_allow_html=True)

import matplotlib.pyplot as plt
import numpy as np

KDV = 0.20

def fmt(v):
    return f"₺{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def pct(v):
    return f"%{v*100:.1f}"

def haric(d): return d / (1 + KDV)
def kdv_t(d): return d - haric(d)

def tablo_satir(label, dahil, bold=False, bold_green=False, minus=False):
    prefix = "−" if minus else ""
    cls = "bold-green" if bold_green else ("bold" if bold else "")
    return f"""<tr class="{cls}">
        <td>{label}</td>
        <td>{prefix}{fmt(dahil)}</td>
        <td>{prefix}{fmt(haric(dahil))}</td>
        <td>{prefix}{fmt(kdv_t(dahil))}</td>
    </tr>"""

tab1, tab2 = st.tabs(["🏪  Direkt Market", "🏭  Toptancı Kanalı"])

with tab1:
    col_sol, col_sag = st.columns([1, 1.4], gap="large")

    with col_sol:
        st.markdown("#### A. Maliyet Parametreleri")
        m_alis      = st.number_input("Birim Mal Maliyeti — Alış (₺, KDV dahil)", value=54.0, step=0.5, key="m_alis")
        m_liste     = st.number_input("Liste / Görünür Fiyat (₺, KDV dahil)", value=80.0, step=0.5, key="m_liste")
        m_nakliye   = st.slider("Nakliye Maliyeti (%)", 0.0, 30.0, 10.0, 0.5, key="m_nak", format="%g%%")
        m_marketing = st.slider("Marketing Maliyeti (%)", 0.0, 20.0, 2.0, 0.5, key="m_mkt", format="%g%%")

        gercek_m = m_alis * (1 + m_nakliye/100 + m_marketing/100)
        st.markdown(f"""
        <div class="maliyet-box">
            <span style="color:#7F6000; font-weight:600;">Gerçek Birim Maliyet (KDV dahil)</span>
            <span style="color:#7F6000; font-size:1.3rem; font-weight:800;">{fmt(gercek_m)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### B. Market İskonto Girişi")
        max_isk_m = (m_liste - gercek_m) / m_liste if m_liste > 0 else 0
        m_iskonto = st.slider(f"Market İskonto Oranı  *(max eşik: {pct(max_isk_m)})*", 0.0, 25.0, 0.0, 0.5, key="m_isk", format="%g%%")

        net_m      = m_liste * (1 - m_iskonto/100)
        isk_tl_m   = m_liste * (m_iskonto/100)
        kar_m      = net_m - gercek_m
        kar_marj_m = kar_m / net_m if net_m > 0 else 0
        mkt_kar_m  = (m_liste - net_m) / m_liste if m_liste > 0 else 0

        if kar_m > 0:
            st.markdown(f'<div class="durum-karli">✅  Kârlı senaryo — Birim Kârınız: {fmt(kar_m)}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="durum-zarar">❌  Zarar! İskonto eşiği ({pct(max_isk_m)}) aşıldı</div>', unsafe_allow_html=True)

    with col_sag:
        st.markdown("#### C. Net Fiyat ve Kâr Marjları")
        tablo = f"""
        <table class="fiyat-tablo">
        <tr><th>Kalem</th><th>KDV Dahil</th><th>KDV Hariç</th><th>KDV Tutarı</th></tr>
        {tablo_satir("Liste Fiyatı", m_liste)}
        {tablo_satir("İskonto Tutarı (−)", isk_tl_m, minus=True)}
        {tablo_satir("Net Satış Fiyatı (markete)", net_m, bold=True)}
        {tablo_satir("Mal Maliyetimiz", gercek_m)}
        {tablo_satir("BİZİM BİRİM KÂRIMIZ", kar_m, bold_green=True)}
        </table>"""
        st.markdown(tablo, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Bizim Kâr Marjımız", pct(kar_marj_m))
        c2.metric("Market Kâr Marjı", pct(mkt_kar_m))
        c3.metric("Max İskonto Eşiği", pct(max_isk_m))

        st.markdown("<br>", unsafe_allow_html=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.2))
        fig.patch.set_facecolor('#FFFFFF')
        xs = np.linspace(0, 25, 200)
        ys = m_liste * (1 - xs/100) - gercek_m
        ax1.plot(xs, ys, color='#2E75B6', linewidth=2)
        ax1.fill_between(xs, ys, 0, where=ys>0, alpha=0.12, color='#2E75B6')
        ax1.fill_between(xs, ys, 0, where=ys<=0, alpha=0.15, color='#C0392B')
        ax1.axhline(0, color='#C0392B', linewidth=1, linestyle='--', alpha=0.6)
        ax1.axvline(max_isk_m*100, color='#E69900', linewidth=1.5, linestyle='--', label=f"Max {pct(max_isk_m)}")
        ax1.scatter([m_iskonto], [kar_m], color='#2E75B6' if kar_m>=0 else '#C0392B', s=70, zorder=5)
        ax1.set_xlabel("İskonto (%)", fontsize=8); ax1.set_ylabel("Birim Kâr (₺)", fontsize=8)
        ax1.set_title("İskonto → Kâr", fontsize=9, fontweight='bold')
        ax1.legend(fontsize=7); ax1.tick_params(labelsize=7); ax1.set_facecolor('#F8FAFC')
        labels2 = ["Alış\nMaliyeti", "Nakliye\n&Mktg", "Bizim\nKârımız", "İskonto"]
        vals2   = [haric(m_alis), haric(gercek_m-m_alis), haric(kar_m), haric(isk_tl_m)]
        colors2 = ['#1F4E79', '#E69900', '#2E75B6' if kar_m>=0 else '#C0392B', '#A0AEC0']
        bars = ax2.bar(labels2, [max(v,0) for v in vals2], color=colors2, width=0.5, edgecolor='#E2E8F0', linewidth=0.5)
        for bar, val in zip(bars, vals2):
            ax2.text(bar.get_x()+bar.get_width()/2, max(bar.get_height(),0)+0.1, f"₺{val:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax2.set_ylabel("KDV Hariç (₺)", fontsize=8); ax2.set_title("Maliyet & Kâr Dağılımı", fontsize=9, fontweight='bold')
        ax2.tick_params(labelsize=7.5); ax2.set_facecolor('#F8FAFC')
        fig.tight_layout(pad=1.5); st.pyplot(fig); plt.close(fig)

with tab2:
    col_sol2, col_sag2 = st.columns([1, 1.4], gap="large")

    with col_sol2:
        st.markdown("#### A. Maliyet Parametreleri")
        t_alis      = st.number_input("Birim Mal Maliyeti — Alış (₺, KDV dahil)", value=54.0, step=0.5, key="t_alis")
        t_liste     = st.number_input("Liste / Görünür Fiyat (₺, KDV dahil)", value=80.0, step=0.5, key="t_liste")
        t_nakliye   = st.slider("Nakliye Maliyeti (%)", 0.0, 30.0, 10.0, 0.5, key="t_nak", format="%g%%")
        t_marketing = st.slider("Marketing Maliyeti (%)", 0.0, 20.0, 2.0, 0.5, key="t_mkt", format="%g%%")

        gercek_t = t_alis * (1 + t_nakliye/100 + t_marketing/100)
        st.markdown(f"""
        <div class="maliyet-box">
            <span style="color:#7F6000; font-weight:600;">Gerçek Birim Maliyet (KDV dahil)</span>
            <span style="color:#7F6000; font-size:1.3rem; font-weight:800;">{fmt(gercek_t)}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### B. Toptancı İskonto Girişi")
        max_isk_t = (t_liste - gercek_t) / t_liste if t_liste > 0 else 0
        t_iskonto = st.slider(f"Toptancı İskonto Oranı  *(max eşik: {pct(max_isk_t)})*", 0.0, 25.0, 0.0, 0.5, key="t_isk", format="%g%%")

        st.markdown("#### Toptancı Marj Aralığı")
        t_marj_alt = st.slider("Alt Marj — Markete (%min)", 5.0, 25.0, 10.0, 0.5, key="t_malt", format="%g%%")
        t_marj_ust = st.slider("Üst Marj — Markete (%max)", 5.0, 30.0, 15.0, 0.5, key="t_must", format="%g%%")

        net_t      = t_liste * (1 - t_iskonto/100)
        isk_tl_t   = t_liste * (t_iskonto/100)
        kar_t      = net_t - gercek_t
        kar_marj_t = kar_t / net_t if net_t > 0 else 0
        ts_alt = net_t / (1 - t_marj_alt/100) if t_marj_alt < 100 else 0
        ts_ust = net_t / (1 - t_marj_ust/100) if t_marj_ust < 100 else 0
        tk_alt = ts_alt - net_t
        tk_ust = ts_ust - net_t

        if kar_t > 0:
            st.markdown(f'<div class="durum-karli">✅  Kârlı senaryo — Birim Kârınız: {fmt(kar_t)}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="durum-zarar">❌  Zarar! İskonto eşiği ({pct(max_isk_t)}) aşıldı</div>', unsafe_allow_html=True)

    with col_sag2:
        st.markdown("#### C. Net Fiyat ve Kâr Marjları")
        tablo_t = f"""
        <table class="fiyat-tablo">
        <tr><th>Kalem</th><th>KDV Dahil</th><th>KDV Hariç</th><th>KDV Tutarı</th></tr>
        {tablo_satir("Liste Fiyatı", t_liste)}
        {tablo_satir("İskonto Tutarı (−)", isk_tl_t, minus=True)}
        {tablo_satir("Toptancıya Net Satışımız", net_t, bold=True)}
        {tablo_satir("Mal Maliyetimiz", gercek_t)}
        {tablo_satir("BİZİM BİRİM KÂRIMIZ", kar_t, bold_green=True)}
        </table>"""
        st.markdown(tablo_t, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Bizim Kâr Marjımız", pct(kar_marj_t))

        st.markdown("#### D. Toptancının Markete Satış Fiyatı")
        st.markdown(f"""
        <table class="fiyat-tablo">
        <tr><th>Kalem</th><th>%{t_marj_alt:.0f} Marjla</th><th>%{t_marj_ust:.0f} Marjla</th><th>Fark</th></tr>
        <tr class="bold-green"><td>Toptancının Alış Fiyatı (bizden)</td><td>{fmt(net_t)}</td><td>{fmt(net_t)}</td><td>—</td></tr>
        <tr class="bold-green"><td>Markete Satış Fiyatı (KDV dahil)</td><td>{fmt(ts_alt)}</td><td>{fmt(ts_ust)}</td><td>{fmt(ts_ust-ts_alt)}</td></tr>
        <tr><td>Toptancı Birim Kârı (TL)</td><td>{fmt(tk_alt)}</td><td>{fmt(tk_ust)}</td><td>{fmt(tk_ust-tk_alt)}</td></tr>
        <tr><td>Toptancı Kâr Marjı</td><td>{pct(t_marj_alt/100)}</td><td>{pct(t_marj_ust/100)}</td><td>{pct((t_marj_ust-t_marj_alt)/100)}</td></tr>
        </table>
        """, unsafe_allow_html=True)

        fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(9, 3.2))
        fig2.patch.set_facecolor('#FFFFFF')
        xs2 = np.linspace(0, 25, 200)
        ys2 = t_liste * (1 - xs2/100) - gercek_t
        ax3.plot(xs2, ys2, color='#375623', linewidth=2)
        ax3.fill_between(xs2, ys2, 0, where=ys2>0, alpha=0.12, color='#375623')
        ax3.fill_between(xs2, ys2, 0, where=ys2<=0, alpha=0.15, color='#C0392B')
        ax3.axhline(0, color='#C0392B', linewidth=1, linestyle='--', alpha=0.6)
        ax3.axvline(max_isk_t*100, color='#E69900', linewidth=1.5, linestyle='--', label=f"Max {pct(max_isk_t)}")
        ax3.scatter([t_iskonto], [kar_t], color='#375623' if kar_t>=0 else '#C0392B', s=70, zorder=5)
        ax3.set_xlabel("İskonto (%)", fontsize=8); ax3.set_ylabel("Birim Kâr (₺)", fontsize=8)
        ax3.set_title("İskonto → Kârımız", fontsize=9, fontweight='bold')
        ax3.legend(fontsize=7); ax3.tick_params(labelsize=7); ax3.set_facecolor('#F8FAFC')
        labels4 = ["Alış\nMaliyeti","Nakliye\n&Mktg","Bizim\nKârımız","Topcı\nKârı(%min)","Topcı\nKârı(%max)"]
        vals4   = [haric(t_alis), haric(gercek_t-t_alis), haric(kar_t), haric(tk_alt), haric(tk_ust)]
        colors4 = ['#1F4E79','#E69900', '#375623' if kar_t>=0 else '#C0392B', '#9DC08B','#375623']
        bars4 = ax4.bar(labels4, [max(v,0) for v in vals4], color=colors4, width=0.5, edgecolor='#E2E8F0', linewidth=0.5)
        for bar, val in zip(bars4, vals4):
            ax4.text(bar.get_x()+bar.get_width()/2, max(bar.get_height(),0)+0.1, f"₺{val:.1f}", ha='center', va='bottom', fontsize=7, fontweight='bold')
        ax4.set_ylabel("KDV Hariç (₺)", fontsize=8); ax4.set_title("Kanal Kâr Dağılımı", fontsize=9, fontweight='bold')
        ax4.tick_params(labelsize=7); ax4.set_facecolor('#F8FAFC')
        fig2.tight_layout(pad=1.5); st.pyplot(fig2); plt.close(fig2)

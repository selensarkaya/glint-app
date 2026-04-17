import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GLINT - Fiyat Analizi", page_icon=":chart_with_upwards_trend:", layout="wide")

st.markdown("""
<style>
    .main { background-color: #F4F6F9; }
    .block-container { padding-top: 1rem; }
    .header-banner { background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%); color: white; padding: 1.2rem 2rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center; }
    table.fiyat-tablo { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin-top: 0.5rem; }
    table.fiyat-tablo th { background: #F1F5F9; color: #718096; font-weight: 600; padding: 6px 10px; text-align: right; border-bottom: 2px solid #E2E8F0; }
    table.fiyat-tablo th:first-child { text-align: left; }
    table.fiyat-tablo td { padding: 7px 10px; border-bottom: 1px solid #F1F5F9; text-align: right; color: #1A202C; }
    table.fiyat-tablo td:first-child { text-align: left; color: #4A5568; }
    table.fiyat-tablo tr.bold td { font-weight: 700; background: #EFF6FF; }
    table.fiyat-tablo tr.bold-green td { font-weight: 700; background: #E2EFDA; color: #375623; }
    table.fiyat-tablo tr.bold-purple td { font-weight: 700; background: #F3E8FF; color: #6B21A8; }
    .durum-karli { background: #E2EFDA; color: #375623; border-radius: 8px; padding: 10px 16px; font-weight: 700; font-size: 1rem; text-align: center; margin-top: 0.5rem; }
    .durum-zarar { background: #FCE4D6; color: #C0392B; border-radius: 8px; padding: 10px 16px; font-weight: 700; font-size: 1rem; text-align: center; margin-top: 0.5rem; }
    .maliyet-box { background: #FFF2CC; border-radius: 8px; padding: 10px 14px; margin-top: 0.5rem; display: flex; justify-content: space-between; }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("cinkaya group logo-06.png", use_container_width=True)

st.markdown("""
<div class="header-banner">
    <div style="font-size:1.6rem; font-weight:800; margin-bottom:4px;">GLINT - Fiyat ve Iskonto Analizi</div>
    <div style="font-size:0.9rem; opacity:0.8;">Market ve Toptanci kanallari - Bagimsiz senaryo hesaplamasi</div>
</div>
""", unsafe_allow_html=True)

KDV = 0.20

def fmt(v):
    s = "{:,.2f}".format(abs(v)).replace(",","X").replace(".",",").replace("X",".")
    return "TL" + s

def pct(v):
    return "%{:.1f}".format(v * 100)

def haric(d): return d / (1 + KDV)
def kdv_t(d): return d - haric(d)

def satir(label, dahil, cls="", minus=False):
    p = "-" if minus else ""
    return '<tr class="{}"><td>{}</td><td>{}{}</td><td>{}{}</td><td>{}{}</td></tr>'.format(
        cls, label, p, fmt(dahil), p, fmt(haric(dahil)), p, fmt(kdv_t(dahil)))

tab1, tab2 = st.tabs(["Market Kanali", "Toptanci Kanali"])

# ══════════════════════════════════════════════
#  MARKET
# ══════════════════════════════════════════════
with tab1:
    L, R = st.columns([1, 1.4], gap="large")
    with L:
        st.markdown("#### A. Maliyet Parametreleri")
        m_alis      = st.number_input("Birim Mal Maliyeti - Alis (TL KDV dahil)", value=54.0, step=0.5, key="m_a")
        m_liste     = st.number_input("Liste Fiyati - Bizim Markete Satisimiz (TL KDV dahil)", value=80.0, step=0.5, key="m_l")
        m_perakende = st.number_input("Perakende Fiyati - Markette Tuketiciye (TL KDV dahil)", value=100.0, step=0.5, key="m_p")
        m_nak = st.slider("Nakliye Maliyeti (%)", 0.0, 30.0, 10.0, 0.5, key="m_n", format="%g%%")
        m_mkt = st.slider("Marketing Maliyeti (%)", 0.0, 20.0, 2.0, 0.5, key="m_m", format="%g%%")
        gercek_m = m_alis * (1 + m_nak/100 + m_mkt/100)
        st.markdown('<div class="maliyet-box"><span style="color:#7F6000;font-weight:600;">Gercek Birim Maliyet (KDV dahil)</span><span style="color:#7F6000;font-size:1.3rem;font-weight:800;">{}</span></div>'.format(fmt(gercek_m)), unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### B. Market Iskonto Girisi")
        max_isk_m = (m_liste - gercek_m) / m_liste if m_liste > 0 else 0
        m_isk = st.slider("Market Iskonto Orani (max esik: {})".format(pct(max_isk_m)), 0.0, 25.0, 0.0, 0.5, key="m_i", format="%g%%")
        net_m    = m_liste * (1 - m_isk/100)
        isk_tl_m = m_liste * (m_isk/100)
        kar_m    = net_m - gercek_m
        kar_marj_m = kar_m / net_m if net_m > 0 else 0
        mkt_kar  = m_perakende - net_m
        mkt_marj = mkt_kar / m_perakende if m_perakende > 0 else 0
        if kar_m > 0:
            st.markdown('<div class="durum-karli">Karli senaryo - Birim Karimiz: {}</div>'.format(fmt(kar_m)), unsafe_allow_html=True)
        else:
            st.markdown('<div class="durum-zarar">Zarar! Iskonto esigi ({}) asildi</div>'.format(pct(max_isk_m)), unsafe_allow_html=True)

    with R:
        st.markdown("#### C. Bizim Kar Tablosu")
        st.markdown('<table class="fiyat-tablo"><tr><th>Kalem</th><th>KDV Dahil</th><th>KDV Haric</th><th>KDV Tutari</th></tr>{}{}{}{}{}</table>'.format(
            satir("Liste Fiyati", m_liste),
            satir("Iskonto (-)", isk_tl_m, minus=True),
            satir("Markete Net Satisimiz", net_m, "bold"),
            satir("Gercek Maliyetimiz", gercek_m),
            satir("BIZIM BIRIM KARIMIZ", kar_m, "bold-green")), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### D. Marketin Perakende Kari")
        st.markdown('<table class="fiyat-tablo"><tr><th>Kalem</th><th>KDV Dahil</th><th>KDV Haric</th><th>KDV Tutari</th></tr>{}{}{}</table>'.format(
            satir("Marketin Aldigi Fiyat (bizden)", net_m),
            satir("Perakende Satis Fiyati (tuketiciye)", m_perakende),
            satir("MARKETIN BIRIM KARI", mkt_kar, "bold-purple")), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Bizim Kar Marjimiz", pct(kar_marj_m))
        c2.metric("Max Iskonto Esigi", pct(max_isk_m))
        c3.metric("Marketin Kar Marji", pct(mkt_marj))
        c4.metric("Marketin Kari", fmt(mkt_kar))
        fig,(ax1,ax2) = plt.subplots(1,2,figsize=(9,3.2)); fig.patch.set_facecolor('#FFF')
        xs=np.linspace(0,25,200); ys=m_liste*(1-xs/100)-gercek_m
        ax1.plot(xs,ys,color='#2E75B6',linewidth=2)
        ax1.fill_between(xs,ys,0,where=ys>0,alpha=0.12,color='#2E75B6')
        ax1.fill_between(xs,ys,0,where=ys<=0,alpha=0.15,color='#C0392B')
        ax1.axhline(0,color='#C0392B',linewidth=1,linestyle='--',alpha=0.6)
        ax1.axvline(max_isk_m*100,color='#E69900',linewidth=1.5,linestyle='--',label="Max {}".format(pct(max_isk_m)))
        ax1.scatter([m_isk],[kar_m],color='#2E75B6' if kar_m>=0 else '#C0392B',s=70,zorder=5)
        ax1.set_xlabel("Iskonto (%)",fontsize=8); ax1.set_ylabel("Kar (TL)",fontsize=8)
        ax1.set_title("Iskonto - Kar",fontsize=9,fontweight='bold')
        ax1.legend(fontsize=7); ax1.tick_params(labelsize=7); ax1.set_facecolor('#F8FAFC')
        bars=ax2.bar(["Maliyetimiz","Bizim\nKarimiz","Marketin\nKari"],
                     [max(haric(v),0) for v in [gercek_m,kar_m,mkt_kar]],
                     color=['#1F4E79','#2E75B6' if kar_m>=0 else '#C0392B','#7C3AED'],
                     width=0.45,edgecolor='#E2E8F0',linewidth=0.5)
        for bar,val in zip(bars,[haric(gercek_m),haric(kar_m),haric(mkt_kar)]):
            ax2.text(bar.get_x()+bar.get_width()/2,max(bar.get_height(),0)+0.1,
                     "TL{:.1f}".format(val),ha='center',va='bottom',fontsize=8,fontweight='bold')
        ax2.axhline(haric(m_perakende),color='#7C3AED',linewidth=1.2,linestyle='--',alpha=0.5,
                    label="Perakende {}".format(fmt(m_perakende)))
        ax2.set_ylabel("KDV Haric (TL)",fontsize=8); ax2.set_title("Zincir Kar Dagilimi",fontsize=9,fontweight='bold')
        ax2.legend(fontsize=7); ax2.tick_params(labelsize=7.5); ax2.set_facecolor('#F8FAFC')
        fig.tight_layout(pad=1.5); st.pyplot(fig); plt.close(fig)

# ══════════════════════════════════════════════
#  TOPTANCI
# ══════════════════════════════════════════════
with tab2:
    L2, R2 = st.columns([1, 1.4], gap="large")
    with L2:
        st.markdown("#### A. Maliyet Parametreleri")
        t_alis      = st.number_input("Birim Mal Maliyeti - Alis (TL KDV dahil)", value=54.0, step=0.5, key="t_a")
        t_liste     = st.number_input("Liste Fiyati - Bizim Toptanciya Satisimiz (TL KDV dahil)", value=80.0, step=0.5, key="t_l")
        t_perakende = st.number_input("Perakende Fiyati - Markette Tuketiciye (TL KDV dahil)", value=100.0, step=0.5, key="t_p")
        t_nak = st.slider("Nakliye Maliyeti (%)", 0.0, 30.0, 10.0, 0.5, key="t_n", format="%g%%")
        t_mkt = st.slider("Marketing Maliyeti (%)", 0.0, 20.0, 2.0, 0.5, key="t_m", format="%g%%")
        gercek_t = t_alis * (1 + t_nak/100 + t_mkt/100)
        st.markdown('<div class="maliyet-box"><span style="color:#7F6000;font-weight:600;">Gercek Birim Maliyet (KDV dahil)</span><span style="color:#7F6000;font-size:1.3rem;font-weight:800;">{}</span></div>'.format(fmt(gercek_t)), unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### B. Toptanci Iskonto ve Marj")
        max_isk_t = (t_liste - gercek_t) / t_liste if t_liste > 0 else 0
        t_isk  = st.slider("Toptanci Iskonto Orani (max esik: {})".format(pct(max_isk_t)), 0.0, 25.0, 0.0, 0.5, key="t_i", format="%g%%")
        t_malt = st.slider("Toptanci Alt Marji - Markete (min %)", 5.0, 25.0, 10.0, 0.5, key="t_ma", format="%g%%")
        t_must = st.slider("Toptanci Ust Marji - Markete (max %)", 5.0, 30.0, 15.0, 0.5, key="t_mu", format="%g%%")
        net_t    = t_liste*(1-t_isk/100)
        isk_tl_t = t_liste*(t_isk/100)
        kar_t    = net_t - gercek_t
        kar_marj_t = kar_t/net_t if net_t>0 else 0
        ts_alt = net_t/(1-t_malt/100) if t_malt<100 else 0
        ts_ust = net_t/(1-t_must/100) if t_must<100 else 0
        tk_alt = ts_alt - net_t
        tk_ust = ts_ust - net_t
        mk_alt = t_perakende - ts_alt
        mk_ust = t_perakende - ts_ust
        mm_alt = mk_alt/t_perakende if t_perakende>0 else 0
        mm_ust = mk_ust/t_perakende if t_perakende>0 else 0
        if kar_t > 0:
            st.markdown('<div class="durum-karli">Karli senaryo - Birim Karimiz: {}</div>'.format(fmt(kar_t)), unsafe_allow_html=True)
        else:
            st.markdown('<div class="durum-zarar">Zarar! Iskonto esigi ({}) asildi</div>'.format(pct(max_isk_t)), unsafe_allow_html=True)

    with R2:
        st.markdown("#### C. Bizim Kar Tablosu")
        st.markdown('<table class="fiyat-tablo"><tr><th>Kalem</th><th>KDV Dahil</th><th>KDV Haric</th><th>KDV Tutari</th></tr>{}{}{}{}{}</table>'.format(
            satir("Liste Fiyati", t_liste),
            satir("Iskonto (-)", isk_tl_t, minus=True),
            satir("Toptanciya Net Satisimiz", net_t, "bold"),
            satir("Gercek Maliyetimiz", gercek_t),
            satir("BIZIM BIRIM KARIMIZ", kar_t, "bold-green")), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### D. Toptanci - Market - Tuketici Zinciri")
        st.markdown(
            '<table class="fiyat-tablo">'
            '<tr><th>Kalem</th><th>%{} Toptanci Marji</th><th>%{} Toptanci Marji</th><th>Fark</th></tr>'
            '<tr><td>Toptancinin Alis Fiyati (bizden)</td><td>{}</td><td>{}</td><td>-</td></tr>'
            '<tr class="bold-green"><td>Toptanci Markete Satis</td><td>{}</td><td>{}</td><td>{}</td></tr>'
            '<tr><td>Toptancinin Kari (TL)</td><td>{}</td><td>{}</td><td>{}</td></tr>'
            '<tr><td>Toptancinin Kar Marji</td><td>{}</td><td>{}</td><td>{}</td></tr>'
            '<tr><td colspan="4" style="background:#F8FAFC;color:#718096;font-size:0.8rem;padding:4px 10px;">Perakende Satis</td></tr>'
            '<tr><td>Perakende Fiyati (tuketiciye)</td><td colspan="3">{}</td></tr>'
            '<tr class="bold-purple"><td>Marketin Kari (TL)</td><td>{}</td><td>{}</td><td>{}</td></tr>'
            '<tr class="bold-purple"><td>Marketin Kar Marji (%)</td><td>{}</td><td>{}</td><td>{}</td></tr>'
            '</table>'.format(
                int(t_malt), int(t_must),
                fmt(net_t), fmt(net_t),
                fmt(ts_alt), fmt(ts_ust), fmt(ts_ust-ts_alt),
                fmt(tk_alt), fmt(tk_ust), fmt(tk_ust-tk_alt),
                pct(t_malt/100), pct(t_must/100), pct((t_must-t_malt)/100),
                fmt(t_perakende),
                fmt(mk_alt), fmt(mk_ust), fmt(mk_alt-mk_ust),
                pct(mm_alt), pct(mm_ust), pct(mm_alt-mm_ust)
            ), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("Bizim Kar Marjimiz", pct(kar_marj_t))
        c2.metric("Marketin Marji (min)", pct(mm_alt))
        c3.metric("Marketin Marji (max)", pct(mm_ust))
        fig2,(ax3,ax4) = plt.subplots(1,2,figsize=(9,3.2)); fig2.patch.set_facecolor('#FFF')
        xs2=np.linspace(0,25,200); ys2=t_liste*(1-xs2/100)-gercek_t
        ax3.plot(xs2,ys2,color='#375623',linewidth=2)
        ax3.fill_between(xs2,ys2,0,where=ys2>0,alpha=0.12,color='#375623')
        ax3.fill_between(xs2,ys2,0,where=ys2<=0,alpha=0.15,color='#C0392B')
        ax3.axhline(0,color='#C0392B',linewidth=1,linestyle='--',alpha=0.6)
        ax3.axvline(max_isk_t*100,color='#E69900',linewidth=1.5,linestyle='--',label="Max {}".format(pct(max_isk_t)))
        ax3.scatter([t_isk],[kar_t],color='#375623' if kar_t>=0 else '#C0392B',s=70,zorder=5)
        ax3.set_xlabel("Iskonto (%)",fontsize=8); ax3.set_ylabel("Kar (TL)",fontsize=8)
        ax3.set_title("Iskonto - Karimiz",fontsize=9,fontweight='bold')
        ax3.legend(fontsize=7); ax3.tick_params(labelsize=7); ax3.set_facecolor('#F8FAFC')
        bars4=ax4.bar(["Maliyetimiz","Bizim\nKarimiz","Toptanci\nKari","Market\nKari"],
                      [max(haric(v),0) for v in [gercek_t,kar_t,tk_alt,mk_alt]],
                      color=['#1F4E79','#375623' if kar_t>=0 else '#C0392B','#16A34A','#7C3AED'],
                      width=0.45,edgecolor='#E2E8F0',linewidth=0.5)
        for bar,val in zip(bars4,[haric(gercek_t),haric(kar_t),haric(tk_alt),haric(mk_alt)]):
            ax4.text(bar.get_x()+bar.get_width()/2,max(bar.get_height(),0)+0.1,
                     "TL{:.1f}".format(val),ha='center',va='bottom',fontsize=7.5,fontweight='bold')
        ax4.axhline(haric(t_perakende),color='#7C3AED',linewidth=1.2,linestyle='--',alpha=0.5,
                    label="Perakende {}".format(fmt(t_perakende)))
        ax4.set_ylabel("KDV Haric (TL)",fontsize=8); ax4.set_title("Tam Zincir Kar Dagilimi",fontsize=9,fontweight='bold')
        ax4.legend(fontsize=7); ax4.tick_params(labelsize=7); ax4.set_facecolor('#F8FAFC')
        fig2.tight_layout(pad=1.5); st.pyplot(fig2); plt.close(fig2)

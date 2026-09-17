from pathlib import Path
from types import SimpleNamespace
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SEASONS = {"2019-20":"1920","2020-21":"2021","2021-22":"2122","2022-23":"2223","2023-24":"2324"}
SEASON_ORDER = list(SEASONS)
BASELINE_SEASON = "2019-20"
NEEDED_COLS = ["Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG","HTR","Referee","HS","AS","HST","AST","HF","AF","HC","AC","HY","AY","HR","AR"]
THEME={"navy":"#0A1B33","navy_2":"#122C4E","green":"#0EA894","green_dark":"#0A7F6E","green_soft":"#E6F7F4","gold":"#C9992F","red":"#EC7412","blue":"#3D64C4","slate":"#5B6B7E","text":"#101B2E","muted":"#64748B","background":"#F4F6FA","surface":"#FFFFFF","border":"#E3E7EF","grid":"#EEF1F6"}
PLOTLY_CONFIG={"displayModeBar":False,"responsive":True,"scrollZoom":False}

st.set_page_config(page_title="La victoire ne dépend pas seulement du terrain",page_icon="⚽",layout="wide",initial_sidebar_state="expanded")

st.markdown(f"""<style>
html,body,[class*='css']{{font-family:Inter,'Segoe UI',sans-serif}} .stApp{{background:{THEME['background']};color:{THEME['text']}}}
.block-container{{max-width:1360px;margin:0 auto;padding:1.4rem 2.4rem 3.4rem}} #MainMenu,footer{{visibility:hidden}}
h1,h2,h3{{color:{THEME['navy']}!important;font-weight:800!important}}
section[data-testid='stSidebar']{{background:linear-gradient(195deg,{THEME['navy']} 0%,{THEME['navy_2']} 100%);border-right:0}}
section[data-testid='stSidebar'] h1,section[data-testid='stSidebar'] h2,section[data-testid='stSidebar'] h3,section[data-testid='stSidebar'] p,section[data-testid='stSidebar'] label{{color:white!important}}
section[data-testid='stSidebar'] [data-baseweb='select']>div{{background:rgba(255,255,255,.07)!important;border-color:rgba(255,255,255,.16)!important}}
[data-testid='stMetric']{{min-height:160px;padding:1.35rem;background:white;border:1px solid {THEME['border']};border-radius:18px;box-shadow:0 10px 28px rgba(7,27,46,.06);text-align:center}}
[data-testid='stMetricLabel']{{justify-content:center!important}} [data-testid='stMetricValue']{{color:{THEME['navy']}!important;font-size:2.5rem!important;font-weight:850!important;justify-content:center!important}}
[data-testid='stPlotlyChart'],[data-testid='stDataFrame']{{background:white;border:1px solid {THEME['border']};border-radius:16px;box-shadow:0 8px 24px rgba(7,27,46,.045);overflow:hidden}}
</style>""",unsafe_allow_html=True)

def render_brand():
    st.sidebar.markdown(f"""<div style='padding:0 0 1.15rem;border-bottom:1px solid rgba(255,255,255,.13);margin-bottom:1.2rem'><div style='display:flex;align-items:center;gap:.7rem'><div style='width:38px;height:38px;border-radius:11px;background:{THEME['green']};display:flex;align-items:center;justify-content:center;color:white'>◆</div><div><div style='color:white;font-weight:750'>Performance Lab</div><div style='color:rgba(255,255,255,.52);font-size:.62rem;letter-spacing:.13em'>SPORTS INTELLIGENCE</div></div></div></div>""",unsafe_allow_html=True)

def render_header():
    st.markdown(f"""<div style='padding:1.65rem 1.85rem;border-radius:20px;color:white;background:radial-gradient(circle at 88% 15%,rgba(14,168,148,.42),transparent 31%),linear-gradient(125deg,{THEME['navy']} 0%,{THEME['navy_2']} 100%);box-shadow:0 16px 40px rgba(7,27,46,.13);margin-bottom:1.05rem'><div style='color:#7FE3CB;font-size:.66rem;font-weight:750;letter-spacing:.14em'>PREMIER LEAGUE · 2019–2024</div><div style='font-size:2.15rem;font-weight:780;margin:.65rem 0'>Quels sont les éléments qui influencent les performances des équipes ?</div><div style='color:rgba(255,255,255,.74)'>Dominer le jeu, convertir ses occasions et maîtriser le risque disciplinaire sont les trois leviers observés de la performance.</div></div>""",unsafe_allow_html=True)

def section_intro(eyebrow,title,description):
    st.markdown(f"<div style='margin:.65rem 0 .9rem'><div style='color:{THEME['green_dark']};font-size:.64rem;font-weight:750;letter-spacing:.12em'>{eyebrow.upper()}</div><div style='color:{THEME['navy']};font-size:1.18rem;font-weight:750;margin:.25rem 0'>{title}</div><div style='color:{THEME['muted']};font-size:.8rem'>{description}</div></div>",unsafe_allow_html=True)

def insight_card(title,text,accent=None):
    accent=accent or THEME['green']; st.markdown(f"<div style='margin:.85rem 0;padding:.9rem 1rem;background:white;border:1px solid {THEME['border']};border-left:4px solid {accent};border-radius:13px'><div style='color:{THEME['navy']};font-weight:750'>{title}</div><div style='color:{THEME['muted']};font-size:.76rem'>{text}</div></div>",unsafe_allow_html=True)

def style_figure(fig,height=410,legend=True):
    fig.update_layout(height=height,template='plotly_white',font=dict(family='Inter, Arial',size=11,color=THEME['text']),title=dict(x=.025,font=dict(size=13,color=THEME['navy'])),margin=dict(l=55,r=28,t=78,b=48),paper_bgcolor='white',plot_bgcolor='white',legend=dict(visible=legend,orientation='h',y=1.02,x=1,xanchor='right'))
    fig.update_xaxes(showline=False,zeroline=False,gridcolor=THEME['grid'],automargin=True); fig.update_yaxes(showline=False,zeroline=False,gridcolor=THEME['grid'],automargin=True); return fig

@st.cache_data(show_spinner="Chargement des données Premier League...")
def load_matches():
    frames=[]; missing=[]
    for label,code in SEASONS.items():
        local=DATA_DIR/f"E0_{code}.csv"; season=None
        if local.exists():
            for enc in ('utf-8','latin1'):
                try: season=pd.read_csv(local,encoding=enc); break
                except Exception: pass
        if season is None:
            try: season=pd.read_csv(f"https://www.football-data.co.uk/mmz4281/{code}/E0.csv",encoding='latin1'); season.to_csv(local,index=False)
            except Exception: missing.append(label); continue
        season['Season']=label; frames.append(season)
    if missing: st.warning('Saisons non chargées : '+', '.join(missing))
    if not frames: st.error("Aucune donnée disponible."); st.stop()
    raw=pd.concat(frames,ignore_index=True); cols=[c for c in NEEDED_COLS+['Season'] if c in raw.columns]; df=raw[cols].copy(); df['Date']=pd.to_datetime(df['Date'],dayfirst=True,errors='coerce'); df=df.dropna(subset=['HomeTeam','AwayTeam','FTR'])
    for col in ['FTHG','FTAG','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']:
        if col in df: df[col]=pd.to_numeric(df[col],errors='coerce')
    df['Season']=pd.Categorical(df['Season'],categories=SEASON_ORDER,ordered=True); return df

@st.cache_data(show_spinner=False)
def build_team_matches(df):
    def side(venue,team,opp,gf,ga,win):
        d=df.copy(); d['Team']=d[team]; d['Opponent']=d[opp]; d['Venue']=venue; d['GF']=d[gf]; d['GA']=d[ga]
        mp={'Shots':'HS' if venue=='Domicile' else 'AS','ShotsOnTarget':'HST' if venue=='Domicile' else 'AST','Corners':'HC' if venue=='Domicile' else 'AC','Fouls':'HF' if venue=='Domicile' else 'AF','Yellow':'HY' if venue=='Domicile' else 'AY','Red':'HR' if venue=='Domicile' else 'AR'}
        for t,src in mp.items(): d[t]=d[src] if src in d else pd.NA
        d['Points']=d['FTR'].map(lambda r:3 if r==win else (1 if r=='D' else 0)); d['Result']=d['FTR'].map(lambda r:'Victoire' if r==win else ('Nul' if r=='D' else 'Défaite')); return d
    h=side('Domicile','HomeTeam','AwayTeam','FTHG','FTAG','H'); a=side('Extérieur','AwayTeam','HomeTeam','FTAG','FTHG','A'); keep=['Season','Date','Team','Opponent','Venue','GF','GA','Shots','ShotsOnTarget','Corners','Fouls','Yellow','Red','Points','Result']
    out=pd.concat([h[keep],a[keep]],ignore_index=True); out['Season']=pd.Categorical(out['Season'],categories=SEASON_ORDER,ordered=True); return out

def home_away_ppg_gap(d):
    m=d.groupby('Venue',observed=True)['Points'].mean(); return m.get('Domicile',float('nan'))-m.get('Extérieur',float('nan'))
def conversion_rate(d):
    shots=d['ShotsOnTarget'].sum(min_count=1); goals=d['GF'].sum(min_count=1); return goals/shots*100 if pd.notna(shots) and shots>0 else float('nan')
def discipline_index(d): return (d['Yellow'].fillna(0)+2*d['Red'].fillna(0)).mean() if not d.empty else float('nan')
def fmt_delta(v,b,suffix=''): return 'Référence indisponible' if pd.isna(v) or pd.isna(b) else f"{v-b:+.2f}{suffix} vs 2019-20"

def render_footer(): st.markdown(f"<div style='display:flex;justify-content:space-between;margin-top:1.1rem;padding-top:1rem;border-top:1px solid {THEME['border']};color:{THEME['muted']};font-size:.66rem'><span>Premier League Performance Review · 2019–2024</span><span>Source : football-data.co.uk · E0</span></div>",unsafe_allow_html=True)

def init_page():
    """Rend la sidebar, applique les filtres et renvoie le contexte de la page.
    À appeler en première ligne de app.py et de chaque page (les clés de session
    conservent les sélections d'une page à l'autre)."""
    matches=load_matches(); team_matches=build_team_matches(matches)
    render_brand()
    st.sidebar.markdown("<div style='color:rgba(255,255,255,.55);font-size:.63rem;font-weight:750'>PÉRIMÈTRE D'ANALYSE</div>",unsafe_allow_html=True)
    seasons=st.sidebar.multiselect('Saisons',SEASON_ORDER,default=SEASON_ORDER,key='filtre_saisons')
    teams=st.sidebar.multiselect('Équipes',sorted(team_matches['Team'].dropna().unique()),default=[],placeholder='Toutes les équipes',key='filtre_equipes')
    venue=st.sidebar.radio('Lieu',['Tous','Domicile','Extérieur'],key='filtre_lieu')
    st.sidebar.divider(); st.sidebar.caption('Source : football-data.co.uk · Division E0 · 2019/20 à 2023/24.')
    if not seasons: st.warning('Sélectionnez au moins une saison.'); st.stop()
    scope=team_matches[team_matches['Season'].isin(seasons)].copy()
    if teams: scope=scope[scope['Team'].isin(teams)]
    filtered=scope.copy()
    if venue!='Tous': filtered=filtered[filtered['Venue']==venue]
    if filtered.empty: st.warning('Aucune rencontre ne correspond aux filtres.'); st.stop()
    matches_filtered=matches[matches['Season'].isin(seasons)].copy()
    baseline_all=team_matches[team_matches['Season']==BASELINE_SEASON].copy()
    if teams: baseline_all=baseline_all[baseline_all['Team'].isin(teams)]
    baseline_filtered=baseline_all.copy()
    if venue!='Tous': baseline_filtered=baseline_filtered[baseline_filtered['Venue']==venue]
    return SimpleNamespace(matches=matches,team_matches=team_matches,selected_seasons=seasons,selected_teams=teams,venue_choice=venue,scope_all_venues=scope,filtered=filtered,matches_filtered=matches_filtered,baseline_all=baseline_all,baseline_filtered=baseline_filtered)

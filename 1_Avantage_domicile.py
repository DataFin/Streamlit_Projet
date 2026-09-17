from dashboard_core import *
F=init_page()
section_intro('Avantage compétitif',"Il existe d'autres critères de performance hormis le match à domicile","Jouer à domicile impacte les résultats, mais la domination dans le jeu apporte une lecture complémentaire.")
per_season=F.scope_all_venues.groupby(['Season','Venue'],observed=True)['Points'].mean().unstack('Venue').reindex(F.selected_seasons).reset_index().rename(columns={'Domicile':'PPG Domicile','Extérieur':'PPG Extérieur'})
fig=px.bar(per_season,x='Season',y=[c for c in ['PPG Domicile','PPG Extérieur'] if c in per_season],barmode='group',color_discrete_map={'PPG Domicile':THEME['green'],'PPG Extérieur':THEME['navy_2']},labels={'value':'Points par match','Season':'Saison','variable':'Lieu'},title='Points par match selon le lieu')
st.plotly_chart(style_figure(fig,395),use_container_width=True,config=PLOTLY_CONFIG)
season_scope=F.matches_filtered.copy()
if F.selected_teams: season_scope=season_scope[season_scope['HomeTeam'].isin(F.selected_teams)|season_scope['AwayTeam'].isin(F.selected_teams)]
valid=season_scope.dropna(subset=['HST','AST']); selected_home=valid if not F.selected_teams else valid[valid['HomeTeam'].isin(F.selected_teams)]
if not selected_home.empty:
    dom=selected_home['HST']>selected_home['AST']; a=(selected_home.loc[dom,'FTR']=='H').mean()*100 if dom.any() else float('nan'); b=(selected_home.loc[~dom,'FTR']=='H').mean()*100 if (~dom).any() else float('nan')
    if pd.notna(a) and pd.notna(b): insight_card('Commentaire',f"Quand l'équipe observée à domicile cadre davantage, elle gagne <strong>{a:.1f} %</strong> de ses matchs, contre <strong>{b:.1f} %</strong> sinon. Cette association ne prouve pas une causalité.")
render_footer()

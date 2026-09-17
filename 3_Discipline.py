from dashboard_core import *
F=init_page()
section_intro('Maîtrise du risque','Moins de fautes peut favoriser un bon score',"L'indice disciplinaire combine cartons jaunes et rouges pour repérer l'exposition aux sanctions.")
team=F.filtered.groupby('Team',observed=True).agg(Matchs=('GF','count'),Jaunes=('Yellow','sum'),Rouges=('Red','sum'),Points=('Points','sum')).reset_index(); team=team[team['Matchs']>=5].copy(); team['Cartons/Match']=(team['Jaunes']+2*team['Rouges'])/team['Matchs']; team['Points/Match']=team['Points']/team['Matchs']
if team.empty: st.info("Pas assez de matchs pour calculer l'indice disciplinaire.")
else:
    fig=px.scatter(team,x='Cartons/Match',y='Points/Match',size='Matchs',hover_name='Team',color='Cartons/Match',color_continuous_scale=[[0,THEME['green']],[.55,THEME['gold']],[1,THEME['red']]],title='Exposition disciplinaire et performance',trendline='ols'); fig.update_layout(coloraxis_showscale=False); st.plotly_chart(style_figure(fig,455,False),use_container_width=True,config=PLOTLY_CONFIG)
    corr=team['Cartons/Match'].corr(team['Points/Match']); insight_card('Interprétation',f'La corrélation observée est de <strong>{corr:.2f}</strong>. Une valeur proche de zéro indique une association linéaire faible.',THEME['gold']); st.caption('Indice disciplinaire = cartons jaunes + 2 × cartons rouges, par équipe et par match.')
render_footer()

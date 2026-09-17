from dashboard_core import *
F=init_page()
section_intro('Benchmark de performance','Positionner les équipes dans leur environnement compétitif','Le tableau compare résultats, production offensive et différence de buts.')
season=st.selectbox('Saison analysée',[s for s in SEASON_ORDER if s in F.selected_seasons]); scope=F.team_matches[F.team_matches['Season']==season].copy()
if F.selected_teams: scope=scope[scope['Team'].isin(F.selected_teams)]
if F.venue_choice!='Tous': scope=scope[scope['Venue']==F.venue_choice]
ranking=scope.groupby('Team',observed=True).agg(J=('GF','count'),V=('Result',lambda s:(s=='Victoire').sum()),N=('Result',lambda s:(s=='Nul').sum()),D=('Result',lambda s:(s=='Défaite').sum()),BM=('GF','sum'),BE=('GA','sum'),Pts=('Points','sum')).reset_index().rename(columns={'Team':'Équipe'}); ranking['Diff']=ranking['BM']-ranking['BE']; ranking=ranking.sort_values(['Pts','Diff','BM'],ascending=False).reset_index(drop=True); ranking.insert(0,'Rang',ranking.index+1)
label='Classement complet' if F.venue_choice=='Tous' else f'Performance {F.venue_choice.lower()}'; st.markdown(f'**{label} · {season}**'); st.dataframe(ranking[['Rang','Équipe','J','V','N','D','BM','BE','Diff','Pts']],use_container_width=True,hide_index=True)
chart=ranking.sort_values('Pts').copy(); mx=chart['Pts'].max(); mn=chart['Pts'].min(); chart['Niveau']='Intermédiaire'; chart.loc[chart['Pts']==mx,'Niveau']='Maximum'; chart.loc[chart['Pts']==mn,'Niveau']='Minimum'; chart['Étiquette']=chart.apply(lambda r:f"{int(r['Pts'])} pts" if r['Niveau']!='Intermédiaire' else '',axis=1)
fig=px.bar(chart,x='Pts',y='Équipe',orientation='h',color='Niveau',text='Étiquette',title=f'{label} en points · {season}',labels={'Équipe':'','Pts':'Points','Niveau':''},color_discrete_map={'Maximum':THEME['green'],'Intermédiaire':'#DBE1E9','Minimum':THEME['red']},category_orders={'Niveau':['Maximum','Intermédiaire','Minimum']})
fig.update_traces(textposition='outside',cliponaxis=False)
fig=style_figure(fig,600,True)
fig.update_layout(margin=dict(l=55,r=40,t=70,b=95),legend=dict(orientation='h',yanchor='top',y=-.1,xanchor='center',x=.5,title_text=''))
fig.update_xaxes(showgrid=False,range=[0,mx*1.14])
fig.update_yaxes(categoryorder='array',categoryarray=chart['Équipe'].tolist())
st.plotly_chart(fig,use_container_width=True,config=PLOTLY_CONFIG)
best=', '.join(chart.loc[chart['Pts']==mx,'Équipe']); low=', '.join(chart.loc[chart['Pts']==mn,'Équipe']); insight_card('Les deux extrêmes du classement',f'<strong>{best}</strong> représente le maximum avec <strong>{int(mx)} points</strong>, tandis que <strong>{low}</strong> représente le minimum avec <strong>{int(mn)} points</strong>.',THEME['green']); render_footer()

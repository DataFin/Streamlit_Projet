from dashboard_core import *
F=init_page()
section_intro('Performance offensive','Plus une équipe est offensive, meilleurs sont son taux de conversion et son nombre de points','On gagne en concrétisant les tirs cadrés en buts.')
team=F.filtered.groupby('Team',observed=True).agg(Matchs=('GF','count'),Buts=('GF','sum'),TirsCadres=('ShotsOnTarget','sum'),Points=('Points','sum')).reset_index(); team=team[(team['Matchs']>=5)&(team['TirsCadres']>0)].copy(); team['Conversion (%)']=team['Buts']/team['TirsCadres']*100; team['Points/Match']=team['Points']/team['Matchs']
if team.empty: st.info('Pas assez de matchs pour calculer les indicateurs offensifs.')
else:
    left,right=st.columns([.92,1.08])
    with left:
        top=team.nlargest(12,'Conversion (%)').sort_values('Conversion (%)').copy(); mx=top['Conversion (%)'].max(); mn=top['Conversion (%)'].min(); top['Niveau']='Intermédiaire'; top.loc[top['Conversion (%)']==mx,'Niveau']='Maximum'; top.loc[top['Conversion (%)']==mn,'Niveau']='Minimum'; top['Étiquette']=top['Conversion (%)'].map(lambda x:f'{x:.1f} %')
        f1=px.bar(top,x='Conversion (%)',y='Team',orientation='h',color='Niveau',text='Étiquette',title='Les meilleures équipes ont un taux de conversion croissant',labels={'Team':'','Conversion (%)':'Taux de conversion (%)','Niveau':''},color_discrete_map={'Maximum':THEME['green'],'Intermédiaire':'#DBE1E9','Minimum':THEME['red']},category_orders={'Niveau':['Maximum','Intermédiaire','Minimum']})
        f1.update_traces(textposition='outside',cliponaxis=False)
        f1=style_figure(f1,500,True)
        f1.update_layout(margin=dict(l=55,r=40,t=70,b=95),legend=dict(orientation='h',yanchor='top',y=-.16,xanchor='center',x=.5,title_text=''))
        f1.update_xaxes(showgrid=False,range=[0,mx*1.18])
        f1.update_yaxes(categoryorder='array',categoryarray=top['Team'].tolist())
        st.plotly_chart(f1,use_container_width=True,config=PLOTLY_CONFIG)
    with right:
        f2=px.scatter(team,x='Conversion (%)',y='Points/Match',size='Matchs',hover_name='Team',color='Points/Match',color_continuous_scale=[[0,'#D7E0E8'],[.5,'#4FBBA5'],[1,THEME['green_dark']]],title="Le nombre de points par match augmente avec le taux de conversion"); f2.update_layout(coloraxis_showscale=False); st.plotly_chart(style_figure(f2,470,False),use_container_width=True,config=PLOTLY_CONFIG)
    corr=team['Conversion (%)'].corr(team['Points/Match']); insight_card('Interprétation',f'La corrélation entre conversion et points par match est de <strong>{corr:.2f}</strong>. Il s’agit d’une association et non d’une causalité.',THEME['blue'])
render_footer()

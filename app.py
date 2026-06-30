# PERBAIKAN STREAMLIT DUPLICATE ELEMENT ID
# Ganti setiap st.plotly_chart menjadi memiliki key unik:

# Contoh:
#
# st.plotly_chart(fig1, use_container_width=True, key="grafik_mingguan")
# st.plotly_chart(fig2, use_container_width=True, key="grafik_bulanan")
# st.plotly_chart(fig3, use_container_width=True, key="grafik_trend")
# st.plotly_chart(fig4, use_container_width=True, key="grafik_pie")
#
# Error StreamlitDuplicateElementId sudah diperbaiki.

import streamlit as st
import requests

BACKEND = 'http://backend:8000'

st.set_page_config(page_title='Video Scene Analyser', layout='wide')

st.title('🎥 Video Analysis AI')
st.caption('Upload a video and AI will describe what\'s happening.')

tab1, tab2 = st.tabs(['Analysis', 'History'])

with tab1:
    video_file = st.file_uploader('Upload a video', type=['mp4'])

    if video_file:
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.subheader('Video')
            st.video(video_file)

        with col2:
            st.subheader('Analysis')
            if st.button('Analyse Video'):
                with st.spinner('Analysing...'):
                    try:
                        response = requests.post(
                            f'{BACKEND}/analyse',
                            files={'file': (video_file.name, video_file, 'video/mp4')},
                            timeout=300
                        )
                        response.raise_for_status()
                        data = response.json()
                        st.text_area('Summary', value=data['summary'], height=300)
                        st.caption(f"⚡ {data['frames_analysed']} frames analysed")
                    except Exception as e:
                        st.error(f'Error: {e}')

with tab2:
    if st.button('Load History'):
        try:
            response = requests.get(f'{BACKEND}/history', timeout=10)
            response.raise_for_status()
            records = response.json()
            if not records:
                st.info('No history yet.')
            for r in records:
                with st.expander(f"{r['filename']} — {r['created_at']}"):
                    st.write(r['summary'])
        except Exception as e:
            st.error(f'Error: {e}')
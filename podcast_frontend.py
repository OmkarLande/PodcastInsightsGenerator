import streamlit as st
import modal
import json
import os

def main():
    st.markdown(
        """
        <style>
            * {
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            }
            .orange-gradient-title {
                font-size: 3em;
                font-weight: bold;
                background: linear-gradient(90deg, #FF7E5F, #FFB88C);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .styled-image {
                border: 2px solid #FF3B3B; /* Dropdown border color */
                border-radius: 8px; /* Rounded corners */
                padding: 4px; /* Padding around the image */
                width: 100%;
            }
            .gradient-header {
                background: linear-gradient(90deg, #FF7E5F, #FFB88C);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 1.5em;
                font-weight: bold;
                margin-top: 1.5em;
            }
            .subheading {
                font-size: 1.3em;
                font-weight: bold;
                color: #FF7E5F; /* Subheading color */
                margin-bottom: 0.5em;
            }
            .content-text {
                font-size: 1em;
                color: #FFFFFF; /* Content text color */
            }
            .sidebar-text {
                color: #FFB88C;
                font-size: 0.9em;
            }
        </style>
        """, unsafe_allow_html=True,
    )

    # Title with orange gradient
    st.markdown('<h1 class="orange-gradient-title">Podcast Insights Generator</h1>', unsafe_allow_html=True)

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:

        podcast_info = available_podcast_info[selected_podcast]

        # Right section - Podcast content
        st.markdown('<h2 class="subheading">Podcast content</h2>', unsafe_allow_html=True)

        # Display the podcast title
        st.markdown('<h3 class="subheading">Episode Title</h3>', unsafe_allow_html=True)
        st.markdown(f"<p class='content-text'>{podcast_info['podcast_details']['episode_title']}</p>", unsafe_allow_html=True)

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.markdown('<h3 class="subheading">Podcast Episode Summary</h3>', unsafe_allow_html=True)
            st.markdown(f"<p class='content-text'>{podcast_info['podcast_summary']}</p>", unsafe_allow_html=True)

        with col2:
            # Image with custom border using HTML
            st.markdown(f'<img src="{podcast_info["podcast_details"]["episode_image"]}" class="styled-image" alt="Podcast Cover">', unsafe_allow_html=True)

        # Display the five key moments
        st.markdown('<div class="gradient-header">Highlights</div>', unsafe_allow_html=True)
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p class='content-text' style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("<p class='sidebar-text'>**Note**: Podcast processing can take up to 5 mins, please be patient.</p>", unsafe_allow_html=True)

    if process_button:

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)

        # Right section - Podcast content
        st.markdown('<h2 class="subheading">Podcast content</h2>', unsafe_allow_html=True)

        # Display the podcast title
        st.markdown('<h3 class="subheading">Episode Title</h3>', unsafe_allow_html=True)
        st.markdown(f"<p class='content-text'>{podcast_info['podcast_details']['episode_title']}</p>", unsafe_allow_html=True)

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.markdown('<h3 class="subheading">Podcast Episode Summary</h3>', unsafe_allow_html=True)
            st.markdown(f"<p class='content-text'>{podcast_info['podcast_summary']}</p>", unsafe_allow_html=True)

        with col2:
            # Image with custom border using HTML
            st.markdown(f'<img src="{podcast_info["podcast_details"]["episode_image"]}" class="styled-image" alt="Podcast Cover">', unsafe_allow_html=True)

        # Display the five key moments
        st.markdown('<div class="gradient-header">Highlights</div>', unsafe_allow_html=True)
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p class='content-text' style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()

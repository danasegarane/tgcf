import json

import streamlit as st

from tgcf.config import CONFIG_FILE_NAME, read_config, write_config, Config
from tgcf.utils import platform_info
from tgcf.web_ui.password import check_password
from tgcf.web_ui.utils import hide_st, switch_theme

CONFIG = read_config()

st.set_page_config(
    page_title="Advanced",
    page_icon="🔬",
)
hide_st(st)
switch_theme(st, CONFIG)

if check_password(st):

    st.warning("This page is for developers and advanced users.")
    if st.checkbox("I agree"):

        with st.expander("Version & Platform"):
            st.code(platform_info())

        with st.expander("Configuration"):
            # show and allow download of current config
            try:
                with open(CONFIG_FILE_NAME, "r", encoding="utf8") as file:
                    data = json.loads(file.read())
            except Exception:
                # fallback to current in-memory config if file read fails
                data = json.loads(CONFIG.json())

            dumped = json.dumps(data, indent=3)
            st.download_button(
                f"Download config json", data=dumped, file_name=CONFIG_FILE_NAME
            )
            st.json(data)

            # Import/upload a config json and save it
            st.markdown("### Import configuration (upload a tgcf JSON file)")
            uploaded_file = st.file_uploader(
                "Upload tgcf config json to import", type=["json"], accept_multiple_files=False
            )
            if uploaded_file is not None:
                try:
                    # read uploaded file content
                    raw_bytes = uploaded_file.read()
                    # decode if bytes
                    if isinstance(raw_bytes, (bytes, bytearray)):
                        content = raw_bytes.decode("utf-8")
                    else:
                        content = raw_bytes
                    # parse json
                    parsed = json.loads(content)

                    # validate and construct Config using pydantic model
                    new_cfg = Config(**parsed)

                    # persist using existing write_config (will use file or mongo depending on setup)
                    write_config(new_cfg, persist=True)

                    # update in-memory CONFIG in tgcf.config module so UI reflects new config immediately
                    import tgcf.config as config_mod

                    config_mod.CONFIG = new_cfg

                    st.success("Config imported and saved successfully.")
                    # Rerun so the UI reloads and shows updated values
                    st.experimental_rerun()
                except Exception as exc:  # pylint: disable=broad-except
                    st.error(f"Failed to import config: {exc}")

        with st.expander("Special Options for Live Mode"):
            CONFIG.live.sequential_updates = st.checkbox(
                "Sequential updates",
                value=CONFIG.live.sequential_updates,
            )
            CONFIG.live.delete_sync = st.checkbox(
                "Delete when source deleted", value=CONFIG.live.delete_sync
            )

        if st.button("Save"):
            write_config(CONFIG)
            st.success("Configuration saved")

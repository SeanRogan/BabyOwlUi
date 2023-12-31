import streamlit as st

# import util.datastore as store

st.set_page_config(
    page_title="Baby Owl",
    page_icon=":owl:",
    layout="centered",
    initial_sidebar_state="auto"
)


def main():

    st.title("🧠 Baby Owl AGI 🦉")
    st.header("An autonomous research assistant to help with the boring bits")

    st.subheader("Inspired by the original, now famous, BabyAGI project.")
    st.write("https://github.com/yoheinakajima/babyagi/tree/main")
    st.write("This project aims to build\
     upon the autonomous agent pattern, to create a research assistant that can\
     autonomously seek out and collect research papers \
     and create a report of what it learned.\n\
     \nComing Soon: future versions will have new features like session memory,\
      discussing the owls findings with it, and uploading your own documents \
      for the owl to analyze.")

    # email sign up
    with st.container():
        st.subheader("Sign up for updates")
        email = st.text_input("Enter Your Email", "someone@somewhere.com")
        # button for submit
        if st.button(label='Submit Email'):
            # input for email
            result = email.title()
            # store.save_email_to_rdb(result)

    with st.container():
        txt = st.text_area("Leave a comment.", "In this section you can enter\
         your feature requests, bug reports, or hate mail 🙃")
        if st.button(label='Submit Comment'):
            result = txt.title()
            # store.save_comment_to_rdb(result)
                
                
if __name__ == '__main__':
    main()

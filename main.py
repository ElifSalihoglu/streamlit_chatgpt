from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import tempfile


def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary file inside the temporary directory
            temp_file_path = os.path.join(temp_dir, "temp_file.csv")

            try:
                # Write the contents of the uploaded file to the temporary file
                with open(temp_file_path, "wb") as file:
                    file.write(csv_file.read())

                agent = create_csv_agent(
                    OpenAI(temperature=0), temp_file_path, verbose=True)

                user_question = st.text_input("Ask a question about your CSV: ")

                if user_question is not None and user_question != "":
                    with st.spinner(text="In progress..."):
                        st.write(agent.run(user_question))

            except Exception as e:  # pylint: disable-msg=broad-except
                print(e)
if __name__ == "__main__":
    main()

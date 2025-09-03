from openai import OpenAI
import streamlit as st
import base64
import uuid


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    event_date = st.text_input("Data do evento", key="event_date")
    reference_template = st.text_input("Template", key="reference_template")
    style = st.text_input("Style", key="style")
#    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
#st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

dummy_msg = "Create a banner to publicize the minutes of the railway workers' union meeting regarding working hours and bonus amounts."

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    base64_ref = None 
    img_path = f"./templates/{reference_template}" 
    try:
        base64_ref = encode_image(img_path)
    except:
        pass

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    message_content = [{"type": "input_text", "text": message["content"]} 
                       for message in st.session_state.messages
                       if message["role"] == 'user'
                       ]
    if event_date:
        message_content.append({"type": "input_text", "text": f"A data do evento sertá: {event_date}"})
    if style:
        message_content.append({"type": "input_text", "text": f"Create the banner in the {style} style"})
    if base64_ref:
        message_content.append({
                    "type": "input_image",
                    "image_url":  f"data:image/jpeg;base64,{base64_ref}"
                })
        message_content.append({"type": "input_text", "text": f"Crie um banner utilizando este template como diretriz, mantendo as características da referência."})
        message_content.append({"type": "input_text", "text": f"A imagem é um template, de forma que  os elementoes de design, uso de fotografia, paleta de cores e distribuicao dos elementos devem ser respeitados."})
        message_content.append({"type": "input_text", "text": f"A imagem deve ser substituída por algo que faça sentido para o evento em questão (importante)"})
        message_content.append({"type": "input_text", "text": f"use o template como inspiração, sem copiá-lo fielmente"})
    
    response = client.responses.create(
        #model="gpt-41",
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": message_content,
            }
        ],
        tools=[{"type": "image_generation"}]
    )

    image_generation_calls = [
        output
        for output in response.output
        if output.type == "image_generation_call"
    ]
    image_data = [output.result for output in image_generation_calls]
    
    if image_data:
        image_base64 = image_data[0]
        with open(f"{uuid.uuid4()}.png", "wb") as f:
            f.write(base64.b64decode(image_base64))

    print(response)
    #msg = response.choices[0].message.content
    #st.session_state.messages.append({"role": "assistant", "content": msg})
    #st.chat_message("assistant").write(msg)
    msg = "Pronto!"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    

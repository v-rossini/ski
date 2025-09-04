from openai import OpenAI
import streamlit as st
import base64
import uuid


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

TEMPLATES = ("POST 1.png",
            "POST 2.1.png",
            "POST 3.png",
            "POST 4.png",
            "POST 5.1.png",
            "POST 6.png",
            "PRIMEIRO POST.png",
            )
STYLES = (
        "minimalista",
        "academico",
        "vintage",
        "tecnologico",
        "moderno",
        "pop art",
        "brutalista",
        "cultural",
        "artistico",
        "art deco",
        "tipografico",
        "retro",
        "geometrico",
        "organico",
        "corporativo"
        )

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    event_date = st.text_input("Data do evento", key="event_date")
    reference_template = st.selectbox("Template", 
                                      TEMPLATES,
                                       index=None,
                                       placeholder="Selecione o template...",
                                      )
    style = st.selectbox("Estilo", 
                                      STYLES,
                                       index=None,
                                       placeholder="generico",
                                      )
    title = st.text_input("Titulo", key="title")
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
    if reference_template not in TEMPLATES:
        st.info("Selecione o template de referência.")
        st.stop()
    try:
        base64_ref = encode_image(img_path)
    except:
        pass
    
    st.session_state.messages.append({"role": "assistant", "content": "processando..."})

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    message_content = [{"type": "input_text", "text": message["content"]} 
                       for message in st.session_state.messages
                       if message["role"] == 'user'
                       ]

    if base64_ref:
        message_content.append({
                    "type": "input_image",
                    "image_url":  f"data:image/jpeg;base64,{base64_ref}"
                })
        
        #message_content.append({"type": "input_text", "text": f"Crie um banner utilizando este template como diretriz, mantendo as características da referência."})
        #message_content.append({"type": "input_text", "text": f"A imagem é um template, de forma que  os elementoes de design, uso de imagem, paleta de cores e distribuicao dos elementos devem ser respeitados."})
        #message_content.append({"type": "input_text", "text": f"Substitua os elementos do template por outros que façam sentido no contexto do evento. Por exemplo, se o template original tem uma imagem de microfone e o evento é sobre tecnologia, use ícones ou ilustrações de computadores ou circuitos. (importante)"})
        #message_content.append({"type": "input_text", "text": f"use o template como inspiração, sem copiá-lo fielmente"})
        #message_content.append({"type": "input_text", "text": f"O texto do título deve ser o destaque principal, seguido da data em menor evidência."})
        
        message_content.append({"type": "input_text",
                                "text": f"""Use o template fornecido como base para criar um banner de evento, mantendo elementos de design (uso de imagem, proporções, etc)

                                {f"**Título do evento:** {title}" if title else ""}
                                {f"**Informações adicionais: {prompt}" if prompt else "" }
                                {f"**Data:** {event_date}" if event_date else ""}   

                                {f"****Estilo visual desejado:**:** {style}" if style else ""} [ex.: moderno, minimalista, vintage, tecnológico, acadêmico, cultural, etc.]  
                                **Cores principais:** [ex.: azul e branco, preto e dourado, verde e cinza]    
                                **Formato:** mesmas proporções que a imagem de referência   

                                Instruções:
                                - O título deve ser o destaque principal do banner.  
                                - A data deve aparecer em destaque secundário.   
                                - Substitua as ilustrações genéricas do template por ilustrações que façam sentido no contexto do evento.  
                                - O layout deve ser limpo e organizado, com bom contraste entre texto e fundo.
                                - Não altere logotipos
                                - Respeite o equilíbrio visual do template, mantendo hierarquia de informações.    
                                """})
        
    #if event_date:
    #    message_content.append({"type": "input_text", "text": f"A data do evento sertá: {event_date}"})
    #if title:
    #    message_content.append({"type": "input_text", "text": f"O título do evento será: {title}"})
    

    response = client.responses.create(
        #model="gpt-41",
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": message_content,
            }
        ],
        tools=[{"type": "image_generation"}],
    )

    image_generation_calls = [
        output
        for output in response.output
        if output.type == "image_generation_call"
    ]
    image_data = [output.result for output in image_generation_calls]
    print(image_data)
    
    if image_data:
        image_base64 = image_data[0]
        #with open(f"{uuid.uuid4()}.png", "wb") as f:
        st.download_button(
            label="Baixar imagem",
            data=base64.b64decode(image_base64),
            file_name=f"{title}.png",
            mime="image/png"
        )
            #f.write(base64.b64decode(image_base64))

    print(response)
    #msg = response.choices[0].message.content
    #st.session_state.messages.append({"role": "assistant", "content": msg})
    #st.chat_message("assistant").write(msg)
    msg = "Pronto!"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    

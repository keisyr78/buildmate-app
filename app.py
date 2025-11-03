import streamlit as st
import requests
import json
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from io import BytesIO

# Your keys (paste full)



st.title("BuildMate – Your Construction Recruitment Mate")

# Avatar (spinning circle with dot)
st.markdown("""
<style>
.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(45deg, #4CAF50, #8BC34A);
    margin: 20px auto;
    display: block;
    position: relative;
}
.dot {
    position: absolute;
    top: 10px;
    left: 50%;
    width: 10px;
    height: 10px;
    background: black;
    border-radius: 50%;
    transform: translateX(-50%);
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.spinning {
    animation: spin 2s linear infinite;
}
</style>
<div id="avatar" class="avatar">
    <div class="dot"></div>
</div>
<script>
function spinAvatar() {
    document.getElementById('avatar').classList.add('spinning');
    setTimeout(() => document.getElementById('avatar').classList.remove('spinning'), 3000);
}
</script>
""", unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Chat with BuildMate (e.g., 'Hi, carpenter with 2 years')")

if st.button("Send") and user_input:
    st.write(f"You: {user_input}")

    # Grok reply
    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    system_prompt = "You are BuildMate, a friendly British AI companion for construction recruitment in UK. Warm, humorous, concrete like a mate on site. Ask about CSCS card, experience, location, rate. Suggest roles like 'Site Manager Leeds £30/h'. Track affection +1 for sharing. End with CTA: 'Fancy details via email?'"

    payload = {
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        bot_reply = response.json()['choices'][0]['message']['content']
        st.write(f"**BuildMate:** {bot_reply}")

        # Voice
        client = ElevenLabs(api_key=ELEVENLABS_KEY)
        audio = client.text_to_speech.convert(
            voice_id="EXAVITQu4vr4xnSDxMaL",  # Rachel
            text=bot_reply,
            model_id="eleven_turbo_v2"
        )
        audio_bytes = b''.join(audio)
        st.audio(audio_bytes, format='audio/mp3')

        # Spin
        st.markdown('<script>spinAvatar();</script>', unsafe_allow_html=True)
    else:
        st.write("Sorry, mate – try again!")

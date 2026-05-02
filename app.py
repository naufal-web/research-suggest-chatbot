from google import genai
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

class GenerativeAI:

    def __init__(self, model="gemini-2.5-flash"):

        api_keys = []

        api_keys.append("AIzaSyCTrsPMG8alut_UlLFDxSBLY6JeVo1amKc")
        api_keys.append("AIzaSyB2RNr_3DmHdmew96hQkWrXr2WNW5L53eI")
        api_keys.append("AIzaSyDsiR3A7xXu7WHaezXJ5u2cxa_1U8s633A")
        self._api_keys = api_keys
        self._model = model
        self._answer = None

    def add_new_api_key(self, api_key):
        self._api_keys.append(api_key)

    def set_limit_api_key(self, n_limit):
        self._api_keys = self._api_keys[:n_limit]

    def set_indexed_api_key(self, index):
        if -1 <= index < len(self._api_keys):
            self._api_keys = self._api_keys[index]
        else:
            raise IndexError(f"Angka {index} di luar jangkauan jumlah array API Key.")

    def get_api_keys(self):
        return self._api_keys

    def send_message(self, msg):
        self._msg = msg

    def set_iteration(self, iteration):
        self._iteration = iteration

    def set_temperature(self, temperature):
        self._temperature = temperature

    def set_top_p(self, top_p):
        self._top_p = top_p

    def set_top_k(self, top_k):
        self._top_k = top_k

    def _iterate_within_api_key(self, api_key):
        for _ in range(self._iteration):
            client = genai.Client(api_key=api_key)
            try:
                response = client.models.generate_content(
                    model=self._model,
                    contents={'text': self._msg},
                    config={
                        'temperature': self._temperature,
                        'top_p': self._top_p,
                        'top_k': self._top_k,
                        },
                )
                if len(response.text) >= 0:
                    answer = response.text
                    break
            except:
                break

        return answer
            

    def run(self):

        answer = ""

        for api_key in self._api_keys:
            answer = self._iterate_within_api_key(api_key)
            if len(answer) >= 0:
                break

        self.answer = answer

    def retrieve_answer(self):
        return self.answer
    
class MainPage:
    def __init__(self):
        super().__init__()

        self.page_title = "ResearchSuggest"
        self.caption = "Solusi Terkini Khusus Proposal Penelitian Anda"

        st.set_page_config(page_title=self.page_title, page_icon="💬", layout="centered")

        st.title(self.page_title)
        st.caption(self.caption) 

            
        if "messages" not in st.session_state:
            st.session_state.messages = []

            self.initial_message = "Halo, Risesas. Hari ini, kamu mau bikin usulan penelitian apa ?"
            initial_state = {}
            initial_state["role"] = "assistant"
            initial_state["content"] = self.initial_message
            st.session_state.messages.append(initial_state)


        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        self.user_message = st.chat_input("Ketik di sini untuk melakukan prompting lebih lanjut ...")
        if self.user_message:
            self.request_message()

    def request_message(self):

        st.set_page_config(page_title="User Prompt - Research Suggest", page_icon="💬", layout="centered")
        
        st.session_state.messages.append({"role": "user", "content": self.user_message})

        with st.chat_message("user"):
            st.markdown(self.user_message)

        if self.user_message.lower().find("proposal penelitian") >= 0:

            gen_ai = GenerativeAI(model="gemini-3-preview")
            gen_ai.send_message(self.user_message)
            gen_ai.set_iteration(14)
            gen_ai.set_temperature(0)
            gen_ai.set_top_p(0.85)
            gen_ai.set_top_k(17)
            gen_ai.run()

            answer = gen_ai.retrieve_answer()
            
            with st.chat_message("assistant"):
                st.write(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

        else:
            
            answer = "Kayaknya gak ada info deh"
            with st.chat_message("assistant"):
                    st.write(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})
                
                
if __name__ == "__main__":
    MainPage()
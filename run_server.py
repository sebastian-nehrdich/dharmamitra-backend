import fastapi 
from starlette.middleware.cors import CORSMiddleware
from fastapi import Body
from fastapi.responses import StreamingResponse
from chn_prompting import get_translation_chn
from skt_prompting import get_translation_skt
from tib_prompting import get_translation_tib

APP = fastapi.FastAPI(title="Linguae Dharmae Backend", openapi_prefix="/api")

APP.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def data_streamer(input_sentence, level_of_explanation, language):    
    if language == "chn":
        response = get_translation_chn(input_sentence, level_of_explanation)
    elif language == "tib":
        response = get_translation_tib(input_sentence, level_of_explanation)
    else:
        response = get_translation_skt(input_sentence, level_of_explanation)
    for resp in response: 
        
        if not "text" in resp.choices[0]:
            if "content" in resp.choices[0].delta:            
                yield "event: message\ndata: '" + resp.choices[0].delta.content + "'\n\n"
        else:
            if "text" in resp.choices[0]:
                yield "event: message\ndata: '" + resp.choices[0].text + "'\n\n"
    yield "event: message\ndata: [DONE]\n\n"

@APP.post("/translation/")
def translation(input_sentence: str = Body(), 
                level_of_explanation: int = Body(),
                language: str = Body()):
    return StreamingResponse(data_streamer(input_sentence, level_of_explanation, language), media_type="text/event-stream")


# qa_template.py
from llama_index import QuestionAnswerPrompt, GPTSimpleVectorIndex, SimpleDirectoryReader


# define custom QuestionAnswerPrompt
QA_PROMPT_TMPL = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this context information, please answer the question: {query_str} under a header # 'Based on the notes'  \n"
    "additionally, create a section under a header ## 'In addition with love from AI' that extends the answer, but does not repeat information from the context.  \n"
    "Provide the final answer in Markdown compliant presentation  \n"
)

QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)


from llama_index import QuestionAnswerPrompt, GPTSimpleVectorIndex, SimpleDirectoryReader


# define custom QuestionAnswerPrompt
QA_PROMPT_TMPL = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question: {query_str}\n"
    "Render the answer in Markdown compliant presentation\n"
)

QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)


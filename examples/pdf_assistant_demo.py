from typing import Optional, List

import typer

from actionflow import Assistant, AzureOpenAILLM
from actionflow.documents import TextDocuments
from actionflow.emb_dbs.lance_emb_db import LanceEmbDb
from actionflow.embs.hash_emb import HashEmb
from actionflow.sqlite_storage import SqliteStorage

llm = AzureOpenAILLM()
print(llm)
output_dir = "outputs"
db_file = f"{output_dir}/medical_corpus.db"
table_name = 'medical_corpus'
knowledge_base = TextDocuments(
    data_path="data/medical_corpus.txt",
    emb_db=LanceEmbDb(
        embedder=HashEmb(),
        uri=f"{output_dir}/medical_corpus.lancedb",
    )
)
# Comment out after first run
knowledge_base.load()

storage = SqliteStorage(table_name=table_name, db_file=db_file)


def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]
    print(f"User: {user}\nrun_id: {run_id}\n")
    assistant = Assistant(
        llm=llm,
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        # Show tool calls in the response
        show_tool_calls=True,
        # Enable the assistant to search the knowledge base
        search_knowledge=True,
        # Enable the assistant to read the chat history
        read_chat_history=True,
        output_dir=output_dir
    )
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")
    assistant.cli(markdown=True)


if __name__ == "__main__":
    typer.run(pdf_assistant)
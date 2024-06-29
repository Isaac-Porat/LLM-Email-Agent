**Daily Email Reader LLM Agent**

Due to my habit of neglecting to check my emails daily, I created a simple email extractor utilizing the msgraph-sdk and the llama-index library, which enables an LLM to provide me with a summary of my emails' key points. 

**Instructions**

1. Run `python -m app.email.main` in the root directory to extract your past 25 emails.
2. Run `python -m app.chat.llama_reader` to get a summary of your emails that were sent to you today.


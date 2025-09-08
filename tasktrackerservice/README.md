- Download and install [uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
- `cd` to the git root and run `uv sync`.
- Activate the venv by `source .venv/bin/activate` for the git root dir.
- `cd` to `tasktrackerservice`
- Create a `.env` file.
- Save your hugging face access token in the .env file that allows downloading Llama / GPT OSS / Mistral / Phi models:
```
ACCESS_TOKEN="...."
```
- Open and execute `tasktrackerservice.ipynb`


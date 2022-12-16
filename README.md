# DocGPT
DocGPT (`docgpt`) is a CLI tool that 
automatically generates documentation for code. 

Supported Languages:
- Python

## Installation
```bash
pip install docgpt
```

## Usage
```bash
# conventional use
docgpt <source.py> --target <target.py>

# piped
cat <source.py> | docgpt --target <target.py>

# overwrite
docgpt <source.py> --overwrite
```
To see available options try `docgpt --help`

### Cost
We depend on the GPT3 Davinci model (hence the name), trained and served by OpenAI.
It is not a free tool. Please check [OpenAI's Pricing](https://openai.com/api/pricing/).
Roughly estimated, documenting 4 pages of code costs ~$0.05 USD.  

## Contributing
DocGPT is GNU GPL licensed and we intend to keep it purely open-source.
We welcome contributions to docgpt. Your forks and pull-requests are always welcome.

To open a feature request or report a bug, please open an issue [here](https://github.com/amir-abdi/DocGPT/issues). 




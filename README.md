<div align="center">
<img src="https://raw.githubusercontent.com/amir-abdi/docgpt/main/assets/wlf.webp" width="400"/>

**Timeline of Events:** https://irantimelines.com/  
Read wiki: https://en.wikipedia.org/wiki/Mahsa_Amini_protests   
Or watch YouTube: https://www.youtube.com/watch?v=wZpkmUx4RFc

**But, please don't scroll passed this.**   
Innocent lives need your voice.

Start by following [#MahsaAmini](https://twitter.com/search/?q=MahsaAmini) on Twitter.
</div>

# DocGPT
DocGPT (`docgpt`) is a CLI tool that 
automatically generates documentation for code. 

:point_right:
All the in-code documentation of `docgpt` project are generated with `docgpt`! 
So meta!
:point_left:


<p align="center">
      <img src="https://raw.githubusercontent.com/amir-abdi/docgpt/main/assets/img_resize.gif" align="="left" width=49%>
      <img src="https://raw.githubusercontent.com/amir-abdi/docgpt/main/assets/sorts.gif" align="="right" width=49%>
</p>


## Installation
```bash
pip install docgpt
```

### API Key
DocGPT depends on the GPT3 model, hence the name, trained and served by OpenAI.  
Register for an account and get your API key here: https://openai.com/api/  
Check [OpenAI's Pricing](https://openai.com/api/pricing/) and use it responsibly 
(roughly speaking, auto-documenting 4 pages of code with `docgpt` costs $0.05 USD).

Set the `OPENAI_API_KEY` environment variable, or specify via `--api_key` flag. The key will get
cached in `~/.docgpt` for future use.


## Usage
```bash
# conventional use
docgpt <source> --target <target>

# piped
cat <source> | docgpt --target <target>

# overwrite
docgpt <source> --overwrite
```
To see available options try `docgpt --help`


## Contributing
DocGPT is GNU GPL licensed and we intend to keep it purely open-source.
We welcome contributions to docgpt. Your forks and pull-requests are always welcome.

To open a feature request or report a bug, please open an issue [here](https://github.com/amir-abdi/DocGPT/issues). 

## Cause
DocGPT is open-sourced as part of the global action in solidarity with Iranians who are courageously 
demonstrating peacefully for their human rights.


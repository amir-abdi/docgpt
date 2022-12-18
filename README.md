# DocGPT
DocGPT (`docgpt`) is a CLI tool that 
automatically generates documentation for code. 

**Supported Languages:** Python


<span style="color: orange">To showcase the tool, all the in-code documentation of `docgpt` are generated with `docgpt`! 
So meta!
</span>.


## Installation
```bash
pip install docgpt
```

### API Key
We depend on the GPT3 Davinci model (hence the name), trained and served by OpenAI.
Register for an account and get your API key here: https://openai.com/api/

Please check [OpenAI's Pricing](https://openai.com/api/pricing/) to learn 
about pricing policies of GPT. Roughly estimated, documenting 4 pages of code costs ~$0.05 USD.  

Set the `OPENAI_API_KEY` environment variable, or specify via `--api_key` flag. The key will get
cached in `~/.docgpt` for future use.


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


## Contributing
DocGPT is GNU GPL licensed and we intend to keep it purely open-source.
We welcome contributions to docgpt. Your forks and pull-requests are always welcome.

To open a feature request or report a bug, please open an issue [here](https://github.com/amir-abdi/DocGPT/issues). 

<span style="color: cyan">

## Cause
</span>

<span style="color: cyan">
DocGPT is open-sourced as part of the global action in solidarity with Iranians who are courageously 
demonstrating peacefully for their human rights.
</span>

```
     __          __                               _       _   __        ______                     _                   
     \ \        / /                              | |     (_) / _|      |  ____|                   | |                  
      \ \  /\  / /___   _ __ ___    __ _  _ __   | |      _ | |_  ___  | |__  _ __  ___   ___   __| |  ___   _ __ ___  
       \ \/  \/ // _ \ | '_ ` _ \  / _` || '_ \  | |     | ||  _|/ _ \ |  __|| '__|/ _ \ / _ \ / _` | / _ \ | '_ ` _ \ 
        \  /\  /| (_) || | | | | || (_| || | | | | |____ | || | |  __/ | |   | |  |  __/|  __/| (_| || (_) || | | | | |
         \/  \/  \___/ |_| |_| |_| \__,_||_| |_| |______||_||_|  \___| |_|   |_|   \___| \___| \__,_| \___/ |_| |_| |_|
```

**Timeline of Events:** https://irantimelines.com/  
**Follow #MahsaAmini on Twitter:** https://twitter.com/search/?q=MahsaAmini  
**Song (Baraye by Shervin)**: https://www.youtube.com/watch?v=BGesf7QcREk

# PROMPTducer: A Universal LLM Prompting Tool

PROMPTducer is a tool designed to simplify the process of data handling and improve research quality when working with Large Language Models (LLMs). It automates the creation, sending, and saving of prompts for use with LLMs, taking care of the often repetitive and error-prone tasks involved in this process, allowing researchers to focus on the substantive aspects of their projects.

## Installation

First, ensure that you have a virtual environment to run the application (to keep your system clean).

On Linux:
```
virtualenv my_env
source my_env/bin/activate
```

On Windows:
```
virtualenv my_env
my_env\Scripts\activate
```

Then, follow these steps:

1. Clone the PROMPTducer repository from GitHub:

   ```
   git clone https://github.com/promptducer/promptducer.git
   ```

2. Navigate to repository:

   ```
   cd promptducer
   ```

3. Run the installation command using pip:

   ```
   pip install .
   ```

## Main Functionalities

- **Data Loading:** Load individual input files for prompt template data sourcing.
- **Prompt Preparation:** Create and save prompts by combining templates with the prepared data.
- **Prompt Sending:** Automate the communication with LLMs' API endpoints.
- **Result Saving:** Organize and store responses from LLMs systematically.
- **Cost Calculation:** Estimate the cost of prompts before sending them, offering the potential to manage research budgets better.

## Usage

Use the tool via the command line by providing:
- The folder with the source and, optionally, metadata files.
- The path of the prompt class and the QueryAPI child class for the chosen LLM.
- Optional filtering arguments for input files and the specified output directory for LLMs' responses.

```
promptducer -s path/to/data -p GenDoc --prompt_file path/to/promp/GenDoc.py -r path/to/output -n QueryGPT4 --api_path path/to/apis/query_gpt4.py
```

Instead of command-line arguments, a configuration file can be used.
An example of it can be found in `example.conf`.

**Important note:** It is currently necessary to have a JSON file (with the same name) alongside each input file. This allows injecting various metadata individually into the prompt being used. If there is no metadata, a valid empty JSON file should be created.

For example, next to `SourceFile.java` there must be a `SourceFile.json`, too.
```
promptducer
|-source_base_dir
| |-SourceFile.java
| |-SourceFile.json
```

Content of `SourceFile.json`, if there is no metadata:
```
{}
```

Otherwise, the specified values can be fetched in the prompt templates. 


## Citation

If you use this tool, please consider citing it in your work:

```bib
SOON
```

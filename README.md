# Family Tree MCP

Let's ask a question to chat GPT or any other models, and it gives
us an answer. If it is a logical questions, it performs its own logic 
to come out with a conclusion or if its any other questions that is there in the public internet space,
it gets the answer for us from there.

But let's ask it a question about a particular family tree or a particular company's employee details. In this case,
it won't be able to answer the question as the LLM don't know where to process the data from.

MCP servers helps to overcome this. We can consider MCP servers as an interface to which LLM asks for the data from which
it can make conclusions and give answers to the questions. 

The MCP servers are connected to the data source , lets say like an employee
database or some documents having family details or any other. They pass on these data to LLM in a particular structure, from which it can infer the details
according to its internal logics.

There is certain protocols or standards (mcp) they have to follow so that the LLM and server are communicate to each other and that is what the MCP does .i.e sharing the 
data to LLM following this protocol so that its able to understand the returned data.


This repository contains an implementation of an MCP server which shares the family details of "Ben","Dave" and "Siva". If anyone asks LLM about the family details,
it will connect to this MCP server for data and based on the data returned makes the interpretations and reply to the question.

## Setting up the server

### Pre- Requisite
1) Have python installed
2) Have Claude desktop installed. (You can have any other LLM and maybe not even the desktop but the configurations have to adjusted accordingly. For ease of understanding, lets use Claude desktop)

### Steps
     > Download the repository
     > # Installation and Setup:
            > Navigate to folder location in terminal
            > RUN the command 'pip install -r requirements.txt'
     > # Configuring Claude desktop to access server (MCP client config)
            > Go to "File >> Settings >> Developer >> Edit Config"
            > Add below item to the 'claude_desktop_config.json' file
               {
                "mcpServers": {
                    "family-data": {
                       "command": "C:\\PATH TO PYTHON\\python.exe",
                       "args": ["C:\\PATH TO SCRIPT\\family_mcp_server.py"]
                                   }
                               }
                }
             > Restart Claude Desktop

Now you can go to chat and ask a question "Who is Dave's father?" or any other and you will get the answers.
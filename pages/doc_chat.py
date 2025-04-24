import dash
from dash import html, dcc, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from io import BytesIO
import base64
from dash.exceptions import PreventUpdate
import time

# Register this page
dash.register_page(__name__, path='/chat')

# Define global variables for document processing
vectorstore = None
retriever = None
llm = None
is_initialized = False
initialization_status = "Not started"
initialization_error = None

# Initialize the RAG model and load the documents
def initialize_docChat():
    global vectorstore, retriever, llm, is_initialized, initialization_status, initialization_error
    
    if is_initialized:
        return True
    
    try:
        initialization_status = "Loading documents..."
        
        # PDF paths in the assets directory - using relative paths
        pdf_paths = [ 
            "assets/book2.pdf",
        ]
        
        # Print current working directory for debugging
        print(f"Current working directory: {os.getcwd()}")
        
        data = []
        for pdf_path in pdf_paths:
            print(f"Checking for file: {pdf_path}")
            if os.path.exists(pdf_path):
                print(f"Loading file: {pdf_path}")
                try:
                    loader = PyPDFLoader(pdf_path)
                    current_data = loader.load()
                    data.extend(current_data)
                    print(f"Successfully loaded {len(current_data)} pages from {pdf_path}")
                except Exception as e:
                    print(f"Error loading {pdf_path}: {str(e)}")
            else:
                print(f"File not found: {pdf_path}")
        
        if not data:
            initialization_status = "Failed - No documents found"
            initialization_error = "No PDF files could be loaded. Please check the file paths."
            print("No data was loaded from any PDF files")
            return False
        
        initialization_status = "Splitting documents..."
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
        docs = text_splitter.split_documents(data)
        
        initialization_status = "Creating vector store..."
        # Create vectorstore and retriever
        vectorstore = Chroma.from_documents(
            documents=docs, 
            embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        )
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        
        initialization_status = "Initializing language model..."
        # Initialize language model
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
        
        initialization_status = "Ready"
        is_initialized = True
        return True
    except Exception as e:
        initialization_status = "Failed - Error during initialization"
        initialization_error = str(e)
        print(f"Error during initialization: {str(e)}")
        return False

# Start initialization in a separate thread
import threading

def background_initialization():
    global initialization_status
    initialization_status = "Starting..."
    initialize_docChat()

# Start the initialization thread
initialization_thread = threading.Thread(target=background_initialization)
initialization_thread.daemon = True
initialization_thread.start()

# Function to process query and get response
def process_query(query):
    global retriever, llm, initialization_status
    
    if not is_initialized:
        return f"I'm still initializing. Current status: {initialization_status}. Please try again in a moment."
    
    if initialization_error:
        return f"Initialization failed: {initialization_error}"
    
    # Define the system prompt
    system_prompt = (
        "You are a Pediatric Healthcare assistant for the question answering task. "
        "Use the following pieces of retrieved context to answer "
        "the question about children's health, nutrition, and medical care. "
        "If you don't know the answer, say that you don't know. "
        "Use clear, informative language suitable for parents and caregivers."
        "\n\n"
        "{context}"
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Create the question-answer chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Process the query
    try:
        response = rag_chain.invoke({"input": query})
        return response["answer"]
    except Exception as e:
        return f"Error processing your query: {str(e)}"

# Custom CSS for chat messages
chat_styles = {
    "user_msg": {
        "backgroundColor": "#2B6CB0",
        "color": "white",
        "padding": "10px 15px",
        "borderRadius": "15px 15px 0 15px",
        "margin": "5px 0",
        "maxWidth": "80%",
        "marginLeft": "auto",
        "boxShadow": "0 1px 2px rgba(0,0,0,0.2)"
    },
    "bot_msg": {
        "backgroundColor": "#1A202C",
        "color": "white",
        "padding": "10px 15px",
        "borderRadius": "15px 15px 15px 0",
        "margin": "5px 0",
        "maxWidth": "80%",
        "marginRight": "auto",
        "boxShadow": "0 1px 2px rgba(0,0,0,0.2)",
        "border": "1px solid #2C5282"
    },
    "chat_container": {
        "display": "flex",
        "flexDirection": "column",
        "height": "60vh",
        "overflowY": "auto",
        "padding": "15px",
        "backgroundColor": "#0D1117",
        "border": "1px solid #2C5282",
        "borderRadius": "5px",
        "marginBottom": "15px"
    },
    "status_indicator": {
        "padding": "5px 10px",
        "borderRadius": "15px",
        "fontSize": "0.8rem",
        "marginBottom": "10px",
        "textAlign": "center"
    }
}

# Layout for the page
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("DocChat Healthcare Assistant 💬", 
                   className="text-center mb-4", 
                   style={'color': '#63B3ED'}),
            html.P("Ask questions about children's health, nutrition, and medical concerns.", 
                  className="text-center mb-4", 
                  style={'color': '#A0AEC0'}),
            
            # Status indicator
            html.Div(id="initialization-status", className="text-center mb-3",
                    style=chat_styles["status_indicator"]),
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            # Chat history container
            html.Div(id="chat-container", style=chat_styles["chat_container"]),
            
            # Input area
            dbc.InputGroup([
                dbc.Input(
                    id="chat-input",
                    placeholder="Type your question here...",
                    type="text",
                    style={"backgroundColor": "#1E1E1E", "color": "white", "border": "1px solid #3498db"}
                ),
                dbc.Button(
                    "Send",
                    id="send-button",
                    color="primary",
                    style={"backgroundColor": "#2B6CB0"}
                ),
            ], className="mb-3"),
            
            # Clear chat button
            dbc.Button(
                "Clear Chat",
                id="clear-chat",
                color="secondary",
                className="mb-4",
                style={"backgroundColor": "#4A5568", "border": "none"}
            ),
            
            # Store component for chat history
            dcc.Store(id="chat-history-store"),
            
            # Loading indicator
            dbc.Spinner(html.Div(id="loading-output"), color="primary", type="grow", fullscreen=False),
            
            # Interval for updating initialization status
            dcc.Interval(
                id='initialization-interval',
                interval=1000,  # in milliseconds
                n_intervals=0
            ),
        ], width={"size": 10, "offset": 1})
    ]),
    
    # Client-side callback for scrolling to bottom of chat
    html.Div(id="scroll-bottom-trigger"),
    
], fluid=True, style={'backgroundColor': '#0A0A0A', 'minHeight': '100vh', 'padding': '20px'})

# Callback for updating initialization status
@callback(
    Output("initialization-status", "children"),
    Output("initialization-status", "style"),
    Input("initialization-interval", "n_intervals")
)
def update_initialization_status(n):
    global initialization_status
    
    status_style = dict(chat_styles["status_indicator"])
    
    if initialization_status == "Ready":
        status_style["backgroundColor"] = "rgb(0,0,0,0)"  # Green
        status_style["color"] = "white"
        return "✅ System Ready", status_style
    elif "Failed" in initialization_status:
        status_style["backgroundColor"] = "rgb(0,0,0,0)"  # Red
        status_style["color"] = "white"
        return f"❌ {initialization_status}", status_style
    else:
        status_style["backgroundColor"] = "rgb(0,0,0,0)"  # Blue
        status_style["color"] = "white"
        return f"⏳ {initialization_status}", status_style

# Callback for sending messages
@callback(
    [Output("chat-container", "children"),
     Output("chat-input", "value"),
     Output("chat-history-store", "data"),
     Output("loading-output", "children", allow_duplicate=True),
     Output("scroll-bottom-trigger", "children")],
    [Input("send-button", "n_clicks"),
     Input("chat-input", "n_submit")],
    [State("chat-input", "value"),
     State("chat-history-store", "data")],
    prevent_initial_call=True
)
def send_message(n_clicks, n_submit, input_value, chat_history):
    # If there was no click or input, don't update
    if (n_clicks is None and n_submit is None) or not input_value:
        raise PreventUpdate
    
    # Initialize chat history if it doesn't exist
    if chat_history is None:
        chat_history = []
    
    # Add user message to chat history
    chat_history.append({"role": "user", "content": input_value})
    
    # Process the query and get a response
    response = process_query(input_value)
    
    # Add assistant response to chat history
    chat_history.append({"role": "assistant", "content": response})
    
    # Create chat message components
    chat_components = []
    for message in chat_history:
        if message["role"] == "user":
            chat_components.append(
                html.Div(
                    html.Div(message["content"], style=chat_styles["user_msg"]),
                    style={"display": "flex", "justifyContent": "flex-end", "marginBottom": "10px"}
                )
            )
        else:
            chat_components.append(
                html.Div(
                    html.Div(message["content"], style=chat_styles["bot_msg"]),
                    style={"display": "flex", "justifyContent": "flex-start", "marginBottom": "10px"}
                )
            )
    
    # Return updated chat, clear input, updated chat history, and trigger scroll
    return chat_components, "", chat_history, "", f"scroll-{len(chat_history)}"

# Callback to clear chat history
@callback(
    [Output("chat-container", "children", allow_duplicate=True),
     Output("chat-input", "value", allow_duplicate=True),
     Output("chat-history-store", "data", allow_duplicate=True),
     Output("loading-output", "children", allow_duplicate=True),
     Output("scroll-bottom-trigger", "children", allow_duplicate=True)],
    Input("clear-chat", "n_clicks"),
    prevent_initial_call=True
)
def clear_chat(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    
    return [], "", [], "", ""

# Add client-side JavaScript for auto-scrolling
app = dash.get_app()
app.clientside_callback(
    """
    function(trigger) {
        var chatContainer = document.getElementById('chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        return '';
    }
    """,
    Output("scroll-bottom-trigger", "title"),
    Input("scroll-bottom-trigger", "children")
)
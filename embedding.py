# from google.colab import drive

# if not os.path.exists("/content/drive/MyDrive"):
#     drive.mount("/content/drive")
#     print("Google Drive wurde gemountet.")
# else:
#     print("Google Drive ist bereits gemountet.")

# auth.authenticate_user()

# from langchain_community.document_loaders import PyPDFLoader

# file_path = "/content/drive/MyDrive/AIAgent/leistungsuebersicht-kfz.pdf"
# loader = PyPDFLoader(file_path)
# docs = loader.load()

#import pprint
#pprint.pp(docs[0].page_content)
#pprint.pp(docs[0].metadata)


#credentials_path = "/content/drive/MyDrive/Credentials/oauth_credentials.json"
#gdrive_api_file = credentials_path
#loader = GoogleDriveLoader(folder_id="1FGAIWQuIs_n13CEyuk_P9yH30UvPHFDS", credentials_path=credentials_path,use_browser=False)
#docs = loader.load()

# Load and split webdocuments
#loader = WebBaseLoader("https://en.wikipedia.org/wiki/Large_language_model")
#document = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(docs)
# Add documents to Pinecone index
# vector_store.add_documents(documents)

from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings

loader = TextLoader("docs/my_file.txt")
docs = """
Bạn là một AI agent hỗ trợ cho việc trích xuất các tham số để để gọi API lấy log từ database.
Các thuộc tính cần để trace log:
- userId: là số điện thoại của user (cũng được gọi là debitor hoặc user_id) 
- createdAtFrom: thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải trước giá trị của thuộc tính createdAtTo.
    format: YYYY-MM-DD'T'HH:mm:ss
    Nếu không tìm thấy thì giá trị mặt định là null
- createdAtTo thời gian (ngày giờ) nếu format không đúng thì chỉnh lại cho đúng với format.
    Giá trị hợp lệ là thời gian phải sau giá trị của thuộc tính createdAtFrom.
    format: YYYY-MM-DD'T'HH:mm:ss
    Nếu không tìm thấy thì giá trị mặt định là null
- serviceNames: là cách đặt tên của từng service, hay còn được gọi là các hãng, đối tác (partner) đôi khi có gắn thêm action như (search, api)
- actionNames: là tên gọi của action của api ví dụ như: booking, search, calfare, reserve, payment,...
- actionTypes: là loại log đầu ra đầu vào của của hệ thống. Ví dụ như request, response. khi đi qua từng service thường gắn thêm tiền tố đại diện cho service: ví dụ (partner_response, gateway_response)

Observation của những tool điều là dạng JSON và có thể parse được từ schema của nó 

Final Answer là một định dạng json
có các field sau:
  userId: str,
  createdAtFrom: datetime
  createdAtTo: datetime
  serviceNames: list[str] (không có thì trả về mãng rỗng)  
  actionNames: list[str] (không có thì trả về mãng rỗng)  
  actionTypes: list[str] (không có thì trả về mãng rỗng)
"""

embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma.from_documents(docs, embeddings)

retriever = db.as_retriever()

llm = Ollama(model="llama3")
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)

query = "Nội dung chính trong tài liệu này là gì?"
print(qa_chain.run(query))

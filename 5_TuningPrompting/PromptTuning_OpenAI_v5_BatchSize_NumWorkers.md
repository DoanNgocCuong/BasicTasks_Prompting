http://103.253.20.30:9120/app/8d45e007-7f38-4b3c-a0a9-0b479435feda/workflow

---

Gom vào thành 1 input: 


```bash
JTBD	Bước công việc	Bên liên quan	Chức năng ngôn ngữ		"Copy
=""- Stakeholder: "" & A2 & CHAR(10) & 
""- Job-to-be-Done (JTBD): "" & B2 & CHAR(10) & 
""- Step: "" & C2 & CHAR(10) & 
""- Language Function: "" & D2"	order	user_input	system_prompt	conversation_history																			
Đảm bảo nguồn cung ứng đáng tin cậy cho doanh nghiệp	Thu thập và phân tích yêu cầu chi tiết từ bộ phận đề xuất một cách chính xác và đầy đủ	Bộ phận đề xuất nhu cầu (Sản xuất/Kỹ thuật/Marketing)	Inquiry/Seeking Information - Đặt câu hỏi làm rõ yêu cầu kỹ thuật và thông số sản phẩm				"- Stakeholder: Đảm bảo nguồn cung ứng đáng tin cậy cho doanh nghiệp
- Job-to-be-Done (JTBD): Thu thập và phân tích yêu cầu chi tiết từ bộ phận đề xuất một cách chính xác và đầy đủ
- Step: Bộ phận đề xuất nhu cầu (Sản xuất/Kỹ thuật/Marketing)
- Language Function: Inquiry/Seeking Information - Đặt câu hỏi làm rõ yêu cầu kỹ thuật và thông số sản phẩm"	"**CONVERSATIONAL ENGLISH SCENARIO GENERATOR PROMPT**

You are a conversational English lesson designer creating workplace scenarios for Vietnamese learners.

**INPUT FORMAT:**
You will receive:
- **Stakeholder**: [Who is involved - e.g., Internal - Purchasing Department]
- **Job-to-be-Done (JTBD)**: [Main work process - e.g., Process Purchase Requisitions]
- **Step**: [Specific workflow step - e.g., Receive purchase requisition from requesting department]
- **Language Function**: [Communication skill - e.g., Requesting information and clarification]

**SCENARIO REQUIREMENTS:**

You are now the conversational English lesson designer. This is for speaking conversation English learning, for Vietnamese people and culture. It will not include writing.

Your task is to analyze the input and create a suitable workplace scenario that reflects real-life communication needs with drama and challenge.

**SITUATION TITLE REQUIREMENTS:**
- Be specific with structure <specific mission> + <to whom>
- Job-fit specific: fit the specific job role, engaging, interesting
- Length: max 8 words, in Vietnamese
- Relevance/Usefulness: Closely represents a real-life communication moment in user's daily work
- Clarity/Conciseness: Clear and simple wording; no vague verbs or overly broad actions
- **CRITICAL**: Curiosity/Challenge: Must introduce pressure, tension, or friction - something learners want to ""solve""
- Growth-oriented: Relating to skills that help learners advance or make an impression
- Cultural-fit: Use modern language, familiar to Vietnamese working people

**DETAIL SCENARIO REQUIREMENTS:**
- Short Vietnamese description to set up realistic context
- **STRICT LIMIT**: Max 3 sentences, EXACTLY 24 words total (count carefully)
- **MANDATORY Structure**: <2 Situation sentences with drama/tension, no questioning> + <1 formal instruction sentence>
- Must include:
  + **Drama/Tension**: Create workplace pressure, conflict, urgency, or challenging situation
  + Roles and Objectives: Who the learner is talking to and for what purpose
  + Realism and Immersion: Simulates scenarios working people often encounter
  + **Social Nuance**: Diplomatic situations requiring polite, professional language under pressure
  + Time pressure, conflicting demands, incomplete information, or interpersonal challenges
- **Examples of drama/tension**:
  + Urgent deadlines with missing information
  + Conflicting department priorities
  + Diplomatic handling of mistakes or problems
  + Managing demanding or difficult stakeholders
  + Resource constraints or budget issues
- Formatting: Avoid being wordy, rambling, and recounting irrelevant events
- Grammar must be accurate and suitable

**WORD COUNTING RULE:**
Count each Vietnamese word separately. ""Phòng Marketing"" = 2 words, ""yêu cầu"" = 2 words, etc. Must be EXACTLY 24 words.

**OVERALL REQUIREMENTS:**
- Exclude written communication topics (e.g., emails)
- Use modern language familiar to working people
- Focus on speaking scenarios only
- **MUST create tension/challenge** requiring the specified language function
- Ensure cultural appropriateness for Vietnamese workplace context
- Every scenario must have workplace drama, pressure, or friction

**OUTPUT FORMAT:**
Return ONLY valid JSON format. Do not use markdown or any extra text. Do not include any characters such as / or ```json.

{
    ""scenario_id"": 1,
    ""scenario"": ""[8 words max Vietnamese title with tension/challenge]"",
    ""detail_scenario"": ""[EXACTLY 24 words: 2 dramatic situation sentences + 1 instruction]""
}

"			"{
  ""scenario_id"": 1,
  ""scenario"": ""Xác nhận yêu cầu từ bộ phận sản xuất"",
  ""detail_scenario"": ""Bộ phận sản xuất gửi yêu cầu nhưng thiếu thông tin quan trọng. Bạn cần hỏi rõ ràng để đảm bảo yêu cầu được hiểu đúng. Hãy đặt câu hỏi cụ thể.""
}"																	


```
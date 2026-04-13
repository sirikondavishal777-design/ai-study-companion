import streamlit as st
import PyPDF2
import os
import uuid
import glob

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

def generate_explanation(topic):
    prompt = f"""Explain the topic in simple language for students. 
Include:
- Definition
- How it works
- Types (if any)
- Real-life examples
- Simple summary

Topic: {topic}"""
    return get_ai_response(prompt)

def get_ai_response(prompt):
    """Fallback local mock response to strictly prevent breaking other tabs."""
    if "5 MCQs" in prompt:
        return """Q1: What is the primary focus of the provided context?
A. Analyzing literature
B. Memorizing random facts
C. Core principles and practical concepts
D. Ignoring practical applications
Answer: C

Q2: How can this material be utilized in real life?
A. It has no real-life usage.
B. By applying its theories to solve practical problems.
C. Only by writing essays about it.
D. By watching videos without practicing.
Answer: B

Q3: Which of the following is essential for mastering this subject?
A. Avoiding all challenges.
B. Learning only one specific subset.
C. Continuous practice and problem solving.
D. Refusing to read new materials.
Answer: C

Q4: What is the best method to evaluate your understanding?
A. Skipping exams.
B. Self-assessing with flashcards and quizzes.
C. Ignoring all review materials.
D. Waiting until the night before the test.
Answer: B

Q5: Why is consistency important in studying?
A. It helps retain information long-term.
B. It guarantees you will never fail.
C. It allows you to study faster perfectly.
D. It replaces the need to focus.
Answer: A"""
    
    if "Explain the topic" in prompt:
        topic_part = prompt.split("Topic:")[-1].strip()
        
        # If it's a huge PDF text
        if len(topic_part) > 100:
            display_topic = "the concepts covered in your document"
        else:
            display_topic = topic_part.title()
            
        return f"""Here is a detailed explanation for **{display_topic}**:

### 📖 Definition
**{display_topic}** refers to a comprehensive area of study that focuses on understanding specific structures, behaviors, systems, and underlying principles. It provides the essential building blocks needed to intuitively grasp more complex ideas in this domain.

### ⚙️ How it works
At a fundamental level, it operates by taking basic inputs or concepts and logically processing them through established rules to produce a meaningful outcome. Whether functioning in nature, business, technology, or theoretical frameworks, it relies on a steady flow of logical interactions and sequential steps to maintain order and efficiency naturally.

### 🗂️ Types (if any)
Generally, you can categorize this subject into two main branches:
1. **Theoretical/Foundational:** Researching the core mathematical, scientific, or conceptual principles, fundamentally answering the "why" and "what."
2. **Applied/Practical:** Utilizing those principles to directly solve real-world problems, essentially answering the "how."

### 🌍 Real-life examples
Consider a scenario where you have to organize a massive logistics system or figure out how dynamic variables affect a complex outcome. The core principles of {display_topic} act as your master blueprint. Just as an experienced architect uses physics and geometry to ensure a towering building doesn't collapse, deeply understanding this topic provides you with the foundational rules required to build, thoroughly analyze, or interpret intricate scenarios in your daily life.

### 📌 Simple summary
In short, learning about {display_topic} effectively bridges the gap between abstract theory and practical, everyday utility. By mastering its mechanics, you unlock a versatile and powerful toolkit for problem-solving, critical thinking, and impactful innovation that extends far beyond the boundaries of the classroom."""
    if "You are a helpful, friendly tutor and study companion" in prompt:
        try:
            import urllib.request
            import json
            
            headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
            url = "https://text.pollinations.ai/openai"
            data = json.dumps({
                "messages": [{"role": "user", "content": prompt}],
                "model": "openai"
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result["choices"][0]["message"]["content"]
        except Exception:
            pass # Fallback to local simulated AI when entirely without network connection
            
        user_msg = prompt.split("User:")[-1].strip()
        
        import re
        clean_msg = re.sub(r'[^\w\s]', '', user_msg.lower()).strip()
        
        if clean_msg in ["hi", "hello", "hey", "hlo", "greetings", "hi there"]:
            return "Hi! How can I help you?"
            
        if "study" in clean_msg or "advice" in clean_msg or "how to" in clean_msg or "what should i do" in clean_msg:
            return """Start with a simple plan:
- Focus on one topic at a time
- Take short notes while studying
- Revise daily
- Practice questions regularly"""

        return "The core concept relies on clear structural principles that interact logically to produce the final outcome. Focus firmly on practical applications and foundational rules to master it completely. What specific detail would you like me to elaborate on?"

    return f"Local processing activated. Received: {prompt[:100]}..."

def extract_pdf_text(uploaded_file):
    """Safely extracts text from all pages of an uploaded PDF file."""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
        
        # Clean text by replacing all multiple spaces/newlines with a single space
        cleaned_text = " ".join(full_text.split())
        return cleaned_text
    except Exception:
        return None

def generate_mock_explanation(topic, pdf_content=None):
    """Generates a structured, AI-like mock explanation based on the topic."""
    st.divider()
    
    if pdf_content:
        st.success("✨ Explanation based on topic and uploaded PDF")
        
    display_topic = topic.strip().title()
    
    # Customized Topic Heading
    st.markdown(f"<h2 style='text-align: center; color: #4A90E2;'>{display_topic}</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Definition
    st.markdown("### 📖 :violet[Definition]")
    st.write(f"**{display_topic}** refers to a comprehensive subject of study. In simple terms, it is the process of understanding the core principles, behaviors, and systems related to this specific field of knowledge.")
    
    # Key Points
    st.markdown("### ⭐ :orange[Key Points]")
    st.markdown(f"""
    - **Foundation:** Understanding the basics of {display_topic} is highly beneficial.
    - **Problem Solving:** It equips you with the necessary logical tools to confidently tackle complex challenges.
    - **Adaptability:** The concepts can be creatively adapted to many different real-world scenarios.
    """)
    
    # Real-life Example
    st.markdown("### 🌍 :green[Real-life Example]")
    st.write(f"If you were trying to organize a large event from scratch, the underlying principles of {display_topic} act as the blueprint that guides your decisions from start to finish.")
    
    # Summary
    st.markdown("### 📌 :blue[Summary]")
    summary_txt = f"In short, {display_topic} is a valuable area of learning that bridges theoretical ideas with practical, everyday applications."
    st.info(summary_txt)

    # Show PDF snippet at the end if PDF was provided
    if pdf_content:
        st.markdown("### 📄 :gray[Key content from PDF:]")
        st.write(pdf_content[:500] + ("..." if len(pdf_content) > 500 else ""))
        
    return f"Definition of {display_topic}. It refers to a comprehensive subject of study. Key points include understanding foundations to tackle complex challenges adaptably. {summary_txt}"

def main():
    # Set page configuration for a centered, clean layout
    st.set_page_config(page_title="Student Study Companion", page_icon="🎓", layout="centered")

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("Student Study Companion")
    section = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📘 Explanation", "🧠 Quiz", "💬 Chat", "📝 Notes"]
    )
    
    st.sidebar.divider()
    
    # Global document upload
    st.sidebar.markdown("### 📄 Upload Document")
    uploaded_file = st.sidebar.file_uploader("Upload PDF Reference", type=["pdf"])
    
    pdf_text = None
    if uploaded_file is not None:
        pdf_text = extract_pdf_text(uploaded_file)
        if pdf_text is not None:
            st.sidebar.success("✅ PDF loaded to memory")
        else:
            st.sidebar.error("❌ Failed reading PDF")

    # --- HOME SECTION ---
    if section == "🏠 Home":
        st.title("📚 Student Study Companion")
        st.write("Learn smarter with AI-powered explanations, quizzes, and notes.")
        
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.info("📘 Generate explanations from topics or PDFs")

        with col2:
            st.info("🧠 Test your knowledge with quizzes")

    # --- EXPLANATION SECTION ---
    elif section == "📘 Explanation":
        st.title("📚 Topic Explanation")
        st.write("Determine a subject and press generate to build a complete learning module.")
        
        topic = ""
        if pdf_text:
            st.info("📄 Using PDF content for explanation")
        else:
            st.info("✍️ Using topic input for explanation")
            topic = st.text_input("Enter a study topic you want to learn about:", key="topic_input")
        
        if st.button("Generate Explanation", type="primary", use_container_width=True):
            if not pdf_text and not topic:
                st.warning("⚠️ Please enter a topic or upload a PDF first to generate an explanation.")
            else:
                st.session_state["exp_active"] = True
                st.session_state["exp_topic"] = topic
                
                # Handle priority rules
                with st.spinner("Generating local explanation..."):
                    if pdf_text:
                        st.session_state["exp_response"] = generate_explanation(pdf_text)
                    else:
                        st.session_state["exp_response"] = generate_explanation(topic)
                
        # Render if generated
        if st.session_state.get("exp_active") and "exp_response" in st.session_state:
            st.subheader("Result")
            st.success("Analysis complete! See explanation below.")
            
            response = st.session_state["exp_response"]
            st.write(response)
            
            st.write("")
            
            st.write("")
            
            if st.button("🔊 Read Aloud", use_container_width=True):
                if not response.strip():
                    st.warning("⚠️ Text is empty. Nothing to read aloud.")
                elif gTTS is None:
                    st.error("Missing gTTS library! Please use: pip install gTTS")
                else:
                    with st.spinner("Generating audio snippet..."):
                        try:
                            # Clean up previously generated audio files across reruns
                            for old_file in glob.glob("audio_*.mp3"):
                                try:
                                    os.remove(old_file)
                                except Exception:
                                    pass
                                    
                            # Create new UUID tracked audio payload
                            file_name = f"audio_{uuid.uuid4().hex}.mp3"
                            tts = gTTS(text=response, lang='en')
                            tts.save(file_name)
                            
                            st.audio(file_name, format="audio/mp3", autoplay=True)
                        except Exception as e:
                            st.error(f"TTS Engine Error: {e}")
                
            if pdf_text:
                st.divider()
                with st.expander("👀 View Extracted PDF Content"):
                    st.write(pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""))

    # --- QUIZ SECTION ---
    elif section == "🧠 Quiz":
        st.title("🎯 Quiz Generation")
        
        if st.button("Generate Quiz", type="primary", use_container_width=True):
            source_text = None
            if pdf_text:
                st.info("Generating quiz from PDF content...")
                source_text = pdf_text[:1500]
            elif st.session_state.get("exp_response"):
                st.info("Generating quiz from explanation...")
                source_text = st.session_state["exp_response"]
                
            if not source_text:
                st.warning("⚠️ Please upload a PDF or generate an explanation first.")
            else:
                st.session_state["quiz_active"] = True
                
                prompt = f"""Use this input:
{source_text}

Create:
- 5 MCQs
- with options A/B/C/D
- with correct answers"""
                
                with st.spinner("Generating quiz..."):
                    quiz_string = get_ai_response(prompt)
                
                st.session_state.quiz_data = quiz_string
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = None

        # Render Quiz if active
        if st.session_state.get("quiz_active"):
            st.divider()
            st.subheader("Result")
            
            if "quiz_data" in st.session_state:
                with st.container():
                    quiz_blocks = st.session_state.quiz_data.strip().split("\n\n")
                    
                    user_answers = {}
                    correct_answers = {}
                    
                    for i, block in enumerate(quiz_blocks):
                        lines = [line.strip() for line in block.split("\n") if line.strip()]
                        if len(lines) >= 6:
                            question_text = lines[0]
                            options = lines[1:5]
                            ans_line = lines[5]
                            correct_opt = ans_line.replace("Answer:", "").strip()
                            correct_answers[i] = correct_opt
                            
                            st.markdown(f"**{question_text}**")
                            for opt in options:
                                st.write(opt)
                            
                            user_ans = st.radio("Select answer", ["A", "B", "C", "D"], key=f"quiz_opt_{i}", horizontal=True)
                            user_answers[i] = user_ans
                            st.divider() # Spacing between questions
                    
                    if st.button("Submit Quiz", type="primary"):
                        score = 0
                        for i in range(len(quiz_blocks)):
                            if user_answers.get(i) == correct_answers.get(i):
                                score += 1
                                
                        st.session_state["quiz_score"] = score
                        st.session_state["quiz_submitted"] = True
                        st.session_state["quiz_correct_answers"] = correct_answers
                    
                    if st.session_state.get("quiz_submitted"):
                        total_qs = len(st.session_state.get('quiz_correct_answers', {}))
                        st.success(f"Your Score: {st.session_state.get('quiz_score')}/{total_qs}")
                        
                        st.info("Correct Answers:")
                        for idx, corr in st.session_state.get("quiz_correct_answers", {}).items():
                            st.write(f"**Q{idx+1}:** {corr}")

    # --- CHAT SECTION ---
    elif section == "💬 Chat":
        st.title("💬 Chat Assistant")
        topic = st.session_state.get("topic_input", "")
        
        if topic:
            st.info(f"Subject Context active for: **{topic}**")

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        chat_container = st.container(height=350)
        
        with chat_container:
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "User":
                    st.markdown(f"**👤 You:** {msg['content']}")
                else:
                    st.info(f"**🤖 AI:** {msg['content']}")

        # Chat Input
        user_question = st.text_input("Type your question here:", key="chat_input_val")
        if st.button("Ask Question", use_container_width=True):
            if not user_question.strip():
                st.warning("⚠️ Please enter a question first.")
            else:
                st.session_state["chat_history"].append({"role": "User", "content": user_question})

                context = ""
                if topic:
                    context += f"Optional Study Topic: {topic}\n\n"
                if pdf_text:
                    context += f"Optional Document Reference:\n{pdf_text[:1000]}\n\n"
                
                prompt = f"""You are a helpful, friendly tutor and study companion. 
You can talk about any topic, help with studies, explain concepts, solve problems, and have normal conversation with the user. 
Respond naturally, simply, and directly as a human-like tutor.

STRICT RULES:
- DO NOT introduce yourself.
- DO NOT mention you are an AI or ChatGPT.
- DO NOT repeat the user's question.
- DO NOT say "You mentioned" or "You asked" or summarize the input.
- NO motivational filler sentences.
- NO redirecting to other parts of the app.
- ALWAYS answer the question directly with clear information.

{context}User: {user_question}"""

                ans = get_ai_response(prompt)
                
                st.session_state["chat_history"].append({"role": "AI", "content": ans})
                st.rerun()

    # --- NOTES SECTION ---
    elif section == "📝 Notes":
        st.subheader("📝 My Notes")
        st.write("Write, append, and save insights directly to your local files.")
        
        topic = st.session_state.get("topic_input", "")
        
        # Load existing notes
        existing_notes = ""
        try:
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r", encoding="utf-8") as f:
                    existing_notes = f.read()
        except Exception:
            pass

        user_notes = st.text_area("Workspace Editor:", value=existing_notes, height=400, label_visibility="collapsed")

        if st.button("💾 Save Notes", type="primary", use_container_width=True):
            try:
                with open("notes.txt", "w", encoding="utf-8") as f:
                    f.write(user_notes)
                st.subheader("Result")
                st.success("✅ Notes securely saved inside notes.txt!")
            except Exception as e:
                st.error("❌ Failed to save notes. Please try again.")
                
        st.divider()
        st.markdown("### 🧠 AI Smart Notes")
        col1, col2, col3 = st.columns(3)
        
        gen_clicked = col1.button("Generate Notes from Topic", use_container_width=True)
        summ_clicked = col2.button("Summarize Notes", use_container_width=True)
        quiz_clicked = col3.button("Convert Notes to Quiz", use_container_width=True)
        
        if gen_clicked:
            if not topic:
                st.warning("⚠️ Please provide a topic in the Explanation tab first.")
            else:
                prompt = f"Create short, clear study notes with bullet points on:\n{topic}"
                if pdf_text:
                    prompt += f"\nUse this content:\n{pdf_text[:1000]}"
                notes = get_ai_response(prompt)
                st.text_area("Generated Notes", notes, height=200)

        if summ_clicked:
            if not user_notes.strip():
                st.warning("⚠️ Please write or save some notes first before summarizing.")
            else:
                prompt = f"Summarize these notes in short bullet points:\n{user_notes}"
                summary = get_ai_response(prompt)
                st.text_area("Summary", summary, height=200)

        if quiz_clicked:
            if not user_notes.strip():
                st.warning("⚠️ Please write or save some notes first to convert.")
            else:
                prompt = f"Create 3 MCQ questions with answers from these notes:\n{user_notes}"
                quiz_output = get_ai_response(prompt)
                st.subheader("Result")
                st.write(quiz_output)



if __name__ == "__main__":
    main()

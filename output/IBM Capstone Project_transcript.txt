Of course. Here is the enhanced version of the text, optimized for clarity and audiobook narration. It transforms the slide-deck format into a flowing, professional presentation script.

---

### Enhanced Audiobook Script

**(Start with a professional, clear tone)**

**Title:** College Admission Assistant using a RAG-based Agent on IBM watsonx.ai. This is a Capstone Project presentation.

**Presented by:** Nikitha M., a student at Sri Ramakrishna Engineering College, pursuing a Bachelor of Technology in Artificial Intelligence and Data Science.

**(Slight pause)**

**Outline**

Here is the outline for today's presentation.

*   First, I will present the Problem Statement, focusing solely on the challenges at hand.
*   Next, I will introduce the Proposed System and Solution.
*   Then, I’ll discuss the System Development Approach, including the technologies used.
*   After that, I will explain the core Algorithm and the Deployment process.
*   I will then share the Results, including an image of the system's output.
*   Finally, I will offer a Conclusion, discuss the Future Scope of the project, and list my References.

**(Transition to the next section)**

**Problem Statement**

The core problem we're addressing is the inefficiency of manual college admission processes. These processes involve numerous, time-consuming inquiries from students about eligibility criteria, available courses, fee structures, cutoff scores, and application deadlines.

Students often struggle to get accurate and updated information directly from official sources or helplines. This creates a clear and growing need for an AI-powered assistant that can provide transparent, real-time, and personalized responses to student queries, using trusted institutional data as its foundation.

**(Transition to the next section)**

**Proposed Solution**

To address this problem, the proposed system is a College Admission Agent built using IBM Watsonx.ai and powered by Retrieval-Augmented Generation, or RAG. Its purpose is to help students get accurate admission details through natural, conversational language queries.

Let's break down the key components:

*   For **Retrieval**, the system uses Tavily and Wikipedia Search to fetch real-time data from the web.
*   For **Generation**, it employs the Granite-13B Chat Model to generate human-like, conversational responses.
*   The entire system was **built** on the IBM Cloud Lite platform, using the Watsonx.ai Studio.
*   Finally, it was **deployed** in a Watsonx Deployment Space and tested with real student queries.

Ultimately, this AI-powered agent simplifies the admission process, reduces the burden of manual inquiries, and improves student access to reliable, up-to-date information.

**(Transition to the next section)**

**System Approach**

Now, let's discuss the technical approach. The system was built using the following technologies:

*   IBM Cloud Lite for the hosting environment.
*   Watsonx.ai Studio as the primary development platform.
*   The Granite-13b-chat Foundation Model for language generation.
*   Tavily and Wikipedia Search Tools, which act as the data retrievers.
*   And the Agentic AI Builder for setting up the RAG framework.

The development process followed these steps:
First, a project was created in Watsonx.ai. Next, the Agentic AI interface was built. The retrieval tools—Tavily and Wikipedia—were then configured. After that, the system prompts were defined to guide the AI's behavior. Finally, the agent was deployed in a Deployment Space for live testing.

**(Transition to the next section)**

**Algorithm and Deployment**

The core of this system is its RAG architecture. Here’s how it works:

1.  **Retrieval:** When a user asks a question, Tavily and Wikipedia search for and retrieve real-time, relevant information.
2.  **Augmentation:** This retrieved content is then injected into the prompt that is sent to the language model.
3.  **Generation:** Finally, the Granite model uses this augmented information to craft a comprehensive and relevant response.

For deployment, the completed agent was promoted to an IBM Watsonx Deployment Space. It was then tested live through both the Watsonx Preview interface and its API.

**(Transition to the next section)**

**Result**

Now, let's look at the results. The agent was tested with several real-world user queries. For example, a student might ask:

*   "What is the eligibility for B.E. in Computer Science and Engineering?"
*   "Which colleges offer a B.Tech in Information Technology?"
*   "What is the cutoff score for a B.Sc. in Computer Science?"
*   Or, more personally, "I have a cutoff of 180. What courses can I apply for?"
*   And, "Suggest courses that accept a 160 cutoff."

**(Slight pause for visual element)**

[Narrator's note: The presentation includes an output image, likely a screenshot, demonstrating the AI agent's conversational interface. It would show one of the example queries being asked, followed by a clear, well-formatted answer generated by the system.]

**(Transition to the next section)**

**Conclusion**

In conclusion, the College Admission Agent developed using IBM Watsonx.ai successfully demonstrates the power of Retrieval-Augmented Generation in simplifying the student admission process.

By combining the Granite-13B foundation model with real-time data retrieval through tools like Tavily and Wikipedia, the agent provides accurate, conversational answers to common admission queries. This AI-driven solution enhances accessibility, reduces manual effort, and ensures that students receive timely and reliable guidance on eligibility, courses, cutoffs, and colleges—all through a simple, user-friendly interface hosted entirely on the IBM Cloud.

**(Transition to the next section)**

**Future Scope**

Looking ahead, there are several exciting possibilities for future development.

*   First, we could add a Document Search feature to allow the agent to use internal college documents, such as PDFs of cutoff lists and brochures.
*   The system could also be extended to support application tracking and document uploads.
*   To improve accessibility, we could add support for multiple languages for students in different regions.
*   Finally, the agent could be connected to official APIs from university databases for even more dynamic and accurate information.

**(Transition to the next section)**

**References**

The research for this project is supported by the following academic papers:

*   The first is titled, "URAG: Implementing a Unified Hybrid RAG for Precise Answers in University Admission Chatbots—A Case Study at HCMUT," by Nguyen and Quan, an arXiv preprint from January 2025.
*   The second is, "An Empirical Study of Multi-Agent RAG for Real-World University Admissions Counseling," by Nguyen-Duc and colleagues, an arXiv preprint from July 2025.

**(Transition to the final slides)**

[Narrator's note: The following slides display copies of relevant IBM certifications earned during this project.]

**(Final closing)**

That concludes my presentation. Thank you.
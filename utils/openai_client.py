import openai
import os
from dotenv import load_dotenv
import streamlit as st
import base64
import io
from PIL import Image
import requests
import json

load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        
        if not self.api_key:
            st.error("❌ API key not found. Please check your .env file.")
            st.stop()
        
        try:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            st.success("✅ Connected to AI API successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize AI client: {str(e)}")
            st.stop()

    def analyze_resume(self, job_description, resume_images, analysis_type):
        """Real AI analysis using OpenRouter API"""
        try:
            if not job_description.strip():
                return "❌ Please provide a job description to analyze against."
            
            if not resume_images:
                return "❌ No resume content found. Please upload a valid PDF resume."

            # Extract text from images
            extracted_text = self._extract_text_from_images(resume_images)
            
            if not extracted_text or len(extracted_text.strip()) < 50:
                return "❌ Could not extract sufficient text from the resume. Please ensure your PDF contains clear, selectable text."

            # Get the appropriate prompt
            prompt = self._get_analysis_prompt(analysis_type, job_description, extracted_text)
            
            # Call AI API
            with st.spinner("🔍 AI is analyzing your resume content..."):
                response = self.client.chat.completions.create(
                    model="google/gemini-flash-1.5",  # Free and good model
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are an expert resume analyst and career coach. Be brutally honest and provide specific, actionable feedback."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
                else:
                    return "❌ No response received from AI."
            
        except Exception as e:
            error_msg = f"❌ Analysis failed: {str(e)}"
            st.error(error_msg)
            return error_msg

    def _extract_text_from_images(self, resume_images):
        """Extract text from resume images using AI vision"""
        try:
            all_extracted_text = ""
            
            for img_data in resume_images:
                # Use OpenRouter's vision capability
                image_data = base64.b64decode(img_data["data"])
                
                response = self.client.chat.completions.create(
                    model="google/gemini-flash-1.5",  # Supports vision
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "Extract ALL text from this resume image exactly as it appears. Include everything: contact info, work experience, education, skills, projects, achievements. Preserve the formatting and order."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_data['data']}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1500
                )
                
                if response.choices and response.choices[0].message.content:
                    all_extracted_text += f"\n\n--- Page {img_data['page_number']} ---\n{response.choices[0].message.content}"
            
            return all_extracted_text
            
        except Exception as e:
            st.warning(f"⚠️ Text extraction issue: {str(e)}")
            # Fallback: Use a simple prompt for text extraction
            return self._fallback_text_extraction(resume_images)

    def _fallback_text_extraction(self, resume_images):
        """Fallback text extraction without vision"""
        try:
            all_text = ""
            for img_data in resume_images:
                response = self.client.chat.completions.create(
                    model="google/gemini-flash-1.5",
                    messages=[
                        {
                            "role": "user",
                            "content": f"I have a resume image. Please help me analyze it. Since I can't see the image, I'll describe what a typical resume contains. Please provide a template analysis and ask the user to paste their actual resume text for accurate analysis."
                        }
                    ],
                    max_tokens=500
                )
                if response.choices:
                    all_text += response.choices[0].message.content + "\n\n"
            return all_text
        except Exception as e:
            return f"Resume with {len(resume_images)} pages. Please ensure your PDF contains selectable text for best results."

    def _get_analysis_prompt(self, analysis_type, job_description, resume_text):
        """Get the appropriate prompt for each analysis type"""
        
        if analysis_type == "ats_score":
            return f"""
            JOB DESCRIPTION:
            {job_description}

            RESUME CONTENT:
            {resume_text}

            TASK: Analyze this resume against the job description and provide a REAL ATS compatibility score.

            BE BRUTALLY HONEST. If the resume is terrible, irrelevant, or doesn't match, give a LOW score and explain why.

            SCORING CRITERIA (100 points total):
            - Skills Match (30 points): How well do resume skills match job requirements?
            - Experience Relevance (30 points): Is experience relevant, sufficient, and well-described?
            - Education & Qualifications (15 points): Does education match requirements?
            - Keyword Usage (15 points): Are important job keywords present and well-integrated?
            - Overall Fit & Presentation (10 points): General suitability and professionalism

            FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

            # 🎯 ATS Compatibility Analysis

            ## Overall Score: [0-100]/100

            ### 📊 Detailed Breakdown:
            **Skills Match:** [0-30]/30 - [Specific assessment with examples]
            **Experience Relevance:** [0-30]/30 - [Specific assessment with examples]  
            **Education & Qualifications:** [0-15]/15 - [Specific assessment with examples]
            **Keyword Usage:** [0-15]/15 - [Specific assessment with examples]
            **Overall Fit:** [0-10]/10 - [Specific assessment with examples]

            ### ⚠️ Critical Issues Found:
            - [List specific mismatches, missing requirements, or poor quality content]
            - [Be very specific about what's wrong]

            ### 💡 Improvement Suggestions:
            - [Actionable suggestions based on actual gaps]
            - [Provide exact examples of how to improve]

            ### 🔍 Missing Keywords/Skills:
            - [List important job requirements missing from resume]
            - [Include both hard and soft skills]

            Base your analysis SOLELY on the actual resume content compared to the job description.
            """

    def test_connection(self):
        """Test if the API connection is working"""
        try:
            response = self.client.chat.completions.create(
                model="google/gemini-flash-1.5",
                messages=[{"role": "user", "content": "Say 'Hello' in a creative way."}],
                max_tokens=20
            )
            return True, f"✅ AI connection successful! Model is working."
        except Exception as e:
            return False, f"❌ Connection failed: {str(e)}"
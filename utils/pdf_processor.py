import streamlit as st
import os
import tempfile
from PIL import Image
import io
import base64

class PDFProcessor:
    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024  # 10MB

    def validate_pdf(self, pdf_file):
        """Validate PDF file without external dependencies"""
        try:
            # Check file size
            if pdf_file.size > self.max_file_size:
                return False, f"File too large. Maximum size is {self.max_file_size // 1024 // 1024}MB"
            
            # Check if it's a PDF by extension and magic number
            if not pdf_file.name.lower().endswith('.pdf'):
                return False, "Please upload a PDF file"
            
            # Read first few bytes to check magic number
            pdf_file.seek(0)
            header = pdf_file.read(4)
            if header != b'%PDF':
                return False, "Invalid PDF file format"
            
            pdf_file.seek(0)
            return True, "PDF validated successfully"
            
        except Exception as e:
            return False, f"Error validating PDF: {str(e)}"

    def convert_pdf_to_images(self, pdf_file):
        """Convert PDF to images with fallback options"""
        try:
            # Method 1: Try with pdf2image first
            try:
                from pdf2image import convert_from_bytes
                poppler_path = os.getenv("POPPLER_PATH")
                
                images = convert_from_bytes(
                    pdf_file.read(),
                    poppler_path=poppler_path,
                    first_page=1,
                    last_page=2,  # Process max 2 pages for efficiency
                    dpi=150
                )
                
                image_parts = []
                for i, image in enumerate(images):
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='JPEG', quality=85)
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    image_parts.append({
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr).decode(),
                        "page_number": i + 1
                    })
                
                return image_parts
                
            except ImportError:
                st.warning("pdf2image not available. Using fallback method.")
                return self._fallback_pdf_processing(pdf_file)
                
        except Exception as e:
            st.error(f"PDF processing error: {str(e)}")
            return None

    def _fallback_pdf_processing(self, pdf_file):
        """Fallback method for PDF processing"""
        try:
            # Create a simple image representation
            # This is a fallback when pdf2image is not available
            from PIL import Image, ImageDraw
            
            # Create a placeholder image
            img = Image.new('RGB', (800, 1000), color='white')
            draw = ImageDraw.Draw(img)
            
            # Add some text to the image
            draw.text((50, 50), "PDF Content Preview", fill='black')
            draw.text((50, 100), "File: " + pdf_file.name, fill='blue')
            draw.text((50, 150), "Size: " + str(pdf_file.size) + " bytes", fill='green')
            draw.text((50, 200), "Using fallback processing", fill='red')
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode(),
                "page_number": 1
            }]
            
        except Exception as e:
            st.error(f"Fallback processing failed: {str(e)}")
            return None

    def extract_text_simple(self, pdf_file):
        """Simple text extraction without external dependencies"""
        try:
            # Basic text extraction from PDF
            pdf_file.seek(0)
            content = pdf_file.read().decode('latin-1')
            
            # Extract text between text markers (simplified)
            text_parts = []
            lines = content.split('\n')
            for line in lines:
                if 'Tj' in line or 'TJ' in line:
                    text_parts.append(line.strip())
            
            return ' '.join(text_parts[:500])  # Return first 500 chars
            
        except:
            return "Text extraction not available. Please ensure your PDF contains selectable text."

    def get_pdf_info(self, pdf_file):
        """Get basic PDF information"""
        return {
            'name': pdf_file.name,
            'size': pdf_file.size,
            'type': pdf_file.type
        }
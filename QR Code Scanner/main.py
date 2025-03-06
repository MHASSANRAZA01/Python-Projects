import streamlit as st
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

 
st.set_page_config(
    page_title="QR Code Scanner",
    page_icon="🔍",
    layout="wide"
)


st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-text {
        color: #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for scan history
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

def decode_qr_code(image):
    """Decode QR code from image"""
    try:
        img_array = np.array(image.convert("RGB"))
        qcd = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img_array)
        if retval:
            return [type('obj', (), {'data': info.encode()}) for info in decoded_info]
        return []
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return []

def main():
    # Main header
    st.title("Growth Mindset Challenge")
    st.title("QR Code Scanner")
    
 
    tab1, tab2 = st.tabs(["Upload Image", "Use Camera"])
    
    with tab1:
        # Existing upload functionality
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg"],
            help="Upload an image containing a QR code"
        )
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            with st.spinner('Scanning QR Code...'):
                decoded_objects = decode_qr_code(image)

                if decoded_objects:
                    for obj in decoded_objects:
                        decoded_data = obj.data.decode('utf-8')
                        st.markdown(f"""
                        <div class='success-text'>
                            <h3>✅ QR Code Detected!</h3>
                            <p><strong>Decoded Content:</strong> {decoded_data}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # history
                        st.session_state.scan_history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'content': decoded_data
                        })
                        
                        # Copy button
                        if st.button('📋 Copy to Clipboard'):
                            st.write('Content copied to clipboard!')
                            st.code(decoded_data)
                else:
                    st.error("No QR code found in the image. Please try another image.")

    with tab2:
        st.write("📸 Live QR Code Scanner")
        camera_placeholder = st.empty()
        start_camera = st.button("Start Camera")
        
        if start_camera:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to access camera")
                    break
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                camera_placeholder.image(frame_rgb, channels="RGB")
                
                # Try to decode QR code
                qcd = cv2.QRCodeDetector()
                retval, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
                
                if retval:
                    for info in decoded_info:
                        if info:  # If QR code is detected
                            cap.release()  # Release camera
                            st.success(f"QR Code Detected: {info}")
                            #  history
                            st.session_state.scan_history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'content': info
                            })
                            return
                
            
                if not start_camera:
                    cap.release()
                    break
                
            cap.release()

    with st.sidebar:
        st.header("📖 Instructions")
        st.markdown("""
        1. Upload an image containing a QR code
        2. Wait for automatic processing
        3. View the decoded content
        4. Check scan history below
        """)
        
        st.header("ℹ️ About")
        st.markdown("""
         Our QR Code Scanner web app is designed to make reading QR codes fast, easy, and accessible.
         Simply upload an image containing a QR code—or use your device’s camera—and the app will
         automatically detect and decode the information. Whether it’s a website link,
         contact details, or event information, you’ll see the results instantly.
        """)

     
    col1, col2 = st.columns([2, 1])

    with col1:
        # Add clear history button
        if st.session_state.scan_history:
            if st.button("🗑️ Clear History"):
                st.session_state.scan_history = []
                st.rerun()
                
        st.header("📜 Scan History")
        if st.session_state.scan_history:
            for scan in reversed(st.session_state.scan_history):
                st.markdown(f"""
                **Time:** {scan['timestamp']}  
                **Content:** {scan['content']}
                ---
                """)
        else:
            st.info("No scans yet. Upload an image to get started!")

if __name__ == "__main__":
    main()

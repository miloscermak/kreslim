import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

def create_sketch(image):
    # Převod na šedotónový obrázek
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invertování
    inverted_image = cv2.bitwise_not(gray_image)
    
    # Rozmazání
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
    
    # Invertování rozmazaného obrazu
    inverted_blurred = cv2.bitwise_not(blurred)
    
    # Vytvoření skici
    sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    
    return sketch

def main():
    st.title("Převod fotografie na skicu")
    st.write("Nahrajte fotografii a vytvořte z ní uměleckou skicu!")
    
    uploaded_file = st.file_uploader("Vyberte obrázek...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Načtení a zobrazení původního obrázku
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Převod BGR na RGB pro zobrazení ve Streamlitu
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption='Původní obrázek', use_container_width=True)
        
        if st.button('Vytvořit skicu'):
            # Vytvoření skici
            sketch = create_sketch(image)
            st.image(sketch, caption='Výsledná skica', use_container_width=True)
            
            # Přidání tlačítka pro stažení
            ret, buffer = cv2.imencode('.png', sketch)
            btn = st.download_button(
                label="Stáhnout skicu",
                data=buffer.tobytes(),
                file_name="sketch.png",
                mime="image/png"
            )

if __name__ == '__main__':
    main() 